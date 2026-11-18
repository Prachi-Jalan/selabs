from board import SIZE, EMPTY, in_bounds, move_piece, remove_piece


def owner(piece):
    """'R' or 'B' for a piece, None for an empty square."""
    return None if piece == EMPTY else piece[0]


def is_king(piece):
    return piece.endswith("K")


def opponent(player):
    return "B" if player == "R" else "R"


def directions(piece):
    """Row/col steps a piece may move in. Men move forward only; kings both ways."""
    if is_king(piece):
        return [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    forward = -1 if owner(piece) == "R" else 1
    return [(forward, -1), (forward, 1)]


def simple_moves_from(board, start):
    sr, sc = start
    piece = board[sr][sc]
    moves = []
    for dr, dc in directions(piece):
        er, ec = sr + dr, sc + dc
        if in_bounds(er, ec) and board[er][ec] == EMPTY:
            moves.append((er, ec))
    return moves


def captures_from(board, start):
    """List of (end, jumped) pairs for every single jump available from start."""
    sr, sc = start
    piece = board[sr][sc]
    enemy = opponent(owner(piece))
    jumps = []
    for dr, dc in directions(piece):
        mr, mc = sr + dr, sc + dc
        er, ec = sr + 2 * dr, sc + 2 * dc
        if (in_bounds(er, ec) and board[er][ec] == EMPTY
                and owner(board[mr][mc]) == enemy):
            jumps.append(((er, ec), (mr, mc)))
    return jumps


def pieces_of(board, player):
    return [(r, c) for r in range(SIZE) for c in range(SIZE)
            if owner(board[r][c]) == player]


def any_capture(board, player):
    return any(captures_from(board, pos) for pos in pieces_of(board, player))


def has_legal_move(board, player):
    return any(captures_from(board, p) or simple_moves_from(board, p)
               for p in pieces_of(board, player))


def validate_move(board, player, start, end, must_continue_from=None):
    """
    Check a single step. Returns (kind, jumped, error):
      kind is "capture" or "move" when legal, else None and error explains why.
    Forced capture: if any capture exists for this player, a simple move is refused.
    must_continue_from: during a multi-capture, only that piece may jump again.
    """
    if owner(board[start[0]][start[1]]) != player:
        return None, None, "That is not your piece."
    if must_continue_from is not None and start != must_continue_from:
        return None, None, f"You must keep jumping with the piece at {must_continue_from}."

    for dest, jumped in captures_from(board, start):
        if dest == end:
            return "capture", jumped, None

    if must_continue_from is not None:
        return None, None, "You must make another capture with this piece."
    if any_capture(board, player):
        return None, None, "A capture is available - you must take it."
    if end in simple_moves_from(board, start):
        return "move", None, None
    return None, None, "Invalid move."


def apply_move(board, start, end, jumped):
    move_piece(board, start, end)
    if jumped is not None:
        remove_piece(board, jumped)


def promote(board, pos):
    """Promote the piece at pos if it reached its far row. Returns True if promoted."""
    r, c = pos
    piece = board[r][c]
    if piece == "R" and r == 0:
        board[r][c] = "RK"
        return True
    if piece == "B" and r == SIZE - 1:
        board[r][c] = "BK"
        return True
    return False


def winner(board, player_to_move):
    """
    Called before a player's turn. Returns (winner, reason) if the game is over,
    else (None, None). A side with no pieces or no legal moves loses.
    """
    if not pieces_of(board, player_to_move):
        return opponent(player_to_move), "no pieces left"
    if not has_legal_move(board, player_to_move):
        return opponent(player_to_move), "no legal moves"
    return None, None
