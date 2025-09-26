# Chess: Fog of War

## Description

A local two player fog of war chess game built with python. Pieces move and capture the same way as in standard chess, but there are **no checks, checkmates, castling, en passant, or pawn promotion**. Players are not informed if their king is in check, and both staying in check or moving into check are legal moves. 

Each player will see a different version of the board, where they can only view their **own pieces** and **opposing pieces that can be captured**. The rest of the opponent's pieces are hidden. Hidden pieces are clearly indicated to avoid confusion with visible empty squares. 

The game ends when a player's king is captured by the opposing player.

**Requirements:**
* Two Players
* One Computer
* Python

## Instructions

* Install Python[https://www.python.org/downloads/](https://www.python.org/downloads/)
* Add Python to <code>Path</code>
* Run one of the following files:
    * ChessGUI.py (recommended)
    * ChessGame.py

## How To Play ChessGUI

Click on a chess piece and then click on a valid space that the piece can move to. After a successful move has been made, the respective player's pieces will become hidden and the opposing pieces will be revealed before switching turns to the opposing player.

## How To Play ChessGame

After the game launches in terminal, the player will be prompted to enter two chess locations separated by a comma. Locations must be legal chess coordinates, i.e., a letter (a-h) for the column and a number (1-8) for the row. The piece at the first location will be moved to the second location if possible. For example, entering "d2, d4" will move the piece at d2 to d4.

After each move and before switching turns, a board pertaining to the current player's view will be printed onto the terminal as a 2d array. Lowercase letters represent black pieces, uppercase letters represent white pieces, empty spaces are shown as ' ', and hidden pieces are shown as '?'. 