import sys
from pathlib import Path

# Make tools/ importable (catalogue.py, check_site.py).
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
