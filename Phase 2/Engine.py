import math
import random
EMPTY=None
nextmove=None
CHECKMATE=100
col_val={"a":0,"b":1,"c":2,"d":3,"e":4,"f":5,"g":6,"h":7}
col_val_oppo={0:"a",1:"b",2:"c",3:"d",4:"e",5:"f",6:"g",7:"h"}
User_Piece = ["ROOK_W1","KNIGHT_W1","BISHOP_W1","QUEEN_W","KING_W","PAWN_W1","PAWN_W2","PAWN_W3", "PAWN_W4","PAWN_W5","PAWN_W6","PAWN_W7","PAWN_W8","ROOK_W2","KNIGHT_W2","BISHOP_W2"]
AI_Piece = ["ROOK_B1","KNIGHT_B1","BISHOP_B1","QUEEN_B","KING_B","PAWN_B1","PAWN_B2","PAWN_B3", "PAWN_B4","PAWN_B5","PAWN_B6","PAWN_B7","PAWN_B8","ROOK_B2","KNIGHT_B2","BISHOP_B2"]
Piece_val={"ROOK":5,"QUEEN":9,"KING":100,"PAWN":1,"BISHOP":3,"ROOK":5,"KNIGHT":3}
All_Piece=["ROOK_W1","KNIGHT_W1","BISHOP_W1","QUEEN_W","KING_W","PAWN_W1","PAWN_W2","PAWN_W3", "PAWN_W4","PAWN_W5","PAWN_W6","PAWN_W7","PAWN_W8","ROOK_W2","KNIGHT_W2","BISHOP_W2",
"ROOK_B1","KNIGHT_B1","BISHOP_B1","QUEEN_B","KING_B","PAWN_B1","PAWN_B2","PAWN_B3", "PAWN_B4","PAWN_B5","PAWN_B6","PAWN_B7","PAWN_B8","ROOK_B2","KNIGHT_B2","BISHOP_B2"]

X = [2, 1, -1, -2, -2, -1, 1, 2];
Y = [1, 2, 2, 1, -1, -2, -2, -1];

moves = ["a0","a1","a2","a3","a4","a5","a6","a7",
       "b0","b1","b2","b3","b4","b5","b6","b7",
       "c0","c1","c2","c3","c4","c5","c6","c7",
       "d0","d1","d2","d3","d4","d5","d6","d7",
       "e0","e1","e2","e3","e4","e5","e6","e7",
       "f0","f1","f2","f3","f4","f5","f6","f7",
       "g0","g1","g2","g3","g4","g5","g6","g7",
    "h0", "h1", "h2", "h3", "h4", "h5", "h6", "h7"
         ]
DEPTH=2

class GameState():
    def __init__(self):
        #board is an 8X8 2D list, each element of the list has 2 characters
        self.  board=[["ROOK_B1","KNIGHT_B1","BISHOP_B1","QUEEN_B","KING_B","BISHOP_B2","KNIGHT_B2","ROOK_B2"],
           ["PAWN_B1","PAWN_B2","PAWN_B3","PAWN_B4","PAWN_B5", "PAWN_B6","PAWN_B7","PAWN_B8"],
           [EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY],
           [EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY],
           [EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY],
           [EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY],
           ["PAWN_W1","PAWN_W2","PAWN_W3", "PAWN_W4","PAWN_W5","PAWN_W6","PAWN_W7","PAWN_W8"],
           ["ROOK_W1","KNIGHT_W1","BISHOP_W1","QUEEN_W","KING_W","BISHOP_W2","KNIGHT_W2","ROOK_W2"]
           ]
        #
        # self.whiteToMove = True
        self.moveLog = []
        self.white_check=False
        self.black_check=False
        self.white_checkMate=False
        self.Black_checkMate=False
    def check_on_king(self,ai_turn,object):
        king_moves=[]
        self.white_check = False
        all_moves=[]
        if ai_turn==False:
            print("Checking for check on king...")
            r,c=get_piece_loc("KING_W",self.board)
            king_loc=col_val_oppo[int(c)]+str(r)
            for p in AI_Piece:
                if p!="KING_W":
                    AllPossibleMove(p, object,all_moves)

            for m in all_moves:
                if m[1]==king_loc:
                    print("Check is predicted")
                    self.white_check=True
            if self.white_check==True:
                found=[]
                AllPossibleMove("KING_W",object,king_moves)
                for k_mov in king_moves:
                    kin_pos=k_mov[1]
                    for m in all_moves:
                        if m[1]==kin_pos:
                            found.append(m[1])
                            break
                if len(king_moves)==len(found):
                    self.white_checkMate=True
                    print("\n")
                    print("Check mate on white by black")
                    print("\n")
                    a=input("Press 1 to exit")
                    if a==1:print("Checking out")
                    if a==0: self.white_checkMate=False

        return False




    def adding_move(self,move):

        self.moveLog(move)


    def new_board(self, piece_move, loc, piece_name):

        r, c = loc.pop()
        #print("r:", r, "c:", c)
        self.board[r][c] = EMPTY
        new_r = piece_move[1]
        new_c = piece_move[0]
        new_r = int(new_r)
        self.board[new_r][col_val[new_c]] = piece_name

    def display(self,board):
        print("\n")
        for r in board:
            for c in r:
                print(c, end=" ")
            print()


    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.start_row][move.start_col] = move.pieceMoved
            self.board[move.end_row][move.end_col] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove




