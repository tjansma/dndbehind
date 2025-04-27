# Development Guide

## Getting Started

### Prerequisites
- Python 3.11 or higher
- pip package manager
- virtualenv (recommended)
- Git

### Initial Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd dndbehind
```

2. Create and activate virtual environment:
```bash
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Unix:
source .venv/bin/activate
```

3. Install dependencies:
```bash
pip install -e ".[test]"
```

4. Set up environment variables:
- Copy `.env.example` to `.env`
- Generate secure keys for `SECRET_KEY` and `JWT_SECRET_KEY`
- Configure `DATABASE_URL` if not using SQLite

5. Initialize database:
```bash
flask db upgrade
```

## Development Workflow

### Running the Application

1. Start development server:
```bash
flask run
```

2. Access the API at `http://localhost:5000`

### Running Tests

1. Run all tests:
```bash
pytest
```

2. Run tests with coverage:
```bash
pytest --cov=dndbehind --cov-report=html:doc/coverage tests/
```

3. View coverage report in `doc/coverage/index.html`

### Database Migrations

1. Create a new migration:
```bash
flask db migrate -m "Description of changes"
```

2. Review migration script in `migrations/versions/`

3. Apply migration:
```bash
flask db upgrade
```

4. Rollback if needed:
```bash
flask db downgrade
```

## Code Structure

### Main Components

1. **Models** (`dndbehind/models.py`)
   - Database models
   - Type definitions
   - Model relationships

2. **Authentication** (`dndbehind/auth/`)
   - User authentication
   - Role-based access control
   - JWT handling

3. **Management** (`dndbehind/mgmt/`)
   - Content management
   - Resource endpoints

### Adding New Features

1. **New Model**
   - Add model class in `models.py`
   - Create migration
   - Add TypedDict if needed
   - Add tests in `tests/test_models.py`

2. **New Endpoint**
   - Choose appropriate blueprint
   - Add route function
   - Apply RBAC decorators
   - Add tests in corresponding test file

3. **New Authorization Rule**
   - Add decorator in `auth/rbac.py`
   - Apply to relevant routes
   - Add tests in `tests/test_auth.py`

## Best Practices

### Code Style
- Follow PEP 8 guidelines
- Use type hints
- Write comprehensive docstrings
- Keep functions focused and small
- Use meaningful variable names

### Testing
- Write tests for new features
- Maintain high coverage
- Test edge cases
- Use fixtures when appropriate
- Keep tests focused and descriptive

### Security
- Never commit secrets
- Use environment variables
- Validate all inputs
- Apply appropriate RBAC
- Handle errors gracefully

### Git Workflow
1. Create feature branch
2. Make focused commits
3. Write clear commit messages
4. Run tests before committing
5. Create pull request
6. Address review feedback

## Deployment

### Docker Deployment
1. Build image:
```bash
docker build -t dndbehind .
```

2. Run container:
```bash
docker run -p 5000:5000 \
  -e SECRET_KEY=<your-secret> \
  -e JWT_SECRET_KEY=<your-jwt-secret> \
  dndbehind
```

### Production Considerations
- Use production-grade database
- Set secure secret keys
- Configure proper logging
- Set up monitoring
- Use HTTPS
- Configure CORS properly
- Set appropriate JWT expiration

## Troubleshooting

### Common Issues

1. **Database Errors**
   - Check connection string
   - Verify migrations
   - Check permissions
   - Validate constraints

2. **Authentication Issues**
   - Verify JWT configuration
   - Check token expiration
   - Validate user credentials
   - Verify role assignments

3. **Permission Errors**
   - Check user roles
   - Verify ownership rules
   - Review RBAC decorators
   - Check JWT claims

### Debug Tools
- Flask debug mode
- pytest -v for verbose tests
- Database command line tools
- JWT debugging utilities