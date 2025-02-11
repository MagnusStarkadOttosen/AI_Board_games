from Logic.graph_logic import build_anytree, export_colored_tree
from Logic.tree_logic import GameLogic, GameTreeNode

class HexapawnLogic(GameLogic):
    def __init__(self):
        super().__init__()

    def check_winner(self, state):
        """Determine if there is a winner."""
        if "W" in state[0]:
            return "W"
    
        if "B" in state[2]:
            return "B"
        
        white_count = sum(row.count("W") for row in state)
        black_count = sum(row.count("B") for row in state)
        
        if black_count == 0:
            return "W"
        
        if white_count == 0:
            return "B"
        
        if not self.get_valid_moves(state, "W") and not self.get_valid_moves(state, "B"):
            return "Tie"

        return None
    
    def get_valid_moves(self, state, turn):
        """Return all valid moves for a given state and turn."""
        moves = []
        direction = -1 if turn == "W" else 1 # White moves up and black moves down

        for row in range(3):
            for col in range(3):
                if state[row][col] == turn:
                    new_row = row + direction

                    if 0 <= new_row < 3 and state[new_row][col] == "_":
                        moves.append(((row, col), (new_row, col))) # Move forward

                    for d_col in [-1, 1]: # Capture diagonally
                        new_col = col + d_col
                        if 0 <= new_row < 3 and 0 <= new_col < 3:
                            if state[new_row][new_col] not in ["_", turn]:
                                moves.append(((row, col), (new_row, new_col)))
        return moves
    
    def apply_move(self, state, move):
        """Apply a move to a state and return the new state."""
        new_state = [row[:] for row in state] # Make copy of current state
        (r1, c1), (r2, c2) = move
        new_state[r2][c2] = new_state[r1][c1] # Move the piece
        new_state[r1][c1] = "_" # Remove the old piece
        return new_state

    def next_turn(self, turn):
        """Return the next player's turn."""
        return "B" if turn == "W" else "W"
    
    def state_to_tuple(self, state):
        """Convert the game state to a tuple (for deduplication)."""
        original = tuple(tuple(row) for row in state)
        mirrored = tuple(tuple(row[::-1]) for row in state)
        return min(original, mirrored)


# ---- Running the Hexapawn Game ----

# Initialize the game logic
hexapawn_logic = HexapawnLogic()

# Define the starting board
initial_board = [
    ["B", "B", "B"],
    ["_", "_", "_"],
    ["W", "W", "W"]
]

# Create the root node and expand the game tree
root = GameTreeNode(initial_board, turn="W", game_logic=hexapawn_logic)
root.generate_children()

# Convert to anytree format and export
anytree_root = build_anytree(root)
export_colored_tree(anytree_root)