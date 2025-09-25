# Author: Anthony Sokry
# Updated: September 2025

from tkinter import *
from ChessGame import ChessGame



class ChessGUI:
    """
    Represents a graphical user interface for Fog of War chess game.
    Uses ChessGame class for game data.
    """
    def __init__(self, game):
        """
        Initializes graphical user interface.
        """
        self._game = game
        self._board_dict = {0: 'a', 100: 'b', 200: 'c', 300: 'd', 400: 'e', 500: 'f', 600: 'g', 700: 'h'}

        # Instantiate a window instance
        self._window_size_width = 800
        self._window_size_height = 800
        self._square_size = 100
        self._window = Tk() 
        self._window.geometry(f"{self._window_size_width}x{self._window_size_height}")
        self._window.config(background="gray")

        # Window title and icon
        self._window.title("Chess: Fog of War")
        icon = PhotoImage(file='assets/black_pieces/b_q.png')
        self._window.iconphoto(True, icon)

        # Pause variables
        self._text_duration = 2000 # In milliseconds
        self._pause = False

        # Canvas
        self._canvas = Canvas(self._window, width=self._window_size_width, height=self._window_size_height, bg="white")
        self._canvas.pack()

        # Board information
        self._board_width = 8
        self._board_height = 8
        self._total_squares = self._board_width * self._board_height
        self._brown_square = PhotoImage(file='assets/brown-square.png')
        self._light_brown_square = PhotoImage(file='assets/light-brown-square.png')
        self.create_board_gui()

        # Chess movement information
        self._img_to_move = None
        self._img_chess_pos = None
        self._hidden = PhotoImage(file='assets/hidden.png')

        # Chess pieces information
        self._total_pieces = 32
        b_rook = PhotoImage(file='assets/black_pieces/b_r.png')
        b_knight = PhotoImage(file='assets/black_pieces/b_n.png')
        b_bishop = PhotoImage(file='assets/black_pieces/b_b.png')
        b_queen = PhotoImage(file='assets/black_pieces/b_q.png')
        b_king = PhotoImage(file='assets/black_pieces/b_k.png')
        b_pawn = PhotoImage(file='assets/black_pieces/b_p.png')
        w_rook = PhotoImage(file='assets/white_pieces/w_r.png')
        w_knight = PhotoImage(file='assets/white_pieces/w_n.png')
        w_bishop = PhotoImage(file='assets/white_pieces/w_b.png')
        w_queen = PhotoImage(file='assets/white_pieces/w_q.png')
        w_king = PhotoImage(file='assets/white_pieces/w_k.png')
        w_pawn = PhotoImage(file='assets/white_pieces/w_p.png')
        self._b_piece_order = [b_rook, b_knight, b_bishop, b_queen, b_king, b_bishop, b_knight, b_rook]
        self._w_piece_order = [w_rook, w_knight, w_bishop, w_queen, w_king, w_bishop, w_knight, w_rook]
        self._pieces_dict = {
            'p': b_pawn, 'r': b_rook, 'n': b_knight, 'b': b_bishop, 'q': b_queen, 'k': b_king,
            'P': w_pawn, 'R': w_rook, 'N': w_knight, 'B': w_bishop, 'Q': w_queen, 'K': w_king
        }
        self.create_pieces_gui()

    def on_click_img(self, event):
        """
        On click event for chess piece images. Click on a valid chess 
        piece and then click on valid space to move to.
        """
        # Check if the game is over
        if self._game.is_game_over() or self._pause is True:
            return
        
        img_id = self._canvas.find_closest(event.x, event.y)
        # Check if an image id was found
        if img_id is not None:
            chess_pos = self.to_chess_pos(img_id)
            array_pos = self._game.location_to_list_pos(chess_pos)
        else:
            return

        if img_id[0] > self._total_squares:
            if self._img_to_move is None:
                # Save current piece image
                self._img_chess_pos = chess_pos
                piece = self._game.get_piece_at(array_pos)
                if self._game.is_valid_piece(array_pos, piece):
                    self._img_to_move = img_id[0]
                else:
                    self.clear_move_info()
                    self.display_text(f"Player Turn: {self._game.get_player_turn()}")
            else:
                # Capture target piece image
                if self._game.make_move(self._img_chess_pos, chess_pos):
                    self.move_img(self._img_to_move, img_id)
                    self.delete_canvas_item(img_id)
                    self.toggle_pieces()
                else:
                    self.display_text("Invalid Capture")
                self.clear_move_info()
        elif img_id[0] <= self._total_squares and self._img_to_move is not None:
            # Move piece image to blank square
            if self._game.make_move(self._img_chess_pos, chess_pos):
                self.move_img(self._img_to_move, img_id)
                self.toggle_pieces()
            else:
                self.display_text("Invalid Move")
            self.clear_move_info()

        # Re-check if game is over
        if self._game.is_game_over():
            self.display_text(f"{self._game.get_game_state()}", True)

    def to_chess_pos(self, img_id):
        """
        Converts image's position to chess position.
        """
        # Get image's coordinates
        x1, y1, x2, y2 = self._canvas.bbox(img_id)
        
        # Convert to chess coordinates
        x1 = self._board_dict[x1]
        y1 = self._board_height - int(str(y1)[0])
        pos = x1 + str(y1)

        return pos
    
    def move_img(self, img_to_move, pos_id):
        """
        Move given image to new position.
        """
        x1, y1, x2, y2 = self._canvas.bbox(pos_id)
        self._canvas.coords(img_to_move, x1, y1)
    
    def clear_move_info(self):
        """
        Sets move info variables back to None.
        """
        self._img_to_move = None
        self._img_chess_pos = None

    def create_board_gui(self):
        """
        Create chess board graphical user interface.
        """
        brown_square = self._brown_square
        light_brown_square = self._light_brown_square
        for row in range(self._board_height):
            for col in range(self._board_width):
                square_x = col * self._square_size
                square_y = row * self._square_size
                if row % 2 != 0: 
                    if col % 2 == 0:
                        # Squares at odd numbered rows with even numbered columns
                        img_id = self._canvas.create_image(square_x, square_y, image=brown_square, anchor=NW)
                    else:
                        # Squares at odd numbered rows with odd numbered columns
                        img_id = self._canvas.create_image(square_x, square_y, image=light_brown_square, anchor=NW)
                elif row % 2 == 0:
                    if col % 2 != 0:
                        # Squares at even numbered rows with odd numbered columns
                        img_id = self._canvas.create_image(square_x, square_y, image=brown_square, anchor=NW)
                    else: 
                        # Squares at even numbered rows with even numbered columns
                        img_id = self._canvas.create_image(square_x, square_y, image=light_brown_square, anchor=NW)
                
                # Bind square image to on-click event
                self._canvas.tag_bind(img_id, "<Button-1>", self.on_click_img)

    def create_pieces_gui(self):
        """
        Create chess piece graphical user interface.
        """
        for piece_num in range(self._total_pieces):
            piece_x = (piece_num % 8) * self._square_size
            if piece_num <= 7: 
                # Black pieces, that are not pawns
                piece = self._b_piece_order[piece_num]
                piece_y = 0 * self._square_size
                img_id = self._canvas.create_image(piece_x, piece_y, image=piece, anchor=NW)
            elif piece_num > 7 and piece_num <= 15: 
                # Black pawns
                piece_y = 1 * self._square_size
                img_id = self._canvas.create_image(piece_x, piece_y, image=self._pieces_dict['p'], anchor=NW)
            elif piece_num > 15 and piece_num <= 23: 
                # White pawns
                piece_y = 6 * self._square_size
                img_id = self._canvas.create_image(piece_x, piece_y, image=self._pieces_dict['P'], anchor=NW)
            elif piece_num > 23: 
                # White pieces, that are not pawns
                piece = self._w_piece_order[piece_num % 8]
                piece_y = 7 * self._square_size
                img_id = self._canvas.create_image(piece_x, piece_y, image=piece, anchor=NW)

            # Bind chess piece image to on-click event
            self._canvas.tag_bind(img_id, "<Button-1>", self.on_click_img)
        # Display player turn text
        self.display_text(f"Player Turn: {self._game.get_player_turn()}")
        # Hide opposing chess pieces
        # self.toggle_pieces()

    def display_text(self, text, persist=False):
        """
        Display given text on the window. If persist is true, text will 
        remain on window indefinitely.
        """
        # Pause game controls
        self._pause = True

        # Display text with background
        text_id = self._canvas.create_text(400, 400, text=text, fill="black", font=("Arial", 24, "bold"))
        bbox = self._canvas.bbox(text_id)
        bg_id = self._canvas.create_rectangle(bbox, fill="white", outline="")
        self._canvas.tag_lower(bg_id, text_id)

        if persist is False:
            # Delete text after some time
            self._window.after(self._text_duration, self.delete_canvas_item, text_id)
            self._window.after(self._text_duration, self.delete_canvas_item, bg_id)

            # Un-pause after some time
            self._window.after(self._text_duration, self.toggle_pause, self._pause)

    def delete_canvas_item(self, item_id):
        """
        Delete canvas given item, i.e., images and text.
        """
        self._canvas.delete(item_id)

    def toggle_pause(self, value):
        """
        Toggle pause.
        """
        self._pause = value is False

    def toggle_pieces(self):
        """
        Hide or reveal chess pieces based on player turn.
        """
        # Get game board
        if self._game.get_game_state() == "UNFINISHED":
            perspective = self._game.get_player_turn()
        else:
            perspective = "all"
        board = self._game.get_board(perspective)
        hidden_icon = self._game.get_hidden_icon()

        # Iterate through each square on board
        for row in range(len(board)):
            for col in range(len(board[0])):
                img_id = self._canvas.find_closest((col * 100) + 50, (row * 100) + 50)
                if img_id is not None:
                    if img_id[0] > self._total_squares:
                        if board[row][col] == hidden_icon:
                            # Hide chess piece
                            self._canvas.itemconfig(img_id, image=self._hidden)
                        elif board[row][col] in self._pieces_dict.keys():
                            # Reveal chess piece
                            letter = board[row][col]
                            chess_img = self._pieces_dict[letter]
                            self._canvas.itemconfig(img_id, image=chess_img)

    def loop(self):
        """
        Place window on computer screen and listens for events.
        """
        self._window.mainloop()

# Run Code
game = ChessGame()
gui = ChessGUI(game)
gui.loop()