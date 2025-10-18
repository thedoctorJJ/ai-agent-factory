# Contributing to AI Agent Factory

Thank you for your interest in contributing to the AI Agent Factory! This guide will help you get started with contributing to the project.

## 🤝 How to Contribute

### 1. Fork and Clone
```bash
# Fork the repository on GitHub
git clone https://github.com/YOUR_USERNAME/ai-agent-factory.git
cd ai-agent-factory
```

### 2. Set Up Development Environment
```bash
# Run the development setup
./scripts/setup/dev-setup.sh

# Install pre-commit hooks
./scripts/setup/install-pre-commit-hook.sh
```

### 3. Create a Feature Branch
```bash
git checkout -b feature/your-feature-name
```

### 4. Make Your Changes
- Follow the [Code Standards](./code-standards.md)
- Write tests for new functionality
- Update documentation as needed

### 5. Test Your Changes
```bash
# Run tests
pytest
npm test

# Check linting
flake8 backend/
eslint frontend/next-app/
```

### 6. Submit a Pull Request
- Create a pull request on GitHub
- Follow the [Pull Request Process](./pull-request-process.md)
- Wait for review and feedback

## 📋 Development Setup

### Prerequisites
- Python 3.11+
- Node.js 18+
- Docker & Docker Compose
- Git

### Environment Setup
```bash
# Initialize environment
./scripts/config/env-manager.sh init

# Configure your local environment
# Edit config/env/.env.local with your values
```

### Running the Platform
```bash
# Backend
cd backend
source venv/bin/activate
uvicorn fastapi_app.main:app --reload

# Frontend
cd frontend/next-app
npm run dev
```

## 🎯 Areas for Contribution

### Backend (FastAPI)
- API endpoints and routes
- Business logic and services
- Database models and migrations
- Authentication and authorization

### Frontend (Next.js)
- React components and pages
- UI/UX improvements
- State management
- API integration

### Documentation
- User guides and tutorials
- API documentation
- Architecture documentation
- Code comments and docstrings

### Infrastructure
- Docker configurations
- CI/CD pipelines
- Deployment scripts
- Monitoring and logging

### Testing
- Unit tests
- Integration tests
- End-to-end tests
- Performance tests

## 📖 Code Standards

### Python (Backend)
- Follow PEP 8 style guide
- Use type hints
- Write docstrings for functions and classes
- Use meaningful variable and function names

### TypeScript/JavaScript (Frontend)
- Follow ESLint configuration
- Use TypeScript for type safety
- Follow React best practices
- Use meaningful component and variable names

### General
- Write clear, self-documenting code
- Add comments for complex logic
- Keep functions small and focused
- Use consistent naming conventions

## 🧪 Testing

### Backend Testing
```bash
cd backend
pytest tests/ -v
pytest tests/ --cov=fastapi_app
```

### Frontend Testing
```bash
cd frontend/next-app
npm test
npm run test:coverage
```

### Integration Testing
```bash
# Run full integration tests
./scripts/testing/run-integration-tests.sh
```

## 📝 Documentation

### Writing Documentation
- Use clear, concise language
- Include code examples
- Keep documentation up-to-date
- Follow the established structure

### Documentation Structure
- **Getting Started**: Basic setup and usage
- **Architecture**: System design and components
- **Guides**: Detailed how-to guides
- **API Reference**: Complete API documentation
- **Deployment**: Production deployment guides

## 🔄 Pull Request Process

### Before Submitting
1. **Test your changes** thoroughly
2. **Update documentation** if needed
3. **Check for linting errors**
4. **Ensure all tests pass**

### Pull Request Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] Tests added/updated
```

### Review Process
1. **Automated checks** must pass
2. **Code review** by maintainers
3. **Testing** in staging environment
4. **Approval** and merge

## 🐛 Reporting Issues

### Bug Reports
- Use the GitHub issue template
- Include steps to reproduce
- Provide environment details
- Add relevant logs or screenshots

### Feature Requests
- Describe the feature clearly
- Explain the use case
- Consider implementation complexity
- Discuss with maintainers first

## 💬 Community

### Communication
- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: General questions and ideas
- **Pull Requests**: Code contributions and reviews

### Code of Conduct
- Be respectful and inclusive
- Focus on constructive feedback
- Help others learn and grow
- Follow the project's values

## 🏆 Recognition

Contributors are recognized in:
- **README.md**: Contributor list
- **Release notes**: Feature acknowledgments
- **GitHub**: Contributor statistics

## 📄 License

By contributing, you agree that your contributions will be licensed under the same license as the project.

---

Thank you for contributing to the AI Agent Factory! 🚀
