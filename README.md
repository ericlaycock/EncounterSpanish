# Encounter Spanish Backend API

FastAPI backend for the Spanish survival language learning mobile app.

## Features

- RESTful API with JWT authentication
- PostgreSQL database with Alembic migrations
- OpenAI integration (GPT-4o-mini, Whisper STT, TTS)
- Server-Sent Events (SSE) for streaming responses
- Word detection and tracking system
- Subscription/paywall management
- Text and voice conversation modes

## Tech Stack

- **Framework**: FastAPI (Python 3.11)
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Migrations**: Alembic
- **Authentication**: JWT (python-jose)
- **AI**: OpenAI API (gpt-4o-mini, whisper-1, tts-1)

## Project Structure

```
backend/
├── app/
│   ├── api/v1/          # API endpoints
│   ├── services/         # Business logic services
│   ├── utils/            # Utility functions
│   ├── models.py         # SQLAlchemy models
│   ├── schemas.py        # Pydantic schemas
│   ├── auth.py           # Authentication
│   ├── database.py       # Database setup
│   └── main.py           # FastAPI app
├── migrations/           # Alembic migrations
├── seeds/               # Seed data scripts
├── requirements.txt
├── Dockerfile
└── railway.json
```

## Setup

### Prerequisites

- Python 3.11+
- PostgreSQL database
- OpenAI API key

### Local Development

1. **Clone the repository**

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your values:
# DATABASE_URL=postgresql://user:password@localhost:5432/encounterspanish
# OPENAI_API_KEY=sk-your-key-here
# JWT_SECRET=your-secret-key
```

5. **Run database migrations**
```bash
alembic upgrade head
```

6. **Seed the database** (optional)
```bash
python -m seeds.seed_data
```

7. **Run the development server**
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

API documentation: `http://localhost:8000/docs`

## Railway Deployment

### Setup

1. **Create Railway account** and create a new project

2. **Add PostgreSQL service**
   - Create a new PostgreSQL database service
   - Note the `DATABASE_URL` connection string

3. **Add backend service**
   - Connect your GitHub repository or deploy from local
   - Railway will detect the `Dockerfile` and `railway.json`

4. **Configure environment variables**
   In Railway dashboard, add:
   - `DATABASE_URL` - From PostgreSQL service
   - `OPENAI_API_KEY` - Your OpenAI API key
   - `JWT_SECRET` - A secure random string
   - `JWT_ALGORITHM` - `HS256` (default)
   - `JWT_EXPIRATION_HOURS` - `24` (default)

5. **Run migrations**
   After first deployment, run migrations:
   ```bash
   railway run alembic upgrade head
   ```

6. **Seed database** (optional)
   ```bash
   railway run python -m seeds.seed_data
   ```

### Deployment Notes

- Railway automatically builds and deploys on git push
- The `railway.json` configures the build and start commands
- Audio files are stored in `/tmp/audio/` (temporary, cleared on restart)
- For production, consider using Railway volumes or S3 for persistent audio storage

## API Endpoints

### Authentication
- `POST /v1/auth/login` - Login and get JWT token

### Subscription
- `GET /v1/subscription/status` - Get subscription status

### Situations
- `GET /v1/situations` - List all situations
- `GET /v1/situations/{id}` - Get situation details
- `POST /v1/situations/{id}/start` - Start a situation
- `POST /v1/situations/{id}/complete` - Complete a situation

### User Words
- `GET /v1/user/words` - Get user's word progress
- `POST /v1/user/words/typed-correct` - Mark words as typed correctly

### Conversations
- `POST /v1/conversations` - Create a conversation
- `POST /v1/conversations/{id}/messages` - Send text message
- `GET /v1/conversations/{id}/stream` - Stream assistant (SSE)
- `POST /v1/conversations/{id}/voice-turn` - Process voice turn (multipart)

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `DATABASE_URL` | PostgreSQL connection string | Yes |
| `OPENAI_API_KEY` | OpenAI API key | Yes |
| `JWT_SECRET` | Secret key for JWT tokens | Yes |
| `JWT_ALGORITHM` | JWT algorithm (default: HS256) | No |
| `JWT_EXPIRATION_HOURS` | Token expiration (default: 24) | No |

## Database Schema

See `app/models.py` for full schema. Key tables:
- `users` - User accounts
- `subscriptions` - User subscriptions
- `words` - Spanish/English word pairs
- `situations` - Learning situations
- `situation_words` - Word mappings for situations
- `user_words` - User progress tracking
- `user_situations` - User situation progress
- `conversations` - Text/voice conversations

## Development

### Running Migrations

```bash
# Create new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

### Testing

API documentation with interactive testing available at `/docs` when server is running.

## Notes

- Model used: `gpt-4o-mini` (as `gpt-4.1-mini` may not be available)
- TTS audio files stored temporarily in `/tmp/audio/`
- First 5 situations (by order_index) are free
- Word detection is deterministic (no ML) - handles accents and phrases
- SSE streaming for Screen 2 text conversations
- Voice mode uses single POST with audio file per turn

## License

Proprietary - All rights reserved

# EncounterSpanish
