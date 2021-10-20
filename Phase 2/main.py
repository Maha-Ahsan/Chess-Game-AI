import pygame as p
import Engine
import math
EMPTY=None
WIDTH = HEIGHT = 512    #512 64
DIMENSION = 8
SQ_SIZE = 64
MAX_FPS = 15
IMAGES={}

#col_val_oppo={0:"a",1:"b",2:"c",3:"d",4:"e",5:"f",6:"g",7:"h"}
col_val_oppo={"a":0,"b":1,"c":2,"d":3,"e":4,"f":5,"g":6,"h":7}
col_val={0:"a",1:"b",2:"c",3:"d",4:"e",5:"f",6:"g",7:"h"}
SCREEN_TITLE="Chess Game"
p.display.set_caption(SCREEN_TITLE)
def loadImages():
    pieces = ["PAWN_W1","PAWN_W2","PAWN_W3", "PAWN_W4","PAWN_W5","PAWN_W6","PAWN_W7","PAWN_W8","ROOK_W1","KNIGHT_W1","BISHOP_W1","QUEEN_W","KING_W","BISHOP_W2","KNIGHT_W2","ROOK_W2",
              "PAWN_B1","PAWN_B2","PAWN_B3","PAWN_B4","PAWN_B5", "PAWN_B6","PAWN_B7","PAWN_B8","ROOK_B1","KNIGHT_B1","BISHOP_B1","QUEEN_B","KING_B","BISHOP_B2","KNIGHT_B2","ROOK_B2"]
    for pie in pieces:
        IMAGES[pie] = p.transform.scale(p.image.load("images/" + pie + ".png"),(SQ_SIZE,SQ_SIZE))

def drawGameState(screen,gs,sq,name):
    drawBoard(screen)
    HighlightSquares(screen, gs, sq,name)
    drawPieces(screen,gs.board)

def HighlightSquares(screen, object, sqSelected,piece_name) :

    if piece_name != "" :
        validMoves = []
        loc =  Engine.get_piece_loc(piece_name,object.board)
        #print("Location: ",loc)

        #for piece in Engine.All_Piece :
        Engine.AllPossibleMove(piece_name, gs, validMoves)

        #print("In highlight Square")
        if sqSelected != () :
            row,col = sqSelected
            #print("Row: ",row,"Col: ",col)
            row = math.floor(row/64)
            col = math.floor(col/64)
            #print("Converted row: ",row," Converted Col: ",col)

            piece_name = object.board[row][col]
            #print("Piecename: ",piece_name)
            if piece_name != EMPTY :    #movable piece
                piece_name = piece_name.split('-')
                s=p.Surface((SQ_SIZE,SQ_SIZE))
                s.set_alpha(200)
                s.fill(p.Color(105, 74, 56))
                screen.blit(s,(col*SQ_SIZE,row*SQ_SIZE))

                #highlight moves

                s.fill(p.Color(0, 79, 45))

                for move in validMoves :
                    c =int(col_val_oppo[move[1][0]])
                    r = int(move[1][1])
                    #print("Row: ", type(r), "Col: ", type(c))
                    if row == loc[0] and col == loc[1] :
                        if object.board[r][c] == EMPTY :
                            #print("Move: ",move)
                            screen.blit(s,(c*SQ_SIZE,r*SQ_SIZE))
        if var==True:
            r, c = Engine.get_piece_loc("KING_W", gs.board)
            #print("R in main:", r, "C in main:", c)
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100)
            s.fill(p.Color("red"))
            screen.blit(s, (c * SQ_SIZE, r * SQ_SIZE))


def drawBoard(screen):
    colors = [p.Color(166, 28,60),p.Color('white')]

    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c) % 2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE,SQ_SIZE))

def drawPieces(screen,board):

    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece =board[r][c]
            #print("Piece=",piece)
            if piece != EMPTY and piece!=0:
                screen.blit(IMAGES[piece],p.Rect(c*SQ_SIZE,r*SQ_SIZE,SQ_SIZE,SQ_SIZE))

def display(board):
    print("\n")
    for r in board:
        for c in r:
            print(c, end=" ")
        print()


