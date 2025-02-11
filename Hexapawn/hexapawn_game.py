class Hexapawn_Node:
    def __init__(self, board, turn, parent=None):
        self.board = board
        self.turn = turn
        self.parent = parent
        self.children = []
    
    def generate_valid_children(self):
        moves = get_valid_moves(self.board, self.turn)
        for move in moves:
            new_board = apply_move(self.board, move)
            next_turn = "B" if self.turn == "W" else "W"
            child = Hexapawn_Node(new_board, next_turn, parent=self)
            self.children.append(child)
            child.generate_valid_children()
    
    def __repr__(self):
        return "\n".join("".join(row) for row in self.board) + "\n"

def get_valid_moves(board, turn):
    moves = []
    direction = -1 if turn == "W" else 1

    for row in range(3):
        for col in range(3):
            if board[row][col] == turn:
                new_row = row + direction

                if 0 <= new_row < 3 and board[new_row][col] == ".":
                    moves.append(((row, col), (new_row, col)))

                for d_col in [-1, 1]:
                    new_col = col + d_col
                    if 0 <= new_row < 3 and 0 <= new_col < 3:
                        if board[new_row][new_col] not in [".", turn]:
                            moves.append(((row, col), (new_row, new_col)))
    return moves


def apply_move(board, move):
    new_board = [row[:] for row in board]
    (r1, c1), (r2, c2) = move
    new_board[r2][c2] = new_board[r1][c1]
    new_board[r1][c1] = "."
    return new_board

def print_tree(node, depth=0):
    print(" " * depth * 2 + f"Turn: {node.turn}\n{node}")
    for child in node.children:
        print_tree(child, depth + 1)

initial_board = [
    ["B","B","B"],
    [".",".","."],
    ["W","W","W"]
]

root = Hexapawn_Node(initial_board, "W")
root.generate_valid_children()

print_tree(root)