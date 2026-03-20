"""Executable helpers for the degen-themed blackjack side bet example."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from src.executables.executables import Executables


class GameExecutables(Executables):
    """No custom executable helpers are required for this example game."""

    pass
