import pygame
from pygame import *
import sys
import time
import random
import math

#Contains Game Settings: sproutset.py on Github
from sproutset import Settings

#Objects
#Game Window 
pygame.init()
ss = Settings()
win = pygame.display.set_mode((ss.width, ss.height))
pygame.display.set_caption('The Sprouts Game')

running = True
clock = pygame.time.Clock()

#Player
PlayerOne = 'Test1'
PlayerOneScore = 0

PlayerTwo = 'Test2'
PlayerTwoScore = 0

turn = 1 

#Dots
dot_pos = []

#Lines
all_lines = []
current_line = []

def sprouts():
    global ss
    #Start Screen
    win.fill(ss.WHITE, None, 0)
    text_writing('The Sprouts Game', ss.BLACK, 500, 25, 25) #Textwriting function
    text_writing(f'{PlayerOne} score =' + str(PlayerOneScore), ss.BLACK, 125, 20, 12) #Updating Player Score text objects
    text_writing(f'{PlayerTwo} score =' + str(PlayerTwoScore), ss.BLACK, 125, 40, 12)
    pygame.draw.line(win, ss.BLACK, (0,52), (1000,52)) #Used to mimic an above playing field menu
    pygame.display.update()

    #Instructions screen here
    #redraw_box()
    #text_writing('The Rules:\n1. Not more than 3 lines per dot. Ect.', ss.BLACK, 500, 300, 25)    
    
    start_sequence() #Function that draws three random starter dots
    
    #Game Modes
    global current_line
    LineMode = True
    DrawingLine = False
    DotMode = False

    ####MAIN GAME LOOP:
    while True:

        #Starts collecting key and mouse events:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #Press 'x' to exit
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: #Press left mouse button
                    if LineMode:

                        #Starts line:
                        if DrawingLine == False: 
                            DrawingLine = True
                            start_line = event.pos
                            if check_line(start_line) == False:

                                #Updates text box:
                                redraw_box()
                                text_writing('Start on dot', ss.RED, 500, 25, 20)
                            
                            else:
                                current_line = []
                                current_line.append(start_line)

                            #Updates text box:
                            redraw_box()
                            text_writing('Draw a dot on the line you just drew', ss.ORANGE, 500, 25, 25)
                        
                        
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
                            #Updates text box:
                            redraw_box()
                            text_writing('Too close to existing dot', ss.RED, 500, 25, 20) 
                        
                        else:
                            #Draws dot:
                            DrawingLine = False
                            draw_dot(currentdotposition, ss.BLUE)
                            dot_pos.append(currentdotposition) #Saves location

                            #Updates text box:
                            redraw_box()
                            text_writing('Draw a line starting from any dot', ss.ORANGE, 500, 25, 25)

                            #Switches back to line drawing:
                            DotMode = False
                            LineMode = True


            #Connects start and end with line:
            elif event.type == pygame.MOUSEMOTION: #Move mouse
                if DrawingLine:
                    current_point = pygame.mouse.get_pos()
                    pygame.draw.line(win, ss.BLACK, start_line, current_point)
                    start_line = current_point 
                    current_line.append(start_line) #Saves line location

                 
        pygame.display.update()
    
        clock.tick(10) #10 Frames per second


#Functions:

#Writes all text 
def text_writing(message,colour, x, y, size):
    font = pygame.font.SysFont('Arial.ttf', size)
    text = font.render(message, False, colour)
    textRect = text.get_rect()
    textRect.center = (x,y)
    win.blit(text, textRect)

#Updates text box surface - Will use to update score later on
def redraw_box():
    pygame.draw.rect(win, ss.WHITE, (250, 5, 500, 46), 0)
    pygame.display.update()

#Draws a dot anywhere, of any colour
def draw_dot(position, dot_colour):
    pygame.draw.circle(win, dot_colour, (position), 10, 10)
    pygame.display.update()

#Draws 3 random starter dots
def start_sequence():
    for i in range(3):
        random_pos = (random.randint(100,900), random.randint(100,500))
        draw_dot(random_pos, ss.RED)
        dot_pos.append(random_pos)
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

#Checks whether line starts on existing dot (This doesn't work yet)
def check_line(start_line):
    for dot in dot_pos:
        if distance((dot), (start_line)) > 20:
            return False
    return True


if __name__ == '__main__':
    sprouts()





#To Do:

#Line drawing will only work if starting at dot location, ending at dot location
#Only allows three lines per one dot
#Line can't cross itself

#Keep and assign score. 

#Implement GAME OVER



#Attempt at seperating draw line as function, this didn't work as well. Ignore.
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
                        pygame.draw.line(win, ss.BLACK, last_pos, mouse_position, 1)
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