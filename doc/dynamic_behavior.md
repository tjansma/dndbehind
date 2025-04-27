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