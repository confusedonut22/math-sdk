"""Configuration for the degen-themed blackjack side bet example game."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from src.config.config import BetMode, Config
from src.config.distributions import Distribution


class GameConfig(Config):
    """Configuration for a lightweight custom side-bet style card game."""

    def __init__(self):
        super().__init__()
        self.game_id = "degen_blackjack_sidebet"
        self.provider_number = 0
        self.working_name = "degen_blackjack_sidebet"
        self.wincap = 5
        self.win_type = "other"
        self.rtp = 0
        self.construct_paths()

        self.num_reels = 0
        self.num_rows = []
        self.paytable = {}
        self.include_padding = False
        self.special_symbols = {"wild": [], "scatter": [], "multiplier": []}
        self.freespin_triggers = {self.basegame_type: {}, self.freegame_type: {}}
        self.anticipation_triggers = {self.basegame_type: 0, self.freegame_type: 0}

        self.bet_modes = [
            BetMode(
                name="base",
                cost=1.0,
                rtp=self.rtp,
                max_win=self.wincap,
                auto_close_disabled=False,
                is_feature=True,
                is_buybonus=False,
                distributions=[
                    Distribution(
                        criteria="basegame",
                        quota=1.0,
                        conditions={
                            "reel_weights": {},
                            "force_wincap": False,
                            "force_freegame": False,
                        },
                    ),
                ],
            ),
        ]
