"""Pure game logic for the degen-themed blackjack side bet sample."""

from __future__ import annotations

from dataclasses import dataclass

CARD_POOL = [
    {"rank": "A", "label": "Degen Ace", "value": 11, "suit": "Laser Eyes"},
    {"rank": "K", "label": "Whale King", "value": 10, "suit": "Diamond Hands"},
    {"rank": "Q", "label": "Moon Queen", "value": 10, "suit": "Rocket Fuel"},
    {"rank": "J", "label": "Ape Jack", "value": 10, "suit": "Banana Club"},
    {"rank": "10", "label": "Tenx Ticket", "value": 10, "suit": "Green Candle"},
    {"rank": "9", "label": "Cloud Nine", "value": 9, "suit": "Hopium"},
    {"rank": "8", "label": "Infinity Exit", "value": 8, "suit": "Liquidation"},
    {"rank": "7", "label": "Lucky Seven Gwei", "value": 7, "suit": "Gas Wars"},
    {"rank": "6", "label": "Six Figure Screenshot", "value": 6, "suit": "PnL"},
    {"rank": "5", "label": "Five Alarm Margin Call", "value": 5, "suit": "Leverage"},
    {"rank": "4", "label": "Four Hour Chop", "value": 4, "suit": "Rangebound"},
    {"rank": "3", "label": "Triple Top", "value": 3, "suit": "Resistance"},
    {"rank": "2", "label": "Double Bottom", "value": 2, "suit": "Support"},
]

OUTCOME_CYCLE = [
    "player_blackjack",
    "dealer_bust",
    "player_win",
    "push",
    "dealer_win",
    "player_bust",
]

PRESET_HANDS = {
    "player_blackjack": ([0, 1], [8, 7]),
    "dealer_bust": ([6, 5, 11], [9, 10, 4]),
    "player_win": ([8, 9, 10], [11, 12, 8]),
    "push": ([3, 4], [1, 4]),
    "dealer_win": ([11, 12, 9], [6, 5, 12]),
    "player_bust": ([1, 2, 4], [8, 10, 11]),
}

PAYOUT_MAP = {
    "player_blackjack": (5.0, "Blackjack, anon. The side bet nukes straight to 5x."),
    "dealer_bust": (2.0, "Dealer got rugged above 21. Side bet prints 2x."),
    "player_win": (2.0, "Your degen hand held support and beat the dealer for 2x."),
    "push": (1.0, "Perfect chop. You get the side bet stake back at 1x."),
    "dealer_win": (0.0, "Dealer faded your conviction. The side bet whiffs."),
    "player_bust": (0.0, "You over-leveraged and busted. Better luck next candle."),
}


@dataclass(frozen=True)
class RoundResult:
    outcome: str
    payout: float
    verdict: str
    player_hand: list[dict]
    dealer_hand: list[dict]
    player_total: int
    dealer_total: int


def score_hand(hand: list[dict]) -> int:
    """Score a blackjack hand, softening aces from 11 to 1 when needed."""
    total = sum(card["value"] for card in hand)
    ace_count = sum(1 for card in hand if card["rank"] == "A")
    while total > 21 and ace_count > 0:
        total -= 10
        ace_count -= 1
    return total



def build_hand_for_outcome(outcome: str) -> tuple[list[dict], list[dict]]:
    """Return preset hands for a deterministic example outcome."""
    player_indexes, dealer_indexes = PRESET_HANDS[outcome]
    player_hand = [CARD_POOL[index].copy() for index in player_indexes]
    dealer_hand = [CARD_POOL[index].copy() for index in dealer_indexes]
    return player_hand, dealer_hand



def resolve_round(sim: int) -> RoundResult:
    """Resolve one deterministic round based on the sample outcome cycle."""
    outcome = OUTCOME_CYCLE[sim % len(OUTCOME_CYCLE)]
    player_hand, dealer_hand = build_hand_for_outcome(outcome)
    player_total = score_hand(player_hand)
    dealer_total = score_hand(dealer_hand)
    payout, verdict = PAYOUT_MAP[outcome]
    return RoundResult(
        outcome=outcome,
        payout=payout,
        verdict=verdict,
        player_hand=player_hand,
        dealer_hand=dealer_hand,
        player_total=player_total,
        dealer_total=dealer_total,
    )



def format_card(card: dict) -> str:
    """Return a terminal-friendly label for a themed card."""
    return f"{card['label']} [{card['rank']} / {card['suit']}]"
