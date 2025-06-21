# 🚀 Reddit Automation Toolkit

**AI-Powered Reddit Content Automation with Policy Compliance**

Transform your blog articles into engaging, policy-compliant Reddit posts with intelligent subreddit recommendations and direct posting capabilities.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red.svg)](https://streamlit.io/)
[![PRAW](https://img.shields.io/badge/praw-7.7+-orange.svg)](https://praw.readthedocs.io/)
[![Status](https://img.shields.io/badge/status-production--ready-green.svg)]()

## ✨ Features

### 🎯 **Complete End-to-End Workflow**
- **Article Analysis**: Intelligent content analysis and topic extraction
- **Smart Recommendations**: AI-powered subreddit suggestions with relevance scoring
- **Policy Compliance**: Automatic compliance checking for subreddit rules
- **Direct Posting**: One-click posting to Reddit with full API integration

### 🤖 **AI-Powered Intelligence**
- **Content Understanding**: Advanced NLP for topic and theme extraction
- **Subreddit Matching**: Smart algorithm for finding relevant communities
- **Post Generation**: AI-generated titles and content optimized for each subreddit
- **Risk Assessment**: Automatic spam and policy violation detection

### 🛡️ **Enterprise-Grade Features**
- **Error Handling**: Comprehensive error management with recovery mechanisms
- **Database Tracking**: Complete post history and analytics
- **Rate Limiting**: Built-in Reddit API rate limit compliance
- **Validation**: Multi-layer content and subreddit validation

### 🌐 **User Interfaces**
- **Web Dashboard**: Beautiful Streamlit interface for complete workflow
- **Terminal Tools**: Command-line automation for power users
- **API Integration**: Full Reddit and AI API integration

## 🚀 Quick Start

### Prerequisites

1. **Python 3.8+** installed on your system
2. **Reddit Account** with API access
3. **Groq API Key** (optional, for enhanced AI features)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/reddit-automation-toolkit.git
   cd reddit-automation-toolkit
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   
   Create a `.env` file in the project root:
   ```env
   # Reddit API Credentials (Required)
   REDDIT_CLIENT_ID=your_reddit_client_id
   REDDIT_CLIENT_SECRET=your_reddit_client_secret
   REDDIT_USERNAME=your_reddit_username
   REDDIT_PASSWORD=your_reddit_password
   REDDIT_USER_AGENT=reddit_automation_bot_1.0
   
   # AI API Key (Optional - enables enhanced features)
   GROQ_API_KEY=your_groq_api_key
   ```

4. **Run the system health check**
   ```bash
   python scripts/complete_health_check.py
   ```

5. **Launch the web dashboard**
   ```bash
   streamlit run apps/enhanced_dashboard.py --server.port=8501
   ```

Visit `http://localhost:8501` to access the web interface.

## 📖 Detailed Setup Guide

### Getting Reddit API Credentials

1. Go to [Reddit App Preferences](https://www.reddit.com/prefs/apps)
2. Click "Create App" or "Create Another App"
3. Choose "script" as the app type
4. Fill in the required information:
   - **Name**: Your app name (e.g., "Reddit Automation Bot")
   - **Description**: Brief description of your automation
   - **Redirect URI**: `http://localhost:8080` (required but not used)
5. Copy the client ID (under the app name) and client secret

### Getting Groq AI API Key (Optional)

1. Visit [Groq Console](https://console.groq.com/)
2. Sign up for a free account
3. Navigate to API Keys section
4. Create a new API key
5. Copy the key to your `.env` file

*Note: The system works with fallback algorithms if no AI key is provided.*

## 🎮 Usage

### Web Dashboard (Recommended)

1. **Start the dashboard**:
   ```bash
   streamlit run apps/enhanced_dashboard.py --server.port=8501
   ```

2. **Complete Workflow**:
   - Enter your article URL
   - Review AI-generated subreddit recommendations
   - Select target subreddits
   - Generate policy-compliant posts
   - Post directly to Reddit with one click

3. **Monitor Results**:
   - View posting history
   - Track performance analytics
   - Monitor compliance status

### Terminal Automation

For power users and automation:

```bash
# Get subreddit recommendations
python apps/terminal_automation.py recommend "https://medium.com/@yourname/your-article"

# Generate posts for specific subreddits
python apps/terminal_automation.py generate "https://medium.com/@yourname/your-article"

# View posting history
python apps/terminal_automation.py history
```

### Interactive Menu

```bash
python main.py
```

## 🏗️ Architecture

### Core Components

```
reddit-automation-toolkit/
├── 📱 apps/                          # User interfaces
│   ├── enhanced_dashboard.py         # Main web dashboard
│   └── terminal_automation.py        # CLI automation tool
├── 🧠 core/                          # Core business logic
│   ├── enhanced_reddit_client.py     # Reddit API integration
│   ├── enhanced_subreddit_recommender.py # AI recommendation engine
│   ├── workflow_manager.py           # Complete workflow orchestration
│   ├── database.py                   # Data persistence layer
│   ├── error_handling.py             # Error management system
│   └── utils.py                      # Utility functions
├── ⚙️ config/                        # Configuration files
│   └── templates.py                  # Post templates and rules
├── 🧪 tests/                         # Comprehensive test suite
├── 📊 scripts/                       # Utility scripts
└── 📁 data/                          # Database and logs
```

### Key Features

- **Modular Design**: Clean separation of concerns
- **Error Resilience**: Comprehensive error handling and recovery
- **Scalable**: Easy to extend with new features
- **Production Ready**: Built for real-world usage

## 🔧 Configuration

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `REDDIT_CLIENT_ID` | ✅ | Reddit app client ID |
| `REDDIT_CLIENT_SECRET` | ✅ | Reddit app client secret |
| `REDDIT_USERNAME` | ✅ | Your Reddit username |
| `REDDIT_PASSWORD` | ✅ | Your Reddit password |
| `REDDIT_USER_AGENT` | ⚠️ | User agent string (auto-generated if not set) |
| `GROQ_API_KEY` | ❌ | Groq AI API key (optional, enables enhanced features) |

### Advanced Configuration

The system uses intelligent defaults, but you can customize:

- **Subreddit Rules**: Modify `config/templates.py` for custom posting rules
- **AI Prompts**: Customize AI generation prompts in the recommender
- **Database**: SQLite by default, easily extensible to PostgreSQL/MySQL

## 🧪 Testing

Run comprehensive tests to ensure everything works:

```bash
# Full system validation
python tests/test_final_validation.py

# Test Reddit posting (creates real test posts)
python tests/test_simple_posting.py

# Complete system health check
python scripts/complete_health_check.py
```

### Test Coverage

- ✅ **Environment & Configuration**: API keys and setup validation
- ✅ **Reddit Integration**: Live API connection and posting tests
- ✅ **AI Integration**: Content analysis and recommendation testing
- ✅ **Workflow Integration**: End-to-end process validation
- ✅ **Database Operations**: Data persistence and retrieval
- ✅ **Error Handling**: Comprehensive error scenarios

## 🚨 Important Notes

### Reddit Policy Compliance

This tool is designed to help create **valuable, educational content** for Reddit communities. Please:

- ✅ **Follow Reddit's Content Policy**: No spam, self-promotion only when educational
- ✅ **Respect Subreddit Rules**: The tool checks rules automatically, but review manually
- ✅ **Add Value**: Focus on helpful, informative content rather than promotion
- ✅ **Be Authentic**: Engage genuinely with communities

### Rate Limiting

- The tool respects Reddit's API rate limits automatically
- Built-in delays between requests to prevent throttling
- Smart retry mechanisms for temporary failures

### Security

- Never commit your `.env` file to version control
- Regularly rotate your API keys
- Use environment-specific configurations for development/production

## 🛠️ Development

### Project Structure

The codebase follows clean architecture principles:

- **Separation of Concerns**: Each module has a single responsibility
- **Dependency Injection**: Easy testing and mocking
- **Error Boundaries**: Isolated error handling per component
- **Configuration Management**: Centralized environment handling

### Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Adding New Features

The modular architecture makes it easy to extend:

- **New Subreddit Sources**: Extend the recommender engine
- **Additional AI Providers**: Add new AI client implementations
- **Custom Post Templates**: Modify the template system
- **New User Interfaces**: Create additional apps using the core modules

## 📊 Performance

### Benchmarks

- **Subreddit Analysis**: ~2-3 seconds per URL
- **Post Generation**: ~1-2 seconds per subreddit
- **Reddit Posting**: ~1 second per post (rate limited)
- **Database Operations**: ~10ms average query time

### Optimization

- Intelligent caching reduces API calls
- Asynchronous processing for multiple subreddits
- Connection pooling for database operations
- Smart retry mechanisms minimize failures

## 🆘 Troubleshooting

### Common Issues

**"Failed to connect to Reddit"**
- Verify your Reddit credentials in `.env`
- Ensure you created a "script" type app, not "web app"
- Check that your Reddit account is in good standing

**"No subreddit recommendations generated"**
- Verify your Groq API key if using AI features
- The system will use fallback algorithms without AI
- Check that your article URL is accessible

**"Permission denied when posting"**
- Verify your Reddit account has sufficient karma
- Check subreddit-specific posting requirements
- Ensure your account age meets minimum requirements

### Getting Help

1. **Check the logs**: Look in `logs/reddit_automation.log`
2. **Run health check**: `python scripts/complete_health_check.py`
3. **Validate setup**: `python tests/test_final_validation.py`
4. **Open an issue**: Use GitHub issues for bug reports

## 📈 Roadmap

### Upcoming Features

- 🔄 **Content Scheduling**: Queue posts for optimal timing
- 📊 **Advanced Analytics**: Detailed performance metrics
- 🎨 **Image Generation**: AI-generated relevant images
- 🌍 **Multi-Platform**: Support for Twitter, LinkedIn
- 👥 **Team Features**: Collaborative content management
- 🔐 **Enhanced Security**: OAuth2 authentication

### Version History

- **v1.0.0**: Initial release with core functionality
- **v1.1.0**: Enhanced AI integration and error handling
- **v1.2.0**: Web dashboard and complete workflow
- **v2.0.0**: Production-ready release with comprehensive testing

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **PRAW**: Excellent Python Reddit API wrapper
- **Streamlit**: Beautiful web app framework
- **Groq**: Fast AI inference platform
- **Reddit Community**: For creating valuable communities to share content

## 📞 Support

- 📧 **Email**: support@reddit-automation-toolkit.com
- 💬 **Discord**: [Join our community](https://discord.gg/reddit-automation)
- 📖 **Documentation**: [Full documentation](https://docs.reddit-automation-toolkit.com)
- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/yourusername/reddit-automation-toolkit/issues)

---

**Made with ❤️ for the Reddit community**

*This tool is designed to help create valuable, educational content for Reddit. Please use responsibly and in accordance with Reddit's content policy and community guidelines.*
