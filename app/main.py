from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from app.api.v1 import auth, subscription, situations, user_words, conversations
from app.database import engine
from app.models import Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Run migrations and wake up the app
    print("🚀 Encounter Spanish API starting up...")
    try:
        from alembic.config import Config
        from alembic import command
        
        print("📦 Running database migrations...")
        alembic_cfg = Config("alembic.ini")
        command.upgrade(alembic_cfg, "head")
        print("✅ Database migrations complete")
    except Exception as e:
        print(f"⚠️  Migration error (continuing anyway): {e}")
        # Fallback: create tables if migrations fail
        try:
            print("📦 Creating tables directly...")
            Base.metadata.create_all(bind=engine)
            print("✅ Tables created")
        except Exception as e2:
            print(f"❌ Failed to create tables: {e2}")
    
    yield
    # Shutdown
    print("👋 Encounter Spanish API shutting down...")

app = FastAPI(
    title="Encounter Spanish API",
    description="Backend API for Spanish survival language app",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware - Allow all origins (including v0 preview domains)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=False,  # Must be False when using ["*"]
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Manual CORS handler for errors (ensures CORS headers are always set)
@app.middleware("http")
async def add_cors_header(request: Request, call_next):
    response = await call_next(request)
    # Always add CORS headers
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS, PATCH"
    response.headers["Access-Control-Allow-Headers"] = "*"
    response.headers["Access-Control-Expose-Headers"] = "*"
    return response

# Handle OPTIONS preflight requests
@app.options("/{full_path:path}")
async def options_handler(request: Request, full_path: str):
    return JSONResponse(
        content={},
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS, PATCH",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Max-Age": "3600",
        }
    )

# Mount static files for audio
app.mount("/audio", StaticFiles(directory="/tmp/audio"), name="audio")

# Include routers
app.include_router(auth.router, prefix="/v1/auth", tags=["auth"])
app.include_router(subscription.router, prefix="/v1/subscription", tags=["subscription"])
app.include_router(situations.router, prefix="/v1/situations", tags=["situations"])
app.include_router(user_words.router, prefix="/v1/user/words", tags=["user-words"])
app.include_router(conversations.router, prefix="/v1/conversations", tags=["conversations"])


@app.get("/")
async def root():
    return {"message": "Encounter Spanish API"}


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.get("/wakeup")
async def wakeup():
    """Wakeup endpoint for Railway sleeping apps"""
    return {"status": "awake", "message": "API is ready"}

