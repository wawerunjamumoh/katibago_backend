# KatibaGo Backend API

Versioned API base URL:

```text
http://127.0.0.1:8000/api/v1/
```

Start the development server with:

```bash
source .venv/bin/activate
python manage.py runserver
```

## Authentication

The API uses Django REST Framework token authentication. Include the token on
protected requests:

```http
Authorization: Token <token>
```

### Register

```http
POST /api/v1/auth/register/
```

```json
{
	"username": "aisha",
	"email": "aisha@example.com",
	"password": "strong-password-123"
}
```

Response:

```json
{
	"user": {
		"id": 1,
		"username": "aisha",
		"email": "aisha@example.com"
	},
	"token": "<token>"
}
```

### Login

```http
POST /api/v1/auth/login/
```

```json
{
	"username": "aisha",
	"password": "strong-password-123"
}
```

Save the returned token and send it as `Authorization: Token <token>`.

### Current user

```http
GET /api/v1/auth/me/
Authorization: Token <token>
```

This request has no body and returns the basic authenticated user payload.

### Current learner profile summary

```http
GET /api/v1/auth/me/profile/
Authorization: Token <token>
```

Returns the learner dashboard payload used by the frontend profile icon and summary cards.

Example response:

```json
{
  "id": 1,
  "user": 1,
  "xp": 280,
  "total_xp": 280,
  "current_streak": 4,
  "streak_freeze_count": 1,
  "current_level": 3,
  "gems_balance": 12,
  "badges": [],
  "achievements": []
}
```

This endpoint is intentionally isolated from the base auth response so the profile view can scale without bloating the main login or identity endpoint.

### Logout

```http
POST /api/v1/auth/logout/
Authorization: Token <token>
```

This request has no body. The token is revoked after a successful logout.

## Learner API

These endpoints expose learner workflows instead of database tables directly.
They require authentication unless stated otherwise.

### Open an article

```http
GET /api/v1/learn/articles/{article_number}/
Authorization: Token <token>
```

Example response:

```json
{
	"article": {
		"article_number": 19,
		"title": "Basic freedoms we are entitled to",
		"difficulty": "easy"
	},
	"learning_objectives": [],
	"experiences": [],
	"legal_explanation": {},
	"safety_shield": {},
	"progress": {
		"status": "in_progress"
	}
}
```

Only active articles are available through this endpoint. The `progress`
object belongs to the authenticated user.

### Start an article

```http
POST /api/v1/articles/{article_number}/start/
Authorization: Token <token>
```

This request has no body. It creates or resumes the authenticated user's
progress and sets the status to `in_progress`.

### Complete an article

```http
POST /api/v1/articles/{article_number}/complete/
Authorization: Token <token>
```

This request has no body. The article must already be in progress. Completion
sets the status to `completed` and awards the article's `xp_reward` once.

Example response:

```json
{
	"message": "Article completed successfully.",
	"article_number": 19,
	"status": "completed",
	"completed_at": "2026-08-21T10:30:00Z",
	"xp_awarded": 40,
	"total_xp": 40
}
```

### View my progress

```http
GET /api/v1/me/progress/
Authorization: Token <token>
```

Example response:GET /api/v1/me/progress/
Authorization: Token <token>

```json
{
  "chapters": [
    {
      "number": 1,
      "official_title": "The Republic",
      "parts": [
        {
          "number": 1,
          "friendly_title": "Foundations",
          "articles": [
            {
              "article_number": 1,
              "citizen_title": "The Sovereignty of the People",
              "status": "completed",
              "progress": 100
            },
            {
              "article_number": 2,
              "citizen_title": "The Constitution",
              "status": "completed",
              "progress": 100
            },
            {
              "article_number": 3,
              "citizen_title": "National Values",
              "status": "unlocked",
              "progress": 0
            },
            {
              "article_number": 4,
              "citizen_title": "...",
              "status": "locked",
              "progress": 0
            }
          ]
        }
      ]
    }
  ]
}
```

```http
GET /api/v1/me/progress/{article_number}/
Authorization: Token <token>
```

This single-article route remains the per-lesson detail endpoint. The list route
returns the full chapter-based curriculum progress tree. Both endpoints are
user-scoped. A learner cannot view another learner's progress.

### Submit a decision response

```http
POST /api/v1/decisionpoints/{decision_point_id}/respond/
Authorization: Token <token>
Content-Type: application/json
```

```json
{
	"selected_choice": 12
}
```

The selected choice must belong to the specified decision point. Submitting
again updates the learner's existing response for that decision point.

## Practical learner flow

The following example uses shell variables so the token is reused safely:

```bash
BASE_URL=http://127.0.0.1:8000/api/v1

# 1. Register and copy the token from the response.
curl -X POST "$BASE_URL/auth/register/" \
	-H "Content-Type: application/json" \
	-d '{
		"username": "aisha",
		"email": "aisha@example.com",
		"password": "strong-password-123"
	}'

# 2. Login if the account already exists.
TOKEN=$(curl -s -X POST "$BASE_URL/auth/login/" \
	-H "Content-Type: application/json" \
	-d '{
		"username": "aisha",
		"password": "strong-password-123"
	}' | python -c 'import json, sys; print(json.load(sys.stdin)["token"])')

# 3. Confirm the user identity.
curl "$BASE_URL/auth/me/" \
	-H "Authorization: Token $TOKEN"

# 3b. Fetch the learner profile summary for the frontend profile icon.
curl "$BASE_URL/auth/me/profile/" \
	-H "Authorization: Token $TOKEN"

# 4. Open Article 19 and read its learning content.
curl "$BASE_URL/learn/articles/19/" \
	-H "Authorization: Token $TOKEN"

# 5. Start the lesson: progress becomes IN_PROGRESS.
curl -X POST "$BASE_URL/articles/19/start/" \
	-H "Authorization: Token $TOKEN"

# 6. Submit a selected choice while working through the experience.
curl -X POST "$BASE_URL/decisionpoints/7/respond/" \
	-H "Authorization: Token $TOKEN" \
	-H "Content-Type: application/json" \
	-d '{"selected_choice": 12}'

# 7. Read progress for Article 19.
curl "$BASE_URL/me/progress/19/" \
	-H "Authorization: Token $TOKEN"

# 8. After reaching the Safety Shield, complete the lesson and award XP.
curl -X POST "$BASE_URL/articles/19/complete/" \
	-H "Authorization: Token $TOKEN"

# 9. Review all progress belonging to this learner.
curl "$BASE_URL/me/progress/" \
	-H "Authorization: Token $TOKEN"

# 10. Revoke the token.
curl -X POST "$BASE_URL/auth/logout/" \
	-H "Authorization: Token $TOKEN"
```

## Resource API

The original resource endpoints remain available for administrative or
content-management use:

| Resource | Collection endpoint |
| --- | --- |
| Chapters | `/api/v1/chapters/` |
| Parts | `/api/v1/parts/` |
| Articles | `/api/v1/articles/` |
| Cases | `/api/v1/cases/` |
| Decision points | `/api/v1/decisionpoints/` |
| Choices | `/api/v1/choices/` |
| Feedback | `/api/v1/feedbacks/` |
| Constitution text | `/api/v1/constitution/` |
| Safety shields | `/api/v1/safteyshields/` |

These are DRF resource routes. Learner clients should prefer the aggregate
`/learn/`, `/me/`, and workflow endpoints above.

## Tests

Run the endpoint-focused tests with:

```bash
python manage.py test \
	apps.content.tests.test_auth_api \
	apps.content.tests.test_learner_workflow
```

Run all tests with:

```bash
python manage.py check
python manage.py test
```
