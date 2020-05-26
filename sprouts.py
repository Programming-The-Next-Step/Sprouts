from math import sqrt
import sys
import time
import random
import pygame
import pygame_menu
from pygame import *


#Contains Game Settings: sproutset.py on Github
from sproutset import Settings

####OBJECTS 
#Game Window 
pygame.init()
ss = Settings()
win = pygame.display.set_mode((ss.width, ss.height))
pygame.display.set_caption('The Sprouts Game')

clock = pygame.time.Clock()

#Player
PlayerOne = ''
PlayerOneScore = 0

PlayerTwo = ''
PlayerTwoScore = 0

NumberStartingDots = 3 #Can be changed to update N dots starting the game with.

#Dots
dot_pos = []

#Lines
final_lines = []
current_line = []

score = 0

####MAIN MENU
def main_menu():
    global win
    global PlayerOne
    global PlayerTwo

    my_theme = pygame_menu.themes.Theme(
    background_color = (0, 0, 0, 0), 
    title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_UNDERLINE,
    title_font = 'Arial.ttf')
    menu = pygame_menu.Menu(599, 999, title = 'The Sprouts Game', theme = my_theme)

    menu.add_text_input('Player 1: ') 
    #PlayerOne = Text_input_result()
    menu.add_text_input('Player 2: ')
    #PlayerTwo = Text_input_result()
 
    menu.add_button('Play', sprouts, font_color = ss.WHITE)
    menu.add_button('The Rules', rules, font_color = ss.WHITE)
    menu.mainloop(win)
    

####SPROUTS GAME
def sprouts():
    global ss

    #Starts screen surface:
    win.fill(ss.WHITE, None, 0)

    #Title
    text_writing('Begin by selecting any dot to start your line', ss.BLACK, 500, 25, 25) #Title
    text_writing(f'{PlayerOne} score = ' + str(PlayerOneScore), ss.BLACK, 900, 20, 12) #Updating Player Score text objects
    text_writing(f'{PlayerTwo} score = ' + str(PlayerTwoScore), ss.BLACK, 900, 40, 12)
    pygame.draw.line(win, ss.BLACK, (0,52), (1000,50)) 
    pygame.display.update()  

    start_sequence() #Function that draws n random starting dots
    
    #Game Modes
    global current_line
    LineMode = True
    DrawingLine = False
    DotMode = False

    running = True

    ####MAIN GAME LOOP:
    while running:
        #Starts collecting key and mouse events from here
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: #Exit game fature
                running = False
                pygame.quit()
                sys.exit()

            #EVENT 1 
            elif event.type == pygame.MOUSEBUTTONDOWN: 
                if event.button == 1: #If left mouse button pressed.
                    if LineMode:

                        #Starts line:
                        if DrawingLine == False: 
                            start_line = event.pos
                            if check_start(start_line) == False: #Function: if don't start line on dot:
                                #Updates text box: 
                                error_display(False, True)
                            
                            else:
                                DrawingLine = True
                                current_line = []
                                current_line.append(start_line)
                                redraw_box(250, 5)
                                text_writing('Connect line to any dot', ss.ORANGE, 500, 25, 25)
                        
                        #EVENT 3
                        #Ends line
                        elif DrawingLine == True: 
                            end_line = event.pos
                            if check_end(end_line) == True:
                                redraw_box(250, 5)
                                text_writing('Error: End line on existing dot', ss.RED, 500, 25, 25)

                            else:
                                DrawingLine = False
                                LineMode = False
                                DotMode = True
                                redraw_box(250, 5)
                                text_writing('Place dot on the line just drawn', ss.ORANGE, 500, 25, 25)
                                final_lines.append(current_line) #Permanently stores last line
                    
                    #EVENT 4
                    #Dot drawing
                    elif DotMode: 
                        #DrawingLine = False
                        currentdotposition = event.pos
                        #First check: Whether new dot is placed too close to existing dot.
                        if check_dots(currentdotposition) == False: 
                            error_display(True, False)
                        
                        else:
                            DrawingLine = False
                            #Second Check: Whether new dot is placed on last line drawn:
                            if distance_check(currentdotposition) == True:
                                draw_dot(currentdotposition, ss.BLUE)
                                dot_pos.append(currentdotposition) #Saves location
                                
                                redraw_box(250, 5)
                                text_writing('Well done!', ss.GREEN, 500, 25, 25)
                                
                                pygame.time.delay(500)

                                redraw_box(250, 5)
                                text_writing('Draw a line starting from any dot', ss.ORANGE, 500, 25, 25)
                                
                                #PlayerOneScore += 1

                                #Switches back to line drawing:
                                DotMode = False
                                LineMode = True

                            else:
                                redraw_box(250, 5)
                                text_writing('Error: Place dot on last line drawn', ss.RED, 500, 25, 25)
                            
            #EVENT 2                                               
            #Connects start and end with line:
            elif event.type == pygame.MOUSEMOTION: #If mouse movement detected.
                if DrawingLine:
                    current_point = pygame.mouse.get_pos()
                    #Will start drawing line in increments of 30pix:
                    if distance(start_line, current_point) > 30: 
                        pygame.draw.line(win, ss.BLACK, start_line, current_point)  
                        start_line = current_point 
                        current_line.append(start_line) #Saves line location
                    
                 
        pygame.display.update()
    
        clock.tick(10) #10 Frames per second


