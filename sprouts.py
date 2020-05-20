import pygame
from pygame import *
import sys
import time
import random
import math

#Contains Game Settings: sproutset.py on Github
from sproutset import Settings

####OBJECTS - Will move later to .py or class
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
NumberStartingDots = 3

#Dots
dot_pos = []

#Lines
all_lines = []
current_line = []

####SPROUTS
def sprouts():
    global ss
    #Start Screen
    win.fill(ss.WHITE, None, 0)
    text_writing('The Sprouts Game', ss.BLACK, 500, 25, 25) #Textwriting function
    text_writing(f'{PlayerOne} score =' + str(PlayerOneScore), ss.BLACK, 125, 20, 12) #Updating Player Score text objects
    text_writing(f'{PlayerTwo} score =' + str(PlayerTwoScore), ss.BLACK, 125, 40, 12)
    pygame.draw.line(win, ss.BLACK, (0,52), (1000,52)) #Used to mimic an above playing field menu
    pygame.display.update()

    #Instructions screen 
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
                            start_line = event.pos
                            if check_line(start_line) == False: #Function: if not on a dot
                                #Updates text box: 
                                error_display(False, True)
                            
                            else:
                                DrawingLine = True
                                current_line = []
                                current_line.append(start_line)
                                #Updates text box:
                        
                        #Ends line
                        elif DrawingLine == True: 
                            DrawingLine = False
                            LineMode = False
                            DotMode = True
                            redraw_box()
                            text_writing('Place dot on the line just drawn', ss.ORANGE, 500, 25, 25)
                    
                    #Draws dot
                    elif DotMode: 
                        currentdotposition = event.pos
                        if check_dots(currentdotposition) == False: #Function: if placed on existing dot
                            #Updates text box:
                            error_display(True, False)
                        
                        else:
                            #Draws dot:
                            DrawingLine = False
                            if distance_check == True: #<--- This function creates problem.
                                draw_dot(currentdotposition, ss.BLUE)
                                dot_pos.append(currentdotposition) #Saves location
                                redraw_box()
                                text_writing('Draw a line starting from any dot', ss.ORANGE, 500, 25, 25)

                            else:
                                #Updates text box: (Will implement in error function later)
                                redraw_box()
                                text_writing('Error: Place dot on line', ss.ORANGE, 500, 25, 25)
                                

                            #Switches back to line drawing:
                            DotMode = False
                            LineMode = True
                            

            #Connects start and end with line:
            elif event.type == pygame.MOUSEMOTION: #Move mouse
                if DrawingLine:
                    current_point = pygame.mouse.get_pos()
                    if distance(start_line, current_point) > 30: #Only starts drawing if 30pix away from dot, resulting in less coordinates
                        pygame.draw.line(win, ss.BLACK, start_line, current_point)
                        start_line = current_point 
                        current_line.append(start_line) #Saves line location
                    
                 
        pygame.display.update()
    
        clock.tick(10) #10 Frames per second


####FUNCTIONS

#Writes all text 
def text_writing(message,colour, x, y, size):
    font = pygame.font.SysFont('Arial.ttf', size)
    text = font.render(message, False, colour)
    textRect = text.get_rect()
    textRect.center = (x,y)
    win.blit(text, textRect)

#Updates text box surface - Will use to update score 
def redraw_box():
    pygame.draw.rect(win, ss.WHITE, (250, 5, 500, 46), 0)
    pygame.display.update()

#Displays error messages
def error_display(error_line, error_dot):
    if error_line:
        redraw_box()
        text_writing('Error: Too close to existing dot', ss.RED, 500, 25, 25)
    
    if error_dot:
        redraw_box()
        text_writing('Error: Start line on dot', ss.RED, 500, 25, 25)

#Draws a dot anywhere, of any colour
def draw_dot(position, dot_colour):
    pygame.draw.circle(win, dot_colour, (position), 10, 10)
    pygame.display.update()

#Draws 3 random starter dots - Implements (faulty) distance check just in case of random overlap
def start_sequence():
    temp_list = []
    for i in range(NumberStartingDots):
        random_pos = (random.randint(100,900), random.randint(100,500)) #Manual playing field input to not overlap 'menu box', get too close to sides
        temp_list.append(random_pos)

    for pos in temp_list: #Checks only for exact same coordinates. Needs updating
        if pos not in dot_pos:
            dot_pos.append(pos)
            draw_dot(pos, ss.RED)
            print(dot_pos)
        else:
            print('Overlap')
            start_sequence()

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

#Checks whether line starts on existing dot
def check_line(start_line):
    for dot in dot_pos:
        if distance((dot), (start_line)) < 10:
            return True
    return False

#These two check if a new dot is placed on a line. They don't yet work how I want them to. 
#Calculates distance from point to line (line1 to line2). All arguments are "position" (x, y)
def dist_point_to_line(line1, line2, point):
    x0 = point[0]
    y0 = point[1]
    x1 = line1[0]
    y1 = line1[1]
    x2 = line2[0]
    y2 = line2[1]
    px = x2-x1
    py = y2-y1
    norm = px*px + py*py
    u =  ((x0 - x1) * px + (y0 - y1) * py) / float(norm)
    if u > 1:
        u = 1
    elif u < 0:
        u = 0
    x = x1 + u * px
    y = y1 + u * py
    dx = x - x0
    dy = y - y0
    dist = sqrt(dx*dx + dy*dy)
    return dist

#Check to implement:
def distance_check():
    if dist_point_to_line(current_line, (current_line -1), dot_pos) < 80:
        return True
    return False
    

if __name__ == '__main__':
    sprouts()


####TO DO
#Distance Check Update - random dots 

#Update line end - only at dot location.
#Only allows three lines per one dot.
#Line can't cross itself... no idea.

#Keep and assign score. 

#Implement GAME OVER