def AllPossibleMove(piece_name,object,move):

    for m in moves:
        flag, loc = evaluate_move(piece_name,m, object.board)
        if flag==True:move.append((piece_name,m))
    return move

def CheckOnKing(king,object):
   # print('\n')
    mov=-1
    org_name = king.split("_")
    color = org_name[1]
    loc=get_piece_loc(king,object.board)
    #print("LOC of king:",loc)
    row,col=loc
    #print("Row of king:",row,"COl of King:",col)
    #print(col_val[int(col)])
    pos=col_val_oppo[col]+str(row)
    #print("King pos:",pos)
    check=[]
    possible_moves=[]
    check_mate=[]
    if color=="W":
        #If your king is white
        #print("Human King")
        for piece in AI_Piece:
            flag,loc=evaluate_move(piece,pos,object.board)
            if flag == True:
                check.append(piece)
                #print("Entering...")
                flag=False
        if len(check)!=0:
            #print("Check By:",check)
            #print("King is Facing Check--Check for check mate")
            possible_moves=AllPossibleMove(king,object)
            #print("Move of king:",possible_moves)
            for m in possible_moves:
                for piece in AI_Piece:
                    flag, loc = evaluate_move(piece,m, object.board)
                    if flag == True:
                        check_mate.append((piece,m))
                        #print("Entering...Broke")
                        break
                        flag = False
            if len(check_mate)==len( possible_moves):
                # print("Checkmate By:",check_mate)
                # print("Its a check mate")
                return 1,1
            else: return 1,0
        else:
            # print("No ckeck/checkmate")
            return 0,0



    elif color=="B":
        print("AI King")

    return
def undoMove(name,old_loc,new_loc,object,old_piece):
    old_row,old_col=old_loc.pop()
    new_row,new_col=new_loc[1],new_loc[0]
    object.board[old_row][old_col]=name
    object.board[int(new_row)][col_val[new_col]]=old_piece

    pass



def scoreMaterial(board):
    score=0
    for row in board:
        for square in row:
           # print("Squre:", square)
            if square !=EMPTY:

                split=square.split('_')
                name=split[0]
                color=split[1]
                if color=='W' or color[0]=='W':
                    score+=Piece_val[name]

                elif color == 'B' or color[0] == 'B':
                    score-= Piece_val[name]
    return score


def get_AI_move(game,color, depth):
    ans=minimax(game,color,depth)
    print("MOve predicted by AI:",ans)
    return ans
def win_score(color):
    if color == "W":
        return -10*Piece_val["KING"]
    if color == "B":
        return 10*Piece_val["KING"]


def evaluate_game(game):
    s=scoreMaterial(game.board)
    return s
    #return material_balance(game.board) + positional_balance(game)
def check_in_board(pie,object):
    for r in range(8):
        for c in range(8):
            if object.board[r][c]==pie:return True
    return False
def legal_moves(game, color):
    all_move=[]
    #print("New:")
    if color=="W":
        for p in User_Piece:
            flag=check_in_board(p,game)
            if flag==True:
                AllPossibleMove(p,game,all_move)


    elif color=="B":
        for p in AI_Piece:
            flag = check_in_board(p, game)
            if flag == True:
                AllPossibleMove(p, game, all_move)
    else: print("Color no match in legal moves")
    return all_move


