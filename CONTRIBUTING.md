# Contributing to AutoReddit Pro

Thank you for your interest in contributing to AutoReddit Pro! This document provides guidelines for contributing to the project.

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- Reddit API credentials
- Groq API key (free)

### Development Setup

1. **Fork the repository**
   ```bash
   # Clone your fork
   git clone https://github.com/your-username/autoreddit-pro.git
   cd autoreddit-pro
   ```

2. **Set up virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment**
   ```bash
   cp .env.example .env
   # Edit .env with your API credentials
   ```

5. **Run health check**
   ```bash
   python scripts/complete_health_check.py
   ```

## 📝 How to Contribute

### Reporting Bugs

1. **Check existing issues** first to avoid duplicates
2. **Use the bug report template** when creating new issues
3. **Include detailed information**:
   - Python version
   - Operating system
   - Error messages and stack traces
   - Steps to reproduce

### Suggesting Features

1. **Check existing feature requests** first
2. **Use the feature request template**
3. **Explain the use case** and expected behavior
4. **Consider implementation complexity**

### Submitting Pull Requests

1. **Create a new branch** for your feature/fix
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Follow the coding standards below
   - Add tests for new functionality
   - Update documentation as needed

3. **Test your changes**
   ```bash
   # Run all tests
   python tests/test_complete_system.py
   python tests/test_final_validation.py
   
   # Run health check
   python scripts/complete_health_check.py
   ```

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add new feature description"
   ```

5. **Push and create pull request**
   ```bash
   git push origin feature/your-feature-name
   ```

## 🎯 Coding Standards

### Python Style Guide

- Follow **PEP 8** for Python code style
- Use **type hints** where appropriate
- Write **docstrings** for all functions and classes
- Keep functions **small and focused**
- Use **meaningful variable names**

### Code Structure

```python
"""
Module docstring explaining the purpose
"""
from typing import Dict, List, Optional
import sys
import os

class ExampleClass:
    """Class docstring explaining the purpose"""
    
    def __init__(self):
        """Initialize the class"""
        pass
    
    def example_method(self, param: str) -> Dict:
        """
        Method docstring explaining what it does
        
        Args:
            param: Description of parameter
            
        Returns:
            Description of return value
        """
        return {}
```

### Commit Message Format

Use conventional commit format:

- `feat: add new feature`
- `fix: resolve bug in module`
- `docs: update documentation`
- `style: format code`
- `refactor: improve code structure`
- `test: add or update tests`
- `chore: update dependencies`

## 🧪 Testing Guidelines

### Test Requirements

- **All new features** must include tests
- **All bug fixes** must include regression tests
- **Tests must pass** before submitting PR
- **Code coverage** should not decrease

### Running Tests

```bash
# Run all tests
python tests/test_complete_system.py

# Run specific test files
python tests/test_final_validation.py
python tests/test_subreddit_recommendations.py

# Run health check
python scripts/complete_health_check.py
```

### Writing Tests

```python
def test_example_functionality():
    """Test that example functionality works correctly"""
    # Arrange
    expected_result = "expected"
    
    # Act
    actual_result = your_function()
    
    # Assert
    assert actual_result == expected_result
```

## 📚 Documentation

### Documentation Requirements

- **Update README.md** for user-facing changes
- **Add docstrings** for all new functions/classes
- **Update API documentation** for interface changes
- **Include usage examples** for new features

### Documentation Style

- Use **clear, concise language**
- Include **code examples** where helpful
- Use **proper markdown formatting**
- Add **screenshots** for UI changes

## 🚀 Release Process

### Version Numbering

We use semantic versioning (semver):
- `MAJOR.MINOR.PATCH`
- `MAJOR`: Breaking changes
- `MINOR`: New features (backward compatible)
- `PATCH`: Bug fixes (backward compatible)

### Release Checklist

- [ ] All tests pass
- [ ] Documentation updated
- [ ] Version number bumped
- [ ] Changelog updated
- [ ] GitHub release created

## 🎯 Areas for Contribution

### High Priority

- **Performance optimization**
- **Error handling improvements**
- **Additional AI model support**
- **Mobile-responsive UI**

### Medium Priority

- **Advanced analytics**
- **Scheduled posting**
- **Multi-account support**
- **Browser extension**

### Low Priority

- **Additional integrations**
- **Advanced templates**
- **Internationalization**
- **Theme customization**

## 📞 Getting Help

### Community Support

- **GitHub Discussions**: For questions and ideas
- **GitHub Issues**: For bug reports and feature requests
- **Code Review**: All PRs receive thorough review

### Maintainer Contact

For urgent issues or security concerns, contact the maintainers directly.

## 📋 Code of Conduct

### Our Standards

- **Be respectful** and inclusive
- **Accept constructive criticism** gracefully
- **Focus on what's best** for the community
- **Show empathy** towards other contributors

### Unacceptable Behavior

- Harassment or discrimination
- Trolling or inflammatory comments
- Personal attacks
- Publishing private information

### Enforcement

Violations may result in temporary or permanent bans from the project.

---

Thank you for contributing to AutoReddit Pro! Your contributions help make Reddit automation better for everyone.
