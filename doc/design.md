# Data

## Entities

### User

| Field          | Type        | Constraints |
|----------------|-------------|-------------|
| **id**         | int         | primary key |
| username       | string(254) | unique      |
| email          | string(254) | unique      |
| password_hash  | string(254) |             |
| last_logged_in | datetime    |             |
| disable        | boolean     |             |


### Role

| Field       | Type         | Constraints |
|-------------|--------------|-------------|
| **id**      | int          | primary key |
| name        | string(254)  | unique      |
| description | string(1000) |             |

### Character

| Field           | Type              | Constraints       |
|-----------------|-------------------|-------------------|
| **id**          | int               | primary key       |
| name            | string(254)       |                   |
| description     | string(1,000,000) |                   |
| backstory       | string(1,000,000) |                   |
| strength        | int               |                   |
| dexterity       | int               |                   |
| constitution    | int               |                   |
| intelligence    | int               |                   |
| wisdom          | int               |                   |
| charisma        | int               |                   |
| _owner_id_      | int               | fk(User.id)       |
| _background_id_ | int               | fk(Background.id) |
    
### Background

| Field       | Type            | Constraints |
|-------------|-----------------|-------------|
| **id**      | int             | primary key |
| name        | string(254)     | unique      |
| description | string(100,000) |             |

## Relationships

| Entity 1   | Rel. type | Entity 2  | Via                         |
|------------|-----------|-----------|-----------------------------|
| User       | n:m       | Role      | "user_role" table           |
| Background | 1:n       | Character | FK: Character.background_id |
| User       | 1:n       | Character | FK: Character.owner_id      |

# Functionality

## Authentication/authorization

### An anonymous visitor must be able to create a new personalized account

### An anonymous visitor must be able to log in and prove their identity, obtaining a token proving their identity and assigned roles for non-anonymous functionality

### An administrator must be able to assign roles to a user

### An administrator must be able to unassign (delete) roles from a user

### An administrator must be able to list all roles assigned to all users

### An administrator must be able to list all roles assigned to a specific user (identified by user ID)

## DnD content management

### A maintainer must be able to add a new (character) background

### A maintainer must be able to retrieve a list of all (character) backgrounds

### A maintainer must be able to retrieve data about a specific background (identified by id)

TODO Not implemented yet.

### A maintainer must be able to retrieve a list of (character) background, filtered by one or more of its attributes

TODO Not implemented yet.