def evaluated_move(game, color):
    #print("Evaluated Move")
    best_score = win_score(color)
    best_moves = []
    loc=[]
    loc1=[]
    moves=legal_moves(game, color)
    for move in moves:
        piece_name,new_loc=move[0],move[1]
        r, c = get_piece_loc(move[0], game.board)
        loc.append((r, c))
        loc1.append((r, c))
        new_loc = move[1]
        old_piece = game.board[int(new_loc[1])][col_val[new_loc[0]]]
        game.new_board(move[1], loc, move[0])
        evaluation = evaluate_game(game)
    #
    #     if is_checkmate(make_move(game, move), opposing_color(game.to_move)):
    #         return [move, evaluation]

        if (color == "W" and evaluation > best_score) or \
                (color == "B" and evaluation < best_score):
            best_score = evaluation
            best_moves = [move]
        elif evaluation == best_score:
            best_moves.append(move)
        undoMove(move[0], loc1, move[1], game, old_piece)
    return [random.choice(best_moves), best_score]
def opposing_color(color):
    if color == "W":
        return "B"
    if color == "B":
        return "W"
def minimax(game, color, depth):
    # if game_ended(game):
    #     return [None, evaluate_game(game)]
    #print("MiniMax func")
    [simple_move, simple_evaluation] = evaluated_move(game, color)

    if depth == 1 or \
            simple_evaluation == win_score(opposing_color(color)):
        return [simple_move, simple_evaluation]

    best_score = win_score(color)
    best_moves = []

    for move in legal_moves(game, color):
        loc=[]
        loc1=[]
        piece_name, new_loc = move[0], move[1]
        r, c = get_piece_loc(move[0], game.board)
        loc.append((r, c))
        loc1.append((r, c))
        new_loc = move[1]
        old_piece = game.board[int(new_loc[1])][col_val[new_loc[0]]]
        #object.new_board(move[1], loc, move[0])
        game.new_board(move[1], loc, move[0])

        # if is_checkmate(his_game, his_game.to_move):
        #     return [move, win_score(his_game.to_move)]

        [_, evaluation] = minimax(game, opposing_color(color), depth - 1)

        if evaluation == win_score(opposing_color(color)):
            return [move, evaluation]

        if (color == "W" and evaluation > best_score) or \
                (color == "B" and evaluation < best_score):
            best_score = evaluation
            best_moves = [move]
        elif evaluation == best_score:
            best_moves.append(move)
        undoMove(move[0], loc1, move[1], game, old_piece)
    return [random.choice(best_moves), best_score]


def movement(piece_move,ai_turn,piece_name,object,mov):#Take input of ai_turn,piece_name,piece_move
    #ai_turn = False
        #object.check_on_king(ai_turn,object)
        print("Enter Movement func")
        print("Piece_Move:",piece_move)
        print("Piee_Name:",piece_name)
    #for i in range(10):
        if ai_turn == False:

            print("\n")
            print("USER TURN")
            found =0
            for i in User_Piece:
                if piece_name==i:
                    found=1
                    break
            if found!=1:
                print("No  Piece of such name:",piece_name)
                return False
            valid, loc = evaluate_move(piece_name, piece_move,object.board)  # Validation
            if valid == True:  # If returned true #True Value will be returned back to for replacement
                print("Can Move")
                loc1=loc.copy()
                object.new_board(piece_move, loc, piece_name)

                object.check_on_king(ai_turn,object)
                if object.white_check==True:
                    print('\n')
                    loc2=loc1.copy()
                    r,c=loc1.pop()
                    print("King is on check-Can only Move King")
                    undoMove(piece_name,loc2, piece_move, object, object.board[r][c])
                    print('\n')
                    return False

                #object.new_board(piece_move, loc, piece_name)
                print(object.board)
                object.display(object.board)

                return True
            else:print("Returning False from Movement")
            return False

        elif ai_turn ==True:

             #-------------
            print("Finiding AI movement")
            print("\n")
            loc=[]
            print("AI TURN")
            move_min=get_AI_move(object,'B',2)
            print("Piece_NAme:",move_min[0][0],"Piece_loc",move_min[0][1])
            new_loc=move_min[0][1]
            print(move_min)
            r, c = get_piece_loc(move_min[0][0], object.board)
            loc.append((r, c))
            print("loc:",loc)
            object.new_board(new_loc, loc, move_min[0][0])
            object.display(object.board)
            return True

