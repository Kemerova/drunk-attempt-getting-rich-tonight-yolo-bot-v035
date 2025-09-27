#!/usr/bin/env python3
"""
Real-time Dashboard for Drunk YOLO Trading Bot V0.35
Watch your money disappear in real-time (probably)
"""
import asyncio
import json
import os
import pandas as pd
import plotly.graph_objs as go
import plotly.utils
from datetime import datetime, timedelta
from flask import Flask, render_template, jsonify
from threading import Thread
import time

app = Flask(__name__)

class BotMonitor:
    def __init__(self):
        self.portfolio_file = "portfolio.json"
        self.csv_file = "trades_metadata.csv"
        self.status = {"running": False, "last_update": None}
    
    def get_portfolio_data(self):
        """Load current portfolio state"""
        if os.path.exists(self.portfolio_file):
            with open(self.portfolio_file, 'r') as f:
                return json.load(f)
        return {}
    
    def get_trade_history(self, days=7):
        """Load recent trade history"""
        if not os.path.exists(self.csv_file):
            return pd.DataFrame()
        
        df = pd.read_csv(self.csv_file)
        if 'timestamp' in df.columns:
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
            cutoff = datetime.now() - timedelta(days=days)
            df = df[df['timestamp'] >= cutoff]
        
        return df
    
    def calculate_performance_metrics(self):
        """Calculate key performance metrics"""
        df = self.get_trade_history(30)  # Last 30 days
        
        if df.empty or 'pnl' not in df.columns:
            return {
                "total_pnl": 0,
                "win_rate": 0,
                "avg_win": 0,
                "avg_loss": 0,
                "total_trades": 0,
                "sharpe_ratio": 0
            }
        
        # Filter completed trades (those with PnL)
        completed = df[df['pnl'].notna()]
        
        total_pnl = completed['pnl'].sum()
        wins = completed[completed['pnl'] > 0]
        losses = completed[completed['pnl'] < 0]
        
        win_rate = len(wins) / len(completed) * 100 if len(completed) > 0 else 0
        avg_win = wins['pnl'].mean() if len(wins) > 0 else 0
        avg_loss = losses['pnl'].mean() if len(losses) > 0 else 0
        
        # Simple Sharpe ratio approximation
        returns = completed['pnl'].values
        sharpe_ratio = returns.mean() / returns.std() if len(returns) > 1 and returns.std() > 0 else 0
        
        return {
            "total_pnl": round(total_pnl, 6),
            "win_rate": round(win_rate, 1),
            "avg_win": round(avg_win, 6),
            "avg_loss": round(avg_loss, 6),
            "total_trades": len(completed),
            "sharpe_ratio": round(sharpe_ratio, 2)
        }
    
    def create_pnl_chart(self):
        """Create PnL over time chart"""
        df = self.get_trade_history(30)
        
        if df.empty or 'pnl' not in df.columns:
            return json.dumps({})
        
        # Calculate cumulative PnL
        completed = df[df['pnl'].notna()].sort_values('timestamp')
        completed['cumulative_pnl'] = completed['pnl'].cumsum()
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=completed['timestamp'],
            y=completed['cumulative_pnl'],
            mode='lines+markers',
            name='Cumulative PnL',
            line=dict(color='green' if completed['cumulative_pnl'].iloc[-1] > 0 else 'red')
        ))
        
        fig.update_layout(
            title='Cumulative PnL Over Time',
            xaxis_title='Date',
            yaxis_title='PnL (SOL)',
            template='plotly_dark'
        )
        
        return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

monitor = BotMonitor()

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/status')
def api_status():
    portfolio = monitor.get_portfolio_data()
    metrics = monitor.calculate_performance_metrics()
    
    return jsonify({
        "status": monitor.status,
        "portfolio": portfolio,
        "metrics": metrics,
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/chart/pnl')
def api_pnl_chart():
    return monitor.create_pnl_chart()

@app.route('/api/positions')
def api_positions():
    portfolio = monitor.get_portfolio_data()
    positions = portfolio.get('positions', {})
    
    # Add current market data (mock for now)
    for mint, pos in positions.items():
        pos['current_price'] = pos.get('avg_price', 0) * (1 + (hash(mint) % 20 - 10) / 100)  # Mock price
        pos['unrealized_pnl'] = (pos['current_price'] - pos.get('avg_price', 0)) * pos.get('qty', 0)
    
    return jsonify(positions)

@app.route('/api/trades')
def api_trades():
    df = monitor.get_trade_history(7)
    if df.empty:
        return jsonify([])
    
    # Convert to records for JSON serialization
    trades = df.to_dict('records')
    for trade in trades:
        if 'timestamp' in trade and pd.notna(trade['timestamp']):
            trade['timestamp'] = trade['timestamp'].isoformat()
    
    return jsonify(trades[-50:])  # Last 50 trades

if __name__ == '__main__':
    print("Starting Drunk YOLO Bot Dashboard V0.35...")
    print("⚠️  WARNING: Untested code - expect bugs!")
    print("Access at: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)