####FUNCTIONS        
#Writes all text 
def text_writing(message,colour, x, y, size):
    font = pygame.font.SysFont('Arial.ttf', size)
    text = font.render(message, True, colour)
    textRect = text.get_rect()
    textRect.center = (x,y)
    win.blit(text, textRect)

#Updates text box surface - Will use to update score 
def redraw_box(x, y):
    pygame.draw.rect(win, ss.WHITE, (x, y, 500, 46), 0)
    pygame.display.update()

def Text_input_result(text):
    print("",text)

    menu.add_text_input('Player 1: Please enter your name :',onreturn=Text_input_result)

def redraw_game_screen(colour, x, y):
    game_screen = pygame.draw.rect(win, colour, (x, y, 1000, 550), 0)
    game_screen.center = (1000, 225)
    pygame.display.update()

#GUI - Tells rules
def rules():
    global win
    win.fill(ss.BLACK, None, 0)
    redraw_game_screen(ss.BLACK, 1000, 600)
    text_writing('Welcome to the Sprouts Game', ss.WHITE, 500, 200, 25)
    text_writing('The Rules:', ss.WHITE, 500, 230, 25)
    text_writing('1. Line drawn must start and end on any existing dot.', ss.WHITE, 500, 260, 25)
    text_writing('2. Line drawn may not cross an existing line.', ss.WHITE, 500, 290, 25)
    text_writing('3. No one dot may have more than three lines attached to it.', ss.WHITE, 500, 320, 25)
    text_writing('The player to draw the last valid line is the winner.', ss.WHITE, 500, 350, 25)
    text_writing('Press Space to return to menu.', ss.WHITE, 500, 400, 25)
    pygame.display.update()

    while True:
        for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        main_menu()

#Displays error messages
def error_display(error_line, error_dot):
    if error_line:
        redraw_box(250, 5)
        text_writing('Error: Too close to existing dot', ss.RED, 500, 25, 25)
    
    if error_dot:
        redraw_box(250, 5)
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
        else:
            print('Overlap')
            start_sequence()

    pygame.display.update()

#Redraws all objects after validation check: cement valid line w/ new colour and bring dots to foreground. 
def redraw():
    pass

#Distance function
def distance(dot1, dot2):
    return sqrt((dot1[0] - dot2[0])**2 + (dot1[1] - dot2[1])**2)

#Checks whether placed dot is too close to existing dot
def check_dots(currentdotposition):
    for dot in dot_pos:
        if distance((dot), (currentdotposition)) < 30:
            return False 
    return True

#Checks whether line starts on existing dot
def check_start(start_line):
    for dot in dot_pos:
        if distance((dot), (start_line)) < 10:
            return True
    return False

#Checks whether line ends on existing dot
def check_end(end_line):
    for dot in dot_pos:
        if distance((dot), (end_line)) < 10:
            return False
    return True

#These two check if a new dot is placed on the last line. They don't yet work how I want them to. 
#Calculates distance from point to line (line1 to line2). All arguments are "position" (x, y)
def dist_point_to_line(line1, line2, point):
    # adapted from: https://stackoverflow.com/a/2233538
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

#Final Check: Compares new dot drawn to each line coordinate tuple within list.
def distance_check(dotposition):
    for i in range(len(current_line)-1):
        if dist_point_to_line(current_line[i], current_line[i+1], dotposition) < 8:
            return True 
    return False


if __name__ == '__main__':
    main_menu()

####TO DO
#Distance Check Update - random dots 

#Only allows three lines per one dot.

#Line can't cross itself... no idea!!

#Keep and assign score. 

#Implement GAME OVER
