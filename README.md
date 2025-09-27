# 🍺 Drunk Attempt at Getting Rich Tonight (after Midnight YOLO trading bot) V0.35

A questionably-coded, async Python trading bot for Pump.fun that I threw together after too many drinks and delusions of grandeur. Features some half-baked MEV protection, sketchy rug detection, and ML scoring that may or may not work. Use at your own risk (and sobriety level).

## 🎲 What This Hot Mess Allegedly Does

### Core YOLO Features
- **Automated Buy/Sell**: Throws money at memecoins automatically
- **Paper Trading**: Pretend mode so you can lose fake money first
- **Risk Management**: Some stop-losses that might work (no promises)
- **Multi-timeframe**: Holds positions until panic or profit

### Questionable Protection
- **MEV Protection**: Jito bundles that may or may not save you from bots
- **Rug Detection**: Tries to spot scams (success rate unknown)
- **ML Scoring**: "AI" that's probably just random numbers
- **Rate Limiting**: Won't spam APIs (hopefully)

### Monitoring & Regret Tracking
- **Real-time Dashboard**: Watch your money disappear in real-time
- **Comprehensive Logging**: CSV files to document your poor decisions
- **Backtesting**: See how badly this would have performed historically
- **Performance Metrics**: Numbers that will make you question your life choices

### "Professional" Features (LOL)
- **Persistent State**: Remembers your bad trades even after crashes
- **Telegram Alerts**: Get notified of your losses instantly
- **Scheduled Trading**: Only lose money during specific hours
- **Multi-wallet Support**: Spread the losses across multiple wallets

## 🛠️ Installation

### Prerequisites
- Python 3.10 or higher
- Solana wallet with SOL for trading
- PumpPortal API key

### Quick Setup
```bash
# Clone or download the bot files
# Run the setup script
python setup.py

# Edit configuration
cp .env.example .env
# Edit .env with your settings
```

### Manual Installation
```bash
# Install dependencies
pip install -r requirements.txt

# Optional: ML features
pip install scikit-learn numpy pandas

# Optional: Dashboard
pip install flask plotly

# Optional: Backtesting
pip install matplotlib seaborn

# Create directories
mkdir -p models logs backups templates
```

## ⚙️ Configuration

### Essential Settings (.env)
```bash
# API Configuration
PUMPPORTAL_API_KEY=ppk_your_api_key_here
MODE=lightning  # or 'local'
PUBLIC_KEY=your_public_key_here
PRIVATE_KEY_B58=your_private_key_base58_here

# Trading Parameters
FIXED_BUY_SOL=0.002
TP_PCT=5
SL_PCT=1
TRAIL_PCT=3
MAX_CONCURRENT_POS=10
DAILY_SOL_BUDGET=0.1

# Paper Trading (RECOMMENDED FOR TESTING)
DRY_RUN=true
VIRTUAL_BALANCE=0.33

# Watchlist (5-10 tokens recommended)
WATCHLIST_MINTS=mint1,mint2,mint3,mint4,mint5

# Advanced Features
ENABLE_MEV_PROTECTION=true
ENABLE_ADVANCED_RUG_DETECTION=true
ENABLE_ML_SCORING=false
```

### Risk Management Settings
```bash
# Position Sizing
MAX_POS_PCT=10  # Max 10% of balance per position
DAILY_PROFIT_TARGET=0.0025  # Close all positions at 0.25% daily profit

# Filters
MIN_COIN_AGE_DAYS=10  # Skip tokens younger than 10 days
MAX_HOLDER_CONCENTRATION_PCT=20  # Skip if top holder owns >20%
MIN_HOLDERS_COUNT=50  # Skip tokens with <50 holders
```

## 🚀 Usage

### 1. Paper Trading (Recommended First)
```bash
# Test the bot with virtual money
python Script
```
The bot will simulate trades and log results to CSV for analysis.

### 2. Real-time Dashboard
```bash
# Start the web dashboard
python dashboard.py
# Open http://localhost:5000
```

### 3. Backtesting
```bash
# Test strategies on historical data
python backtest.py
```

### 4. Live Trading
Only after thorough testing:
```bash
# Set DRY_RUN=false in .env
# Start with small amounts
python Script
```

## 📊 Dashboard Features

The web dashboard provides:
- **Real-time Status**: Bot status, current positions, PnL
- **Performance Metrics**: Win rate, Sharpe ratio, drawdown
- **Interactive Charts**: Equity curve, PnL distribution
- **Trade History**: Recent trades with detailed analysis
- **Position Monitoring**: Current holdings and unrealized PnL

## 🧪 Backtesting

