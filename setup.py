#!/usr/bin/env python3
"""
Setup script for Drunk YOLO Trading Bot V0.35
Handles installation of this questionable experiment
"""
import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_python_version():
    """Ensure Python 3.10+ is being used"""
    if sys.version_info < (3, 10):
        print("❌ Python 3.10 or higher is required")
        print(f"Current version: {sys.version}")
        sys.exit(1)
    print(f"✅ Python version: {sys.version}")

def install_dependencies():
    """Install required Python packages"""
    print("\n📦 Installing dependencies...")
    
    try:
        # Install basic requirements
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Basic dependencies installed")
        
        # Install optional ML dependencies
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "scikit-learn", "numpy", "pandas"])
            print("✅ ML dependencies installed")
        except subprocess.CalledProcessError:
            print("⚠️  ML dependencies failed to install (optional)")
        
        # Install optional dashboard dependencies
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "flask", "plotly"])
            print("✅ Dashboard dependencies installed")
        except subprocess.CalledProcessError:
            print("⚠️  Dashboard dependencies failed to install (optional)")
            
        # Install optional backtesting dependencies
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "matplotlib", "seaborn"])
            print("✅ Backtesting dependencies installed")
        except subprocess.CalledProcessError:
            print("⚠️  Backtesting dependencies failed to install (optional)")
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        sys.exit(1)

def setup_directories():
    """Create necessary directories"""
    print("\n📁 Setting up directories...")
    
    directories = [
        "models",
        "logs",
        "backups",
        "templates"  # For dashboard
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ Created directory: {directory}")

def setup_config():
    """Set up configuration files"""
    print("\n⚙️  Setting up configuration...")
    
    if not os.path.exists(".env"):
        if os.path.exists(".env.example"):
            shutil.copy(".env.example", ".env")
            print("✅ Created .env from example")
            print("⚠️  Please edit .env with your actual configuration")
        else:
            print("❌ .env.example not found")
    else:
        print("✅ .env already exists")

def check_solana_tools():
    """Check if Solana CLI tools are available"""
    print("\n🔗 Checking Solana tools...")
    
    try:
        result = subprocess.run(["solana", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Solana CLI: {result.stdout.strip()}")
        else:
            print("⚠️  Solana CLI not found (optional for some features)")
    except FileNotFoundError:
        print("⚠️  Solana CLI not found (optional for some features)")

def setup_systemd_service():
    """Set up systemd service for Linux users"""
    if sys.platform != "linux":
        return
    
    print("\n🔧 Setting up systemd service (optional)...")
    
    service_content = f"""[Unit]
Description=Pump.fun Trading Bot
After=network.target

[Service]
Type=simple
User={os.getenv('USER', 'ubuntu')}
WorkingDirectory={os.getcwd()}
ExecStart={sys.executable} Script
Restart=always
RestartSec=10
Environment=PYTHONPATH={os.getcwd()}

[Install]
WantedBy=multi-user.target
"""
    
    service_file = f"{os.getcwd()}/pump-bot.service"
    with open(service_file, "w") as f:
        f.write(service_content)
    
    print(f"✅ Service file created: {service_file}")
    print("To install: sudo cp pump-bot.service /etc/systemd/system/")
    print("To enable: sudo systemctl enable pump-bot")
    print("To start: sudo systemctl start pump-bot")

def run_tests():
    """Run basic tests to ensure everything works"""
    print("\n🧪 Running basic tests...")
    
    try:
        # Test imports
        import aiohttp
        import base58
        print("✅ Core imports successful")
        
        # Test configuration loading
        from dotenv import load_dotenv
        load_dotenv()
        print("✅ Configuration loading successful")
        
        # Test paper trading mode
        os.environ["DRY_RUN"] = "true"
        print("✅ Paper trading mode enabled for testing")
        
    except ImportError as e:
        print(f"❌ Import test failed: {e}")
        return False
    
    return True

def print_next_steps():
    """Print next steps for the user"""
    print("\n🎉 Setup complete!")
    print("\n📋 Next steps:")
    print("1. Edit .env file with your configuration:")
    print("   - Add your PumpPortal API key")
    print("   - Configure your wallet keys")
    print("   - Set your watchlist mints")
    print("   - Adjust risk parameters")
    print("\n2. Test in paper mode first:")
    print("   python Script")
    print("\n3. Monitor with dashboard:")
    print("   python dashboard.py")
    print("\n4. Run backtests:")
    print("   python backtest.py")
    print("\n5. When ready for live trading:")
    print("   - Set DRY_RUN=false in .env")
    print("   - Start with small amounts")
    print("   - Monitor closely")
    print("\n🍺 DRUNK WARNING: This code is untested and probably broken!")
    print("   Seriously, don't use real money with V0.35!")
    print("   Test in paper mode and expect bugs!")

def main():
    """Main setup function"""
    print("🍺 Drunk YOLO Bot Setup V0.35")
    print("⚠️  WARNING: Untested code ahead!")
    print("=" * 40)
    
    check_python_version()
    install_dependencies()
    setup_directories()
    setup_config()
    check_solana_tools()
    setup_systemd_service()
    
    if run_tests():
        print_next_steps()
    else:
        print("\n❌ Setup completed with errors. Please check the issues above.")
        sys.exit(1)

if __name__ == "__main__":
    main()