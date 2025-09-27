# Author: Anthony Sokry
# Updated: September 2025

from module.ChessPiece import *



class ChessGame:
    """
    Represents a Fog of War chess game. Uses ChessPiece class 
    for chess pieces' data. White starts first.
    """

    def __init__(self):
        """
        Initializes chess game with standard chess setup.
        Using ChessPiece class to represent individual chess pieces.
        White pieces are represent by "wh".
        Black pieces are represent by "blk".
        Game state starts as "UNFINISHED"
        Player turn is set to "white" since white is going first.
        Letter map is used to help convert board location to list position.
        Use visible_piece_pos to keep track of visible pieces.
        """
        self._board = [
            [Rook("blk"), Knight("blk"), Bishop("blk"), Queen("blk"), King("blk"), Bishop("blk"), Knight("blk"), Rook("blk")],
            [Pawn("blk"), Pawn("blk"), Pawn("blk"), Pawn("blk"), Pawn("blk"), Pawn("blk"), Pawn("blk"), Pawn("blk")],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [Pawn("wh"), Pawn("wh"), Pawn("wh"), Pawn("wh"), Pawn("wh"), Pawn("wh"), Pawn("wh"), Pawn("wh")],
            [Rook("wh"), Knight("wh"), Bishop("wh"), Queen("wh"), King("wh"), Bishop("wh"), Knight("wh"), Rook("wh")]]

        self._letter_map = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
        self._game_state = "UNFINISHED"
        self._player_turn = "white"
        self._hidden_icon = '?'
        self._visible_piece_pos = []
        self._exit_word = "end"

    def get_game_state(self):
        """
        Returns the current game state
        """
        return self._game_state

    def is_game_over(self):
        """
        Returns true if the game is over, false otherwise
        """
        if self._game_state != "UNFINISHED":
            print("Game is over. " + self._game_state)
        return self._game_state != "UNFINISHED"

    def is_king_captured(self, pos):
        """
        Takes a position as parameter. Returns true if a king was captured
        at the position is captured. If true, update game state to who has won
        """
        if self.is_valid_position(pos):
            piece = self.get_piece_at(pos)
            if type(piece) is King and self._game_state == "UNFINISHED":
                if piece.get_color() == "white":
                    self._game_state = "BLACK_WON"
                elif piece.get_color() == "black":
                    self._game_state = "WHITE_WON"
                print(self._game_state)
                return True
        return False

    def switch_turn(self):
        """
        Changes the player turn
        """
        if self._game_state == "UNFINISHED":
            if self._player_turn == "white":
                self._player_turn = "black"
            else:
                self._player_turn = "white"

    def get_player_turn(self):
        """
        Returns the current player turn
        """
        return self._player_turn

    def get_board(self, perspective):
        """
        Takes a perspective as a parameter.
        Returns the game board as a 2d list of strings,
        displaying the board from the indicated perspective.
        Uses data member visible_piece_pos to reveal any
        pieces that are within capture distance of another piece.
        """
        # Check if perspective is valid
        valid_perspectives = ["all", "white", "black"]
        perspective = perspective.lower()
        if perspective not in valid_perspectives:
            print("Invalid perspective")
            return None

        # Make a copy of current board
        board_copy = [arr[:] for arr in self._board]
        # Loop through all positions on board
        row, col = 0, 0
        while row < len(self._board):
            piece = self._board[row][col]  # Get piece at list position
            is_all = perspective == "all"  # Check if perspective is all
            is_visible = (row, col) in self._visible_piece_pos  # Check if piece pos is visible
            if type(piece) is not str:  # Check piece is not empty
                is_same_color = perspective == piece.get_color()  # Check if piece is same color as perspective
                if is_same_color or is_all or is_visible:
                    board_copy[row][col] = piece.get_name()  # Assign piece's string name to board copy
                else:
                    board_copy[row][col] = self._hidden_icon  # Hide piece's name and assign to board copy

            # Increment to next board position
            col += 1
            if col > len(self._board) - 1:
                col = 0
                row += 1

        return board_copy

    def print_board(self, perspective):
        """
        Takes a perspective as a parameter.
        Prints the board with a line break after each row.
        """
        for section in self.get_board(perspective):
            print(section)
        print('')

    def get_hidden_icon(self):
        """
        Returns icon used for hidden pieces.
        """
        return self._hidden_icon

    def make_move(self, move_from, move_to):
        """
        Takes two board locations as parameters.
        Move a piece on the board from first position to second position.
        """
        # Check if the game is over
        if self.is_game_over():
            return False

        # Check if board locations are valid
        func = self.is_valid_location
        if func(move_from) is False or func(move_to) is False:
            print("Invalid board locations")
            return False

        # Convert locations to list positions
        piece_pos = self.location_to_list_pos(move_from)
        target_pos = self.location_to_list_pos(move_to)
        piece = self.get_piece_at(piece_pos)

        # Check if the positions are on the board
        func = self.is_valid_position
        if func(piece_pos) is False or func(target_pos) is False:
            print("Position is out of bounds")
            return False

        # Check if piece is a valid piece
        if self.is_valid_piece(piece_pos, piece) is False:
            return False

        # Check if piece can move to target_pos
        if self.is_valid_move(piece, piece_pos, target_pos) is False:
            return False

        # If Pawn is moving for the first time, disable first_move boolean
        if type(piece) is Pawn:
            if piece.is_first_move():
                piece.disable_first_move()

        piece_name = piece.get_ful_name()
        print(f'{piece_name} {move_from} to {move_to}')

        # Check if a King was captured
        if self.is_king_captured(target_pos) is False:
            # Switch player turns if a king was not captured
            self.switch_turn()

        # Update piece's position on board
        self.update_board(piece, piece_pos, target_pos)

        # Keep track of any visible pieces
        self.update_visible_pieces()

        return True

    def get_piece_at(self, pos):
        """
        Takes a list position as a parameter.
        Returns the chess piece at the given position.
        """
        return self._board[pos[0]][pos[1]]

    def set_piece_at(self, pos, piece):
        """
        Takes a list position and a chess piece as parameters.
        Sets the chess piece at the given position.
        """
        self._board[pos[0]][pos[1]] = piece

    def location_to_list_pos(self, location):
        """
        Takes a chess board location as a parameter.
        Converts the chess board location to a 2d list position
        Example: 'b2' -> [6][1]
        """
        location = location.lower()
        row = len(self._board) - int(location[1])
        col = self._letter_map[location[0]]
        return row, col

    def is_valid_location(self, location):
        """
        Takes a board location as a parameter.
        Returns true if board location is only two characters
        and starts with a board letter and ends with a number.
        """
        location = location.lower()
        is_two_chars = len(location) == 2  # Check if location is only two characters
        board_letters = self._letter_map.keys()

        # Check if location starts with a board letter and ends with a number
        first_char_is_letter = location[0] in board_letters
        second_char_is_int = location[1].isnumeric()

        return is_two_chars and first_char_is_letter and second_char_is_int

    def is_valid_position(self, pos):
        """
        Takes a list position as parameter.
        Returns true if the position is within the board.
        """
        col_len = row_len = len(self._board)
        return 0 <= pos[0] < row_len and 0 <= pos[1] < col_len

    def is_valid_piece(self, piece_pos, piece):
        """
        Takes a position and chess piece as a parameter.
        Returns true if the piece exists at the given position
        and belongs to the current player.
        """
        if type(piece) is str:
            print("Piece does not exist at " + piece_pos)
            return False
        if piece.get_color() != self._player_turn:
            print("Piece does not belong to current Player")
            return False
        return True

    def is_valid_move(self, piece, piece_pos, target_pos, is_print=True):
        """
        Takes a piece and two positions as parameters.
        Returns true if the piece is able to move to target position
        """
        # Check if piece is trying to move in place
        if piece_pos == target_pos:
            if is_print: print("Piece cannot move in place")
            return False

        # Check if there is an ally at target_pos
        target_piece = self.get_piece_at(target_pos)
        if type(target_piece) is not str:
            if piece.get_color() == target_piece.get_color():
                if is_print: print("Cannot capture pieces of the same color")
                return False

        # Get the col and row distance from piece_pos to target_pos
        col_dist = piece_pos[1] - target_pos[1]
        row_dist = piece_pos[0] - target_pos[0]
        # Assign col and row distance to its own variable
        dist = (row_dist, col_dist)

        # If col and row distance is not 0,
        # convert col and row distance to incremental
        # variable of 1 while keeping its sign
        if col_dist != 0:
            col_dist = int(col_dist / abs(col_dist))
        if row_dist != 0:
            row_dist = int(row_dist / abs(row_dist))

        # Set path position to be one square before target pos
        path_pos = (target_pos[0] + row_dist, target_pos[1] + col_dist)

        # Check if piece is a Pawn and if Pawn is
        # capturing or moving. Pawn captures by default.
        if type(piece) is Pawn and col_dist == 0:  # If Pawn is moving and not capturing...
            # Assign if distance is within Pawn's move distance
            valid_dist = piece.is_valid_distance(dist, False)
            # If so, Update path to include target piece as an obstacle
            path_pos = (target_pos[0], target_pos[1])
        elif type(piece) is Pawn and type(target_piece) is str:  # Check if Pawn is capturing empty space
            if is_print: print("Pawn cannot capture empty space")
            return False
        else:
            # Assign if distance is within piece's capture distance
            valid_dist = piece.is_valid_distance(dist)

        # Check if piece can move to target_pos
        if valid_dist is False:
            if print: print("Piece cannot move to target position")
            return False

        # If piece is Knight, exit out of method.
        # Since Knight can jump over pieces.
        if type(piece) is Knight:
            return True

        # Check if there is an obstacle in the path towards the target
        while piece_pos != path_pos:
            obstacle = self.get_piece_at(path_pos)
            if type(obstacle) is not str:
                if is_print: print("There is an obstacle in the way")
                return False
            # Increment position to get closer to piece position
            path_pos = (path_pos[0] + row_dist, path_pos[1] + col_dist)
        return True

    def update_board(self, piece, piece_pos, target_pos):
        """
        Takes a piece and two list positions as parameters.
        Updates the board by moving the piece from piece_pos to target_pos.
        """
        self.set_piece_at(target_pos, piece)
        self.set_piece_at(piece_pos, ' ')

    def update_visible_pieces(self):
        """
        Add any position of pieces that are within
        capture distance of any other piece to list
        of visible pieces. List of visible pieces will
        be used to expose specific pieces on board
        when get_board method is called.
        """
        # Reset list of visible piece positions
        self._visible_piece_pos.clear()
        # Loop through entire board positions
        list_row, list_col = 0, 0
        col_len = row_len = len(self._board[0])
        while list_row < row_len:
            piece_pos = list_row, list_col
            piece = self.get_piece_at(piece_pos)
            if type(piece) is not str:  # Check chess piece is not empty
                # Get list of capture distances of piece
                capture_dist = piece.get_capture_dist()
                # Loop through each of the piece's distance values
                for dist_vals in capture_dist.values():
                    for dist in dist_vals:
                        # Get the target position relative to piece's current position
                        target_col = piece_pos[1] - dist[1]
                        target_row = piece_pos[0] - dist[0]
                        target_pos = target_row, target_col
                        # Check if target position is within the board
                        if self.is_valid_position(target_pos):
                            target = self.get_piece_at(target_pos)
                            # Check if target is not empty and is an enemy
                            if type(target) is not str and target.get_color() != piece.get_color():
                                # Check if piece can potentially capture target
                                if self.is_valid_move(piece, piece_pos, target_pos, False):
                                    # Check if target position is not in list of visible piece positions
                                    if target_pos not in self._visible_piece_pos:
                                        # Add target position to list of visible piece positions
                                        self._visible_piece_pos.append(target_pos)
            # Increment to next board position
            list_col += 1
            if list_col > col_len - 1:
                list_col = 0
                list_row += 1

    def play_terminal(self):
        """
        Starts chess game in terminal. Player inputs two standard chess 
        locations separated by a comma. Then switches to the next 
        player's turn. 
        Example: d2, d4
        """
        print("")
        player = self._player_turn
        print("<--- " + self.get_player_turn().upper() + " Turn" + " --->")
        self.print_board(player)
        print("Enter two chess locations separated by a comma (d2, d4).")
        
        # Loop chess game
        while self._game_state == "UNFINISHED":
            # Get player input
            player_input = input(self.get_player_turn().upper() + " Enter 2 locations: ").strip()
            if self.exit_play(player_input) is True:
                break

            # Separate locations
            locations = player_input.split(", ")
            if len(locations) != 2:
                print("Invalid Input, try inputting two chess locations separated by a comma.")
                print("Example: d2, d4")
                print("")
                continue

            # Get first location
            move_from = locations[0]
            if self.exit_play(move_from) is True:
                break

            # Get second location
            move_to = locations[1]
            if self.exit_play(move_to) is True:
                break

            # Attempt to make move
            move = self.make_move(move_from, move_to)
            if move is True:
                print("")
                print("<--- " + self.get_player_turn().upper() + " Turn" + " --->")
                self.print_board(self._player_turn)
    
    def exit_play(self, word):
        """
        Return true if given word is the exit word. 
        Ends the game if true.
        """
        if word == self._exit_word:
            self._game_state = "FINISHED"
            self.print_board("all")
            return True
        
        return False


# Run Code
if __name__ == "__main__":
    game = ChessGame()
    game.play_terminal()
