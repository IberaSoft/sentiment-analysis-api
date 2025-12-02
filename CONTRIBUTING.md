# Contributing

Thank you for your interest in contributing to the Sentiment Analysis API! This document provides guidelines and instructions for contributing.

## Getting Started

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/your-username/sentiment-analysis-api.git
   cd sentiment-analysis-api
   ```
3. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```
4. Install development dependencies:
   ```bash
   pip install -r requirements-dev.txt
   ```
5. Set up pre-commit hooks:
   ```bash
   pre-commit install
   ```

## Development Workflow

1. Create a new branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```
2. Make your changes
3. Run tests:
   ```bash
   pytest tests/ -v
   ```
4. Run linters:
   ```bash
   black app/ tests/
   isort app/ tests/
   flake8 app/ tests/
   ```
5. Commit your changes:
   ```bash
   git commit -m "Add feature: description"
   ```
6. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```
7. Create a Pull Request

## Code Style

- Follow PEP 8
- Use Black for formatting
- Use isort for import sorting
- Maximum line length: 100 characters
- Use type hints where possible

## Testing

- Write tests for all new features
- Aim for >80% code coverage
- Run tests before submitting PR:
  ```bash
  pytest tests/ --cov=app --cov-report=html
  ```

## Pull Request Guidelines

- Provide a clear description of changes
- Reference related issues
- Ensure all tests pass
- Update documentation if needed
- Keep PRs focused and reasonably sized

## Types of Contributions

### Bug Reports

- Use the GitHub issue tracker
- Include steps to reproduce
- Provide error messages and logs
- Specify environment details

### Feature Requests

- Open an issue describing the feature
- Discuss implementation approach
- Wait for approval before implementing

### Documentation

- Fix typos and improve clarity
- Add examples and use cases
- Update API documentation

### Code Contributions

- Fix bugs
- Implement approved features
- Improve performance
- Refactor code

## Questions?

Feel free to open an issue for questions or discussions.

Thank you for contributing! 🎉

