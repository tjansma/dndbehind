# DnD Behind

A Flask-based REST API for managing D&D characters and related content with role-based access control.

## Features

- User authentication with JWT tokens
- Role-based access control (RBAC)
- Character management
- Background management
- Comprehensive test coverage
- Docker deployment support

## Quick Start

1. Clone the repository and install dependencies:
```bash
git clone <repository-url>
cd dndbehind
python -m venv .venv
.venv\Scripts\activate  # On Windows
source .venv/bin/activate  # On Unix
pip install -e ".[test]"
```

2. Set up environment:
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. Initialize database and run:
```bash
flask db upgrade
flask run
```

## Documentation

Comprehensive documentation is available in the `doc/` directory:

- [API Documentation](doc/api.md)
- [Architecture Overview](doc/architecture.md)
- [Development Guide](doc/development_guide.md)
- [Code Documentation](doc/code_documentation.md)
- [Project Structure](doc/project_inventory.md)

## Testing

Run the test suite:
```bash
pytest
```

Generate coverage report:
```bash
pytest --cov=dndbehind --cov-report=html:doc/coverage tests/
```

## Docker

Build and run with Docker:
```bash
docker build -t dndbehind .
docker run -p 5000:5000 dndbehind
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.