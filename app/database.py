from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from app.config import settings
import time
import logging

logger = logging.getLogger(__name__)

# Create engine with connection retry settings
engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,  # Verify connections before using
    pool_size=10,
    max_overflow=20,
    connect_args={
        "connect_timeout": 10,  # 10 second connection timeout
    }
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def test_connection(max_retries=3, retry_delay=2):
    """Test database connection with retries"""
    from sqlalchemy import text
    for attempt in range(max_retries):
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            logger.info("✅ Database connection successful")
            return True
        except OperationalError as e:
            logger.warning(f"⚠️  Database connection attempt {attempt + 1}/{max_retries} failed: {e}")
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
            else:
                logger.error("❌ Failed to connect to database after all retries")
                return False
        except Exception as e:
            logger.error(f"❌ Unexpected error testing database connection: {e}")
            return False
    return False


def get_db():
    """Dependency for getting database session"""
    db = SessionLocal()
    try:
        yield db
    except OperationalError as e:
        logger.error(f"❌ Database connection error: {e}")
        db.rollback()
        raise
    finally:
        db.close()



