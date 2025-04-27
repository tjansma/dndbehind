# Project File Inventory

## Root Directory Files

### Application Files
- `config.py`
  - Configuration classes for different environments
  - Environment variable handling
  - Database and JWT settings

- `pyproject.toml`
  - Project metadata
  - Dependencies management
  - Build configuration
  - Test settings

- `requirements.txt`
  - Pinned dependency versions
  - Production and development requirements

### Docker Files
- `Dockerfile`
  - Python 3.11 base image configuration
  - Application deployment setup
  - UVICORN server configuration

### Documentation
- `README.md`
  - Project introduction (needs expansion)
- `LICENSE`
  - MIT License text

### Environment Configuration
- `.env.example`
  - Template for environment variables
  - Database URL configuration
  - Secret key placeholders
- `.flaskenv`
  - Flask application configuration

## Application Package (`dndbehind/`)

### Core Files
- `__init__.py`
  - Flask application factory
  - Extension initialization
  - Blueprint registration

- `models.py`
  - SQLAlchemy model definitions
  - User and authentication models
  - D&D game-related models
  - TypedDict definitions

- `utils.py`
  - Utility functions
  - Response helpers
  - Validation functions

### Authentication Module (`auth/`)
- `__init__.py`
  - Blueprint definition
  - Module initialization

- `callbacks.py`
  - JWT callback functions
  - User lookup handling

- `rbac.py`
  - Role-based access control
  - Permission decorators
  - Resource ownership validation

- `routes.py`
  - Authentication endpoints
  - User management routes
  - Role management routes

### Management Module (`mgmt/`)
- `__init__.py`
  - Blueprint definition
  - Module initialization

- `routes.py`
  - Background management endpoints
  - Character management endpoints

## Database (`migrations/`)

### Migration Configuration
- `alembic.ini`
  - Alembic configuration
  - Migration settings

- `env.py`
  - Migration environment setup
  - Database connection handling

- `script.py.mako`
  - Migration script template

### Migration Versions
- `e5e25d18cbd7_users_table.py`
  - Initial users table creation

- `1202982b0431_character_and_background_tables.py`
  - Character and background tables

- `81d5ae96cb39_unique_constraint_on_background_name.py`
  - Background name uniqueness

- `e70bc18b2aa9_fixed_type_in_character_charisma.py`
  - Character attribute fix

- `e797f0dfe52a_user_roles.py`
  - Role management tables

## Tests (`tests/`)

### Test Configuration
- `conftest.py`
  - pytest fixtures
  - Test database setup
  - Test client configuration

### Test Modules
- `test_auth.py`
  - Authentication tests
  - User management tests
  - Role management tests

- `test_models.py`
  - Model validation tests
  - Relationship tests
  - Data integrity tests

- `test_utils.py`
  - Utility function tests
  - Helper function validation

## CI/CD Configuration

### GitLab CI
- `.gitlab-ci.yml`
  - Test pipeline configuration
  - Docker build steps
  - Deployment configuration

### Gitea Actions
- `.gitea/workflows/python-tests.yaml`
  - Python test workflow
  - Code coverage reporting
  - Linting configuration

## VS Code Configuration

### Editor Settings
- `.vscode/settings.json`
  - Editor preferences
  - Python test configuration
  - Font settings

### Launch Configuration
- `.vscode/launch.json`
  - Debug configurations
  - Flask development server setup