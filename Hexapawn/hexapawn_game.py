from anytree import Node, RenderTree
from anytree.exporter import DotExporter

class Hexapawn_Node:
    seen_states = {}

    def __init__(self, board, turn, parent=None, move=None):
        self.board = board
        self.turn = turn
        self.parent = parent
        self.move = move
        self.children = []
        self.winner = check_winner(self.board)
    
    def generate_valid_children(self):
        if self.winner is not None:
            return
        
        board_tuple = canonical_board_tuple(self.board)
        if board_tuple in Hexapawn_Node.seen_states:
            return
        
        Hexapawn_Node.seen_states[board_tuple] = self

        moves = get_valid_moves(self.board, self.turn)
        if not moves:
            if check_winner(self.board) is None:
                self.winner = "Tie"
            return

        for move in moves:
            new_board = apply_move(self.board, move)
            new_board_tuple = canonical_board_tuple(new_board)
            if new_board_tuple in Hexapawn_Node.seen_states:
                existing_child = Hexapawn_Node.seen_states[new_board_tuple]
                if existing_child not in self.children:
                    self.children.append(existing_child)
                continue
            next_turn = "B" if self.turn == "W" else "W"
            child = Hexapawn_Node(new_board, next_turn, parent=self, move=move)
            self.children.append(child)
            child.generate_valid_children()
    
    def board_str(self):
        return "\n".join("".join(row) for row in self.board)

    def __repr__(self):
        return "\n".join("".join(row) for row in self.board) + "\n"

def check_winner(board):
    if "W" in board[0]:
        return "W"
    
    if "B" in board[2]:
        return "B"
    
    white_count = sum(row.count('W') for row in board)
    black_count = sum(row.count('B') for row in board)
    
    if black_count == 0:
        return 'W'
    
    if white_count == 0:
        return 'B'
    
    if not get_valid_moves(board, 'W') and not get_valid_moves(board, 'B'):
        return "Tie"

    return None
    

def get_valid_moves(board, turn):
    moves = []
    direction = -1 if turn == "W" else 1

    for row in range(3):
        for col in range(3):
            if board[row][col] == turn:
                new_row = row + direction

                if 0 <= new_row < 3 and board[new_row][col] == "_":
                    moves.append(((row, col), (new_row, col)))

                for d_col in [-1, 1]:
                    new_col = col + d_col
                    if 0 <= new_row < 3 and 0 <= new_col < 3:
                        if board[new_row][new_col] not in ["_", turn]:
                            moves.append(((row, col), (new_row, new_col)))
    return moves


def apply_move(board, move):
    new_board = [row[:] for row in board]
    (r1, c1), (r2, c2) = move
    new_board[r2][c2] = new_board[r1][c1]
    new_board[r1][c1] = "_"
    return new_board

def print_tree(node, depth=0):
    print(" " * depth * 2 + f"Turn: {node.turn}\n{node}")
    for child in node.children:
        print_tree(child, depth + 1)

def build_anytree(node, parent=None):
    if node.winner == "B":
        color = "red"
    elif node.winner == "W":
        color = "green"
    elif node.winner == "Tie":
        color = "blue"
    else:
        color = "white"
    
    move_text = f"Move: {node.move}" if node.move else "Root"
    tree_node = Node(f"{move_text}\n{node.board_str()}", parent=parent, winner=node.winner, color=color)
    for child in node.children:
        build_anytree(child, tree_node)
    return tree_node

def board_to_tuple(board):
    return tuple(tuple(row) for row in board)

def mirror_board(board):
    return [row[::-1] for row in board]

def canonical_board_tuple(board):
    original = board_to_tuple(board)
    mirrored = board_to_tuple(mirror_board(board))
    return min(original, mirrored)

def export_colored_tree(anytree_root, filename="hexapawn_tree.dot"):
    DotExporter(anytree_root,
                nodeattrfunc=lambda node: f'style=filled, fillcolor={node.color}')\
                .to_dotfile(filename)

initial_board = [
    ["B","B","B"],
    ["_","_","_"],
    ["W","W","W"]
]

root = Hexapawn_Node(initial_board, "W")
root.generate_valid_children()

# print_tree(root)

# anytree_root = build_anytree(root)
# for pre, fill, node in RenderTree(anytree_root):
#     print(f"{pre}{node.name}")

# # DotExporter(anytree_root).to_picture("hexapawn_tree.png")
# from anytree.exporter import DotExporter
# DotExporter(anytree_root).to_dotfile("hexapawn_tree.dot")

anytree_root = build_anytree(root)
export_colored_tree(anytree_root)