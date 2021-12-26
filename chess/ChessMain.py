"""
This is our main driver file. It will be responsible for handling our user input and displaying the current GameState
object.
"""

import pygame as p
from chess import ChessEngine

WIDTH = HEIGHT = 512  # 400 is another option for higher resolution
DIMENSION = 8  # Dimensions of a chessboard are 8x8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15  # for animation later on
IMAGES = {}

"""
Initialize a global dictionary of images. This will be called exactly once in the main
"""


def loadImages():
    pieces = ['B', 'Bb', 'Bk', 'Bn', 'Bq', 'Br', 'Pb', 'Ph', 'Pk', 'Pp', 'Pq', 'Pt']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))
    # Note: we can access an image by saying 'IMAGES['pP']'


"""
The main driver for our code. This will handle user input and updating the graphics
"""


def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False  # flag variable when move is made

    loadImages()  # only do this once, before the while loop
    running = True
    sqSelected = ()  # No square is selected, keep track of the click of the user (tuple: (row, col))
    playerClicks = []  # keep track of player clicks (two tuples: [(6, 4), (4, 4)])
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            # mouse handler
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()  # (x, y) location of the mouse
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                if sqSelected == (row, col):  # the user clicked the square twice
                    sqSelected = ()  # Deselect
                    playerClicks = []  # Clear player clicks
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected)  # append for both first and second place
                if len(playerClicks) == 2:  # After the second click
                     move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                     print(move.getChessNotation())
                     if move in validMoves:
                        gs.makeMove(move)
                        moveMade = True
                        sqSelected = ()  # reset user clicks
                        playerClicks = []
            # key handlers
            elif e.type == p.KEYDOWN:
                 if e.key == p.K_z:  # undo when 'z' is pressed
                    gs.undoMove()
                    moveMade = True

        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False

        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()


"""
Responsible for all the graphics within current game state. 
"""


def drawGameState(screen, gs):
    drawBoard(screen)  # draw squares on the board
    # add in piece highlighting or move suggestions (later)
    drawPieces(screen, gs.board)  # draw pieces on top of those squares


"""
Draw squares n the board. The top eft square is always light.  
"""


def drawBoard(screen):
    colors = [p.Color("light blue"), p.Color("light pink")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r + c) % 2)]
            p.draw.rect(screen, color, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


"""
draw the pieces on the board using the current GameState.board
"""


def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece == "--":  # not empty square
                continue
            screen.blit(IMAGES[piece], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


if __name__ == "__main__":
    main()