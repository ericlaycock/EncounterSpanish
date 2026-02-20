from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from contextlib import asynccontextmanager
import logging
import os
import platform
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Emit boot event as early as possible (before imports that might fail)
try:
    from app.core.logger import log_event
    log_event(
        level="info",
        event="backend_boot",
        message="Backend server starting up",
        request_id="system",
        user_id=None,
        extra={
            "release": os.environ.get("RELEASE_SHA", "unknown"),
            "environment": os.environ.get("ENVIRONMENT", os.environ.get("RAILWAY_ENVIRONMENT", "unknown")),
            "python_version": sys.version.split()[0],
            "platform": platform.platform(),
            "node": platform.node(),
            "auto_migrate": os.environ.get("AUTO_MIGRATE", "false").lower() == "true",
        }
    )
except Exception as e:
    # If logging fails, at least print to stdout
    print(f"⚠️  Failed to emit boot event: {e}", file=sys.stderr)

from app.api.v1 import auth, subscription, situations, user_words, conversations, onboarding, logs
from app.database import engine
from app.models import Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Run migrations and wake up the app
    print("🚀 Encounter Spanish API starting up...")
    
    # Test database connection first with retries
    from app.database import test_connection
    db_connected = test_connection(max_retries=5, retry_delay=3)
    
    if db_connected:
        # Only run migrations if AUTO_MIGRATE env var is set to "true"
        # Otherwise, migrations should be run manually or via CI/CD
        auto_migrate = os.environ.get("AUTO_MIGRATE", "false").lower() == "true"
        
        if auto_migrate:
            try:
                from alembic.config import Config
                from alembic import command
                from alembic.script import ScriptDirectory
                from alembic.runtime.migration import MigrationContext
                
                print("📦 Checking database migrations...")
                alembic_cfg = Config("alembic.ini")
                
                # Check if migrations are needed
                with engine.connect() as connection:
                    context = MigrationContext.configure(connection)
                    current_rev = context.get_current_revision()
                    script = ScriptDirectory.from_config(alembic_cfg)
                    head_rev = script.get_current_head()
                    
                    if current_rev != head_rev:
                        print(f"📦 Database is at revision {current_rev}, upgrading to {head_rev}...")
                        command.upgrade(alembic_cfg, "head")
                        print("✅ Database migrations complete")
                    else:
                        print("✅ Database is up to date, no migrations needed")
            except Exception as e:
                logger.warning(f"⚠️  Migration error (continuing anyway): {e}")
                import traceback
                traceback.print_exc()
                # Fallback: create tables if migrations fail and no tables exist
                try:
                    from sqlalchemy import inspect
                    inspector = inspect(engine)
                    tables = inspector.get_table_names()
                    if not tables:
                        print("📦 No tables found, creating tables directly...")
                        Base.metadata.create_all(bind=engine)
                        print("✅ Tables created")
                except Exception as e2:
                    logger.error(f"❌ Failed to create tables: {e2}")
                    import traceback
                    traceback.print_exc()
                    print("⚠️  App will start without database tables. Migrations can be run manually.")
        else:
            logger.info("ℹ️  Auto-migration disabled. Run migrations manually with: alembic upgrade head")
    else:
        logger.warning("⚠️  Database not available at startup. App will start but database operations may fail.")
        logger.warning("⚠️  This is normal if the database is still provisioning. It will be available shortly.")
    
    yield
    # Shutdown
    print("👋 Encounter Spanish API shutting down...")

app = FastAPI(
    title="Encounter Spanish API",
    description="Backend API for Spanish survival language app",
    version="1.0.0",
    lifespan=lifespan
)

# Request ID middleware (must be first)
from app.middleware.request_id import RequestIDMiddleware
app.add_middleware(RequestIDMiddleware)

# Request logging middleware (after request_id)
from app.middleware.request_logging import RequestLoggingMiddleware
app.add_middleware(RequestLoggingMiddleware)

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
from app.api.v1 import onboarding
app.include_router(onboarding.router, prefix="/v1/onboarding", tags=["onboarding"])
logger.info("  ✅ /v1/onboarding (POST /save-selections, GET /status, GET /available-categories)")
app.include_router(logs.router, prefix="/v1/log", tags=["logs"])
logger.info("  ✅ /v1/log (POST / - frontend logging)")
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



