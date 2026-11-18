SIZE = 8
EMPTY = "."


def initial_board():
    board = [[EMPTY] * SIZE for _ in range(SIZE)]
    for r in range(3):
        for c in range(SIZE):
            if (r + c) % 2 == 1:
                board[r][c] = "B"
    for r in range(5, 8):
        for c in range(SIZE):
            if (r + c) % 2 == 1:
                board[r][c] = "R"
    return board


def empty_board():
    """Blank board, handy for setting up test positions."""
    return [[EMPTY] * SIZE for _ in range(SIZE)]


def in_bounds(r, c):
    return 0 <= r < SIZE and 0 <= c < SIZE


def move_piece(board, start, end):
    board[end[0]][end[1]] = board[start[0]][start[1]]
    board[start[0]][start[1]] = EMPTY


def remove_piece(board, pos):
    board[pos[0]][pos[1]] = EMPTY


def render(board):
    """Return the board as text. Every cell is 2 chars wide so kings ("RK") line up."""
    lines = ["\n    " + " ".join(f"{c:<2}" for c in range(SIZE))]
    for r, row in enumerate(board):
        lines.append(f"{r}   " + " ".join(f"{cell:<2}" for cell in row))
    return "\n".join(lines)
