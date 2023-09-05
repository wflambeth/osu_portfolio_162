# Will Lambeth
# 26 November 2021
# This program defines a playable implementation of the board game Hasami Shogi. 

class HasamiShogiGame:
    """This standalone class contains representations of the players, pieces, and game status, 
    along with methods to play and examine a game. 
    """
    def __init__(self):
        """Initializes a new game with Black and Red pieces in their starting positions. 
        """
        self._active = {'player': 'BLACK', 'pieces': {(9,x) for x in range(1,10)}}
        self._inactive = {'player': 'RED', 'pieces': {(1,x) for x in range(1,10)}}
        self._game_state = 'UNFINISHED'
    
    def format_from_external(self, square):
        """Takes a user-input "algebraic" coordinate string, and returns a pair of numeric 
        coordinates for internal storage and manipulation. 
        """
        return ((ord(square[0]) - 96), int(square[1]))

    def get_game_state(self):
        """Returns a string conveying the current victory status of the game - unfinished 
        or a black or red victory. 
        """
        return self._game_state

    def get_active_player(self):
        """Returns a string conveying the player currently moving or eligible to move. 
        """
        return self._active['player']

    def get_num_captured_pieces(self, color):
        """Takes a color as a string argument, and returns the total pieces of that color
        which have been captured and removed from the board, as an int. 
        """
        if self._active['player'] == color:
            return 9 - len(self._active['pieces'])
        elif self._inactive['player'] == color:
            return 9 - len(self._inactive['pieces'])

    def get_square_occupant(self, input_square):
        """Takes an algebraic string coordinate of a game square, and returns the color 
        of piece currently occupying it as a string (or 'NONE' if unoccupied).
        """
        square = self.format_from_external(input_square)
        if square in self._active['pieces']:
            return self._active['player']
        elif square in self._inactive['pieces']:
            return self._inactive['player']
        else:
            return 'NONE'
    
    def make_move(self, origin, destination):
        """Takes an origin and destination square in algebraic string notation, and 
        manages the process of validating and executing the move, performing any
        captures, and updating the active player and game state. Returns True if move is 
        valid/completed and False otherwise. 
        """
        if self._game_state != 'UNFINISHED':
            return False # moves cannot be made once game is won

        orig_square = self.format_from_external(origin)
        dest_square = self.format_from_external(destination)

        valid_move = self.move_piece(orig_square, dest_square)
        if not valid_move:
            return False
        
        # checks for captures in all four directions surrounding the square moved to. 
        for direction in ([0,-1], [0,1], [-1,0], [1,0]):
            self.perform_captures(dest_square, direction)
        
        if len(self._inactive['pieces']) <= 1:
            self._game_state = self._active['player'] + '_WON'

        # swaps active and inactive properties to reflect change of turn
        self._active, self._inactive = self._inactive, self._active
        return True
    
    def move_piece(self, orig_square, dest_square):
        """Helper function that is passed the origin and destination squares for a move,
        and validates move against existing state of board. Move is completed if valid. 
        """
        # check for active piece in starting location
        if orig_square not in self._active['pieces']:
            return False

        # determine axis (vertical/horizontal) and direction (+/-) of move
        if orig_square[0] == dest_square[0]:
            axis = 1
        elif orig_square[1] == dest_square[1]:
            axis = 0
        else:
            return False # space cannot be reached with legal move
        direction = 1 if dest_square[axis] > orig_square[axis] else -1

        # iterates over squares between piece and destination, terminating if move invalid.
        for x in range(orig_square[axis] + direction, dest_square[axis] + direction, direction):
            if x > 9 or x < 1:
                return False # out of bounds
            current_square = (orig_square[0], x) if axis == 1 else (x, orig_square[1])
            if current_square in self._active['pieces'] | self._inactive['pieces']:
                return False # square occupied
        
        # valid move, update positions
        self._active['pieces'].remove(orig_square)
        self._active['pieces'].add(dest_square)
        return True
    
    def perform_captures(self, square, direction, to_capture=None):
        """Recursive helper function that checks given direction out from a 
        newly-moved piece for potential captures. Takes a given square, a direction
        to iterate in, and (optionally) a set of possible captures identified
        in the current recursive call. No return value."""
        # Set of potential captures passed to subsequent iterations
        if to_capture == None:
            to_capture = set()

        # calls special capture logic if corner is directly adjacent & holds opposing piece
        if (len(to_capture) == 1) and square in ((1,1), (1,9), (9,1), (9,9)):
            self.perform_corner_capture(square)
            return # aborts check for this direction, next square will be out-of-bounds
        
        # checks next square along this direction
        next_square = (square[0] + direction[0], square[1] + direction[1])
        # if opposing piece: add to potential captures and call next iteration
        if next_square in self._inactive['pieces']:
            to_capture.add(next_square)
            self.perform_captures(next_square, direction, to_capture)
        # if friendly piece: any opponents between it and the moved piece are captured    
        elif next_square in self._active['pieces'] and len(to_capture) > 0: 
            self._inactive['pieces'] -= to_capture
        # if empty space or out of bounds, recursion terminates without action
    
    def perform_corner_capture(self, corner_square):
        """Helper function called when a piece is moved adjancent to an opponent-occupied corner. 
        Takes the corner square's coordinates and returns no value.
        """
        # Each corner has exactly two valid adjacent spaces
        count = 0
        for direction in ([0,-1], [0,1], [-1,0], [1,0]):
            if (corner_square[0] + direction[0], corner_square[1] + direction[1]) in self._active['pieces']:
                count += 1
        # If both are occupied by opponent, corner piece is captured
        if count == 2:
            self._inactive['pieces'].remove(corner_square)