This example is a custom side-bet style blackjack game with degen-themed cards and narration.

Each round deals a player hand and dealer hand, resolves blackjack-style scoring, and emits custom
book events that a side-bet frontend can render directly. Outcomes cycle through blackjack, wins,
pushes, dealer wins, and busts so the sample output includes every major state.

Playable terminal demo:
- cd games/degen_blackjack_sidebet
- python play.py

SDK sample generation:
- cd games/degen_blackjack_sidebet
- python run.py

Structure notes:
- Follows the documented Stake Engine sample layout, including `game_events.py` for custom event helpers.

Stake Engine publish check:
- python validate_publish.py
- Validates `library/publish_files/index.json`, referenced lookup CSVs, and referenced `.jsonl.zst` event files against the documented math format.