The backtesting module allows you to:
- Test different parameter combinations
- Analyze historical performance
- Optimize entry/exit strategies
- Validate risk management rules

Example backtest results:
```
Configuration: TP=5%, SL=1%, Score>=0.6
Total Return: 15.3%
Win Rate: 67.2%
Sharpe Ratio: 1.84
Max Drawdown: 3.2%
```

## 🛡️ Risk Management

### Built-in Protections
- **Position Limits**: Maximum concurrent positions
- **Budget Controls**: Daily spending limits
- **Stop Losses**: Automatic loss cutting
- **Time Limits**: Maximum holding periods
- **Rug Detection**: Multi-factor scam detection

### Recommended Practices
1. **Start Small**: Begin with tiny position sizes
2. **Paper Test**: Run simulations for weeks before live trading
3. **Monitor Closely**: Use dashboard and alerts
4. **Regular Reviews**: Analyze CSV logs and adjust parameters
5. **Diversify**: Don't put all funds in one strategy

## 🔧 Advanced Features

### MEV Protection
- **Jito Bundles**: Atomic transaction bundling
- **Wallet Rotation**: Multiple wallet support
- **Priority Fees**: Dynamic fee calculation

### ML-Enhanced Scoring
- **Feature Engineering**: Price impact, holder analysis, age factors
- **Model Training**: Automatic retraining on new data
- **Ensemble Methods**: Multiple scoring approaches

### Rug Detection
- **Holder Analysis**: Concentration risk assessment
- **Creator History**: Pattern recognition
- **Liquidity Analysis**: Lock detection

## 📈 Performance Optimization

### Strategy Tuning
1. **Backtest First**: Use historical data to optimize parameters
2. **Score Thresholds**: Adjust minimum entry scores
3. **Exit Timing**: Optimize TP/SL/trail percentages
4. **Position Sizing**: Balance risk vs. opportunity

### System Optimization
- **RPC Endpoints**: Use high-performance Solana RPC
- **Network Settings**: Optimize timeouts and retries
- **Resource Management**: Monitor CPU and memory usage

## 🚨 Seriously, Don't Actually Use This

### You Will Probably Lose Money
- **Speculative Garbage**: Memecoins are basically gambling
- **Total Loss Guaranteed**: This code is untested and probably broken
- **No Guarantees**: I wrote this drunk, what did you expect?
- **Legal Issues**: I'm not a financial advisor, just an idiot with Python

### Technical Disasters Waiting to Happen
- **Untested Code**: This is V0.35 for a reason
- **Network Failures**: Solana goes down, your trades go boom
- **API Explosions**: Rate limits will ruin your day
- **Security Holes**: Your keys might get stolen (probably not, but maybe)

## 🔍 Troubleshooting

### Common Issues
1. **Connection Errors**: Check RPC URL and network
2. **API Key Issues**: Verify PumpPortal API key format
3. **Insufficient Balance**: Ensure adequate SOL for trading + fees
4. **Watchlist Empty**: Add 5-10 token mints to watchlist

### Debug Mode
```bash
# Enable verbose logging
export LOG_LEVEL=DEBUG
python Script
```

### Support Files
- **Logs**: Check console output and log files
- **CSV Data**: Analyze trades_metadata.csv
- **Portfolio State**: Review portfolio.json

## 📚 Architecture

### Core Components
- **Config**: Environment-based configuration management
- **PumpPortal**: Trading interface with MEV protection
- **Strategy**: Entry/exit logic with ML scoring
- **Portfolio**: Position tracking and risk management
- **Signals**: WebSocket and board scanning

### Data Flow
1. **Signal Generation**: WebSocket + board scanning
2. **Filtering**: Age, score, rug detection
3. **Entry**: Position creation with risk checks
4. **Monitoring**: Real-time PnL tracking
5. **Exit**: TP/SL/trail/time-based exits

## 🤝 Contributing

This bot is designed for educational and research purposes. Contributions welcome:
- Bug fixes and improvements
- New strategy implementations
- Enhanced ML models
- Better rug detection algorithms

## 📄 License

Use at your own risk. This software is provided as-is without warranties.

## 🙏 Acknowledgments

Inspired by:
- Matt Kohrs' trading philosophy (quick exits, profit targets)
- Open-source Pump.fun bots (chainstacklabs, Dexter-inspired repos)
- Solana DeFi ecosystem innovations

---

**🍺 DRUNK DISCLAIMER: This is a half-baked experiment I coded after midnight with questionable judgment. It's probably broken, definitely untested, and will likely lose your money. I'm not responsible when this inevitably goes wrong. Seriously, don't use real money with this thing. Test it in paper mode, laugh at the bugs, and maybe wait for V1.0 when I'm sober.**