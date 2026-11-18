from board import initial_board, render, SIZE
from rules import validate_move, apply_move, promote, captures_from, winner, opponent

NAMES = {"R": "Red", "B": "Black"}


class Checkers:
    def __init__(self, board=None, player="R"):
        self.board = board if board is not None else initial_board()
        self.player = player
        self.continue_from = None   # set while a multi-capture is in progress
        self.over = False

    def print_board(self):
        print(render(self.board))

    def play(self, start, end):
        """
        Try one step for the current player. Returns exactly one player-facing
        message per accepted step (or an error message if rejected).
        """
        kind, jumped, error = validate_move(
            self.board, self.player, start, end, self.continue_from)
        if error:
            return error

        apply_move(self.board, start, end, jumped)
        promoted = promote(self.board, end)
        who = NAMES[self.player]

        if kind == "capture":
            msg = f"{who} captured {jumped[0]} {jumped[1]}, landing on {end[0]} {end[1]}."
        else:
            msg = f"{who} moved {start[0]} {start[1]} -> {end[0]} {end[1]}."
        if promoted:
            msg += " Promoted to king!"

        # Multi-capture: same piece keeps jumping unless it just got crowned.
        if kind == "capture" and not promoted and captures_from(self.board, end):
            self.continue_from = end
            return msg + " Another capture is available - keep jumping."

        self.continue_from = None
        self.player = opponent(self.player)
        win, reason = winner(self.board, self.player)
        if win:
            self.over = True
            msg += f"\nGame over: {NAMES[win]} wins ({NAMES[self.player]} has {reason})."
        return msg

    def run(self):
        print("Checkers - move: sr sc er ec   (q to quit)")
        win, reason = winner(self.board, self.player)
        if win:
            print(f"Game over: {NAMES[win]} wins ({NAMES[self.player]} has {reason}).")
            return
        while not self.over:
            self.print_board()
            try:
                raw = input(f"{self.player}> ").strip().lower().split()
            except EOFError:
                print("\nGoodbye.")
                return
            if raw in (["q"], ["quit"]):
                print("Goodbye.")
                return
            if len(raw) != 4:
                print("Enter four coordinates.")
                continue
            try:
                sr, sc, er, ec = map(int, raw)
            except ValueError:
                print("Coordinates must be numbers.")
                continue
            if not all(0 <= x < SIZE for x in (sr, sc, er, ec)):
                print("Outside board.")
                continue
            print(self.play((sr, sc), (er, ec)))
        self.print_board()