def castling(piece1,piece2,object):
    token1=piece1.split('_')
    token2=piece2.split('_')
    name1=token1[0]
    check=0
    name2=token2[0]
    f=object.check_on_king("False", object)
    if name1!=name2 and f==False:
        if name1=="ROOK" and name2=="KING":
            rook=piece1
            king=piece2
            check=1
        elif name2=="ROOK" and name1=="KING":
            rook=piece2
            king=piece1
            check=1
        if check==1:
            r,c=get_piece_loc(king,object.board)
            if r==7 and c==4:
                r1,c1=get_piece_loc(rook, object.board)
                if r1==7 and (c1==0 or c1==7):
                    print("Execute Castling")
                    flag=check_rook_col(c1,c,r, object.board)
                    if flag==True and rook=="ROOK_W2":
                        loc=[]
                        loc2=[]
                        loc.append((7,7))
                        loc2.append((r,c))
                        object.new_board("f7", loc, rook)
                        object.new_board("g7", loc2, king)
                    elif flag==True and rook=="ROOK_W1":
                        loc=[]
                        loc2=[]
                        loc.append((7,0))
                        loc2.append((r,c))
                        object.new_board("d7", loc, rook)
                        object.new_board("c7", loc2, king)


                    return flag
    return False









    pass
def get_piece_loc(piece_name,board):
    for r in range(8):
        for c in range(8):
            #print("Board:",board[r][c],"r:",r,"c:",c,)
            if board[r][c]==piece_name:
                return r,c
    return -1,-1
def pawn_moves_white(piece_move,r,c,board):
    new_r=piece_move[1]
    new_c=piece_move[0]
    new_r=int(new_r)
    #print("New row:",new_r,"New col:",new_c)
    if board[new_r][col_val[new_c]]!=EMPTY:
        #Killing implementation is left
        name = board[new_r][col_val[new_c]]
        split = name.split("_")
        color = split[1]
        if color[0] == 'B':
            if r - 1 == new_r:
                if c + 1 == col_val[new_c]:
       #             print("KILLED:", board[new_r][col_val[new_c]])
                    return True
                elif c - 1 == col_val[new_c]:
                    return True
        return False
    else:
        if col_val[new_c]==c:
            if r-1==new_r:
        #        print("R:",r,"new_r:",new_r)
                return True

            elif r==6:
                if r-2==new_r:
                    return True

    return False
def pawn_moves_black(piece_move,r,c,board):
    new_r=piece_move[1]
    new_c=piece_move[0]
    new_r=int(new_r)
    #print("New row:",new_r,"New col:",new_c)
    if board[new_r][col_val[new_c]]!=EMPTY:
        name=board[new_r][col_val[new_c]]
        split = name.split("_")
        color=split[1]

        if color[0]=='W':
           # print("Checking for killinh")
            if r+1==new_r:
             #   print("Inc of row")
                if c+1==col_val[new_c]:
              #      print("KILLED:",board[new_r][col_val[new_c]])
                    return True
                if c-1==col_val[new_c]:
                    return True

        #Killing implementation is left
        return False
    else:
        if col_val[new_c]==c:
            if r+1==new_r:


                return True

            elif r==1:
                if r+2==new_r:
                    return True

    return False

def check_diagonals(new_r,new_c,r,c,board):
    iterate=abs(c-new_c)
    #print("r:",r,"c:",c,"new_r:",new_r,"new_c:",new_c)
    if r-new_r>0:#Left Upper Diagonal
        if c-new_c>0:
            # print("Left Upper Diagonal")
            # print("\n")
            # print("\n")
            for i in range(iterate):
                if i!=0:
                    if board[r-i][c-i] != EMPTY:
                        # print("Left Upper Diagonal:",board[r-i][c-i],'x:',r-i,"y:",c-i)
                        return False
            return True
    if r-new_r>0:#Right Upper Diagonal 7-6>0 2-3<0
        if c-new_c<0:
            # print("Right Upper Diagonal")
            # print("\n")
            # print("\n")
            for i in range(iterate):
                if i!=0:
                    if board[r-i][c+i] != EMPTY:
                        # print("Right Upper Diagonal:", board[r-i][c+i], 'x:', r - i, "y:", c +i)
                        return False
            return True
    if r - new_r < 0:#Left Lower Diagonal
        if c - new_c > 0:
            # print("Left Lowe Diagonal")
            # print("\n")
            # print("\n")
            for i in range(iterate):
                if i!=0:
                    if board[r + i][c - i] != EMPTY:
                        # print("Left lower Diagonal:", board[r + i][c - i], 'x:', r +i, "y:", c - i)
                        return False
            return True
    if r - new_r < 0:#Right Lower Diagonal
        if c - new_c < 0:
            # print("Right Lowe Diagonal")
            # print("\n")
            # print("\n")
            for i in range(iterate):
                if i!=0:
                    if board[r + i][c + i] != EMPTY:
                        # print("Right lower Diagonal:", board[r + i][c + i], 'x:', r + i, "y:", c + i)
                        return False
            return True
    return False


