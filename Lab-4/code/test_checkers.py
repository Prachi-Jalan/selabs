import io
import unittest
from unittest.mock import patch

from board import empty_board, initial_board
from game import Checkers


def game_with(pieces, player="R"):
    b = empty_board()
    for (r, c), p in pieces.items():
        b[r][c] = p
    return Checkers(b, player)


class TestCheckers(unittest.TestCase):
    def test_ordinary_move(self):
        g = Checkers()
        msg = g.play((5, 0), (4, 1))
        self.assertIn("moved", msg)
        self.assertEqual(g.board[4][1], "R")
        self.assertEqual(g.board[5][0], ".")
        self.assertEqual(g.player, "B")

    def test_backward_move_for_man_rejected(self):
        g = game_with({(4, 3): "R", (0, 1): "B"})
        self.assertEqual(g.play((4, 3), (5, 4)), "Invalid move.")

    def test_capture_removes_jumped_piece(self):          # Task 1
        g = game_with({(4, 1): "R", (3, 2): "B", (0, 7): "B"})
        msg = g.play((4, 1), (2, 3))
        self.assertIn("captured 3 2", msg)
        self.assertEqual(g.board[3][2], ".")
        self.assertEqual(g.board[2][3], "R")
        self.assertEqual(g.board[4][1], ".")

    def test_cannot_jump_own_piece_or_king(self):
        g = game_with({(4, 1): "R", (3, 2): "RK", (0, 7): "B"})
        self.assertNotIn("captured", g.play((4, 1), (2, 3)))
        self.assertEqual(g.board[3][2], "RK")

    def test_forced_capture(self):
        g = game_with({(4, 1): "R", (3, 2): "B", (6, 5): "R", (0, 7): "B"})
        self.assertIn("must take it", g.play((6, 5), (5, 4)))
        self.assertEqual(g.player, "R")

    def test_multi_capture(self):
        g = game_with({(6, 1): "R", (5, 2): "B", (3, 4): "B", (7, 6): "R", (0, 7): "B"})
        msg = g.play((6, 1), (4, 3))
        self.assertIn("keep jumping", msg)
        self.assertEqual(g.player, "R")
        # a different piece may not move mid-chain
        self.assertIn("must keep jumping", g.play((7, 6), (6, 7)))
        msg = g.play((4, 3), (2, 5))
        self.assertIn("captured 3 4", msg)
        self.assertEqual(g.player, "B")
        self.assertEqual(g.board[5][2], ".")
        self.assertEqual(g.board[3][4], ".")

    def test_promotion_red_and_black(self):
        g = game_with({(1, 2): "R", (6, 5): "B"})
        self.assertIn("Promoted", g.play((1, 2), (0, 1)))
        self.assertEqual(g.board[0][1], "RK")
        self.assertIn("Promoted", g.play((6, 5), (7, 4)))
        self.assertEqual(g.board[7][4], "BK")

    def test_no_promotion_on_own_back_row(self):
        g = game_with({(6, 1): "B", (0, 7): "R"}, player="B")
        g.play((6, 1), (7, 2))
        self.assertEqual(g.board[7][2], "BK")
        g = game_with({(2, 1): "R", (6, 7): "B"})
        g.play((2, 1), (1, 2))
        self.assertEqual(g.board[1][2], "R")

    def test_king_moves_both_directions(self):
        g = game_with({(4, 3): "RK", (0, 1): "B"})
        g.play((4, 3), (5, 4))                      # backward for red
        self.assertEqual(g.board[5][4], "RK")
        g.play((0, 1), (1, 2))
        g.play((5, 4), (4, 5))                      # forward
        self.assertEqual(g.board[4][5], "RK")

    def test_king_captures_backward(self):
        g = game_with({(3, 3): "RK", (4, 4): "B", (0, 1): "B"})
        g.play((3, 3), (5, 5))
        self.assertEqual(g.board[4][4], ".")

    def test_win_by_no_pieces(self):
        g = game_with({(4, 1): "R", (3, 2): "B"})
        msg = g.play((4, 1), (2, 3))
        self.assertIn("Red wins", msg)
        self.assertIn("no pieces", msg)
        self.assertTrue(g.over)

    def test_win_by_no_legal_moves(self):
        # Black man at 6,1 is blocked: both squares ahead are taken, jumps go off-board.
        # Reds on 5,0 and 5,2 stop red from capturing it.
        g = game_with({(6, 1): "B", (7, 0): "R", (7, 2): "R", (5, 0): "R", (5, 2): "R"})
        msg = g.play((5, 2), (4, 3))
        self.assertIn("Red wins", msg)
        self.assertIn("no legal moves", msg)

    def test_one_message_per_move(self):                  # Task 4
        g = Checkers()
        msg = g.play((5, 0), (4, 1))
        self.assertEqual(msg.count("\n"), 0)

    def test_not_your_piece(self):
        g = Checkers()
        self.assertEqual(g.play((2, 1), (3, 0)), "That is not your piece.")
        self.assertEqual(g.play((4, 0), (3, 1)), "That is not your piece.")

    def run_with(self, text):
        with patch("builtins.input", side_effect=text + [EOFError()]), \
                patch("sys.stdout", new_callable=io.StringIO) as out:
            Checkers().run()
        return out.getvalue()

    def test_invalid_coordinates_and_quit(self):
        out = self.run_with(["9 0 4 1", "a b c d", "5 0", "-1 0 0 0", "q"])
        self.assertIn("Outside board.", out)
        self.assertIn("Coordinates must be numbers.", out)
        self.assertIn("Enter four coordinates.", out)
        self.assertIn("Goodbye.", out)

    def test_initial_board_unchanged(self):
        self.assertEqual(sum(row.count("R") for row in initial_board()), 12)
        self.assertEqual(sum(row.count("B") for row in initial_board()), 12)


if __name__ == "__main__":
    unittest.main()
