# Driver file

import pygame as p
import engine 

WIDTH = HEIGHT = 512

DIMENTION = 8

SQ_SIZE = HEIGHT // DIMENTION

MAX_FPS = 15
IMAGES = {}

def loadImages():
    pieces = ["wp", "bp", "wR", "bR","wN", "bN", "wB", "bB", "wQ", "bQ", "wK", "bK"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))
        
    
def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = engine.GameState()
    validMovesList = gs.validMoves()
    print(validMovesList)
    moveMade = False  #flag  var 
    animate = False
    loadImages()
    running = True
    sqSelected = () #last click: tuple
    playerClicks = [] #two tuples
    gameOver = False
    
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver:
                    location = p.mouse.get_pos()
                    col = location[0]//SQ_SIZE
                    row = location[1]//SQ_SIZE
                    
                    if sqSelected == (row, col): #the user clicked the same square
                        sqSelected = () 
                        playerClicks = []
                    else:
                        sqSelected = (row, col)
                        playerClicks.append(sqSelected)
                    if len(playerClicks) == 2:
                        move = engine.Move(playerClicks[0], playerClicks[1], gs.board)
                        for i in range(len(validMovesList)):
                            if move == validMovesList[i]:
                                 gs.makeMove(validMovesList[i])
                                 print(move.getChessNotation())
                                 moveMade = True
                                 animate = True
                                 sqSelected = ()
                                 playerClicks = []
                            
                        if not moveMade:
                            playerClicks = [sqSelected]
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undoMove()
                    moveMade = True
                    animate = False
                if e.key == p.K_r:
                    gs = engine.GameState() 
                    validMovesList = gs.validMoves()
                    print(validMovesList)
                    sqSelected = ()
                    playerClicks = []
                    moveMade = False
                    animate = False
        if moveMade:
            if animate:
                animateMove(gs.movesHistory[-1], screen, gs.board, clock)
            validMovesList = gs.validMoves()
            moveMade = False
            animate = False

        drawGameState(screen, gs, validMovesList, sqSelected)
        
        if gs.checkMate:
            gameOver = True
            if gs.whitesMove:
                drawText(screen, 'Black wins by checkmate')
            else:
                drawText(screen, 'White wins by checkmate')
        elif gs.staleMate:
            gameOver = True
            drawText(screen, 'Stalemate')
        
        clock.tick(MAX_FPS)
        p.display.flip()
        
def highlightSquares(screen, gs, validMoves, sqSelected):
    if sqSelected != ():
        r, c = sqSelected
        if gs.board[r][c][0] == ('w' if gs.whitesMove else 'b'):
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(200)
            s.fill(p.Color("darkmagenta"))
            screen.blit(s, (c*SQ_SIZE, r*SQ_SIZE))
            s.set_alpha(150)
            s.fill(p.Color("darkorchid"))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (SQ_SIZE*move.endCol, SQ_SIZE*move.endRow))


def drawGameState(screen, gs, validMoves, sqSelected):
    drawBoard(screen)
    highlightSquares(screen, gs, validMoves, sqSelected)
    drawPieces(screen, gs.board)
    
def drawBoard(screen):
    global colors 
    colors = [p.Color("white"), p.Color("lightpink")]
    for r in range(DIMENTION):
        for c in range(DIMENTION):
            color = colors[((r+c)%2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawPieces(screen, board):
    for r in range(DIMENTION):
        for c in range(DIMENTION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))  
    
    
def animateMove(move, screen, board, clock):
    global colors
    coords = []
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framesPerSquare = 10
    frameCount = (abs(dR) + abs(dC)) * framesPerSquare
    for frame in range(frameCount + 1):
        r, c = (move.startRow + dR * frame/frameCount, move.startCol + dC * frame/frameCount)
        drawBoard(screen)
        drawPieces(screen, board)
        
        color = colors[(move.endRow + move.endCol) % 2]
        endSquare = p.Rect(move.endCol * SQ_SIZE, move.endRow * SQ_SIZE, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen, color, endSquare)
        
        captured_image = IMAGES.get(move.pieceCaptured)
        if captured_image:
            screen.blit(captured_image, endSquare)
        
        moving_piece_image = IMAGES.get(move.pieceMoves)
        if moving_piece_image:
            screen.blit(moving_piece_image, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
        
        p.display.flip()
        clock.tick(60)

def drawText(screen, text):
    font = p.font.SysFont("Helvetica", 32, True, False)
    textObject = font.render(text, 0 , p.Color('Black'))
    textLocation = p.Rect(0,0,WIDTH, HEIGHT).move(WIDTH/2 - textObject.get_width()/2, HEIGHT/2 - textObject.get_height()/2)
    screen.blit(textObject, textLocation)

if __name__ == "__main__":
    main()