def bishop_moves(piece_move,r,c,piece_color,board):
    new_r = piece_move[1]
    new_c = piece_move[0]
    new_r = int(new_r)
    flag1 = False
    #print("New row:", new_r, "New col:", new_c)
    if board[new_r][col_val[new_c]] != EMPTY:
        # Killing implementatio of killing is left
        name = board[new_r][col_val[new_c]]
        split = name.split("_")
        color = split[1]
        #print(color[0])
        if color[0] != piece_color:
            if abs(col_val[new_c] - c) == abs(new_r - r):
                flag1 = check_diagonals(new_r, col_val[new_c], r, c, board)
        return flag1
    else:
        if abs(col_val[new_c]-c)==abs(new_r-r):
               flag1=check_diagonals(new_r,col_val[new_c],r,c,board)
    return flag1


def queen_moves(piece_move,r,c,piece_color,board):
    new_r = piece_move[1]
    new_c = piece_move[0]
    new_r = int(new_r)
    flag1 = False
    #print("New row:", new_r, "New col:", new_c)
    if board[new_r][col_val[new_c]] != EMPTY:
      #  print("Entered in not equal")
        name = board[new_r][col_val[new_c]]
        split = name.split("_")
        color = split[1]
       # print("Color in queen:",color[0])
        if color[0] != piece_color:
        #    print("Entered in which piee pesent:",board[new_r][col_val[new_c]])

            if abs(col_val[new_c] - c) == abs(new_r - r):
                flag1 = check_diagonals(new_r, col_val[new_c], r, c, board)
            else:
                flag1 = rook_else(new_r, col_val[new_c], r, c, board)
            #if flag1==True:#print("REturnng tureee")
            return flag1
        return False
    else:
        if abs(col_val[new_c]-c)==abs(new_r-r):
               flag1=check_diagonals(new_r,col_val[new_c],r,c,board)
        else:
            flag1 = rook_else(new_r, col_val[new_c], r, c,board)
    return flag1


def check_rook_row(org_r,new_r,c,board):#Check Whether in between rows are empty or not
    if org_r > new_r:#Same col Dec Row
       # print("org_r:",org_r)
        for i in range(org_r-new_r):
            # print("i:",i)
            # print("Board:",board[org_r-i][c])
            if i!=0:
                if board[org_r-i][c] != EMPTY:
                    #print("OPPS false",board[org_r-i][c],org_r-i,c)

                    return False
        return True
    else:
        for i in range(new_r-org_r):#Same Col Inc Row
            if i!=0:
                if board[org_r+i][c] != EMPTY:
                    return False
        return True
def check_rook_col(org_c,new_c,row,board):
    if new_c>org_c:
        for i in range(new_c-org_c):#Same row inc col
            if i!=0:
                if board[row][org_c+i] != EMPTY:
                    return False

        return True
    else:
        for i in range(org_c-new_c):#Same row dec col
            if i!=0:
                if board[row][org_c - i] != EMPTY:
                    return False
        return True

def rook_else(new_r,new_c,r,c,board):
    if new_c == c:  # New move and org pos in same col
        flag1 = check_rook_row(r, new_r, c,board)
        #print("Checking...")
        return flag1
    elif new_r == r:  # Same row
        flag1 = check_rook_col(c, new_c, r,board)
        return flag1
    return False

def rook_moves(piece_move,r,c,piece_color,board):
    new_r=piece_move[1]
    new_c=piece_move[0]
    new_r = int(new_r)
    flag1=False
    # print("New row:", new_r, "New col:", new_c)
    if board[new_r][col_val[new_c]] != EMPTY:
        # Killing implementatio of killing is left
        name = board[new_r][col_val[new_c]]
        split = name.split("_")
        color = split[1]
        if color[0] != piece_color:
            flag1 = rook_else(new_r, col_val[new_c], r, c,board)
            return flag1

        else:
            return False
        #return False
    else:
        flag1=rook_else(new_r,col_val[new_c],r,c,board)
    return flag1
        # if col_val[new_c] == c:#New move and org pos in same col
        #     flag1=check_rook_row(r,new_r,c)
        #     print("Checking...")
        #     return flag1
        # elif new_r==r:#Same row
        #     flag1=check_rook_col(c,col_val[new_c],r)
        #     return flag1

