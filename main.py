import pygame
import sys 
from copy import deepcopy 
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
BROWN=(128,96,77)
WHITE=(255,255,255)
FPS=60
WIN=pygame.display.set_mode((1000,800))
GREEN=(0,255,0)
ANOTHER_COLOR=(61,92,92)
white_won="C:/Users/abban/Downloads/AI/images/white_won.jpg"
black_won="C:/Users/abban/Downloads/AI/images/brown_win.jpg"
White_Image=Image.open(white_won)
Black_Image=Image.open(black_won)
KING=pygame.transform.scale(pygame.image.load("images/Crown.png"),(100,100))
pygame.display.set_caption('AI Checkers')
BLACK=(0,0,0)
pygame.init()
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
            temp=max(r-3,-1)
            moves.update(self.find_move(r-1,temp,-1,piece.color,left,True))
            moves.update(self.find_move(r-1,temp,-1,piece.color,right,False))
        if piece.color==WHITE or piece.king:
            temp=min(r+3,8)
            moves.update(self.find_move(r+1,temp,1,piece.color,left,True))
            moves.update(self.find_move(r+1,temp,1,piece.color,right,False))
        print(moves)
        return moves
    
    def find_move(self,s,e,step,c,l,f,skipped=[]):
        is_loop=True
        moves={}
        last=[]
        for r in range(s,e,step):
            if l<0 or l>=8:
                is_loop=False    
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
        if r==0 or r==7:
            if piece.color==WHITE:
                self.king1+=1
                piece.king=True
            else:
                self.king2+=1
                piece.king=True


def minimax(pos,d,f,game):
    if d==0 or game.gameEnd()!=None:
        return 2*pos.player1-2*pos.player2+(pos.king1*0.5-pos.king2*0.5) , pos
    if f:
        maxEval=float('-inf')
        best_move=None
        for move in get_all_moves(pos,WHITE,game):
            eval=minimax(move,d-1,False,game)[0]
            if eval>=maxEval:
                maxEval=eval
                best_move=move
        return maxEval,best_move
    else:
        minEval=float('inf')
        best_move=None
        for move in get_all_moves(pos,BROWN,game):
            eval=minimax(move,d-1,True,game)[0]
            if eval<=minEval:
                minEval=eval
                best_move=move
        return minEval,best_move


def get_all_moves(board,color,game):
    moves=[]
    pieces=[]
    for r in board.board:
        for piece in r:
            if piece!=0 and piece.color==color:
                pieces.append(piece)
    for piece in pieces:
        valid_moves=board.getMoves(piece)
        for move,skip in valid_moves.items():
            temp_board=deepcopy(board)
            temp_piece=temp_board.board[piece.r][piece.c]
            temp_board.move(temp_piece,move[0],move[1])
            if skip:
                for p in skip:
                    if p!=0:
                        temp_board.board[p.r][p.c]=0
                        if p.color==WHITE:
                            temp_board.player1-=1
                        else:
                            temp_board.player2-=1
            moves.append(temp_board)

    return moves

class Game:
    def __init__(self,win):
        self.current_piece=None
        self.board=Board()
        self.current_player=BROWN
        self.valid_moves={}
        self.win=win

    def select(self,r,c):
        if self.current_piece:
            piece=self.board.board[r][c]
            result=True
            if piece==0 and self.current_piece and  (r,c) in self.valid_moves:
                self.board.move(self.current_piece,r,c)
                if self.valid_moves[(r,c)]:
                    for piece in self.valid_moves[(r,c)]:
                        if piece!=0:
                            self.board.board[piece.r][piece.c]=0
                            if piece.color==BROWN:
                                self.board.player2-=1
                            else:
                                self.board.player1-=1
                self.valid_moves={}
                if self.current_player==BROWN:
                    self.current_player=WHITE
                else:
                    self.current_player=BROWN   
            else:
                result=False
            if not result:
                self.current_piece=None
                self.select(r,c)
        piece=self.board.board[r][c]
        if piece!=0: 
            if piece.color==self.current_player:
                self.current_piece=piece
                self.valid_moves=self.board.getMoves(piece)
                
    def gameEnd(self):
        if self.board.player2<=0:
            return WHITE
        elif  self.board.player1<=0:
            return BROWN
        return None

def main():
    game=Game(WIN)
    while True:
        if game.current_player==WHITE:
            value,new_board=minimax(game.board,3,WHITE,game)
            game.board=new_board
            game.valid_moves={}
            if game.current_player==BROWN:
                game.current_player=WHITE
            else:
                game.current_player=BROWN   
        if game.gameEnd()!= None:
            if game.gameEnd()==WHITE:
                ImageNumpyFormat = np.asarray(White_Image)
                plt.imshow(ImageNumpyFormat)
                plt.draw()
                plt.pause(10)
                plt.close()
            else:
                ImageNumpyFormat = np.asarray(Black_Image)
                plt.imshow(ImageNumpyFormat)
                plt.draw()
                plt.pause(10)
                plt.close()
            return 
        
        smallfont = pygame.font.SysFont('Corbel',25) 
        text = smallfont.render('Draw or Quit' , True , WHITE)
        for event in pygame.event.get():
            if event.type==pygame.MOUSEBUTTONDOWN:
                pos=pygame.mouse.get_pos()
                r,c=pos
                if 820 <= r <=950 and 375 <= c <=400:
                    print("Game Draw, Nobody win, nobody loose.")
                    return 
                r,c=c//100,r//100
                game.select(r,c)
            if event.type==pygame.QUIT:
                return 
            
        game.win.fill(BLACK)
        pygame.draw.rect(game.win,(255,182,193),(800,0,200,800))
        pygame.draw.rect(game.win,(80,80,80),[820,375,130,25])
        game.win.blit(text , (820,375))
        for r in range(8):
            for c in range(r%2,8,2):
                pygame.draw.rect(game.win,ANOTHER_COLOR,(r*100,c*100,100,100))
            for c in range(8):
                piece=game.board.board[r][c]
                if piece!=0:
                    pygame.draw.circle(game.win,piece.color,(piece.x,piece.y),35)
                    if piece.king:
                        game.win.blit(KING,(piece.x-KING.get_width()//2,piece.y-KING.get_height()//2))
        for move in game.valid_moves:
            #print(move)
            r,c=move
            pygame.draw.circle(game.win,GREEN,(c*100+50,r*100+50),15)
            #print(r,c)
        pygame.display.update()
    pygame.quit()

main()