#!/usr/bin/env python3
"""
Backtesting Module for Drunk YOLO Trading Bot V0.35
See how badly this would have performed (spoiler: very badly)
"""
import asyncio
import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import matplotlib.pyplot as plt
import seaborn as sns
from dataclasses import dataclass
import os

@dataclass
class BacktestConfig:
    initial_balance: float = 0.1  # SOL
    fixed_buy_size: float = 0.002  # SOL
    tp_pct: float = 5.0
    sl_pct: float = 1.0
    trail_pct: float = 3.0
    max_hold_minutes: int = 20
    max_concurrent_positions: int = 10
    min_score_threshold: float = 0.6

@dataclass
class Trade:
    mint: str
    entry_time: datetime
    exit_time: Optional[datetime]
    entry_price: float
    exit_price: Optional[float]
    quantity: float
    pnl: Optional[float]
    reason: Optional[str]
    score: float

class Backtester:
    def __init__(self, config: BacktestConfig):
        self.config = config
        self.balance = config.initial_balance
        self.positions: Dict[str, Trade] = {}
        self.completed_trades: List[Trade] = []
        self.equity_curve: List[float] = [config.initial_balance]
        self.timestamps: List[datetime] = [datetime.now()]
    
    def load_historical_data(self, csv_file: str = "trades_metadata.csv") -> pd.DataFrame:
        """Load historical trade signals and outcomes"""
        if not os.path.exists(csv_file):
            # Generate synthetic data for demonstration
            return self.generate_synthetic_data()
        
        df = pd.read_csv(csv_file)
        if 'timestamp' in df.columns:
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
        
        return df
    
    def generate_synthetic_data(self, days: int = 30, signals_per_day: int = 20) -> pd.DataFrame:
        """Generate synthetic historical data for backtesting"""
        np.random.seed(42)  # For reproducible results
        
        data = []
        start_date = datetime.now() - timedelta(days=days)
        
        for day in range(days):
            current_date = start_date + timedelta(days=day)
            
            for signal in range(signals_per_day):
                # Generate realistic signal data
                timestamp = current_date + timedelta(
                    hours=np.random.uniform(0, 24),
                    minutes=np.random.uniform(0, 60)
                )
                
                mint = f"mint_{day}_{signal}"
                score = np.random.beta(2, 5)  # Skewed towards lower scores
                age_days = np.random.exponential(5)  # Most tokens are young
                
                # Simulate price impact and expected output
                price_impact = np.random.exponential(8)  # Most have high impact
                expected_output = np.random.lognormal(13, 1)  # Log-normal distribution
                
                # Simulate actual PnL based on score (higher score = better chance of profit)
                success_prob = score * 0.7 + 0.1  # 10-80% success rate based on score
                if np.random.random() < success_prob:
                    # Winning trade
                    pnl = np.random.exponential(0.001) * np.random.choice([1, 2, 3, 5], p=[0.5, 0.3, 0.15, 0.05])
                else:
                    # Losing trade
                    pnl = -np.random.exponential(0.0005) * np.random.choice([1, 2, 4], p=[0.7, 0.25, 0.05])
                
                data.append({
                    'timestamp': timestamp,
                    'mint': mint,
                    'score': score,
                    'age_days': age_days,
                    'price_impact_pct': price_impact,
                    'expected_output': expected_output,
                    'actual_pnl': pnl,
                    'signal_type': 'token_created'
                })
        
        return pd.DataFrame(data).sort_values('timestamp')
    
    def should_enter_position(self, signal: Dict) -> bool:
        """Determine if we should enter a position based on signal"""
        # Check available balance
        if self.balance < self.config.fixed_buy_size:
            return False
        
        # Check concurrent positions limit
        if len(self.positions) >= self.config.max_concurrent_positions:
            return False
        
        # Check score threshold
        if signal.get('score', 0) < self.config.min_score_threshold:
            return False
        
        # Check other filters (age, price impact, etc.)
        if signal.get('age_days', 0) < 1:  # Too new
            return False
        
        if signal.get('price_impact_pct', 100) > 15:  # Too high impact
            return False
        
        return True
    
    def enter_position(self, signal: Dict, timestamp: datetime) -> Optional[Trade]:
        """Enter a new position"""
        if not self.should_enter_position(signal):
            return None
        
        mint = signal['mint']
        entry_price = 1.0  # Normalized price
        quantity = self.config.fixed_buy_size / entry_price
        
        trade = Trade(
            mint=mint,
            entry_time=timestamp,
            exit_time=None,
            entry_price=entry_price,
            exit_price=None,
            quantity=quantity,
            pnl=None,
            reason=None,
            score=signal.get('score', 0)
        )
        
        self.positions[mint] = trade
        self.balance -= self.config.fixed_buy_size
        
        return trade
    
    def check_exit_conditions(self, trade: Trade, current_time: datetime, actual_pnl: float) -> Optional[str]:
        """Check if position should be exited"""
        # Time-based exit
        hold_minutes = (current_time - trade.entry_time).total_seconds() / 60
        if hold_minutes >= self.config.max_hold_minutes:
            return "time"
        
        # PnL-based exits (using actual PnL from historical data)
        pnl_pct = (actual_pnl / self.config.fixed_buy_size) * 100
        
        if pnl_pct >= self.config.tp_pct:
            return "tp"
        
        if pnl_pct <= -self.config.sl_pct:
            return "sl"
        
        # Simplified trailing stop
        if pnl_pct >= self.config.trail_pct and pnl_pct <= self.config.trail_pct * 0.7:
            return "trail"
        
        return None
    
    def exit_position(self, mint: str, reason: str, exit_time: datetime, actual_pnl: float):
        """Exit a position"""
        if mint not in self.positions:
            return
        
        trade = self.positions.pop(mint)
        trade.exit_time = exit_time
        trade.exit_price = trade.entry_price + (actual_pnl / trade.quantity)
        trade.pnl = actual_pnl
        trade.reason = reason
        
        self.balance += self.config.fixed_buy_size + actual_pnl
        self.completed_trades.append(trade)
        
        # Update equity curve
        self.equity_curve.append(self.balance)
        self.timestamps.append(exit_time)
    
    def run_backtest(self, data: pd.DataFrame) -> Dict:
        """Run the backtest on historical data"""
        print(f"Running backtest on {len(data)} signals...")
        
        # Group data by mint to simulate position lifecycle
        signal_data = {}
        for _, row in data.iterrows():
            mint = row['mint']
            if mint not in signal_data:
                signal_data[mint] = {
                    'signal': row.to_dict(),
                    'timestamp': row['timestamp'],
                    'actual_pnl': row.get('actual_pnl', 0)
                }
        
        # Process signals chronologically
        sorted_signals = sorted(signal_data.items(), key=lambda x: x[1]['timestamp'])
        
        for mint, data_point in sorted_signals:
            signal = data_point['signal']
            timestamp = data_point['timestamp']
            actual_pnl = data_point['actual_pnl']
            
            # Try to enter position
            trade = self.enter_position(signal, timestamp)
            
            if trade:
                # Simulate holding period and exit
                exit_time = timestamp + timedelta(minutes=np.random.uniform(1, self.config.max_hold_minutes))
                exit_reason = self.check_exit_conditions(trade, exit_time, actual_pnl)
                
                if exit_reason:
                    self.exit_position(mint, exit_reason, exit_time, actual_pnl)
        
        # Close any remaining positions
        for mint in list(self.positions.keys()):
            self.exit_position(mint, "backtest_end", sorted_signals[-1][1]['timestamp'], 0)
        
        return self.calculate_metrics()
    
    def calculate_metrics(self) -> Dict:
        """Calculate backtest performance metrics"""
        if not self.completed_trades:
            return {"error": "No completed trades"}
        
        pnls = [trade.pnl for trade in self.completed_trades if trade.pnl is not None]
        
        if not pnls:
            return {"error": "No PnL data"}
        
        wins = [pnl for pnl in pnls if pnl > 0]
        losses = [pnl for pnl in pnls if pnl < 0]
        
        total_return = (self.balance - self.config.initial_balance) / self.config.initial_balance * 100
        
        metrics = {
            "total_trades": len(self.completed_trades),
            "winning_trades": len(wins),
            "losing_trades": len(losses),
            "win_rate": len(wins) / len(pnls) * 100 if pnls else 0,
            "total_pnl": sum(pnls),
            "total_return_pct": total_return,
            "avg_win": np.mean(wins) if wins else 0,
            "avg_loss": np.mean(losses) if losses else 0,
            "max_win": max(pnls) if pnls else 0,
            "max_loss": min(pnls) if pnls else 0,
            "profit_factor": abs(sum(wins) / sum(losses)) if losses and sum(losses) != 0 else float('inf'),
            "sharpe_ratio": np.mean(pnls) / np.std(pnls) if len(pnls) > 1 and np.std(pnls) > 0 else 0,
            "max_drawdown": self.calculate_max_drawdown(),
            "final_balance": self.balance
        }
        
        return metrics
    
    def calculate_max_drawdown(self) -> float:
        """Calculate maximum drawdown"""
        if len(self.equity_curve) < 2:
            return 0
        
        peak = self.equity_curve[0]
        max_dd = 0
        
        for value in self.equity_curve[1:]:
            if value > peak:
                peak = value
            else:
                drawdown = (peak - value) / peak * 100
                max_dd = max(max_dd, drawdown)
        
        return max_dd
    
    def plot_results(self, save_path: str = "backtest_results.png"):
        """Plot backtest results"""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle('Backtest Results', fontsize=16)
        
        # Equity curve
        ax1.plot(self.timestamps, self.equity_curve, 'b-', linewidth=2)
        ax1.set_title('Equity Curve')
        ax1.set_xlabel('Time')
        ax1.set_ylabel('Balance (SOL)')
        ax1.grid(True, alpha=0.3)
        
        # PnL distribution
        pnls = [trade.pnl for trade in self.completed_trades if trade.pnl is not None]
        if pnls:
            ax2.hist(pnls, bins=30, alpha=0.7, color='green', edgecolor='black')
            ax2.axvline(0, color='red', linestyle='--', alpha=0.7)
            ax2.set_title('PnL Distribution')
            ax2.set_xlabel('PnL (SOL)')
            ax2.set_ylabel('Frequency')
        
        # Win/Loss by score
        scores = [trade.score for trade in self.completed_trades]
        colors = ['green' if trade.pnl > 0 else 'red' for trade in self.completed_trades if trade.pnl is not None]
        if scores and colors:
            ax3.scatter(scores, pnls, c=colors, alpha=0.6)
            ax3.set_title('PnL vs Score')
            ax3.set_xlabel('Entry Score')
            ax3.set_ylabel('PnL (SOL)')
            ax3.grid(True, alpha=0.3)
        
        # Exit reasons
        exit_reasons = [trade.reason for trade in self.completed_trades if trade.reason]
        if exit_reasons:
            reason_counts = pd.Series(exit_reasons).value_counts()
            ax4.pie(reason_counts.values, labels=reason_counts.index, autopct='%1.1f%%')
            ax4.set_title('Exit Reasons')
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
        
        print(f"Results saved to {save_path}")

