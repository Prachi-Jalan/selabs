# Lab 4 – VibeCoding: 21_checkers (PES1UG24CS326, Prachi Jalan)

Source repo: https://github.com/SETAPESU26/21_checkers

## Bugs found in the original code
1. **Capture did not remove the jumped piece** (Task 1) – `move_piece` was called but nothing cleared the middle square.
   Repro: `5 0 4 1`, `2 3 3 2`, `4 1 2 3` – Black piece at (3,2) stays on the board.
2. A piece could "capture" its own king (`"RK" not in (".", "R")` was true).
3. Kings could only move forward, like ordinary men.
4. Board printing went out of line once a king ("RK") appeared.
5. No win/no-move detection – the game never ended.

## What was added
- **Task 1:** jumped piece removed; own pieces/kings can't be jumped.
- **Task 2:** game ends when the side to move has no pieces or no legal moves.
- **Task 3:** forced capture, multi-capture turns (same piece must keep jumping; crowning ends the turn), kings move/capture both directions, promotion only on the opponent's back row.
- **Task 4:** one feedback line per accepted move (move / capture / promotion / keep-jumping / game over).
- `test_checkers.py`: 16 unittest cases – ordinary moves, captures, multi-capture, forced capture, promotion, king movement, no-move win, no-piece win, invalid coordinates, quitting.

No new dependencies, no persistence – all state stays in memory.

## Run
    cd code
    python main.py
    python -m unittest -v test_checkers
