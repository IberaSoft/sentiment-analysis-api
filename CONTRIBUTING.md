# Contributing

Thank you for contributing to the Sentiment Analysis API!

## Setup

```bash
# Fork and clone
git clone https://github.com/your-username/sentiment-analysis-api.git
cd sentiment-analysis-api

# Setup environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements-dev.txt
pre-commit install
```

## Workflow

1. Create branch: `git checkout -b feature/your-feature`
2. Make changes
3. Run tests: `pytest tests/ -v`
4. Format code: `black app/ tests/ && isort app/ tests/`
5. Commit: `git commit -m "Add: description"`
6. Push: `git push origin feature/your-feature`
7. Create Pull Request

## Code Standards

- Follow PEP 8
- Use Black (max line length: 100)
- Use type hints
- Aim for >80% test coverage

## Pull Requests

- Clear description of changes
- Reference related issues
- All tests passing
- Update docs if needed

## Contributions

**Bug Reports**: Include steps to reproduce, error messages, environment details

**Feature Requests**: Open issue first, discuss approach, wait for approval

**Documentation**: Fix typos, add examples, improve clarity

**Code**: Fix bugs, implement approved features, improve performance

## Questions?

Open an issue for discussions.

Thank you! 🎉

