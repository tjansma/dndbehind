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

# DnD Behind Architecture Documentation

## Overview
DnD Behind is a Flask-based web application that provides a RESTful API for managing D&D (Dungeons & Dragons) characters and related content. The application uses a modular architecture with clear separation of concerns and follows the principles of role-based access control (RBAC).

## System Components

### Core Components
1. **Flask Application Factory** (`__init__.py`)
   - Initializes Flask application
   - Sets up database connection
   - Configures JWT authentication
   - Registers blueprints for different modules

2. **Configuration Management** (`config.py`)
   - Manages different configuration environments (Production, Testing)
   - Handles environment variables and secrets
   - Configures database connections and JWT settings

3. **Database Layer** (SQLAlchemy)
   - Uses Flask-SQLAlchemy for ORM
   - Supports multiple database backends through SQLAlchemy
   - Migration management through Flask-Migrate (Alembic)

### Authentication & Authorization
1. **JWT Authentication** (`auth/routes.py`)
   - Token-based authentication using Flask-JWT-Extended
   - Secure password hashing using Argon2
   - Session management and user lookup

2. **Role-Based Access Control** (`auth/rbac.py`)
   - Decorator-based permission system
   - Role management and verification
   - User-resource ownership validation

### Feature Modules

1. **Authentication Module** (`auth/`)
   - User management
   - Login/authentication
   - Role management
   - Access control decorators

2. **Management Module** (`mgmt/`)
   - Character background management
   - Character data management
   - Content administration features

## Data Models

### Core Models
1. **User Model**
   - Basic user information
   - Authentication data
   - Role relationships
   - Character ownership

2. **Role Model**
   - Role definitions
   - Permission assignments
   - User associations

3. **Character Model**
   - Character attributes
   - Background relationships
   - Owner relationships

4. **Background Model**
   - Background definitions
   - Character associations

## Security Architecture

### Authentication Flow
1. **User Registration**
   - Secure password hashing
   - Unique constraint validation
   - Email verification (planned)

2. **User Authentication**
   - JWT token generation
   - Role-based claims
   - Token expiration handling

### Authorization System
1. **Role-Based Access Control**
   - Hierarchical roles
   - Resource ownership verification
   - Action-based permissions

2. **Security Decorators**
   - `@role_required`
   - `@self_or_role_required`
   - `@owner_or_role_required`

## Database Schema

### Tables
1. **user**
   - Primary user information
   - Authentication data
   - Account status tracking

2. **role**
   - Role definitions
   - Permission assignments

3. **user_role**
   - Many-to-many relationship table
   - User-role associations

4. **character**
   - Character attributes
   - Ownership references
   - Background references

5. **background**
   - Background definitions
   - Shared content data

## Deployment Architecture

### Docker Deployment
- Python 3.11 base image
- UVICORN ASGI server
- Environment variable configuration
- Port 5000 exposed

### CI/CD Pipeline
1. **Testing Phase**
   - pytest execution
   - Coverage reporting
   - Linting checks

2. **Build Phase**
   - Docker image creation
   - Registry pushing
   - Version tagging

## Development Environment

### Tools and Dependencies
- Python 3.11+
- Flask framework
- SQLAlchemy ORM
- Alembic migrations
- pytest testing framework
- Coverage.py for test coverage
- Docker for containerization

### Development Workflow
1. Local development with SQLite
2. Automated testing with in-memory database
3. Docker build for deployment
4. CI/CD pipeline integration

# DnD Behind API Documentation

## Authentication

### User Management Endpoints

#### POST /auth/user
Creates a new user account.

**Request Body:**
```json
{
    "username": "string",
    "email": "string",
    "password": "string"
}
```

**Responses:**
- 201: User created successfully
- 400: Missing required fields
- 409: Duplicate email/username

#### POST /auth/login
Authenticates a user and returns a JWT token.

**Request Body:**
```json
{
    "username": "string",
    "password": "string"
}
```

**Responses:**
- 200: Success with JWT token
- 400: Missing credentials
- 401: Invalid credentials

#### GET /auth/whoami
Returns the current user's information (requires JWT).

**Responses:**
- 200: User information
- 401: Unauthorized

### Role Management Endpoints