def evaluate_move(piece_name,piece_move,board):
    loc=[]
    # print("Name of piece in evaluate func:",piece_name)
    r,c=get_piece_loc(piece_name,board)#Through GUI
    # print("r:",r,"c:",c)
    loc.append((r,c))
    org_name=piece_name.split("_")
    color=org_name[1]
    flag=False
    if org_name[0]=="PAWN":

        if color[0]=='W':
            flag = pawn_moves_white(piece_move, r, c,board)
        if color[0]=='B':
            #print("Black pawn movement")
            flag = pawn_moves_black(piece_move, r, c,board)
    elif org_name[0]=="ROOK":
        flag=rook_moves(piece_move,r,c,color[0],board)
    elif org_name[0]=="BISHOP":
        flag=bishop_moves(piece_move,r,c,color[0],board)
    elif org_name[0]=="QUEEN":
        flag=queen_moves(piece_move,r,c,color,board)
        #return flag
    elif org_name[0] == "KING":
        flag = king_moves(piece_move, r, c, board,color)
    elif org_name[0] == "KNIGHT":
        flag = knight_moves(piece_move, r, c, board, color[0])

    return flag,loc

def knight_moves(piece_move, r, c,board,piece_color):
    # print("Checking knight MOves")
    new_r = piece_move[1]
    new_c = piece_move[0]
    new_c = col_val[new_c]
    new_r = int(new_r)
    # print("New row:", new_r, "New col:", new_c)
    if board[new_r][new_c] != EMPTY:
        # Killing implementatio of killing is left
        name = board[new_r][new_c]
        split = name.split("_")
        color = split[1]
        #print("Color:",color,"Piece Color:",piece_color)
        if color[0] != piece_color or color!=piece_color:
            for i in range(8):

                # Position of knight after move
                x = r + X[i];
                y = c + Y[i];

                # count valid moves
                if (x >= 0 and y >= 0 and x < 4 and y < 4) :
                    if x==new_r and y==new_c:return True
        return False
    else:
        #print("Entered in else")
        for i in range(8):

            # Position of knight after move
            x = r + X[i];
            y = c + Y[i];

            # count valid moves
            if (x >= 0 and y >= 0 and x < 8 and y < 8):
                if x == new_r and y == new_c: return True
    return False


def king_moves(piece_move, r, c,board,color):
    # print("Checking King MOves")
    new_r = piece_move[1]
    new_c = piece_move[0]
    new_c=col_val[new_c]
    new_r = int(new_r)
    # print("New row:", new_r, "New col:", new_c)
    if r==new_r+1 and c==new_c:
        if board[new_r][new_c] != EMPTY:
            piece=board[new_r][new_c]
            org_name = piece.split("_")
            c=org_name[1]
            if c[0]==color:return False
        return True
    elif r == new_r - 1 and new_c==c:
        if board[new_r][new_c] != EMPTY:
            piece = board[new_r][new_c]
            org_name = piece.split("_")
            c = org_name[1]
            if c[0] == color: return False
        return True
    elif c == new_c+1 and new_r==r:
        if board[new_r][new_c] != EMPTY:
            piece = board[new_r][new_c]
            org_name = piece.split("_")
            c = org_name[1]
            if c[0] == color: return False
        return True
    elif c == new_c-1 and new_r==r:
        if board[new_r][new_c] != EMPTY:
            piece = board[new_r][new_c]
            org_name = piece.split("_")
            c = org_name[1]
            if c[0] == color: return False
        return True
    elif r==new_r-1 and c==new_c-1:
        if board[new_r][new_c] != EMPTY:
            piece = board[new_r][new_c]
            org_name = piece.split("_")
            c = org_name[1]
            if c[0] == color: return False
        return True
    elif r == new_r +1 and c == new_c + 1:
        if board[new_r][new_c] != EMPTY:
            piece = board[new_r][new_c]
            org_name = piece.split("_")
            c = org_name[1]
            if c[0] == color: return False
        return True
    elif r == new_r + 1 and c == new_c - 1:
        if board[new_r][new_c] != EMPTY:
            piece = board[new_r][new_c]
            org_name = piece.split("_")
            c = org_name[1]
            if c[0] == color: return False
        return True
    elif r == new_r - 1 and c == new_c + 1:
        if board[new_r][new_c] != EMPTY:
            piece = board[new_r][new_c]
            org_name = piece.split("_")
            c = org_name[1]
            if c[0] == color: return False
        return True
    return False