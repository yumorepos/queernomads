import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


def load_dotenv(dotenv_path: Path | None = None):
    path = dotenv_path or BASE_DIR / ".env"
    if not path.exists():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-only-change-me")
    _default_db = Path("/tmp/queernomads.db") if os.environ.get("VERCEL") else (BASE_DIR / "queernomads.db")
    DATABASE = os.environ.get("DATABASE_PATH", str(_default_db))
    APP_ENV = os.environ.get("FLASK_ENV", "development")
    TESTING = False


class TestConfig(Config):
    TESTING = True
    DATABASE = str(BASE_DIR / "test_qn.db")


load_dotenv()