#### GET /auth/userrole
Lists all users and their roles (requires admin role).

**Responses:**
- 200: List of users with roles
- 403: Access denied

#### PUT /auth/userrole/{user_id}
Adds roles to a user (requires admin role).

**Request Body:**
```json
{
    "roles": ["string"]
}
```

**Responses:**
- 200: Roles assigned
- 400: Invalid request
- 403: Access denied
- 404: User not found

#### DELETE /auth/userrole/{user_id}
Removes roles from a user (requires admin role).

**Request Body:**
```json
{
    "roles": ["string"]
}
```

**Responses:**
- 200: Roles removed
- 400: Invalid request
- 403: Access denied
- 404: User/role not found

## Content Management

### Background Management

#### POST /background
Creates a new character background (requires maintainer role).

**Request Body:**
```json
{
    "name": "string",
    "description": "string"
}
```

**Responses:**
- 200: Background created
- 400: Invalid request
- 403: Access denied

#### GET /background
Lists all character backgrounds (requires maintainer role).

**Responses:**
- 200: List of backgrounds
- 403: Access denied

### Character Management

#### GET /character/{character_id}
Gets character information (requires ownership or operator role).

**Responses:**
- 200: Character information
- 403: Access denied
- 404: Character not found

# Code Documentation

## Models Module (`models.py`)

### User Class
```python
class User(UserMixin, db.Model)
```
Base user class that handles authentication and role management.

#### Methods
- `set_password(password: str) -> None`
  - Hashes and sets the user's password using Argon2
  - Args: password (str) - The plain text password to hash

- `check_password(password: str) -> bool`
  - Validates a password against the stored hash
  - Returns: bool - True if password matches, False otherwise

- `update_login_time() -> None`
  - Updates the last_logged_in timestamp to current UTC time

- `as_dict() -> UserDict`
  - Converts user object to dictionary representation
  - Returns: UserDict containing user data

- `from_id(user_id: int) -> Self`
  - Class method to retrieve user by ID
  - Raises: LookupError if user not found

### Role Class
```python
class Role(db.Model)
```
Represents user roles for RBAC implementation.

#### Methods
- `from_rolename(rolename: str) -> Self`
  - Class method to retrieve role by name
  - Raises: LookupError if role not found

- `as_dict() -> dict`
  - Converts role object to dictionary representation

### Character Class
```python
class Character(db.Model)
```
Represents a D&D character with attributes and relationships.

#### Methods
- `as_dict() -> CharacterDict`
  - Converts character object to dictionary representation
  - Returns: CharacterDict containing character data

### Background Class
```python
class Background(db.Model)
```
Represents character backgrounds with descriptions.

#### Methods
- `as_dict() -> BackgroundDict`
  - Converts background object to dictionary representation
  - Returns: BackgroundDict containing background data

## Authentication Module (`auth/`)

### RBAC Decorators (`rbac.py`)

#### Functions
- `role_required(*role_names: tuple[str]) -> Callable`
  - Decorator that checks if user has required role(s)
  - Args: role_names - Tuple of required role names

- `self_or_role_required(user_id_arg_name: str, *role_names: tuple[str]) -> Callable`
  - Decorator for endpoints requiring self-access or specific role(s)
  - Args:
    - user_id_arg_name: Name of user ID parameter
    - role_names: Tuple of allowed role names

- `owner_or_role_required(resource_type: type, resource_id_arg_name: str, *role_names: tuple[str]) -> Callable`
  - Decorator for endpoints requiring resource ownership or specific role(s)
  - Args:
    - resource_type: Type of resource (e.g., Character)
    - resource_id_arg_name: Name of resource ID parameter
    - role_names: Tuple of allowed role names

### JWT Callbacks (`callbacks.py`)

#### Functions
- `user_lookup_callback(_jwt_header: dict[str, Any], jwt_data: dict[str, Any]) -> User | None`
  - Callback for JWT user lookup
  - Returns: User object if found, None otherwise

## Management Module (`mgmt/`)

### Routes (`routes.py`)

#### Endpoints
- `create_background() -> Response`
  - Creates new character background
  - Requires: maintainer role
  - Returns: JSON response with new background data

- `list_backgrounds() -> Response`
  - Lists all character backgrounds
  - Requires: maintainer role
  - Returns: JSON array of backgrounds

