"""Custom event helpers for the degen-themed blackjack side bet example."""


def deal_cards_event(gamestate, player_hand: list[dict], dealer_hand: list[dict], player_total: int, dealer_total: int):
    """Emit the dealt player and dealer hands for a round."""
    gamestate.book.add_event(
        {
            "index": len(gamestate.book.events),
            "type": "dealCards",
            "theme": "degen-blackjack",
            "playerHand": player_hand,
            "dealerHand": dealer_hand,
            "playerTotal": player_total,
            "dealerTotal": dealer_total,
        }
    )



def degen_verdict_event(gamestate, verdict: str, payout: float, player_total: int, dealer_total: int):
    """Emit the final themed narration for the round result."""
    gamestate.book.add_event(
        {
            "index": len(gamestate.book.events),
            "type": "degenVerdict",
            "verdict": verdict,
            "playerTotal": player_total,
            "dealerTotal": dealer_total,
            "payoutMultiplier": int(round(payout * 100, 0)),
        }
    )
