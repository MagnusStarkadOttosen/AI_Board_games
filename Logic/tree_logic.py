class GameTreeNode:
    seen_states = {}

    def __init__(self, state, parent=None, move=None, turn=None, game_logic=None):
        self.state = state
        self.parent = parent
        self.move = move
        self.turn = turn
        self.children = []
        self.game_logic = game_logic
        self.winner = game_logic.check_winner(state) if game_logic else None


    def generate_children(self):
        
        # If node is already at a win condition, dont continue
        if self.winner is not None:
            return
        
        # If node is a duplicant dont continue
        state_tuple = self.game_logic.state_to_tuple(self.state)
        if state_tuple in GameTreeNode.seen_states:
            return
        
        # Mark state as seen
        GameTreeNode.seen_states[state_tuple] = self

        # Get all valid moves
        moves = self.game_logic.get_valid_moves(self.state, self.turn)
        if not moves:
            # If there is no valid moves and no winner, the state is a tie
            self.winner = "Tie" if self.game_logic.check_winner(self.state) is None else self.game_logic.check_winner(self.state)
            return
        
        for move in moves:
            # Apply move to generate new game state
            new_state = self.game_logic.apply_move(self.state, move)
            new_state_tuple = self.game_logic.state_to_tuple(new_state)

            # If the new game state is already seen, add the existing game state as a child instead of generating a new one
            if new_state_tuple in GameTreeNode.seen_states:
                existing_child = GameTreeNode.seen_states[new_state_tuple]
                if existing_child not in self.children:
                    self.children.append(existing_child)
                continue
            
            # Determine who is the next player
            next_turn = self.game_logic.next_turn(self.turn)
            # If there isnt an existing state for a valid child make one and link it
            child = GameTreeNode(new_state, parent=self, move=move, turn=next_turn, game_logic=self.game_logic)
            self.children.append(child)
            # Repeat recursively for any children
            child.generate_children()
        
    def board_str(self):
        return "\n".join("".join(row) for row in self.state)

class GameLogic:
    def check_winner(self, state):
        """Determine if there is a winner. To be overridden."""
        raise NotImplementedError
    
    def get_valid_moves(self, state, turn):
        """Return all valid moves for a given state and turn."""
        raise NotImplementedError
    
    def apply_move(self, state, move):
        """Apply a move to a state and return the new state."""
        raise NotImplementedError

    def next_turn(self, turn):
        """Return the next player's turn."""
        raise NotImplementedError
    
    def state_to_tuple(self, state):
        """Convert the game state to a tuple (for deduplication)."""
        raise NotImplementedError
