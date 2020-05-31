import sys
import random
import time
from typing import NamedTuple
from math import sqrt
import pygame
import pygame_menu 
import shapely 
from shapely.geometry import LineString, Point
from pygame.locals import *

#Contain game settings
from sproutset import *

####OBJECTS
#Game Window - Creation
pygame.init()
ss = Settings()
win = pygame.display.set_mode((ss.width, ss.height))
pygame.display.set_caption("The Sprouts Game")
clock = pygame.time.Clock()

#Player - Objects used to assign turn, keep score
active_player = 0
PlayerOneScore = 0
PlayerTwoScore = 0

#Object to implement game over after 3 warnings
warningCount = 0
Winner = ''

names = input("Hello Players! Please enter your names seperated by a space: ")
names_list = []
names_list = names.split() 
PlayerOne = names_list[0]
PlayerTwo = names_list[1]

#Keeps track of coordinates:
#Dots
class position(NamedTuple):
    x: int
    y: int

class pointclass(NamedTuple):
    position: position
    line_count: int = 0

dot_pos = []

#Lines
alllines = []

#User input decides game difficulty.
NumberStartingDots = int(input("With how many starting dots do you want to play sprouts? "))

####Starts here:
####MAIN MENU
def main_menu():
    win = pygame.display.get_surface()
    win.fill(ss.BLACK, None, 0)

    my_theme = pygame_menu.themes.Theme(
        background_color = (0, 0, 0, 0), 
        title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_UNDERLINE,
        title_font = "Arial.ttf") #Custom theme
    menu = pygame_menu.Menu(599, 999, title = "The Sprouts Game", theme = my_theme) #Window
    #menu.add_text_input('Player 1: ', onreturn = get_text_input) #<- no option to retrieve input that worked for me
    menu.add_button("Play", sprouts, font_color = ss.GREEN) #If pressed, starts sprouts()
    menu.add_button("Instructions", rules, font_color = ss.WHITE) #If pressed, displays rules
    menu.mainloop(win) #"draws"

    pygame.display.update()
    
####SPROUTS
def sprouts():
    global warningCount
    #Initialise window
    win.fill(ss.WHITE, None, 0)
    pygame.draw.line(win, ss.BLACK, (1, 50), (1000, 50))
    pygame.display.update()

    # create the initial points and empties lists for if multiple games played consequetively
    start_sequence(NumberStartingDots)
    # draw all points to screen
    redraw_dots()

    global active_player
    active_player = 1
    warningCount = 0
    line_colour = ss.FORESTGREEN 

    #Game Modes
    LineMode = True
    DrawingLine = False
    DotMode = False
    last_pos = None
    text_writing("Start by selecting a dot", "info")

 ####MAIN GAME LOOP:
    while True:
        game_over()
        #Starts collecting key and mouse events from here
        for event in pygame.event.get():
            if event.type == QUIT: #If 'x' pressed
                pygame.quit()
                sys.exit()  #Exit game feature
  
            elif event.type == MOUSEBUTTONDOWN: #If left mouse pressed
                if LineMode:
                    if event.button == 1: # mouse click with left button

                        #EVENT 1
                        #Starts Line:
                        if not DrawingLine:
                            start_line = event.pos
                            #Rule implement: if start line on dot:
                            if connecttovalidpoint(start_line):
                                start_line = dot_pos[dotID(start_line)].position
                                DrawingLine = True
                                current_line = []
                                current_line.append(start_line)
                                last_pos = start_line
                                redraw_dots()
                                text_writing("Connect line to any dot", "info")
                                
                            else:
                                text_writing("Error: start line on dot", "warning")
                        
                        #EVENT 3
                        #Ends Line:
                        else: #DrawingLine = True
                            end_line = event.pos
                            #Rule implement: if line intersects:
                            if intersect_check(current_line):
                                text_writing("Error: lines cant intersect. Nr of warnings: " +str(warningCount +1), "error")
                                warningCount += 1

                                #Erases line just drawn.
                                DrawingLine = False
                                redraw_lines(False)
                                reducelinecount(start_line)
                                redraw_dots()

                            elif connecttovalidpoint(end_line):
                                #Rule implement: if line ends on existing dot
                                end_line = dot_pos[dotID(end_line)].position
                                current_line.append(end_line)

                                #Saves line permanently:
                                alllines.append(current_line)
                                redraw_lines(True)
                                redraw_dots()
                                
                                #Goed back to dot mode
                                DrawingLine = False
                                LineMode = False
                                DotMode = True
                                text_writing("Place dot on the line just drawn", "info")

                            else:
                                text_writing("Error: end line on valid dot. Nr of warnings: " +str(warningCount +1), "warning")
                                warningCount += 1

                                #Removes line drawn
                                DrawingLine = False
                                reducelinecount(start_line)
                                redraw_lines(False)
                                redraw_dots()


                #EVENT 4
                #Draws Dot        
                elif DotMode:
                    if event.button == 1:
                        #Rule check: Whether new dot placed on last line drawn.
                        if dot_on_line(event.pos, current_line):
                            redraw_lines(False)
                            redraw_dots()
                            
                            #Assigns score
                            add_score(active_player)
                            #Assigns score here as 'turn' completed by placing dot on line.

                            #Switches active player
                            if active_player == 1:
                                active_player = 2
                            else:
                                active_player = 1
                            
                            #Switches back to line drawing
                            warningCount = 0 #Resets back to 0 for new player
                            DotMode = False
                            LineMode = True
                            text_writing("Draw a line starting from any dot", "info")
                        else:
                            redraw_dots()
                            text_writing("Error: draw dot on last line drawn", "warning")


            #EVENT 2
            #Draws Line
            elif event.type == MOUSEMOTION: #If mouse movement detected.
                if LineMode:
                    if DrawingLine:
                        current_point = pygame.mouse.get_pos()
                        #Will start drawing line in increments of 20pix
                        if distance(last_pos, current_point) > 20: 
                            current_line.append(current_point)
                            pygame.draw.line(win, line_colour, last_pos, current_point, 2)
                            last_pos = current_point

            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    if LineMode:
                        if DrawingLine:
                            DrawingLine = False
                            redraw_lines(False)
                            reducelinecount(start_line)
                            redraw_dots()

        pygame.display.update()
        clock.tick(10)  #10 frames per second 

