import os
import sys
import unittest

GAME_DIR = '/workspace/math-sdk/games/degen_blackjack_sidebet'
if GAME_DIR not in sys.path:
    sys.path.insert(0, GAME_DIR)

from logic import OUTCOME_CYCLE, resolve_round, score_hand


class TestDegenBlackjackLogic(unittest.TestCase):
    def test_soft_ace_scoring(self):
        hand = [
            {"rank": "A", "value": 11},
            {"rank": "9", "value": 9},
            {"rank": "5", "value": 5},
        ]
        self.assertEqual(score_hand(hand), 15)

    def test_outcome_cycle_and_payouts(self):
        expected = [
            ('player_blackjack', 21, 13, 5.0),
            ('dealer_bust', 20, 19, 2.0),
            ('player_win', 15, 11, 2.0),
            ('push', 20, 20, 1.0),
            ('dealer_win', 10, 19, 0.0),
            ('player_bust', 30, 13, 0.0),
        ]
        self.assertEqual(len(OUTCOME_CYCLE), len(expected))
        for sim, (outcome, player_total, dealer_total, payout) in enumerate(expected):
            result = resolve_round(sim)
            self.assertEqual(result.outcome, outcome)
            self.assertEqual(result.player_total, player_total)
            self.assertEqual(result.dealer_total, dealer_total)
            self.assertEqual(result.payout, payout)


if __name__ == '__main__':
    unittest.main()