if __name__ == '__main__':
    p.init() #PYGAME
    alpha=" "
    screen = p.display.set_mode((8*SQ_SIZE, 8*SQ_SIZE),p.RESIZABLE)
    #     #screen = p.display.set_mode((WIDTH,HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    global var
    var=False
    gs = Engine.GameState()
    display(gs.board)
    #temp_var=False
    loadImages()
    running = True
    sqSelected = () #no of sq is selcted, keep track of the last click
    playerClicks = []
    ai_turn=False
    moved="yo"
    piece_name = ""
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                print("QUITTING!!")
                running = False
        #     #mouse handler
            elif e.type == p.MOUSEBUTTONDOWN :
                if ai_turn==False:#Human Player Turn
                    print("Start of Humani Player")
                    gs.check_on_king(ai_turn,gs)
                    if gs.white_check==True:
                       p.display.set_caption("Chess Game" + "---Check o King")
                       var=True
                    else:var=False
                    location = p.mouse.get_pos()
                    col = location[0]
                    row = location[1]
                    print("col:",col,"row:",row)
                    print("Converted col:",math.floor(col/64),"Converted Row:",math.floor(row/64))
                    if sqSelected == (row,col): #same square selected
                        print("Already Selected")
                        sqSelected = () #deselect
                        playerClicks = []
                    else:
                        sqSelected = (row,col)
                        playerClicks.append(sqSelected)
                        print("PLayer CLicks:",playerClicks)
            #             print(" ",row/64, " ",col/64)

                        if len(playerClicks) == 1:
                            old_row, old_col = playerClicks[0]
                            piece_name = gs.board[math.floor(old_row / 64)][math.floor(old_col / 64)]

                            if piece_name != EMPTY:
                                print("Piecename: ", piece_name)
                                name = piece_name.split('_')
                                print("Piecename: ", piece_name[1])
                                if name[1] == 'W' or name[1][0] == 'W':
                                    print("Highlihting")
                                    # HighlightSquares(screen, gs, sqSelected, piece_name)
                        if len(playerClicks) == 2:
                            print("Sending for movement")
                            #print("Old:", playerClicks[0], "New:",playerClicks[1])
                            old_row,old_col=playerClicks[0]
                            new_row,new_col=playerClicks[1]
                            #print("Old_col:", math.floor(old_col/64), "Old_row:", math.floor(old_row/ 64))
                            print("Piece_Name:",gs.board[math.floor(old_row / 64)][math.floor(old_col / 64)])
                            piece_name=gs.board[math.floor(old_row / 64)][math.floor(old_col / 64)]

                            if piece_name!= EMPTY:
                               # print("new_col:",math.floor(new_col/64),"new_row:",math.floor(new_row/64))
                                new_col=math.floor(new_col/64)
                                new_row=math.floor(new_row/64)
                                #print("new_col:", new_col, "new_row:", new_row)
                                print("Converted_Col:",col_val[new_col],"new_row:", new_row)
                                new_move=col_val[new_col]+str(new_row)
                                print("New Move:",new_move)
                                mov=0
                                if piece_name=="KING_W" or piece_name=="ROOK_W1" or piece_name=="ROOK_W2":
                                    print("Its a king")
                                    new_piece=gs.board[new_row][new_col]
                                    if new_piece!=EMPTY:
                                        if new_piece=="KING_W" or new_piece=="ROOK_W1" or new_piece=="ROOK_W2":
                                            alpha=Engine.castling(piece_name,new_piece,gs)
                                            print("Check Castling")


                                if alpha!=True:
                                    moved=Engine.movement(new_move,ai_turn,piece_name,gs,mov)

                                if moved==True or alpha==True:
                                    ai_turn=True
                                    moved=False
                                    alpha=False
                                    sqSelected = ()  # reset
                                    playerClicks = []
                                elif moved==False and alpha==False:
                                    print("False move of human")
                                    sqSelected = ()  # reset
                                    playerClicks = []
                            else:
                                sqSelected = ()  # reset
                                playerClicks = []

            elif ai_turn==True:
                print("AI Automatic Movement")
                p.display.set_caption("Chess Game" + "---Calculating Move")
                moved = Engine.movement(0, ai_turn,0, gs, 0)
                ai_turn=False
                p.display.set_caption("Chess Game")

            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:  # Undo operation
                    loc = []
                    loc.append((math.floor(new_col / 64), math.floor(new_row / 64)))
                    name = gs.board[math.floor(new_row / 64)][math.floor(new_col / 64)]
                    old_col = math.floor(old_col / 64)
                    old_row = math.floor(old_row / 64)
                    new_move = col_val[old_col] + str(old_row)

                    pos = Engine.get_piece_loc(piece_name, gs.board)
                    old_col = pos[1]
                    old_row = pos[0]

                    loc.append((old_row, old_col))
                    Engine.undoMove(EMPTY, loc, new_move, gs, piece_name)

                elif e.key == p.K_r:  # Reset operation
                    gs = Engine.GameState()
                    sqSelected = ()
                    playerClicks = []
        drawGameState(screen,gs,sqSelected,piece_name)
        clock.tick(MAX_FPS)
        p.display.flip()

#
# # See PyCharm help at https://www.jetbrains.com/help/pycharm/
