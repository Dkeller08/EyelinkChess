import pygame
import Board
import Pieces
import numpy as np

# initialize pygame
pygame.init()

# Title and Icon
pygame.display.set_caption("EyeChess")
icon = pygame.image.load("../Images/Logo.png")
pygame.display.set_icon(icon)
screen = pygame.display.set_mode((600, 600))

# Get board
squares = np.full((8, 8), Board.Square(0, 0, screen, None, False))
for i in range(8):
    for j in range(8):
        piece = Pieces.starting_position(i, j)
        squares[i][j] = Board.Square(i, j, screen, piece, False)
# Set some constants
squarex, squarey = 0, 0
h, w = screen.get_height(), screen.get_width()
Castle = False

# Game Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse2x, mouse2y = pygame.mouse.get_pos()
            movex = int(8 * mouse2x / w)
            movey = int(8 * (h - mouse2y) / h)
            if squares[squarex][squarey].piece is not None and squares[movex][movey].possibleMove and (
                    squares[movex][movey].piece is None or
                    squares[movex][movey].piece.player is not squares[squarex][squarey].piece.player) \
                    and ((isinstance(squares[squarex][squarey].piece, Pieces.Pawn) and (squares[movex][
                                                                                            movey].piece is None or(
                                                                                                abs(movex - squarex) == 1 and abs(
                                                                                            movey - squarey) == 1))) or not isinstance(
                squares[squarex][squarey].piece, Pieces.Pawn)):
                squares[movex][movey] = Board.Square(movex, movey, screen, squares[squarex][squarey].piece, False)
                squares[movex][movey].piece.update(movex, movey)
                squares[squarex][squarey] = Board.Square(squarex, squarey, screen, None, False)
                # Castleing
                if isinstance(squares[movex][movey].piece, Pieces.King) and movex == 6 and movey == 0 and Castle:
                    squares[5][0] = Board.Square(5, 0, screen, squares[7][0].piece, False)
                    squares[5][0].piece.update(5, 0)
                    squares[7][0] = Board.Square(7, 0, screen, None, False)
                if isinstance(squares[movex][movey].piece, Pieces.King) and movex == 2 and movey == 0 and Castle:
                    squares[3][0] = Board.Square(5, 0, screen, squares[0][0].piece, False)
                    squares[3][0].piece.update(3, 0)
                    squares[0][0] = Board.Square(0, 0, screen, None, False)
                if isinstance(squares[movex][movey].piece, Pieces.King) and movex == 2 and movey == 7 and Castle:
                    squares[3][7] = Board.Square(5, 7, screen, squares[0][7].piece, False)
                    squares[3][7].piece.update(3, 7)
                    squares[0][7] = Board.Square(0, 7, screen, None, False)
                if isinstance(squares[movex][movey].piece, Pieces.King) and movex == 6 and movey == 7 and Castle:
                    squares[5][7] = Board.Square(5, 7, screen, squares[7][7].piece, False)
                    squares[5][7].piece.update(5, 7)
                    squares[7][7] = Board.Square(7, 7, screen, None, False)
            squares[squarex][squarey] = Board.Square(squarex, squarey, screen, squares[squarex][squarey].piece, False)
            mousex, mousey = pygame.mouse.get_pos()
            squarex = int(8 * mousex / w)
            squarey = int(8 * (h - mousey) / h)
            Castle = False
            for i in range(8):
                for j in range(8):

                    if squares[squarex][squarey].piece is not None:
                        squares[i][j] = Board.Square(i, j, screen, squares[i][j].piece, False)
                        if squares[squarex][squarey].piece.board[i][j]:
                            squares[i][j] = Board.Square(i, j, screen, squares[i][j].piece, True)
                        # Castleing
                        if isinstance(squares[squarex][squarey].piece, Pieces.King) and squares[squarex][
                            squarey].piece.player == "white" \
                                and squares[5][0].piece is None and squares[6][0].piece is None and isinstance(
                            squares[7][0].piece, Pieces.Rook) \
                                and squares[squarex][squarey].piece.move > 0 and squares[7][0].piece.move > 0:
                            squares[6][0] = Board.Square(6, 0, screen, None, True)
                            Castle = True
                        if isinstance(squares[squarex][squarey].piece, Pieces.King) and squares[squarex][
                            squarey].piece.player == "white" \
                                and squares[3][0].piece is None and squares[2][0].piece is None and squares[1][
                            0].piece is None and isinstance(
                            squares[0][0].piece, Pieces.Rook) \
                                and squares[squarex][squarey].piece.move > 0 and squares[0][0].piece.move > 0:
                            squares[2][0] = Board.Square(2, 0, screen, None, True)
                            Castle = True
                        if isinstance(squares[squarex][squarey].piece, Pieces.King) and squares[squarex][
                            squarey].piece.player == "black" \
                                and squares[3][7].piece is None and squares[2][7].piece is None and squares[1][
                            7].piece is None and isinstance(
                            squares[0][7].piece, Pieces.Rook) \
                                and squares[squarex][squarey].piece.move > 0 and squares[0][7].piece.move > 0:
                            squares[2][7] = Board.Square(2, 7, screen, None, True)
                            Castle = True
                        if isinstance(squares[squarex][squarey].piece, Pieces.King) and squares[squarex][
                            squarey].piece.player == "black" \
                                and squares[5][7].piece is None and squares[6][7].piece is None and isinstance(
                            squares[7][7].piece, Pieces.Rook) \
                                and squares[squarex][squarey].piece.move > 0 and squares[7][7].piece.move > 0:
                            squares[6][7] = Board.Square(6, 7, screen, None, True)
                            Castle = True
                        # Pawn attack
                        if isinstance(squares[squarex][squarey].piece, Pieces.Pawn) and squares[squarex][
                            squarey].piece.player == "white" \
                                and abs(i - squarex) == 1 and j - squarey == 1\
                                and squares[i][j].piece is not None:
                            squares[i][j] = Board.Square(i, j, screen, squares[i][j].piece, True)
                        if isinstance(squares[squarex][squarey].piece, Pieces.Pawn) and squares[squarex][
                            squarey].piece.player == "black" \
                                and abs(i - squarex) == 1 and j - squarey == -1\
                                and squares[i][j].piece is not None:
                            squares[i][j] = Board.Square(i, j, screen, squares[i][j].piece, True)
                    else:
                        squares[i][j] = Board.Square(i, j, screen, squares[i][j].piece, False)
            squares[squarex][squarey] = Board.Square(squarex, squarey, screen, squares[squarex][squarey].piece, True)

        if event.type == pygame.QUIT:
            running = False

    for i in range(8):
        for j in range(8):
            screen.blit(squares[i][j].image, (int(squares[i][j].x), int(squares[i][j].y)))
            piece = squares[i][j].piece
            if piece is not None:
                image_piece = pygame.transform.scale(piece.image, (int(w / 8), int(h / 8)))
                screen.blit(image_piece, (int(squares[i][j].x), int(squares[i][j].y)))

    pygame.display.update()
