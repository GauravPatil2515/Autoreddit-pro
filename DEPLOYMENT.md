# Production Deployment Guide

This guide covers deploying the Reddit Automation Toolkit in a production environment.

## Prerequisites

- Python 3.8 or higher
- Git
- Virtual environment support
- Internet connection for API access

## Quick Production Setup

### 1. Clone and Setup
```bash
git clone https://github.com/your-username/reddit-automation-toolkit.git
cd reddit-automation-toolkit
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configuration
```bash
cp .env.example .env
# Edit .env with your API keys and credentials
```

### 3. Verify Installation
```bash
python scripts/complete_health_check.py
```

### 4. Launch Applications
```bash
# Web Dashboard
streamlit run apps/enhanced_dashboard.py

# Terminal Tool
python apps/terminal_automation.py

# Main Menu
python main.py
```

## API Keys Setup

### Reddit API
1. Visit https://www.reddit.com/prefs/apps
2. Create a new app (type: script)
3. Note the client ID and secret
4. Add to .env file

### Groq AI API
1. Visit https://console.groq.com
2. Create account and generate API key
3. Add to .env file

## Production Considerations

### Security
- Use environment variables for all secrets
- Never commit .env files to version control
- Consider using secrets management systems
- Implement proper authentication for web access

### Performance
- Monitor API rate limits
- Implement proper error handling and retries
- Use database connections efficiently
- Consider caching for frequently accessed data

### Monitoring
- Enable logging in production
- Monitor system resources
- Set up alerts for failures
- Track API usage and costs

### Scaling
- Consider containerization with Docker
- Use reverse proxy for web access
- Implement load balancing if needed
- Consider cloud deployment options

## Docker Deployment (Optional)

Create `Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8501

CMD ["streamlit", "run", "apps/enhanced_dashboard.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

Build and run:
```bash
docker build -t reddit-automation .
docker run -p 8501:8501 --env-file .env reddit-automation
```

## Cloud Deployment Options

### Streamlit Cloud
1. Push to GitHub
2. Connect to Streamlit Cloud
3. Add secrets in dashboard
4. Deploy automatically

### Heroku
1. Create Procfile: `web: streamlit run apps/enhanced_dashboard.py --server.port=$PORT`
2. Add buildpack: `heroku/python`
3. Set config vars for environment variables
4. Deploy

### AWS/GCP/Azure
- Use container services for scalability
- Set up proper networking and security
- Configure auto-scaling based on usage
- Use managed databases for persistence

## Maintenance

### Regular Tasks
- Update dependencies monthly
- Monitor API key expiration
- Clean up old logs and data
- Review and update configurations

### Backup Strategy
- Backup database regularly
- Store configuration backups
- Document deployment procedures
- Test recovery procedures

## Troubleshooting

### Common Issues
1. **API Rate Limits**: Implement exponential backoff
2. **Memory Usage**: Monitor and optimize database queries
3. **Network Issues**: Add proper retry logic
4. **Authentication Errors**: Verify API keys and permissions

### Debug Mode
Enable debug logging by setting `DEBUG=true` in .env file.

### Support
- Check logs first: `logs/` directory
- Run health check: `python scripts/complete_health_check.py`
- Review error messages and stack traces
- Check API status pages for service outages

## Performance Optimization

### Database
- Regular vacuum/optimize operations
- Index frequently queried columns
- Archive old data periodically
- Monitor query performance

### Caching
- Cache subreddit recommendations
- Store frequently accessed configurations
- Use in-memory caching for temporary data
- Implement cache invalidation strategies

### API Usage
- Batch requests where possible
- Implement intelligent retry logic
- Monitor rate limit headers
- Use webhooks instead of polling when available

## Security Best Practices

### API Security
- Rotate API keys regularly
- Use least privilege principles
- Monitor API usage for anomalies
- Implement request validation

### Application Security
- Keep dependencies updated
- Use secure communication (HTTPS)
- Implement proper input validation
- Log security events

### Data Privacy
- Follow data retention policies
- Implement data anonymization
- Secure data transmission
- Regular security audits
