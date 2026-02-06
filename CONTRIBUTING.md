# Contributing to Occamy Field Operations System

Thank you for your interest in contributing to the Occamy Field Operations System! This document provides guidelines and instructions for contributing.

## Table of Contents
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Code Style](#code-style)
- [Testing](#testing)
- [Pull Request Process](#pull-request-process)
- [Feature Requests](#feature-requests)
- [Bug Reports](#bug-reports)

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/yourusername/occamy-field-ops.git`
3. Add upstream remote: `git remote add upstream https://github.com/occamy/field-ops.git`
4. Create a branch: `git checkout -b feature/your-feature-name`

## Development Setup

### Prerequisites
- Python 3.8 or higher
- pip
- virtualenv (recommended)

### Installation

1. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Copy environment file:
```bash
cp .env.example .env
```

4. Initialize database:
```bash
python app.py
```

5. Load demo data (optional):
```bash
python create_demo_data.py
```

### Running the Application

```bash
python app.py
```

The application will be available at `http://localhost:5000`

## Code Style

### Python Style Guide

We follow PEP 8 with some modifications:

- **Line length**: 100 characters maximum
- **Indentation**: 4 spaces (no tabs)
- **Imports**: Group by stdlib, third-party, local
- **Docstrings**: Use triple quotes for all functions and classes

### Example

```python
from datetime import datetime
from flask import Flask, request, jsonify

from app import db
from models import User


def create_user(username, email, password):
    """
    Create a new user in the database.
    
    Args:
        username (str): Unique username
        email (str): User email address
        password (str): Plain text password (will be hashed)
    
    Returns:
        User: Created user object
    
    Raises:
        ValueError: If username or email already exists
    """
    # Check if user exists
    if User.query.filter_by(username=username).first():
        raise ValueError('Username already exists')
    
    # Create user
    user = User(
        username=username,
        email=email,
        password_hash=generate_password_hash(password)
    )
    db.session.add(user)
    db.session.commit()
    
    return user
```

### HTML/CSS Style

- **HTML**: Use semantic HTML5 elements
- **CSS**: Mobile-first approach, avoid !important
- **JavaScript**: Use ES6+ features, avoid jQuery

### Naming Conventions

- **Variables**: `snake_case`
- **Functions**: `snake_case`
- **Classes**: `PascalCase`
- **Constants**: `UPPER_CASE`
- **Files**: `snake_case.py`

## Testing

### Running Tests

```bash
python tests.py
```

Or with pytest:
```bash
pytest tests.py -v
```

### Writing Tests

All new features should include tests. Place tests in `tests.py`:

```python
class NewFeatureTests(OccamyTestCase):
    """Test new feature"""
    
    def test_feature_works(self):
        """Test that feature works as expected"""
        # Arrange
        self.login('test_admin', 'test123')
        
        # Act
        response = self.client.get('/api/new-endpoint')
        
        # Assert
        self.assertEqual(response.status_code, 200)
```

### Test Coverage

Aim for at least 80% code coverage. Check coverage with:

```bash
pip install coverage
coverage run -m pytest tests.py
coverage report
```

## Pull Request Process

### Before Submitting

1. **Update documentation**: Update README.md if needed
2. **Run tests**: Ensure all tests pass
3. **Check code style**: Follow PEP 8
4. **Update changelog**: Add entry to CHANGELOG.md (if exists)
5. **Test manually**: Verify feature works in browser

### PR Guidelines

1. **Title**: Clear, descriptive title
   - Good: "Add export to Excel feature for admin dashboard"
   - Bad: "Fixed stuff"

2. **Description**: Include:
   - What: What does this PR do?
   - Why: Why is this change needed?
   - How: How does it work?
   - Testing: How was it tested?

3. **Commits**: 
   - Use meaningful commit messages
   - One logical change per commit
   - Reference issues: "Fixes #123"

### Example PR Description

```markdown
## Add Excel Export Feature

### What
Adds ability for admins to export activity data to Excel format.

### Why
Admins requested offline data analysis capabilities.

### How
- Added `/api/admin/export` endpoint
- Uses openpyxl library
- Generates Excel file with multiple sheets

### Testing
- Manual testing with 1000+ records
- Added unit tests in tests.py
- Tested in Chrome, Firefox, Safari

### Screenshots
[Include screenshots if UI changes]

Fixes #45
```

## Feature Requests

### Before Submitting

1. **Search existing issues**: Check if already requested
2. **Check roadmap**: May already be planned
3. **Discuss in issues**: Get feedback before coding

### Feature Request Template

```markdown
## Feature Request: [Name]

### Problem
[Describe the problem this solves]

### Proposed Solution
[How should it work?]

### Alternatives Considered
[What other approaches did you consider?]

### Additional Context
[Screenshots, mockups, examples]
```

## Bug Reports

### Before Submitting

1. **Update to latest version**: Bug may be fixed
2. **Check existing issues**: May already be reported
3. **Reproduce consistently**: Verify bug is reproducible

### Bug Report Template

```markdown
## Bug Report: [Brief Description]

### Environment
- OS: [e.g., Windows 10, Ubuntu 20.04]
- Browser: [e.g., Chrome 96]
- Python: [e.g., 3.9.7]
- Version: [e.g., 1.0.0]

### Expected Behavior
[What should happen?]

### Actual Behavior
[What actually happens?]

### Steps to Reproduce
1. Go to '...'
2. Click on '...'
3. Scroll down to '...'
4. See error

### Error Messages
[Include full error traceback]

### Screenshots
[If applicable]
```

## Development Workflow

### Branching Strategy

- `main`: Production-ready code
- `develop`: Development branch
- `feature/*`: New features
- `bugfix/*`: Bug fixes
- `hotfix/*`: Urgent production fixes

### Example Workflow

```bash
# Update your fork
git checkout main
git pull upstream main

# Create feature branch
git checkout -b feature/excel-export

# Make changes and commit
git add .
git commit -m "Add Excel export functionality"

# Push to your fork
git push origin feature/excel-export

# Create pull request on GitHub
```

## Code Review Process

### For Reviewers

- **Be kind**: Constructive feedback only
- **Be specific**: Point out exact issues
- **Explain why**: Don't just say "change this"
- **Approve or request changes**: Clear decision

### For Contributors

- **Respond promptly**: Address feedback quickly
- **Don't take it personally**: It's about the code
- **Ask questions**: If you don't understand feedback
- **Be patient**: Reviews take time

## Areas We Need Help

### High Priority
- [ ] Photo upload and storage
- [ ] Offline data sync
- [ ] Mobile app (React Native)
- [ ] Excel/PDF export

### Medium Priority
- [ ] SMS notifications
- [ ] WhatsApp integration
- [ ] Multi-language support
- [ ] Advanced analytics

### Low Priority
- [ ] Dark mode
- [ ] Email reports
- [ ] Custom branding
- [ ] Integration with accounting software

## Questions?

- **Issues**: GitHub Issues for bugs and features
- **Discussions**: GitHub Discussions for questions
- **Email**: dev@occamy.com for private inquiries

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.

## Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Given appropriate credit in documentation

Thank you for contributing! 🎉
