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