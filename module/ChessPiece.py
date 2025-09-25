# Author: Anthony Sokry
# Updated: September 2025

class ChessPiece:
    """
    Represents a chess piece in a chess game.
    All chess pieces move and capture in the same
    direction, excluding the pawn which captures
    differently from where it can move to.
    """
    def __init__(self, color, name, capture_dist):
        """
        Takes a color, a name, and list of capture distances as parameters.
        Initializes the chess piece with the color, name, and capture distance list.
        """
        # Check if color is neither black nor white
        if color != "blk" and color != "wh":
            raise InvalidChessColorError

        # Update the casing of the name based on the given color
        if color == "blk":
            self._color = "black"
            self._full_name = name
        elif color == "wh":
            self._color = "white"
            self._full_name = name.upper()
        self._name = self._full_name[0]

        # Set list of capture distances
        self._capture_dist = capture_dist

    def get_color(self):
        """
        Returns the color of the piece.
        """
        return self._color

    def get_ful_name(self):
        """
        Returns the full name of the piece.
        """
        return self._full_name

    def get_name(self):
        """
        Returns the name of the piece.
        """
        return self._name

    def get_capture_dist(self):
        """
        Returns the list of capture distance.
        """
        return self._capture_dist

    def is_valid_distance(self, dist):
        """
        Takes a distance as a parameter.
        Returns true if the given distance is within capture distance.
        """
        for dist_vals in self._capture_dist.values():
            if dist in dist_vals:
                return True
        return False


class Pawn(ChessPiece):
    """
    Represents a pawn chess piece.
    """
    def __init__(self, color):
        """
        Takes a color as a parameter.
        Initializes the pawn chess piece with specific
        capture distances and move distances.
        """
        self._capture_dist = ()
        # Assign appropriate data members based on color
        if color == "blk":  # If black pawn
            self._capture_dist = {"all_down": ((-1, 1), (-1, -1))}
            self._first_move_dist = {"down": ((-1, 0), (-2, 0))}
            self._move_dist = {"down": ((-1, 0), )}
        elif color == "wh":  # If white pawn
            self._capture_dist = {"all_up": ((1, -1), (1, 1))}
            self._first_move_dist = {"up": ((1, 0), (2, 0))}
            self._move_dist = {"up": ((1, 0),)}

        # Invoke parent init method with name 'pawn', color, and capture distance list
        super().__init__(color, 'pawn', self._capture_dist)

        # Set first_move to True to track if pawn is moving for the first time
        self._first_move = True

    def is_first_move(self):
        """
        Returns true if this is the pawn's first move.
        """
        return self._first_move

    def disable_first_move(self):
        """
        Disables the first move boolean.
        """
        self._first_move = False

    def is_valid_distance(self, dist, capture=True):
        """
        If capture is True, checks if the given distance
        is within pawn's capture distance. Otherwise,
        checks if the distance is within pawn's move distance.
        """
        dist_values = self._move_dist.values()
        if capture is True:
            dist_values = self._capture_dist.values()
        elif self._first_move is True:
            dist_values = self._first_move_dist.values()
        for vals in dist_values:
            if dist in vals:
                return True
        return False


class Rook(ChessPiece):
    """
    Represents a rook chess piece.
    """
    def __init__(self, color):
        """
        Takes a color as a parameter.
        Initializes the rook chess piece with specific capture distances.
        """
        self._capture_dist = {"left": ((0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7)),
                              "up": ((1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0)),
                              "right": ((0, -1), (0, -2), (0, -3), (0, -4), (0, -5), (0, -6), (0, -7)),
                              "down": ((-1, 0), (-2, 0), (-3, 0), (-4, 0), (-5, 0), (-6, 0), (-7, 0))}

        # Invoke parent init method with name 'rook', color, and capture distance list
        super().__init__(color, 'rook', self._capture_dist)


class Knight(ChessPiece):
    """
    Represents a knight chess piece
    """
    def __init__(self, color):
        """
        Takes a color as a parameter.
        Initializes the knight chess piece with specific capture distances.
        """
        self._capture_dist = {"all": ((1, 2), (2, 1), (2, -1), (1, -2),
                              (-1, -2), (-2, -1), (-2, 1), (-1, 2))}

        # Invoke parent init method with name 'night', color, and capture distance list
        super().__init__(color, 'night', self._capture_dist)
        # Use 'night' instead of 'knight' since Knight piece's name can't be 'k'
        # The King piece's name will be 'k'


class Bishop(ChessPiece):
    """
    Represents a bishop chess piece
    """
    def __init__(self, color):
        """
        Takes a color as a parameter.
        Initializes the bishop chess piece with specific capture distances.
        """
        self._capture_dist = {"up_left": ((1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7)),
                              "down_right": ((-1, -1), (-2, -2), (-3, -3), (-4, -4), (-5, -5), (-6, -6), (-7, -7)),
                              "up_right": ((1, -1), (2, -2), (3, -3), (4, -4), (5, -5), (6, -6), (7, -7)),
                              "down_left": ((-1, 1), (-2, 2), (-3, 3), (-4, 4), (-5, 5), (-6, 6), (-7, 7))}

        # Invoke parent init method with name 'bishop', color, and capture distance list
        super().__init__(color, 'bishop', self._capture_dist)


class Queen(ChessPiece):
    """
    Represents a queen chess piece
    """
    def __init__(self, color):
        """
        Takes a color as a parameter.
        Initializes the queen chess piece with specific capture distances.
        """
        self._capture_dist = {"left": ((0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7)),
                              "up": ((1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0)),
                              "right": ((0, -1), (0, -2), (0, -3), (0, -4), (0, -5), (0, -6), (0, -7)),
                              "down": ((-1, 0), (-2, 0), (-3, 0), (-4, 0), (-5, 0), (-6, 0), (-7, 0)),
                              "up_left": ((1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7)),
                              "down_right": ((-1, -1), (-2, -2), (-3, -3), (-4, -4), (-5, -5), (-6, -6), (-7, -7)),
                              "up_right": ((1, -1), (2, -2), (3, -3), (4, -4), (5, -5), (6, -6), (7, -7)),
                              "down_left": ((-1, 1), (-2, 2), (-3, 3), (-4, 4), (-5, 5), (-6, 6), (-7, 7))}

        # Invoke parent init method with name 'queen', color, and capture distance list
        super().__init__(color, 'queen', self._capture_dist)


class King(ChessPiece):
    """
    Represents a king chess piece
    """
    def __init__(self, color):
        """
        Takes a color as a parameter.
        Initializes the king chess piece with specific capture distances.
        """
        self._capture_dist = {"all": ((0, 1), (1, 0), (1, 1), (-1, 1),
                              (0, -1), (-1, 0), (-1, -1), (1, -1))}

        # Invoke parent init method with name 'king', color, and capture distance list
        super().__init__(color, 'king', self._capture_dist)


class InvalidChessColorError(Exception):
    """
    Exception for invalid chess color.
    Chess piece color must be black or white.
    """
    pass
