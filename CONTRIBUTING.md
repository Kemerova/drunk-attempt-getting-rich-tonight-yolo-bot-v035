# Contributing to Drunk YOLO Trading Bot V0.35

Thanks for wanting to help fix this mess! This project is a questionable experiment in automated memecoin trading that probably needs a lot of work.

## 🤝 How to Contribute

### Reporting Issues
- Use GitHub Issues to report bugs or request features
- Provide detailed information about your environment
- Include steps to reproduce any issues
- Attach relevant log files or error messages

### Code Contributions
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests if applicable
5. Update documentation
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## 🛠️ Development Setup

### Prerequisites
- Python 3.10 or higher
- Git
- Virtual environment (recommended)

### Local Development
```bash
# Clone your fork
git clone https://github.com/yourusername/drunk-yolo-bot.git
cd drunk-yolo-bot

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install optional development dependencies
pip install pytest black flake8 mypy

# Run setup
python setup.py
```

### Testing
```bash
# Run in paper mode for testing
DRY_RUN=true python Script

# Run backtests
python backtest.py

# Check code style
black --check .
flake8 .
mypy Script
```

## 📋 Contribution Guidelines

### Code Style
- Follow PEP 8 Python style guide
- Use type hints for all functions
- Add docstrings for classes and functions
- Keep functions focused and modular
- Use meaningful variable names

### Commit Messages
- Use clear, descriptive commit messages
- Start with a verb (Add, Fix, Update, Remove)
- Keep first line under 50 characters
- Add detailed description if needed

Example:
```
Add ML-based token scoring system

- Implement scikit-learn integration
- Add feature engineering for price impact and holder analysis
- Include automatic model retraining
- Add fallback to rule-based scoring
```

### Pull Request Process
1. Ensure your code passes all tests
2. Update documentation for any new features
3. Add entries to CHANGELOG.md
4. Ensure your PR has a clear description
5. Link any related issues

## 🎯 Areas for Contribution

### High Priority (Fix This Mess)
- **TESTING**: This code is completely untested - help!
- **Bug Fixes**: There are probably many bugs lurking
- **Basic Functionality**: Make sure it actually works
- **Safety Checks**: Add more safeguards against losing money
- **Documentation**: Fix all the drunk comments

### Medium Priority
- **UI/UX**: Dashboard improvements and mobile responsiveness
- **Integrations**: Additional DEX support, more data sources
- **Documentation**: Video tutorials, strategy guides
- **Monitoring**: Advanced alerting and notification systems

### Low Priority
- **Refactoring**: Code organization and modularity improvements
- **Utilities**: Helper scripts and tools
- **Examples**: Sample configurations and strategies

## 🔒 Security Considerations

### Sensitive Information
- Never commit private keys or API keys
- Use environment variables for secrets
- Review code for potential security vulnerabilities
- Test with paper trading first

### Responsible Disclosure
- Report security issues privately via email
- Allow time for fixes before public disclosure
- Provide detailed information about vulnerabilities

## 📚 Resources

### Documentation
- [Solana Documentation](https://docs.solana.com/)
- [PumpPortal API](https://pumpportal.fun/docs)
- [Jito Documentation](https://jito.wtf/docs)

### Development Tools
- [Python Type Hints](https://docs.python.org/3/library/typing.html)
- [Asyncio Guide](https://docs.python.org/3/library/asyncio.html)
- [Pytest Documentation](https://docs.pytest.org/)

## 🚨 Important Notes

### Legal and Ethical
- This is experimental/educational code (don't actually use it)
- V0.35 means it's not ready for real trading
- Please help make it less dangerous before V1.0
- Don't encourage people to use untested trading bots

### Risk Management
- Always test changes in paper mode first
- Consider the financial impact of bugs
- Implement proper error handling
- Add logging for debugging

### Community
- Be respectful and constructive
- Help other contributors
- Share knowledge and best practices
- Follow the code of conduct

## 📞 Contact

- GitHub Issues: For bugs and feature requests
- Discussions: For questions and general discussion
- Email: For security issues and private matters

## 🙏 Recognition

Contributors will be recognized in:
- README.md contributors section
- CHANGELOG.md for significant contributions
- GitHub contributors page

Thank you for helping make this project better! 🚀