####FUNCTIONS
#Writes all game text 
def text_writing(message, texttype):
    win = pygame.display.get_surface()
    text_area = ((0, 0), (999, 48))

    #Locations:
    player_text_pos = (80, 25)
    status_text_pos = (500, 25)
    score_text_pos1 = (900, 15)
    score_text_pos2 = (900, 35)
    pygame.draw.rect(win, ss.WHITE, (text_area))

    #Changes colour dependant on type of text: 
    statuscolor = ss.BLACK #Instructional
    if texttype == "error": #Error message
        statuscolor = ss.RED
    elif texttype == "warning": #Warning message
        statuscolor = ss.ORANGE
    
    #Updating status text objects 
    font = pygame.font.Font("Arial.ttf", 18) 
    text = font.render(message, True, statuscolor, None) 
    textRect = text.get_rect()  
    textRect.center = status_text_pos
    win.blit(text, textRect)

    #Updating 'active player' text object
    font = pygame.font.Font("Arial.ttf", 18) 
    text = font.render("Player: " + names_list[active_player - 1], True, ss.BLACK, None) 
    textRect = text.get_rect()
    textRect.center = player_text_pos
    win.blit(text, textRect)

    #Two score text objects
    font = pygame.font.Font("Arial.ttf", 13)
    scoretext = (str(PlayerOne) + " score: " + str(PlayerOneScore)) 
    text = font.render(scoretext, True, ss.BLACK, None)
    textRect = text.get_rect()
    textRect.center = score_text_pos1
    win.blit(text, textRect)
    
    scoretext = (str(PlayerTwo) + " score: " + str(PlayerTwoScore)) 
    text = font.render(scoretext, True, ss.BLACK, None)
    textRect = text.get_rect()
    textRect.center = score_text_pos2
    win.blit(text, textRect)

    pygame.display.update(text_area)

#Creates the initial n random starting locations of the game. 
def start_sequence(n):
    i = 0
    while i < n: 
        x = random.randint(100,900) #Manually limited potential placement field.
        y = random.randint(100, 500)

        #Checks if their not too close to one another
        if not check_dots((x, y)):
            #Appends their location and initiates 'nr of lines coming from it' as 0.
            dot_pos.append(pointclass((x, y), 0))
            i += 1

