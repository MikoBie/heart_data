__all__ = ["api", "mapping"]
from pathlib import Path

ROOT = Path(__file__).absolute().parent.parent
DATA = ROOT / "data"
RAW = DATA / "raw"
PROC = DATA / "processed"
BIO = PROC / "bioassist"
