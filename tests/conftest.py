"""Shared pytest fixtures."""
import sys
from pathlib import Path

# Allow `import src...` from the repo root regardless of where pytest is launched.
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
