import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

TEST_DB = ROOT / "test_qn.db"
if TEST_DB.exists():
    TEST_DB.unlink()