def main():
    """Run backtest with different configurations"""
    configs = [
        BacktestConfig(tp_pct=3, sl_pct=1, min_score_threshold=0.5),
        BacktestConfig(tp_pct=5, sl_pct=1, min_score_threshold=0.6),
        BacktestConfig(tp_pct=7, sl_pct=2, min_score_threshold=0.7),
    ]
    
    results = []
    
    for i, config in enumerate(configs):
        print(f"\n--- Running Backtest {i+1} ---")
        backtester = Backtester(config)
        data = backtester.load_historical_data()
        metrics = backtester.run_backtest(data)
        
        print(f"Configuration: TP={config.tp_pct}%, SL={config.sl_pct}%, Score>={config.min_score_threshold}")
        print(f"Total Return: {metrics.get('total_return_pct', 0):.2f}%")
        print(f"Win Rate: {metrics.get('win_rate', 0):.1f}%")
        print(f"Sharpe Ratio: {metrics.get('sharpe_ratio', 0):.2f}")
        print(f"Max Drawdown: {metrics.get('max_drawdown', 0):.2f}%")
        
        results.append({
            'config': config,
            'metrics': metrics,
            'backtester': backtester
        })
    
    # Find best configuration
    best_result = max(results, key=lambda x: x['metrics'].get('sharpe_ratio', 0))
    print(f"\n--- Best Configuration (Highest Sharpe) ---")
    print(f"TP: {best_result['config'].tp_pct}%, SL: {best_result['config'].sl_pct}%, Score: {best_result['config'].min_score_threshold}")
    
    # Plot best result
    best_result['backtester'].plot_results()

if __name__ == "__main__":
    main()