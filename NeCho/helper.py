import math


class Piece:
    def __init__(self, colour, n):
        self.colour = colour
        self.n = n


# Calculate the euclidean distance between 2 tokens, given as (x, y) format.
def euclidean(pos1, pos2):
    distance = math.sqrt((pos1[-2] - pos2[-2]) ** 2 + (pos1[-1] - pos2[-1]) ** 2)
    return distance


# Check if the location is available
def check_availability(pos):
    if (pos[0] < 0) or (pos[1] < 0) or (pos[0] > 7) or (pos[1] > 7):
        return False
    return True


def explosion_range(pos):
    exp_range = []
    for row in range(3):
        for col in range(3):
            check_pos = (pos[0] - 1 + col, pos[1] - 1 + row)
            if check_availability(check_pos) and (check_pos != pos):
                exp_range.append(check_pos)
    return exp_range


# Explosion function, will affect the surrounding pieces and recursively explode
def boom(board, pos, black, white):
    if board[pos[0]][pos[1]] is None:
        return
    remove_piece(board, pos, black, white)
    affected = explosion_range(pos)
    for affected_piece in affected:
        boom(board, affected_piece, black, white)


# Helper function to remove the affected pieces from the board and the black and white lists respectively
def remove_piece(board, pos, black, white):
    colour = board[pos[0]][pos[1]].colour
    if colour == 'black':
        black.remove((pos[0], pos[1]))
    elif colour == 'white':
        white.remove((pos[0], pos[1]))
    board[pos[0]][pos[1]] = None


# Move n white/black tokens from old_pos to new_pos
def move(board, n, old_pos, new_pos, colour, pieces):
    if old_pos == new_pos:
        return

    (old_x, old_y) = old_pos
    (new_x, new_y) = new_pos

    board[old_x][old_y].n -= n
    if board[old_x][old_y].n == 0:
        pieces.remove(old_pos)
        board[old_x][old_y] = None

    if board[new_x][new_y] is not None:
        board[new_x][new_y].n += n
    elif board[new_x][new_y] is None:
        board[new_x][new_y] = Piece(colour, n)

    if new_pos not in pieces:
        pieces.append(new_pos)


# Self implement function to list all the possible moves of a given piece
def available_actions(board, colour, pieces):
    actions = []
    for (x, y) in pieces:
        actions.append(("BOOM", (x, y)))
        stack = board[x][y].n
        for d in range(1, stack + 1):
            possible_moves = [(x + d, y), (x, y + d), (x - d, y), (x, y - d)]
            for (new_x, new_y) in possible_moves:
                if check_availability((new_x, new_y)) and \
                        ((board[new_x][new_y] is None) or board[new_x][new_y].colour == colour):
                    actions.append(("MOVE", d, (x, y), (new_x, new_y)))
    return actions


# Evaluate function to calculate current board state for a player
# Ver 1.1
def evaluate(board, colour, black, white):
    # points for black, return -points for white player
    points = 0

    # A stack of pieces worth much more than a single piece
    # In general, a stack of N pieces worth 4^N points than a single piece which worth only 4
    # The total points is the sum of the current player's pieces points minus the one of the opponent
    for row in range(8):
        for col in range(8):
            if board[row][col] is None:
                continue
            stack = board[row][col].n
            if board[row][col].colour == colour:
                points += 4 ** stack
            else:
                points -= 4 ** stack

    # Consider the distance, calculate the total average distance between each black and white
    # Aggressive, minimize the distance
    dis = []
    for black_piece in black:
        for white_piece in white:
            dis.append(euclidean(black_piece, white_piece))
    if len(dis) > 0:
        points -= 10 * (sum(dis) / len(dis))
    return points