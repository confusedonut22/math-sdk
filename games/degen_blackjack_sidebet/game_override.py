"""Override hooks for the degen-themed blackjack side bet example."""

from game_executables import GameExecutables


class GameStateOverride(GameExecutables):
    """Extension point for custom game-specific behavior."""

    def reset_book(self):
        super().reset_book()

    def assign_special_sym_function(self):
        pass
