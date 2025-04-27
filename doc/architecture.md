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