import pygame
BROWN=(128,96,77)
WHITE=(255,255,255)

class Piece:
    def __init__(self,row,col,color):
        self.r=row
        self.c=col
        self.x=100*col+50
        self.y=100*row+50
        self.color=color
        self.king=False
        
class Board:
    def __init__(self):
        self.board=[]
        self.player2=12
        self.player1=12
        self.king2=0
        self.king1=0
        for r in range(8):
            self.board.append([])
            for c in range(8):
                if (r>2 and r<5) or c%2!=(r+1)%2:
                    self.board[r].append(0)
                else:
                    if r<3:
                        self.board[r].append(Piece(r,c,WHITE))
                    else:
                        self.board[r].append(Piece(r,c,BROWN))


    def getMoves(self,piece):
        #print(piece.r,piece.c)
        left=piece.c-1
        right=piece.c+1
        r=piece.r
        moves={}
        if piece.color==BROWN or piece.king:
            moves.update(self.find_move(r-1,max(r-3,-1),-1,piece.color,left,True))
            moves.update(self.find_move(r-1,max(r-3,-1),-1,piece.color,right,False))
        if piece.color==WHITE or piece.king:
            moves.update(self.find_move(r+1,min(r+3,8),1,piece.color,left,True))
            moves.update(self.find_move(r+1,min(r+3,8),1,piece.color,right,False))
        print(moves)
        return moves
    
    def find_move(self,s,e,step,c,l,f,skipped=[]):
        moves={}
        last=[]
        for r in range(s,e,step):
            if l<0 or l>=8:
                break
            temp=self.board[r][l]
            if temp==0:
                if not skipped:
                    moves[(r,l)]=last
                else:
                    if last:
                        moves[(r,l)]=last+skipped
                    else:
                        break
                if last:
                    if step==-1:
                        r=max(r-3,0)
                    else:
                        r=min(r+3,8)
                    print(moves)
                    moves.update(self.find_move(r+step,r,step,c,l-1,True,skipped=last))
                    moves.update(self.find_move(r+step,r,step,c,l+1,False,skipped=last))
                break
            elif temp.color==c:
                break
            else:
                last=[temp]
            if f:
                l-=1
            else:
                l+=1
        return moves


    def move(self,piece,r,c):
        temp=self.board[piece.r][piece.c]
        self.board[piece.r][piece.c]=self.board[r][c]
        self.board[r][c]=temp
        piece.r=r
        piece.c=c
        piece.x=100*piece.c+50
        piece.y=100*piece.r+50
        if r==7 or r==0:
            piece.king=True
            if piece.color==WHITE:
                self.king1+=1
            else:
                self.king2+=1
