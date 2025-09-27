#!/usr/bin/env python3
"""
Monitoring script for Drunk YOLO Trading Bot V0.35
Watch this untested mess (probably) fail in real-time
"""
import json
import os
import time
import subprocess
import sys
from datetime import datetime, timedelta
from typing import Dict, Optional

class BotMonitor:
    def __init__(self):
        self.portfolio_file = "portfolio.json"
        self.csv_file = "trades_metadata.csv"
        self.log_file = "bot.log"
        self.last_check = datetime.now()
    
    def check_bot_running(self) -> bool:
        """Check if the bot process is running"""
        try:
            # Check for python processes running Script
            result = subprocess.run(
                ["pgrep", "-f", "python.*Script"], 
                capture_output=True, 
                text=True
            )
            return result.returncode == 0
        except FileNotFoundError:
            # pgrep not available (Windows), check differently
            try:
                result = subprocess.run(
                    ["tasklist", "/FI", "IMAGENAME eq python.exe"], 
                    capture_output=True, 
                    text=True
                )
                return "Script" in result.stdout
            except FileNotFoundError:
                return False
    
    def get_portfolio_status(self) -> Dict:
        """Get current portfolio status"""
        if not os.path.exists(self.portfolio_file):
            return {"error": "Portfolio file not found"}
        
        try:
            with open(self.portfolio_file, 'r') as f:
                data = json.load(f)
            
            positions = data.get('positions', {})
            return {
                "active_positions": len(positions),
                "daily_spent": data.get('daily_spent', 0),
                "realized_pnl": data.get('realized_pnl', 0),
                "last_update": data.get('day_epoch', 'unknown')
            }
        except Exception as e:
            return {"error": f"Failed to read portfolio: {e}"}
    
    def check_recent_activity(self, hours: int = 1) -> Dict:
        """Check for recent trading activity"""
        if not os.path.exists(self.csv_file):
            return {"error": "No trade history found"}
        
        try:
            import pandas as pd
            df = pd.read_csv(self.csv_file)
            
            if 'timestamp' in df.columns:
                df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
                cutoff = datetime.now() - timedelta(hours=hours)
                recent = df[df['timestamp'] >= cutoff]
                
                return {
                    "recent_signals": len(recent),
                    "recent_trades": len(recent[recent['pnl'].notna()]) if 'pnl' in recent.columns else 0,
                    "last_activity": recent['timestamp'].max().isoformat() if not recent.empty else "none"
                }
            else:
                return {"error": "Invalid CSV format"}
                
        except ImportError:
            return {"error": "pandas not available for activity check"}
        except Exception as e:
            return {"error": f"Failed to check activity: {e}"}
    
    def check_disk_space(self) -> Dict:
        """Check available disk space"""
        try:
            import shutil
            total, used, free = shutil.disk_usage(".")
            free_gb = free / (1024**3)
            
            return {
                "free_space_gb": round(free_gb, 2),
                "warning": free_gb < 1.0  # Warn if less than 1GB free
            }
        except Exception as e:
            return {"error": f"Failed to check disk space: {e}"}
    
    def generate_report(self) -> str:
        """Generate a status report"""
        report = []
        report.append(f"🍺 Drunk YOLO Bot Monitor V0.35 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("⚠️  WARNING: Monitoring untested code!")
        report.append("=" * 60)
        
        # Bot status
        running = self.check_bot_running()
        status_icon = "✅" if running else "❌"
        report.append(f"{status_icon} Bot Status: {'RUNNING' if running else 'STOPPED'}")
        
        # Portfolio status
        portfolio = self.get_portfolio_status()
        if "error" not in portfolio:
            report.append(f"📊 Active Positions: {portfolio['active_positions']}")
            report.append(f"💰 Daily Spent: {portfolio['daily_spent']:.6f} SOL")
            report.append(f"📈 Realized PnL: {portfolio['realized_pnl']:.6f} SOL")
        else:
            report.append(f"❌ Portfolio: {portfolio['error']}")
        
        # Recent activity
        activity = self.check_recent_activity()
        if "error" not in activity:
            report.append(f"🔄 Recent Signals (1h): {activity['recent_signals']}")
            report.append(f"💹 Recent Trades (1h): {activity['recent_trades']}")
            report.append(f"⏰ Last Activity: {activity['last_activity']}")
        else:
            report.append(f"❌ Activity: {activity['error']}")
        
        # System status
        disk = self.check_disk_space()
        if "error" not in disk:
            warning_icon = "⚠️" if disk['warning'] else "✅"
            report.append(f"{warning_icon} Free Space: {disk['free_space_gb']} GB")
        
        return "\n".join(report)
    
    def send_alert(self, message: str):
        """Send alert (placeholder for notification system)"""
        print(f"🚨 ALERT: {message}")
        # Here you could integrate with:
        # - Email notifications
        # - Slack/Discord webhooks
        # - SMS services
        # - Telegram bot
    
    def run_checks(self):
        """Run all monitoring checks"""
        print(self.generate_report())
        
        # Check for critical issues
        if not self.check_bot_running():
            self.send_alert("Bot is not running!")
        
        portfolio = self.get_portfolio_status()
        if "error" not in portfolio and portfolio['active_positions'] > 15:
            self.send_alert(f"High position count: {portfolio['active_positions']}")
        
        disk = self.check_disk_space()
        if "error" not in disk and disk['warning']:
            self.send_alert(f"Low disk space: {disk['free_space_gb']} GB")

def main():
    """Main monitoring function"""
    monitor = BotMonitor()
    
    if len(sys.argv) > 1 and sys.argv[1] == "--continuous":
        # Continuous monitoring mode
        print("Starting continuous monitoring (Ctrl+C to stop)...")
        try:
            while True:
                monitor.run_checks()
                print("\n" + "="*60 + "\n")
                time.sleep(300)  # Check every 5 minutes
        except KeyboardInterrupt:
            print("\nMonitoring stopped.")
    else:
        # Single check
        monitor.run_checks()

if __name__ == "__main__":
    main()