#Implements game over sequence. 
#As game over in sprouts is seen visually, it just works when three warnings recieved. 
def game_over():
    global Winner
    if warningCount == 3:
        if PlayerOneScore > PlayerTwoScore:
            Winner = PlayerOne

        elif PlayerTwoScore > PlayerOneScore:
            Winner = PlayerTwo

        elif PlayerOneScore == PlayerTwoScore:
            if active_player == 1:
                Winner = PlayerTwo

            else:
                Winner = PlayerOne

        #Clears lists for if want to play again. 
        dot_pos.clear()           
        alllines.clear()
        end_screen()

#Assigns score to player:
def add_score(player):
    global PlayerOneScore
    global PlayerTwoScore
    if player == 1:
        PlayerOneScore += 1
    else:
        PlayerTwoScore += 1

#Distance function
def distance(dot1, dot2):
    distance = sqrt((dot1[0] - dot2[0])**2 + (dot1[1] - dot2[1])**2)
    return distance

##These two functions check if a new dot is placed on the last line:
#i. Calculates distance from dot to line (line1 to line2). All arguments are "position" (x, y)
def dist_point_to_line(line1, line2, point):
    #Adapted from: https://stackoverflow.com/a/2233538
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

#ii. Checks whether dot position is on last line drawn and also not on existing dot.
def dot_on_line(position, linestring):
    #Rule Check 1: If not too close to existing dot
    if not check_dots(position):
        #Rule Check 2: If on last line drawn
        for i in range(len(linestring) - 1):
            if linestring[i] != linestring[i + 1]: #function crashes on zero length line segment
                d = dist_point_to_line(linestring[i], linestring[i + 1], position)
                if d < 8: # margin
                    #This appends dot location, and increases 'nr of lines coming from it' by 2
                    #As placing a correct dot on a line theoretically 'splits it' into two lines.
                    dot_pos.append(pointclass(position, 2)) 
                    return True #Correct placement
    return False

#Checks whether placed dot is too close to existing dot (including margin)
def check_dots(position):
    for dot in dot_pos:
        if distance(position, dot.position) <= 20:
            return True #Too close
    return False

##These two functions draw the actual lines/dots to the surface:
#i. Loops through all dot locations, (re)draws them and updates the game surface
def redraw_dots():
    for dot in dot_pos:
        if dot.line_count < 3: #If less than 3 lines attached to dot, they'll be green.
            pygame.draw.circle(win, ss.GREEN, dot.position, 10, 10)
        else:
            pygame.draw.circle(win, ss.RED, dot.position, 10, 10)
    pygame.display.update((0, 52), (999, 549)) #replace with ss.height ect

#ii. Loops through all line locations, re(draws) them and updates the game surface
def redraw_lines(last_line_different_colour):
    game_area = (0, 52, 1000, 599)
    pygame.draw.rect(win, ss.WHITE, game_area)
    for i in range(len(alllines)):
        if last_line_different_colour and i == len(alllines) - 1:
            pygame.draw.lines(win, ss.RED, False, alllines[i], 2) 
        else: #Changes colour dependant on state
            pygame.draw.lines(win, ss.ORANGE, False, alllines[i], 2) 
    pygame.display.update(game_area)

##These two functions check whether line starts and ends at dot:
#i. Finds the index of a dot in [dot_pos] at a given position (within a margin)
def dotID(position):
    for i in range(len(dot_pos)):
        if distance(position, dot_pos[i].position) <= 8:
            return i
    return -1

#ii. Checks that line both starts and ends at dot and that it has < 3 lines attached to it.
def connecttovalidpoint(position):
    i = dotID(position)
    if i >= 0:
        if dot_pos[i].line_count < 3:
            dot_pos[i] = dot_pos[i]._replace(line_count = dot_pos[i].line_count + 1)
            return True
    return False

#Reduces linecount of dot at specified position by 1
def reducelinecount(position):
    i = dotID(position)
    if i >= 0:
        dot_pos[i] = dot_pos[i]._replace(line_count = dot_pos[i].line_count - 1)
        return True
    return False

