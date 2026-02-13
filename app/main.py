from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.api.v1 import auth, subscription, situations, user_words, conversations
from app.database import engine
from app.models import Base

# Create tables (in production, use migrations)
# Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Wake up the app
    print("🚀 Encounter Spanish API starting up...")
    yield
    # Shutdown
    print("👋 Encounter Spanish API shutting down...")

app = FastAPI(
    title="Encounter Spanish API",
    description="Backend API for Spanish survival language app",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*",  # Allow all origins for development/preview
        "https://vm-tg70cu1fxyqwwlve3xrr0w.vusercontent.net",
        "https://*.vusercontent.net",  # v0 preview domains
    ],
    allow_origin_regex=r"https://.*\.vusercontent\.net",  # Allow all v0 preview subdomains
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
    expose_headers=["*"],
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

