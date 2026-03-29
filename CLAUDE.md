# Spanish for Expats — Backend Context

> This file is auto-loaded by Claude when working in this directory.
> For project-level context, see `../CLAUDE.md`.

## Quick Reference

- **Framework**: FastAPI (Python 3.11), Uvicorn
- **Database**: PostgreSQL (Railway), SQLAlchemy 2.0, Alembic migrations
- **Auth**: JWT via python-jose, bcrypt passwords
- **AI**: OpenAI GPT-4.1-mini (chat), Whisper (STT), TTS
- **Tests**: pytest (requires PostgreSQL — not SQLite-compatible due to UUID/JSONB)

## Key Files

| File | Purpose |
|------|---------|
| `app/main.py` | FastAPI app, lifespan, CORS, router registration |
| `app/config.py` | Pydantic Settings (DATABASE_URL, OPENAI_API_KEY, JWT_SECRET, mastery_spoken_threshold) |
| `app/models.py` | All SQLAlchemy models (User, Word, Situation, UserWord, Conversation, etc.) |
| `app/schemas.py` | Pydantic request/response schemas |
| `app/database.py` | Engine, SessionLocal, `get_db()` dependency |
| `app/auth.py` | JWT create/verify, password hashing, `get_current_user()` |

## API Routes (`app/api/v1/`)

| Module | Prefix | Key Endpoints |
|--------|--------|---------------|
| `auth.py` | `/v1/auth` | register, login |
| `situations.py` | `/v1/situations` | list, detail, start, complete, next, daily-usage, admin/ai-logs |
| `conversations.py` | `/v1/conversations` | create, voice-turn |
| `user_words.py` | `/v1/user/words` | get words, unknown words, typed-correct |
| `onboarding.py` | `/v1/onboarding` | status, save-selections, available-categories |
| `subscription.py` | `/v1/subscription` | status |

## Services (`app/services/`)

| Service | Purpose |
|---------|---------|
| `word_selection_service.py` | Selects encounter + high-frequency words for a situation |
| `voice_turn_service.py` | Orchestrates STT → word detection → LLM → TTS pipeline |
| `conversation_service.py` | Word stat updates, mastery checks, completion detection |
| `word_detection.py` | Deterministic word matching in user text/transcript |
| `llm_gateway.py` | OpenAI chat completions wrapper |
| `openai_media_gateway.py` | Whisper STT + TTS wrapper |
| `subscription_service.py` | Free tier limit checking (25 encounters) |
| `daily_encounter_service.py` | 30/day encounter limit checking and recording |

## Patterns

- **Dependency injection**: `Depends(get_db)` for DB sessions, `Depends(get_current_user)` for auth
- **Upserts**: UserWord uses PostgreSQL `ON CONFLICT DO UPDATE`
- **Locking**: `.with_for_update()` on conversation lookups to prevent races
- **Mastery**: `spoken_correct_count >= settings.mastery_spoken_threshold` (default 2)
- **Word selection**: 3 encounter + 2 high-frequency per situation, ordered by frequency_rank

## Admin Analytics

- `GET /v1/situations/admin/ai-logs` — Admin-only endpoint returning aggregate TTS/STT/LLM latency stats (avg/min/max/count per model) plus recent 20 TTS and 20 STT calls with details (format, latency, errors). Useful for monitoring whisper-1 fallback rate and TTS performance.
- AI request logging tables: `llm_requests`, `stt_requests`, `tts_requests` (defined in `app/models/ai_requests.py`)
- Initial message TTS is cached in-memory by `(situation_id, catalan_mode)` in `conversations.py` — clears on deploy

## Database

- Migrations: `alembic upgrade head` (auto-runs on startup if `AUTO_MIGRATE=true`)
- QA seed: `scripts/seed_qa.py` (auto-runs when `ENVIRONMENT=qa`)
- Key constraint: `CheckConstraint` on UserWord.status ('learning'/'mastered'), Conversation.mode ('text'/'voice'), Conversation.status ('active'/'complete')
