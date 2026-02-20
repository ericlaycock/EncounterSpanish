"""Models package - imports all models for backward compatibility"""
# Import all models from the parent models.py file using importlib
import importlib.util
import sys
from pathlib import Path

# Get the path to the parent models.py
parent_dir = Path(__file__).parent.parent
models_py_path = parent_dir / "models.py"

# Load the models.py module with a different name to avoid conflicts
spec = importlib.util.spec_from_file_location("app.models_legacy", str(models_py_path))
models_legacy = importlib.util.module_from_spec(spec)
sys.modules["app.models_legacy"] = models_legacy
spec.loader.exec_module(models_legacy)

# Import all models from the legacy file
User = models_legacy.User
Situation = models_legacy.Situation
Word = models_legacy.Word
SituationWord = models_legacy.SituationWord
UserWord = models_legacy.UserWord
UserSituation = models_legacy.UserSituation
Conversation = models_legacy.Conversation
Subscription = models_legacy.Subscription
# Base is imported from database, not from models.py
from app.database import Base

# Import AI request models from ai_requests.py
from app.models.ai_requests import (
    LLMRequest,
    STTRequest,
    TTSRequest,
)

__all__ = [
    "User",
    "Situation",
    "Word",
    "SituationWord",
    "UserWord",
    "UserSituation",
    "Conversation",
    "Subscription",
    "LLMRequest",
    "STTRequest",
    "TTSRequest",
]

# Also export Base if it exists
if Base:
    __all__.append("Base")
