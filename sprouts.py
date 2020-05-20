import pygame
from pygame import *
import sys
import time
import random
import math

#Contains Game Settings: Will change out later
from settings import Settings

'''
I want to eventually seperate these all into different .py and class files. For now they're here:
'''
#Game Objects
#Window Initiation
pygame.init()
win = pygame.display.set_mode((1000, 600))
pygame.display.set_caption('The Sprouts Game')
running = True

clock = pygame.time.Clock()

#Colours
RED = (255, 0, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
ORANGE = (255,165,0)

#Player
PlayerOne = 'Test1'
PlayerOneScore = 0

PlayerTwo = 'Test2'
PlayerTwoScore = 0

PlayerTurn = 1

#Dots
dot_pos = []

#Lines
all_lines = []
current_line = []

def text_writing(message,colour, x, y, size):
    font = pygame.font.SysFont('Arial.ttf', size)
    text = font.render(message, False, colour)
    textRect = text.get_rect()
    textRect.center = (x,y)
    win.blit(text, textRect)



#Start Screen
win.fill(WHITE, None, 0)
text_writing('The Sprouts Game', ORANGE, 500, 25, 25) #text_writing Function that asks: Text, Colour, Location and Font Size
text_writing(f'{PlayerOne} score =' + str(PlayerOneScore), BLACK, 125, 20, 12) #Updating Player Score text objects
text_writing(f'{PlayerTwo} score =' + str(PlayerTwoScore), BLACK, 125, 40, 12)
pygame.draw.line(win, BLACK, (0,52), (1000,52)) #Used to mimic an above playing field menu
pygame.display.update() #Flips the screen till first event happens.
#time.sleep(5)

#Instructions screen (Doesn't work as wanted yet)
#pygame.draw.rect(win, WHITE, (250, 300, 500, 200), 0)
#text_writing('The Rules:\n1. Not more than 3 lines per dot. Ect.', BLACK, 500, 300, 25)

#Start Initial Sequence - draw 3 dots
def start_sequence():
    for i in range(3):
        random_pos = (random.randint(100,900), random.randint(100,500))
        pygame.draw.circle(win, RED, (random_pos), 10, 10)
        dot_pos.append(random_pos)
        print(dot_pos)
    pygame.display.update()


start_sequence()

#Main Game loop
def sprouts():
    LineMode = True
    DrawingLine = False
    DotMode = False
    while True:
    #While GameRun = True <- May change this out later 
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if LineMode:

                        #Starts line:
                        if DrawingLine == False: 
                            DrawingLine = True
                            current_line = []
                            current_line.append(event.pos)
                            last_point = event.pos

                            #Updates text box:
                            pygame.draw.rect(win, WHITE, (250, 5, 500, 46), 0)
                            pygame.display.update()
                            text_writing('Draw a dot on the line you just drew', ORANGE, 500, 25, 25)
                        
                        
                        #Ends line
                        elif DrawingLine == True: 
                            DrawingLine = False
                            LineMode = False
                            DotMode = True
            
                    
                    #Draws dot
                    elif DotMode: 
                        currentdotposition = event.pos
                        #Ensure they're not too close to existing dot:
                        if check_dots(currentdotposition) == False:
                            #Updates text book:
                            pygame.draw.rect(win, WHITE, (250, 5, 500, 46), 0)
                            pygame.display.update()
                            text_writing('Too close to existing dot', RED, 500, 25, 20) 
                        
                        else:
                            #Draws dot:
                            DrawingLine = False
                            draw_dot(currentdotposition, BLUE)
                            dot_pos.append(currentdotposition) #Saves location

                            #Updates text book:
                            pygame.draw.rect(win, WHITE, (250, 5, 500, 46), 0)
                            pygame.display.update()
                            text_writing('Draw a line starting from a dot', ORANGE, 500, 25, 25)

                            #Switches back to line drawing:
                            DotMode = False
                            LineMode = True


            #Connects start and end with line:
            elif event.type == pygame.MOUSEMOTION:
                if DrawingLine:
                    current_point = pygame.mouse.get_pos()
                    pygame.draw.line(win, BLACK, last_point, current_point)
                    last_point = current_point 
                    current_line.append(last_point) #Saves line location

                 
        pygame.display.update()
    
        clock.tick(10) #10 Frames per second

        

    

#Draws a dot anywhere, of any colour
def draw_dot(position, dot_colour):
    pygame.draw.circle(win, dot_colour, (position), 10, 10)
    pygame.display.update()


#Attempt at seperating draw line as function, this didn't work as well.
def draw_line():
    last_pos = None
    drawing = False
    line_drawn = []
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            
            elif event.type == pygame.MOUSEMOTION:
                if (drawing):
                    mouse_position = pygame.mouse.get_pos()

                    if last_pos is not None:
                        pygame.draw.line(win, BLACK, last_pos, mouse_position, 1)
                    last_pos = mouse_position

            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_position = (0, 0)
                drawing = False


            elif event.type == pygame.MOUSEBUTTONDOWN:
                drawing = True
                print(line_drawn)

            #while drawing == True:
                #line_drawn.append(last_post)

        pygame.display.update()


#Distance function
def distance(dot1, dot2):
    return math.sqrt((dot1[0] - dot2[0])**2 + (dot1[1] - dot2[1])**2)

#Checks whether placed dot is too close to existing dot
def check_dots(currentdotposition):
    for dot in dot_pos:
        if distance((dot), (currentdotposition)) < 30:
            return False 
    return True





if __name__ == '__main__':
    sprouts()





#To Do:

#Line drawing will only work if starting at dot location, ending at dot location
#Only allows three lines per one dot
#Line can't cross itself

#Keep and assign score. 



