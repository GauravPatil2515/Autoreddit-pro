# 🚀 AutoReddit Pro - AI-Powered Reddit Content Automation

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.32+-red.svg)](https://streamlit.io/)
[![PRAW](https://img.shields.io/badge/praw-7.7+-orange.svg)](https://praw.readthedocs.io/)
[![Groq](https://img.shields.io/badge/groq-ai-green.svg)](https://groq.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Professional Reddit content automation toolkit powered by Groq's free Llama models. Transform your blog articles into engaging, policy-compliant Reddit posts with intelligent subreddit recommendations and one-click posting.

## ✨ Features

### 🎯 Complete End-to-End Workflow

- **Smart Content Analysis**: AI-powered article analysis and topic extraction
- **Intelligent Recommendations**: Advanced subreddit suggestion algorithm with relevance scoring
- **Policy Compliance**: Automatic rule checking and compliance validation
- **One-Click Posting**: Direct posting to Reddit with full API integration
- **Real-time Monitoring**: Live dashboard with analytics and post tracking

### 🤖 AI-Powered Intelligence

- **Free Groq Llama Models**: No API costs - uses Groq's free tier
- **Content Understanding**: Deep analysis of article themes and topics
- **Natural Language Generation**: Human-like post creation
- **Smart Subreddit Matching**: ML-powered community recommendations

### 🌐 Professional Web Interface

- **Modern Streamlit Dashboard**: Beautiful, responsive web interface
- **Real-time Analytics**: Post performance tracking and insights
- **Workflow Visualization**: Step-by-step process monitoring
- **History Management**: Complete posting history with filtering

### ⚡ Terminal Automation

- **CLI Tools**: Command-line interface for automation scripts
- **Batch Processing**: Handle multiple articles efficiently
- **Scheduled Posting**: Integration-ready scheduling system
- **Developer-Friendly**: Perfect for CI/CD pipelines

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Reddit account and API credentials
- Groq API key (free)

### 1. Installation

```bash
git clone https://github.com/yourusername/autoreddit-pro.git
cd autoreddit-pro
pip install -r requirements.txt
```

### 2. Configuration

```bash
cp .env.example .env
# Edit .env with your API credentials
```

### 3. Launch Dashboard

```bash
streamlit run apps/enhanced_dashboard.py
```

Visit `http://localhost:8501` to access the web interface!

## 📋 Setup Guide

### Get Reddit API Credentials

1. Visit [Reddit Apps](https://www.reddit.com/prefs/apps)
2. Create a new app (type: "script")
3. Note your client ID and secret
4. Add credentials to `.env` file

### Get Groq AI API Key (Free)

1. Visit [Groq Console](https://console.groq.com)
2. Sign up for free account
3. Generate API key
4. Add to `.env` file

### Environment Variables

```bash
# Reddit API Configuration
REDDIT_CLIENT_ID=your_client_id
REDDIT_CLIENT_SECRET=your_client_secret
REDDIT_USERNAME=your_username
REDDIT_PASSWORD=your_password
REDDIT_USER_AGENT=AutoRedditPro/1.0 by your_username

# Groq AI Configuration (Free)
GROQ_API_KEY=your_groq_api_key
```

## 🎯 Usage Examples

### Web Dashboard

```bash
# Launch the enhanced dashboard
streamlit run apps/enhanced_dashboard.py

# Custom port
streamlit run apps/enhanced_dashboard.py --server.port=8080
```

### Terminal Automation

```bash
# Get subreddit recommendations
python apps/terminal_automation.py recommend "https://medium.com/@author/article"

# Generate post for specific subreddit
python apps/terminal_automation.py generate "https://medium.com/@author/article" --subreddit programming

# View posting history
python apps/terminal_automation.py history
```

### Interactive Menu

```bash
# Launch interactive application selector
python main.py
```

## 🏗️ Architecture

```
autoreddit-pro/
├── 📁 apps/                    # Main applications
│   ├── enhanced_dashboard.py   # Streamlit web interface
│   └── terminal_automation.py  # CLI automation tool
├── 📁 core/                    # Core modules
│   ├── ai_client.py           # Groq AI integration
│   ├── enhanced_reddit_client.py # Reddit API client
│   ├── enhanced_subreddit_recommender.py # AI recommendations
│   ├── workflow_manager.py    # Workflow orchestration
│   ├── database.py           # SQLite database
│   ├── error_handling.py     # Error management
│   └── utils.py              # Utility functions
├── 📁 config/                 # Configuration
│   └── templates.py          # Post templates
├── 📁 tests/                  # Test suite
├── 📁 docs/                   # Documentation
└── 📁 scripts/               # Utility scripts
```

## 🔧 Advanced Features

### Workflow Management

- **Multi-step Processing**: URL → Analysis → Recommendations → Generation → Posting
- **Error Recovery**: Robust error handling with automatic retries
- **Progress Tracking**: Real-time workflow status monitoring
- **Validation**: Pre-posting compliance and quality checks

### AI Integration

- **Multiple Models**: Support for various Groq Llama models
- **Smart Prompting**: Optimized prompts for different content types
- **Context Awareness**: Understanding of subreddit cultures and rules
- **Quality Control**: AI-powered content quality assessment

### Database Features

- **Post History**: Complete tracking of all posted content
- **Analytics**: Performance metrics and insights
- **Search**: Advanced filtering and search capabilities
- **Export**: Data export for external analysis

## 📊 Testing

### Run Health Check

```bash
python scripts/complete_health_check.py
```

### Run Test Suite

```bash
# Complete system tests
python tests/test_complete_system.py

# Specific component tests
python tests/test_final_validation.py
python tests/test_subreddit_recommendations.py
```

### Validation Results

- ✅ Environment Setup
- ✅ Core Modules
- ✅ Reddit Functionality
- ✅ AI Integration
- ✅ Database Operations
- ✅ Workflow Integration
- ✅ Error Handling

## 🚀 Deployment

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env with your credentials

# Run health check
python scripts/complete_health_check.py

# Start dashboard
streamlit run apps/enhanced_dashboard.py
```

### Docker Deployment

```bash
# Build image
docker build -t autoreddit-pro .

# Run container
docker run -p 8501:8501 --env-file .env autoreddit-pro
```

### Cloud Deployment

- **Streamlit Cloud**: One-click deployment
- **Heroku**: Full-stack deployment with database
- **AWS/GCP/Azure**: Enterprise-grade scaling

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions.

## 📈 Performance

- **Fast Processing**: Sub-second subreddit recommendations
- **Efficient API Usage**: Optimized for rate limits
- **Scalable Architecture**: Handles multiple concurrent workflows
- **Low Resource Usage**: Minimal memory and CPU footprint

## 🛡️ Security & Compliance

- **Secure Credential Storage**: Environment-based configuration
- **Rate Limiting**: Respects Reddit API limits
- **Policy Compliance**: Automatic subreddit rule checking
- **Error Handling**: Graceful failure management
- **Audit Trail**: Complete logging of all operations

## 🤝 Contributing

We welcome contributions! Please see our Contributing Guidelines for details.

### Development Setup

```bash
# Clone repository
git clone https://github.com/yourusername/autoreddit-pro.git
cd autoreddit-pro

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements.txt

# Run tests
python -m pytest tests/
```

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Groq**: For providing free access to powerful Llama models
- **Reddit**: For their comprehensive API
- **Streamlit**: For the amazing web framework
- **PRAW**: For the excellent Reddit API wrapper

## 📞 Support

- **Documentation**: [Full Documentation](docs/)
- **Issues**: GitHub Issues
- **Discussions**: GitHub Discussions

## 🗺️ Roadmap

- [ ] Advanced analytics dashboard
- [ ] Mobile-responsive interface  
- [ ] Scheduled posting with calendar
- [ ] Multi-account management
- [ ] Advanced content templates
- [ ] Integration with more AI models
- [ ] WordPress/Ghost integration
- [ ] Browser extension

---

**Made with ❤️ for the Reddit community**

*AutoReddit Pro - Where AI meets Reddit automation*
