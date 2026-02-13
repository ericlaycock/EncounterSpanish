from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
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
        import traceback
        traceback.print_exc()
        # Fallback: create tables if migrations fail
        try:
            print("📦 Creating tables directly...")
            Base.metadata.create_all(bind=engine)
            print("✅ Tables created")
        except Exception as e2:
            print(f"❌ Failed to create tables: {e2}")
            import traceback
            traceback.print_exc()
            # Don't crash - let the app start anyway
            print("⚠️  App will start without database tables. Migrations can be run manually.")
    
    yield
    # Shutdown
    print("👋 Encounter Spanish API shutting down...")

app = FastAPI(
    title="Encounter Spanish API",
    description="Backend API for Spanish survival language app",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware - Allow all origins using regex
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r".*",  # Match any origin
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Manual CORS handler - ensures headers are set even on exceptions
@app.middleware("http")
async def add_cors_header(request: Request, call_next):
    try:
        response = await call_next(request)
    except Exception as e:
        # Create error response with CORS headers
        response = JSONResponse(
            content={"detail": str(e)},
            status_code=500,
        )
    
    # Always add CORS headers to every response
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS, PATCH"
    response.headers["Access-Control-Allow-Headers"] = "*"
    response.headers["Access-Control-Expose-Headers"] = "*"
    return response

# Global exception handlers with CORS
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        content={"detail": exc.detail},
        status_code=exc.status_code,
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS, PATCH",
            "Access-Control-Allow-Headers": "*",
        }
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        content={"detail": exc.errors()},
        status_code=422,
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS, PATCH",
            "Access-Control-Allow-Headers": "*",
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        content={"detail": "Internal server error"},
        status_code=500,
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS, PATCH",
            "Access-Control-Allow-Headers": "*",
        }
    )

# Handle OPTIONS preflight requests explicitly
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


@app.get("/test-cors")
async def test_cors():
    """Test endpoint to verify CORS is working"""
    return {
        "status": "CORS test",
        "message": "If you can see this, CORS is working!",
        "headers": "Check browser network tab for CORS headers"
    }

