# backend/othello_core.py
EMPTY = "."
BLACK = "●"
WHITE = "○"
BOARD_SIZE = 8
DIRECTIONS = [(-1, -1), (-1, 0), (-1, 1),
              (0, -1),          (0, 1),
              (1, -1),  (1, 0), (1, 1)]

def init_board():
    board = [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    mid = BOARD_SIZE // 2
    board[mid-1][mid-1] = BLACK
    board[mid-1][mid] = WHITE
    board[mid][mid-1] = WHITE
    board[mid][mid] = BLACK
    return board

def copy_board(board):
    return [row.copy() for row in board]

def is_valid_pos(r, c):
    return 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE

def get_flipped_pieces(board, r, c, player):
    enemy = WHITE if player == BLACK else BLACK
    flip_list = []
    for dr, dc in DIRECTIONS:
        temp = []
        cr, cc = r + dr, c + dc
        while is_valid_pos(cr, cc) and board[cr][cc] == enemy:
            temp.append((cr, cc))
            cr += dr
            cc += dc
        if is_valid_pos(cr, cc) and board[cr][cc] == player and temp:
            flip_list.extend(temp)
    return flip_list

def can_place(board, r, c, player):
    if not is_valid_pos(r,c) or board[r][c] != EMPTY:
        return False
    return len(get_flipped_pieces(board, r, c, player)) > 0

def get_all_valid_moves(board, player):
    moves = []
    for r in range(8):
        for c in range(8):
            if can_place(board, r, c, player):
                moves.append([r,c])
    return moves

def place_piece(board, r, c, player):
    flips = get_flipped_pieces(board, r, c, player)
    board[r][c] = player
    for fr, fc in flips:
        board[fr][fc] = player
    return len(flips)

def count_score(board):
    b,w = 0,0
    for row in board:
        for cell in row:
            if cell == BLACK: b+=1
            elif cell == WHITE: w+=1
    return b,w

def game_over(board):
    return len(get_all_valid_moves(board, BLACK)) == 0 and len(get_all_valid_moves(board, WHITE)) == 0

# 序列化：转JSON可传输格式
def board_to_json(board):
    res = []
    for row in board:
        line = []
        for cell in row:
            if cell == EMPTY: line.append(0)
            elif cell == BLACK: line.append(1)
            else: line.append(2)
        res.append(line)
    return res

def json_to_board(arr):
    map_dict = {0:EMPTY, 1:BLACK, 2:WHITE}
    return [[map_dict[cell] for cell in row] for row in arr]