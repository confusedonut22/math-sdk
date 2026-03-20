"""Terminal-playable runner for the degen-themed blackjack side bet sample."""

from __future__ import annotations

from logic import format_card, resolve_round


def print_round(sim: int, balance: float, bet: float) -> float:
    result = resolve_round(sim)
    payout_amount = bet * result.payout
    ending_balance = balance - bet + payout_amount

    print("\n=== Degen Blackjack Side Bet ===")
    print(f"Round #{sim + 1}")
    print(f"Starting balance: {balance:.2f}")
    print(f"Bet: {bet:.2f}")
    print("\nPlayer hand:")
    for card in result.player_hand:
        print(f"  - {format_card(card)}")
    print(f"  Total: {result.player_total}")

    print("\nDealer hand:")
    for card in result.dealer_hand:
        print(f"  - {format_card(card)}")
    print(f"  Total: {result.dealer_total}")

    print(f"\nOutcome: {result.outcome}")
    print(result.verdict)
    print(f"Payout multiplier: {result.payout:.2f}x")
    print(f"Round payout: {payout_amount:.2f}")
    print(f"Ending balance: {ending_balance:.2f}")
    return ending_balance



def main() -> None:
    balance = 100.0
    bet = 1.0
    sim = 0

    print("Welcome to Degen Blackjack Side Bet.")
    print("Press Enter to deal the next deterministic round, or type q to quit.")

    while True:
        command = input("\nDeal next round? [Enter/q]: ").strip().lower()
        if command in {"q", "quit", "exit"}:
            print(f"\nGG. Cashing out with balance {balance:.2f}.")
            return
        balance = print_round(sim, balance, bet)
        sim += 1


if __name__ == "__main__":
    main()
