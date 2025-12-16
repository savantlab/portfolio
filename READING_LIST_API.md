# Reading List API

Authenticated API for managing a reading list via command line or HTTP requests.

## Features

- **Email-based authentication** - Only authorized emails can access the API
- **Token-based access** - Secure tokens for API requests
- **CLI tool** - Easy command-line interface for managing items
- **Full CRUD operations** - Create, read, update, delete reading list items
- **Categories & metadata** - Organize items with categories, URLs, and descriptions

## Quick Start

### 1. Start the API Server

```bash
cd /Users/savantlab/Savantlab/savantlab-portfolio
source venv/bin/activate
python flask_driver_runner.py app:app
```

The API runs on `http://localhost:5001`

### 2. Authenticate

Request a token for your email:

```bash
python reading_list_cli.py auth stephie.maths@icloud.com
```

This returns:
```
✓ Token created: <long-token-string>
✓ Expires in: 24 hours

Save your token:
  export API_TOKEN="<token>"
```

### 3. Verify Token

In production, tokens must be verified (e.g., via email link or 2FA). For development:

```bash
python reading_list_cli.py verify <token>
```

### 4. Set Token Environment Variable

```bash
export API_TOKEN="<your-token>"
```

Now you can use all commands below.

## CLI Commands

### Add Item

```bash
python reading_list_cli.py add "Title" [options]
```

**Options:**
- `--url URL` - Resource URL
- `--category CATEGORY` - Category (General, Research, Tutorial, News, Opinion, Book, Paper)
- `--description TEXT` - Item description

**Example:**
```bash
python reading_list_cli.py add "Mental Rotation Paradox" \
  --url https://arxiv.org/abs/2301.12345 \
  --category Research \
  --description "Key paper on spatial cognition"
```

### List All Items

```bash
python reading_list_cli.py list
```

Shows all items with completion status, categories, and descriptions.

### Get Specific Item

```bash
python reading_list_cli.py get <item_id>
```

Returns full JSON for one item.

### Mark as Read/Unread

```bash
python reading_list_cli.py mark-read <item_id>
```

Toggles the completed status of an item.

### Delete Item

```bash
python reading_list_cli.py delete <item_id> [--force]
```

Prompts for confirmation unless `--force` is used.

## HTTP API Reference

### Authentication

All endpoints (except `/api/auth/*`) require:

```
Authorization: Bearer <token>
```

### Request Token

**POST** `/api/auth/token`

```json
{
  "email": "stephie.maths@icloud.com"
}
```

**Response (201):**
```json
{
  "token": "...",
  "message": "Token created...",
  "expires_in": "24 hours"
}
```

### Verify Token

**POST** `/api/auth/verify`

```json
{
  "token": "<token>"
}
```

**Response (200):**
```json
{
  "success": true,
  "message": "Token verified and activated!"
}
```

### Get All Items

**GET** `/api/reading-list`

**Response (200):**
```json
[
  {
    "id": 1,
    "title": "Mental Rotation",
    "url": "https://...",
    "description": "...",
    "category": "Research",
    "completed": false
  }
]
```

### Add Item

**POST** `/api/reading-list`

```json
{
  "title": "Article Title",
  "url": "https://...",
  "description": "...",
  "category": "Research"
}
```

**Response (201):**
```json
{
  "id": 1,
  "title": "Article Title",
  "url": "https://...",
  "description": "...",
  "category": "Research",
  "completed": false
}
```

### Get Item

**GET** `/api/reading-list/<item_id>`

**Response (200):**
```json
{
  "id": 1,
  "title": "...",
  "url": "...",
  "description": "...",
  "category": "...",
  "completed": false
}
```

### Update Item

**PUT** `/api/reading-list/<item_id>`

```json
{
  "title": "New Title",
  "description": "New Description"
}
```

**Response (200):**
```json
{
  "id": 1,
  "title": "New Title",
  ...
}
```

### Toggle Completed Status

**POST** `/api/reading-list/<item_id>/toggle`

**Response (200):**
```json
{
  "id": 1,
  "title": "...",
  "completed": true
}
```

### Delete Item

**DELETE** `/api/reading-list/<item_id>`

**Response (200):**
```json
{
  "success": true
}
```

## cURL Examples

### Add item with cURL

```bash
TOKEN="your-token-here"

curl -X POST http://localhost:5001/api/reading-list \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Article Title",
    "category": "Research",
    "url": "https://example.com/article"
  }'
```

### Get all items with cURL

```bash
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:5001/api/reading-list
```

### Mark as read with cURL

```bash
curl -X POST -H "Authorization: Bearer $TOKEN" \
  http://localhost:5001/api/reading-list/1/toggle
```

## Configuration

Set environment variables to customize behavior:

```bash
# Base API URL (default: http://localhost:5001)
export API_URL="http://localhost:5001"

# Authentication token
export API_TOKEN="your-token"

# Authorized email (in Flask app, default: stephie.maths@icloud.com)
export AUTHORIZED_EMAIL="your-email@domain.com"

# Token expiry in hours (default: 24)
export TOKEN_EXPIRY_HOURS="48"
```

## Security Notes

⚠️ **Development Only**: Tokens are printed directly in development mode. In production:

1. Tokens should be sent via email
2. Use HTTPS for all API communication
3. Store tokens securely (not in plain text)
4. Implement proper 2FA verification
5. Add rate limiting
6. Use database instead of in-memory storage

## Storage

Currently, items are stored in memory and lost when the server restarts. For persistent storage, migrate to a database like:

- SQLite (simple, good for personal use)
- PostgreSQL (production-ready)
- MongoDB (flexible schema)

## License

© 2025 Savantlab