- `get_character(character_id: int) -> Response`
  - Retrieves character data
  - Requires: character ownership or operator role
  - Returns: JSON response with character data

## Utility Functions (`utils.py`)

### Functions
- `required_keys_present(required_keys: set[str], data: dict[str, Any]) -> bool`
  - Validates presence of required keys in dictionary
  - Returns: bool indicating if all required keys exist

- `make_response_without_resource_state(message: str, status_code: int) -> Response`
  - Creates JSON response without resource data
  - Returns: Flask Response object

- `make_response_with_resource_state(message: str, status_code: int, resource_state: dict[str, str | int]) -> Response`
  - Creates JSON response including resource data
  - Returns: Flask Response object

  # Dynamic Behavior Documentation

## Authentication Flows

### User Registration Flow
1. Client sends POST request to `/auth/user` with username, email, and password
2. Server validates required fields
3. Server checks for unique constraints on username and email
4. Password is hashed using Argon2
5. New user record is created in database
6. Response includes user data and Location header with user resource URL

### Login Flow
1. Client sends POST request to `/auth/login` with username and password
2. Server validates credentials
3. Server checks if user account is not disabled
4. JWT token is generated with:
   - User ID as subject
   - User roles as claims
   - Configured expiration time
5. Last login time is updated
6. JWT token is returned to client

### Authentication Middleware
1. JWT token is extracted from Authorization header
2. Token is validated for:
   - Signature validity
   - Expiration time
   - Required claims
3. User is loaded using JWT payload
4. User and claims are made available to route handlers

## Authorization Flows

### Role-Based Access Control
1. Request arrives at protected endpoint
2. RBAC decorator extracts JWT token
3. Required roles are checked against token claims
4. If role match found, request proceeds
5. If no match, 403 Forbidden response

### Resource Ownership Verification
1. Request arrives at protected endpoint
2. Resource ID is extracted from URL
3. Resource is loaded from database
4. Owner relationship is verified against current user
5. If ownership verified or user has required role, request proceeds
6. If neither condition met, 403 Forbidden response

## Data Management Flows

### Character Background Creation
1. Client sends POST request to `/background`
2. Server verifies maintainer role
3. Required fields are validated
4. Unique name constraint is checked
5. Background is saved to database
6. Response includes created background data

### Character Management
1. Client requests character data
2. Server verifies:
   - User owns character OR
   - User has operator role
3. Character data is retrieved
4. Full character state is returned

## Error Handling

### Validation Errors
1. Required field missing:
   - 400 Bad Request
   - Message indicating missing fields

2. Unique constraint violation:
   - 409 Conflict
   - Message indicating duplicate value

### Authentication Errors
1. Invalid credentials:
   - 401 Unauthorized
   - Generic error message

2. Account disabled:
   - 401 Unauthorized
   - Specific disabled account message

### Authorization Errors
1. Missing token:
   - 401 Unauthorized
   - Message requesting authentication

2. Insufficient permissions:
   - 403 Forbidden
   - Access denied message

### Resource Errors
1. Resource not found:
   - 404 Not Found
   - Message indicating resource type

2. Conflict in resource state:
   - 409 Conflict
   - Message describing conflict

## Database Interactions

### Transaction Management
1. Database operations are wrapped in transactions
2. Rollback on error
3. Commit on success
4. Connection pooling handled by SQLAlchemy

### Migration Process
1. New migrations detected on startup
2. Pending migrations are applied
3. Schema version is updated
4. Application startup continues

## Runtime Configuration

### Environment Variables
1. Load .env file if present
2. Override with system environment variables
3. Apply configuration to Flask app
4. Initialize extensions with config

### Development vs Production
1. Development:
   - Debug mode enabled
   - SQLite database
   - Detailed error messages

2. Production:
   - Debug mode disabled
   - Configurable database
   - Limited error information
   - UVICORN server

## Testing Workflow

### Unit Tests
1. Setup test database
2. Create test fixtures
3. Execute test cases
4. Cleanup test data
5. Report coverage

### Integration Tests
1. Setup test client
2. Create test database
3. Run authentication flows
4. Test API endpoints
5. Verify responses
6. Clean up resources

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
