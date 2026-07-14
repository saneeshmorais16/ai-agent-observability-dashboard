import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = DATA_DIR / "outputs"
DATABASE_PATH = BASE_DIR / "agent_observability.db"
APP_ENV = os.getenv("APP_ENV", "development")
DEFAULT_COST_PER_1K_INPUT_TOKENS = float(os.getenv("DEFAULT_COST_PER_1K_INPUT_TOKENS", "0.001"))
DEFAULT_COST_PER_1K_OUTPUT_TOKENS = float(os.getenv("DEFAULT_COST_PER_1K_OUTPUT_TOKENS", "0.002"))
