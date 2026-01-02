# Custom Authentication & Authorization System

Backend application on Django REST Framework with custom authentication and authorization system. The project implements its own access control model, not fully based on standard Django mechanisms (Groups/Permissions).

## Project Description

This service is a REST API for user management and resource access control. The main feature is a custom authorization system that allows flexible access rights configuration through roles, resources, and actions.

### What the project solves

- **User authentication**: registration, login, logout, profile management
- **Custom authorization**: flexible role-based access control system
- **Access management**: administrative API for rights configuration
- **Access testing**: mock endpoints for system testing

### Custom Authorization

Instead of standard Django Groups/Permissions, a custom model is used:
- **Role** — defines a group of users (admin, user, etc.)
- **Resource** — object that requires access (projects, reports, etc.)
- **Action** — operation that can be performed (read, create, update, delete)
- **Permission** — rule: role can perform action on resource

## Access Control Schema

### Roles

Role defines a group of users with specific rights:

- **admin** — administrator with full access to all resources
- **user** — regular user with limited rights

### Resources

Resource is an object or group of objects that require access:

- **projects** — projects
- **reports** — reports
- **access** — access control system management (admin only)

### Actions

Action is an operation that can be performed on a resource:

- **read** — view/read
- **create** — create
- **update** — update
- **delete** — delete
- **admin** — administrative actions

### Permission Rules

Rule links role, resource, and action. For example:

- `admin` can `read` `projects` 
- `admin` can `create` `projects` 
- `user` can `read` `projects` 

### Access Check

1. User must be authenticated (have valid token)
2. System checks user roles
3. For each role, rights to resource and action are checked
4. If right is found — access granted (200 OK)
5. If user is not authenticated — 401 Unauthorized
6. If user is authenticated but has no rights — 403 Forbidden

## Project Setup

### Local Setup

1. **Clone the repository**:
```bash
git clone <repository-url>
cd custom-auth-system
```

2. **Create virtual environment**:
```bash
python -m venv venv
source venv/bin/activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Create .env file and edit it**:
```bash
cp .env-example .env
```

5. **Create migrations**:
```bash
python manage.py makemigrations
```

6. **Apply migrations** (creates database tables):
```bash
python manage.py migrate
```

**Important**: Migrations must be applied before loading fixtures, otherwise you will get `no such table` error.

7. **Load test data**:
```bash
python manage.py loaddata access/fixtures/initial_data.json
```

8. **Create superuser** (optional):
```bash
python manage.py createsuperuser
```

9. **Run server**:
```bash
python manage.py runserver
```

Server will be available at: http://localhost:8000

### Docker Setup

1. **Build image**:
```bash
docker build -t auth-app .
```

2. **Run container**:
```bash
docker run -p 8000:8000 --env-file .env auth-app
```

Or use environment variables directly:
```bash
docker run -p 8000:8000 \
  -e SECRET_KEY=your-secret-key \
  -e DEBUG=True \
  -e ALLOWED_HOSTS=localhost,127.0.0.1 \
  auth-app
```

## API Examples

### Registration

```bash
curl -X POST http://localhost:8000/api/users/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "full_name": "John Doe",
    "password": "securepassword123",
    "password_confirm": "securepassword123"
  }'
```

**Response**:
```json
{
  "message": "User registered successfully.",
  "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "full_name": "John Doe",
    "date_joined": "2024-01-15T10:00:00Z",
    "last_login": null
  }
}
```

### Login

```bash
curl -X POST http://localhost:8000/api/users/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword123"
  }'
```

**Response**:
```json
{
  "message": "Login successful.",
  "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "full_name": "John Doe",
    "date_joined": "2024-01-15T10:00:00Z",
    "last_login": "2024-01-15T10:30:00Z"
  }
}
```

### Request to Protected Resource (with token)

```bash
curl -X GET http://localhost:8000/api/mock/projects/ \
  -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
```

**Response (if has rights)**:
```json
{
  "message": "Access granted to projects",
  "data": [
    {
      "id": 1,
      "name": "Project Alpha",
      "description": "First project",
      "status": "active",
      "created_at": "2024-01-15T10:00:00Z"
    }
  ],
  "count": 3
}
```

### Example 401 Error (not authenticated)

```bash
curl -X GET http://localhost:8000/api/mock/projects/
```

**Response**:
```json
{
  "detail": "Authentication credentials were not provided."
}
```

### Example 403 Error (no rights)

If user doesn't have access rights to resource:

**Response**:
```json
{
  "detail": "You do not have permission to perform this action."
}
```

### Update Profile

```bash
curl -X PATCH http://localhost:8000/api/users/profile/update/ \
  -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b" \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "John Updated Doe"
  }'
```

### Logout

```bash
curl -X POST http://localhost:8000/api/users/logout/ \
  -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
```

### Delete User (soft delete)

```bash
curl -X DELETE http://localhost:8000/api/users/delete/ \
  -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
```

## Implementation Details

### Soft Delete

When deleting a user:
- Token is deleted (logout)
- `is_active` field is set to `False`
- User cannot login again
- Database record is preserved

### Custom Rights Check

Uses `HasResourcePermission` class that:
1. Checks user authentication
2. Gets user roles from `UserRole` table
3. Checks for permission through `Role → Permission → Resource + Action` relationship
4. Returns `True` if permission found, otherwise `False`

### Permission Classes

- `IsAuthenticated` — standard DRF authentication check
- `HasResourcePermission` — custom access rights check
- `IsAdminPermission` — check for admin role for administrative operations

### Middleware

Standard Django middleware is used:
- `AuthenticationMiddleware` — for token handling
- `SessionMiddleware` — for sessions (optional)

## Administrative API

All administrative endpoints require `admin` role and `access:admin` permission.

### Get Roles List

```bash
curl -X GET http://localhost:8000/api/access/roles/ \
  -H "Authorization: Token <admin-token>"
```

### Create Permission Rule

```bash
curl -X POST http://localhost:8000/api/access/permissions/ \
  -H "Authorization: Token <admin-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "role_id": 2,
    "resource_id": 1,
    "action_id": 1
  }'
```

### Assign Role to User

```bash
curl -X POST http://localhost:8000/api/access/user-roles/ \
  -H "Authorization: Token <admin-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "role_id": 2
  }'
```

### Get Access Control System Overview

```bash
curl -X GET http://localhost:8000/api/access/overview/ \
  -H "Authorization: Token <admin-token>"
```

## Security

- Passwords are stored in hashed form (Django default)
- Tokens are used for authentication
- Soft delete prevents data loss
- Rights check at API endpoints level