#These two check check whether line intersects with existing line:
def line_intersection(line1, line2): 
    ls1 = LineString(line1)
    ls2 = LineString(line2)

    if ls1.distance(ls2) < 0.1:
        return True 
    
    else:
        return False

#The old function: 
def old_line_intersection(line1, line2):
    #Adapted from: https://stackoverflow.com/questions/20677795/how-do-i-compute-the-intersection-point-of-two-lines
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
       #raise Exception('lines do not intersect')
       return False

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div

    #This didn't work all the time, so resorted to importing shapely. 
    if ((x < line1[0][0] or x < line2[0][0] or x > line1[1][0] or x > line2[1][0]) and \
        (y < line1[0][1] or y < line2[0][1] or y > line1[1][1] or y > line2[1][1])):
        return False
    else:
        return True #intersect

#Checks for line intersections
def intersect_check(linestring):

    #First checks if it doesn't intersect itself
    for i in range(len(linestring) - 1):
        segment1 = (linestring[i], linestring[i+ 1])
        for j in range(len(linestring) - 1):
            segment2 = (linestring[j], linestring[j + 1])
            if (j != i) and (j != i - 1) and (j != i + 1): #Segment can't check itself or its neighbours
                if line_intersection(segment1, segment2):
                    return True

    #Then checks all other existing lines
    for existingline in alllines:
        for i in range(len(existingline) - 1):
            existingsegment = (existingline[i - 1], existingline[i])
            for j in range(1, (len(linestring) - 2)): #Doesn't check first and last segments, false positives
                linesegment = (linestring[j], linestring[j + 1])
                intersection = line_intersection(existingsegment, linesegment)
                if intersection:
                    return True

    return False

#Idea for function to check if remaining turns available & implement game over
def checkfreepoints():
    freepoints = 0
    for point in dot_pos:
        if point.line_count < 3:
            freepoints += 1
    return freepoints
    pass

#This function writes the menu text.
def menu_writing(message,colour, x, y, size):
    font = pygame.font.SysFont('Arial.ttf', size)
    text = font.render(message, True, colour)
    textRect = text.get_rect()
    textRect.center = (x,y)
    win.blit(text, textRect)

#GUI - Instruction window 
def rules():
    win = pygame.display.get_surface()
    win.fill(ss.BLACK, None, 0)

    #Any form of 'new line' technique doesn't work using pygame_menu. This was the only way:
    menu_writing("Welcome " + str(PlayerOne) + " and " + str(PlayerTwo) + ", to the Sprouts Game!", ss.WHITE, 500, 150, 25)
    menu_writing('Simply draw a line starting and ending at a dot then place a new dot on that line.', ss.WHITE, 500, 180, 20)
    menu_writing('The Rules:', ss.WHITE, 500, 240, 20)
    menu_writing('1. Any line drawn must start and end on an existing dot (including the starting dot).', ss.WHITE, 500, 270, 20)
    menu_writing('2. Any line drawn may not cross an existing line.', ss.WHITE, 500, 300, 20)
    menu_writing('3. Any one dot may have no more than three lines attached to it.', ss.WHITE, 500, 330, 20)
    menu_writing('The player to draw the last valid line is the winner!', ss.WHITE, 500, 410, 20)
    menu_writing('The game will end when 3 warnings are recieved', ss.WHITE, 500, 440, 20)
    menu_writing('Press Space to return to menu.', ss.WHITE, 500, 500, 20)
    
    pygame.display.update()

    while True:
        for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE: #Return to main_menu()
                        main_menu()
                        
                elif event.type == QUIT: #Exits game window
                    pygame.quit()
                    sys.exit()

#GUI - Game Over window that also declares winner
def end_screen():
    win = pygame.display.get_surface()
    win.fill(ss.BLACK, None, 0)

    menu_writing("Game Over!", ss.RED, 500, 240, 40)
    menu_writing("Well done! The winner is: " + str(Winner), ss.WHITE, 500, 300, 20)
    menu_writing("Press space to try again.", ss.WHITE, 500, 360, 20)

    pygame.display.update()

    while True:
        for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE: #Return to main_menu()
                        main_menu()
                        
                elif event.type == QUIT: #Exits game window
                    pygame.quit()
                    sys.exit()

if __name__ == '__main__':
    main_menu()
