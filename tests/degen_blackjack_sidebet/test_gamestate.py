import sys
import types
import unittest

sys.modules.setdefault('zstandard', types.SimpleNamespace(ZstdCompressor=type('ZstdCompressor', (), {'compress': lambda self, data: data})))

GAME_DIR = '/workspace/math-sdk/games/degen_blackjack_sidebet'
ROOT_DIR = '/workspace/math-sdk'
for path in [GAME_DIR, ROOT_DIR]:
    if path not in sys.path:
        sys.path.insert(0, path)

from game_config import GameConfig
from gamestate import GameState


class TestDegenBlackjackGameState(unittest.TestCase):
    def test_round_book_contains_required_keys_and_events(self):
        gamestate = GameState(GameConfig())
        gamestate.criteria = 'basegame'
        gamestate.betmode = 'base'
        gamestate.run_spin(0)

        book = gamestate.library[1]
        self.assertIn('id', book)
        self.assertIn('events', book)
        self.assertIn('payoutMultiplier', book)
        self.assertEqual(book['payoutMultiplier'], 500)
        self.assertEqual([event['type'] for event in book['events']], ['dealCards', 'winInfo', 'degenVerdict', 'finalWin'])


if __name__ == '__main__':
    unittest.main()
