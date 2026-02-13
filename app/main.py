from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from contextlib import asynccontextmanager
import logging
from app.api.v1 import auth, subscription, situations, user_words, conversations
from app.database import engine
from app.models import Base

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


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
    import traceback
    try:
        logger.info(f"📥 {request.method} {request.url.path} - Headers: {dict(request.headers)}")
        response = await call_next(request)
        logger.info(f"📤 {request.method} {request.url.path} - Status: {response.status_code}")
    except Exception as e:
        # Log the full error with traceback
        error_trace = traceback.format_exc()
        logger.error(f"❌ ERROR in {request.method} {request.url.path}: {str(e)}")
        logger.error(f"📋 Full traceback:\n{error_trace}")
        # Create error response with CORS headers
        response = JSONResponse(
            content={"detail": str(e), "error_type": type(e).__name__},
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
    import traceback
    logger.warning(f"⚠️  HTTPException {exc.status_code} on {request.method} {request.url.path}: {exc.detail}")
    logger.debug(f"📋 Traceback:\n{traceback.format_exc()}")
    return JSONResponse(
        content={"detail": exc.detail, "status_code": exc.status_code},
        status_code=exc.status_code,
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS, PATCH",
            "Access-Control-Allow-Headers": "*",
        }
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    import traceback
    logger.warning(f"⚠️  ValidationError 422 on {request.method} {request.url.path}")
    logger.warning(f"📋 Validation errors: {exc.errors()}")
    logger.debug(f"📋 Traceback:\n{traceback.format_exc()}")
    return JSONResponse(
        content={"detail": exc.errors(), "status_code": 422},
        status_code=422,
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS, PATCH",
            "Access-Control-Allow-Headers": "*",
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    import traceback
    error_trace = traceback.format_exc()
    logger.error(f"❌ UNHANDLED EXCEPTION on {request.method} {request.url.path}")
    logger.error(f"❌ Exception type: {type(exc).__name__}")
    logger.error(f"❌ Exception message: {str(exc)}")
    logger.error(f"📋 Full traceback:\n{error_trace}")
    return JSONResponse(
        content={
            "detail": "Internal server error",
            "error_type": type(exc).__name__,
            "error_message": str(exc)
        },
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
logger.info("🔗 Registering API routes...")
app.include_router(auth.router, prefix="/v1/auth", tags=["auth"])
logger.info("  ✅ /v1/auth")
app.include_router(subscription.router, prefix="/v1/subscription", tags=["subscription"])
logger.info("  ✅ /v1/subscription")
app.include_router(situations.router, prefix="/v1/situations", tags=["situations"])
logger.info("  ✅ /v1/situations (GET /, GET /{id}, POST /{id}/start, POST /{id}/complete)")
app.include_router(user_words.router, prefix="/v1/user/words", tags=["user-words"])
logger.info("  ✅ /v1/user/words")
app.include_router(conversations.router, prefix="/v1/conversations", tags=["conversations"])
logger.info("  ✅ /v1/conversations (POST /, POST /{id}/messages, GET /{id}/stream, POST /{id}/voice-turn)")
logger.info("✅ All routes registered")


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


@app.post("/seed")
async def seed_database_endpoint():
    """One-time endpoint to seed the database with situations and words"""
    import sys
    import os
    
    try:
        logger.info("🌱 Starting database seed via endpoint...")
        
        # Import and run the seed function directly
        # Add current directory to path
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        
        # Import seed function from standalone script
        import importlib.util
        spec = importlib.util.spec_from_file_location("seed_standalone", "seed_standalone.py")
        seed_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(seed_module)
        
        # Capture output
        import io
        from contextlib import redirect_stdout, redirect_stderr
        
        output_buffer = io.StringIO()
        error_buffer = io.StringIO()
        
        with redirect_stdout(output_buffer), redirect_stderr(error_buffer):
            seed_module.seed_database()
        
        output = output_buffer.getvalue()
        errors = error_buffer.getvalue()
        
        logger.info("✅ Database seed completed successfully")
        logger.info(f"Output: {output}")
        if errors:
            logger.warning(f"Warnings: {errors}")
        
        return {
            "status": "success",
            "message": "Database seeded successfully",
            "output": output,
            "errors": errors if errors else None
        }
    except Exception as e:
        logger.error(f"❌ Error running seed: {e}")
        import traceback
        error_trace = traceback.format_exc()
        logger.error(error_trace)
        return {
            "status": "error",
            "message": str(e),
            "traceback": error_trace
        }

