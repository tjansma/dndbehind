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