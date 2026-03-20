"""Game state for the degen-themed blackjack side bet example."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from game_events import deal_cards_event, degen_verdict_event
from game_override import GameStateOverride
from logic import resolve_round
from src.events.event_constants import EventConstants
from src.events.events import final_win_event


class GameState(GameStateOverride):
    """Simulates one degen-themed blackjack side bet per round."""

    def run_spin(self, sim, simulation_seed=None):
        self.reset_seed(sim, simulation_seed)
        self.repeat = True
        while self.repeat:
            self.reset_book()
            result = resolve_round(sim)

            deal_cards_event(self, result.player_hand, result.dealer_hand, result.player_total, result.dealer_total)

            self.win_data = {
                "totalWin": result.payout,
                "wins": [
                    {
                        "win": result.payout,
                        "positions": [],
                        "meta": {
                            "outcome": result.outcome,
                            "playerTotal": result.player_total,
                            "dealerTotal": result.dealer_total,
                            "playerHand": result.player_hand,
                            "dealerHand": result.dealer_hand,
                            "commentary": result.verdict,
                        },
                    }
                ],
            }
            self.win_manager.update_spinwin(result.payout)
            self.win_manager.update_gametype_wins(self.gametype)
            self.book.add_event(
                {
                    "index": len(self.book.events),
                    "type": EventConstants.WIN_DATA.value,
                    "totalWin": int(round(result.payout * 100, 0)),
                    "wins": self.win_data["wins"],
                }
            )
            degen_verdict_event(self, result.verdict, result.payout, result.player_total, result.dealer_total)

            self.evaluate_finalwin()

        self.imprint_wins()

    def evaluate_finalwin(self) -> None:
        self.update_final_win()
        final_win_event(self)
        self.check_repeat()

    def run_freespin(self):
        pass
