#!/usr/bin/python

try:
    import sys
    import math
    import os
    import pygame
    import time
    import thread

    from pygame.locals import *
    from client import *
    from player import *
    from host import *
    import high_score
   
except ImportError, err:
    print "Couldn't laod modulez. %s" % (err)
    sys.exit(2)


def prompt(x,y,prompt_string,font,screen):
    """Create a prompt for a user to enter a string
    Arguments:
    x -- the x location of the input box to be rendered
    y -- the y location of the input box to be rendered
    prompt_string -- the string to be rendered in the input box
    font -- the font to render the strings with
    screen -- the main screen to render on
    Returns:
    return_string -- a string of what the user entered
    """
    #the value to be returned
    return_string=""
    #calculate the size of the input box, and set it to the 
    width,height = font.size(prompt_string)
    height=height*2+10
    width=width+10
    box = pygame.Rect((x-5, y-5), (width,height))
    #draw the blue box around the input    
    screen.fill((0,0,255),box)
    text = font.render(prompt_string,True,(255,255,255))
    screen.blit(text,(x,y))
    #calculate the white part of the input area
    input_area = pygame.Rect((x, y+height/2-5), (width-10,height/2-5))
    #loop until done(set if enter or escape is hit)
    done=False
    while not done:
        #fill the input area with white
        screen.fill((255,255,255),input_area)
        #put what's currently inputted into the input area
        input_text = font.render(return_string,True,(0,0,0))
        screen.blit(input_text,(x,y+height/2-5))
        pygame.display.flip()
        #wait for an event
        event=pygame.event.wait()
        if event.type == pygame.KEYDOWN:
            #if escape was hit assume the user doesn't want to enter anything, return nothing
            if event.key == pygame.K_ESCAPE:
                done=True
                return_string=""
            #if return was hit, assume the user is finished entering text and return what's been entered
            elif event.key == pygame.K_RETURN:
                done=True
            #if backspace is hit, move the carat back one space and destroy the last letter
            elif event.key == pygame.K_BACKSPACE:
                #make sure there's something in the string first, don't want to kill what's not there
                if len(return_string)>0:
                    return_string=return_string[0:len(return_string)-1]
            else:
                #add the typed letter to the string
                return_string=return_string+event.unicode
    return return_string

def load_image(name, colorkey=None):
    """ Load image and return image object"""
    fullname = os.path.join('images', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannot load image:', fullname
        raise SystemExit, message
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey)
    return image

# GLOBALS
#used to control menus and shit
STATE = 0 #0=main_menu, 1=host_options, 2=player_options, 3=invites
BOARD_SIZE = 0
DOT_SIZE = 0
LINE_WIDTH = 1


BLACK_DOT=None
YELLOW_DOT=None
RED_DOT=None
BLUE_DOT=None
GREEN_DOT=None
PURPLE_DOT=None
ORANGE_DOT=None

PLAYER=None


#event handler for actual gameplay
def handle_ev(pos):
    x,y = pos
    x_pos = math.floor(x / DOT_SIZE)
    y_pos = math.floor(y / DOT_SIZE)
    loc = [x_pos, y_pos]
    print loc
    print PLAYER.board.is_dot_at(loc)
    PLAYER.dotClicked(loc)

def draw_board(grid):
    bg = pygame.display.get_surface()
    for foo in grid:
        color, x, y = foo
        rect = dot_rect(x, y)
        if color == None:
            bg.blit(BLACK_DOT, rect)
        if color == 'yellow':
            bg.blit(YELLOW_DOT, rect)
        if color == 'red':
            bg.blit(RED_DOT, rect)
        if color == 'blue':
            bg.blit(BLUE_DOT, rect)
        if color == 'orange':
            bg.blit(ORANGE_DOT, rect)
        if color == 'green':
            bg.blit(GREEN_DOT, rect)
        if color == 'purple':
            bg.blit(PURPLE_DOT, rect)

    #vertical lines
    for i in range(BOARD_SIZE + 1):
        start_pos = ((i * DOT_SIZE) + (i * LINE_WIDTH), 0)
        end_pos = ((i * DOT_SIZE) + (i * LINE_WIDTH), DIMENSION)
        pygame.draw.line(bg, (0,0,0), start_pos, end_pos, LINE_WIDTH)

    #horizontal lines
    for i in range(BOARD_SIZE + 1):
        start_pos = (0, (i * DOT_SIZE) + (i * LINE_WIDTH))
        end_pos = (DIMENSION, (i * DOT_SIZE) + (i * LINE_WIDTH))
        pygame.draw.line(bg, (0,0,0), start_pos, end_pos, LINE_WIDTH)

    # blit everything to the screen
    pygame.display.flip()


def dot_rect(x,y):
    x_new = (x - 1) * DOT_SIZE + x
    y_new = (y - 1) * DOT_SIZE + y
    rect = (x_new, y_new)
    return rect
   
###############################

##   ##     ###  #####  ##  #
# # # #    #  #    #    # # #
#  #  #   #####    #    #  ##
#     #  #    #  #####  #   #

###############################

def main():
    global STATE
    state = STATE

    global BOARD_SIZE
    global DOT_SIZE
    global DIMENSION

    global BLACK_DOT
    global YELLOW_DOT
    global RED_DOT
    global BLUE_DOT
    global GREEN_DOT
    global PURPLE_DOT
    global ORANGE_DOT
    global PLAYER
    global LINE_WIDTH


    # RGB color tuples
    yellow = (255,255,0)
    green = (0,255,0)
    black = (0,0,0)
    white = (255,255,255)
    blue = (0,0,255)
    red = (255,0,0)
    purple = (150,5,255)
    orange = (255,100,5)



    # init screen
    pygame.init()
    screen = pygame.display.set_mode((900, 700))
    pygame.display.set_caption('Splat!')

    # fill background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill(green)
     
    screen.blit(background, (0,0))
    pygame.display.flip()

    ################
    # MENU SHIIIIT #
### host/join menu ###############################
    drawn_host_join_menu = 0
    while state == 0:
        if drawn_host_join_menu == 0:
            font = pygame.font.Font(None, 20)
            menu = pygame.Surface((400,400))
            menu = menu.convert()
            menu.fill((250,250,250))

            host_rect = pygame.Rect(40, 260, 120, 50)
            join_rect = pygame.Rect(240, 260, 120, 50)
            pygame.draw.rect(menu, (190,250,250), host_rect)
            pygame.draw.rect(menu, (190,250,250), join_rect)
            text_ask1 = font.render("Would you like to host a",1,(0,0,0))
            text_ask2 = font.render("game or join a game?",1,(0,0,0))
            text_ask1_rect = text_ask1.get_rect()
            text_ask2_rect = text_ask2.get_rect()
            text_ask1_rect.centery = 50
            text_ask1_rect.centerx = 200
            text_ask2_rect.centery = 70
            text_ask2_rect.centerx = 200
            menu.blit(text_ask1, text_ask1_rect)
            menu.blit(text_ask2, text_ask2_rect)
            text_host = font.render("Host", 1, (0,0,0))
            text_join = font.render("Join", 1, (0,0,0))
            menu.blit(text_host, host_rect)
            menu.blit(text_join, join_rect)

            background.blit(menu, (250,100))
            screen.blit(background, (0,0))
            pygame.display.flip()

            host_rect.top = 360
            host_rect.left = 290
            join_rect.top = 360
            join_rect.left = 490

            drawn_host_join_menu = 1
        else:
            for event in pygame.event.get():
                if event.type == QUIT:
                    raise SystemExit
                    screen.blit(background, (0, 0))
                    pygame.display.flip()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.display.quit()
                        sys.exit()
                if event.type == MOUSEBUTTONUP:
                    if host_rect.collidepoint(event.pos):
                        state = 1
                        background.fill(green)
                        screen.blit(background, (0,0))
                        pygame.display.flip()
                    if join_rect.collidepoint(event.pos):
                        state = 2
                        background.fill(green)
                        screen.blit(background, (0,0))
                        pygame.display.flip()





### host options #####################################
    drawn_host_options = 0
    while state == 1:
        if drawn_host_options == 0:
        #draw
            host_menu = pygame.Surface((600,250))
            host_menu = host_menu.convert()
            host_menu.fill(white)

            yellow_rect = pygame.Rect(0,0,100,100)
            pygame.draw.rect(host_menu, yellow, yellow_rect)
            green_rect = pygame.Rect(100,0,100,100)
            pygame.draw.rect(host_menu, green, green_rect)
            blue_rect = pygame.Rect(200,0,100,100)
            pygame.draw.rect(host_menu, blue, blue_rect)
            red_rect = pygame.Rect(300,0,100,100)
            pygame.draw.rect(host_menu, red, red_rect)
            purple_rect = pygame.Rect(400,0,100,100)
            pygame.draw.rect(host_menu, purple, purple_rect)
            orange_rect = pygame.Rect(500,0,100,100)
            pygame.draw.rect(host_menu, orange, orange_rect)


            p2_rect = pygame.Rect(50, 100, 100, 50)
            p2 = load_image('player2.png')
            host_menu.blit(p2, p2_rect)
            p3_rect = pygame.Rect(150, 100, 150, 50)
            p3 = load_image('player3.png')
            host_menu.blit(p3, p3_rect)
            p4_rect = pygame.Rect(300, 100, 200, 50)
            p4 = load_image('player4.png')
            host_menu.blit(p4, p4_rect)            
            pygame.draw.line(host_menu, black, (50, 100), (50, 150))
            pygame.draw.line(host_menu, black, (150, 100), (150, 150))
            pygame.draw.line(host_menu, black, (300, 100), (300, 150))
            pygame.draw.line(host_menu, black, (500, 100), (500, 150))
            pygame.draw.line(host_menu, black, (0, 150), (500, 150))

            b6_rect = pygame.Rect(0, 150, 50, 50)
            b6 = load_image('6x6.png')
            host_menu.blit(b6, b6_rect)
            b7_rect = pygame.Rect(50, 150, 50, 50)
            b7 = load_image('7x7.png')
            host_menu.blit(b7, b7_rect)
            b8_rect = pygame.Rect(100, 150, 50, 50)
            b8 = load_image('8x8.png')
            host_menu.blit(b8, b8_rect)
            b9_rect = pygame.Rect(150, 150, 50, 50)
            b9 = load_image('9x9.png')
            host_menu.blit(b9, b9_rect)
            b10_rect = pygame.Rect(200, 150, 50, 50)
            b10 = load_image('10x10.png')
            host_menu.blit(b10, b10_rect)
            pygame.draw.line(host_menu, black, (50, 150), (50, 200))
            pygame.draw.line(host_menu, black, (100, 150), (100, 200))
            pygame.draw.line(host_menu, black, (150, 150), (150, 200))
            pygame.draw.line(host_menu, black, (200, 150), (200, 200))
            pygame.draw.line(host_menu, black, (250, 150), (250, 200))
            pygame.draw.line(host_menu, black, (0, 200), (250, 200))
            pygame.draw.line(host_menu, black, (0, 150), (500, 150))

            background.blit(host_menu, (0,0))
            screen.blit(background, (0,0))
            pygame.display.flip()            
            #
            drawn_host_options = 1
        else:
            for event in pygame.event.get():
                if event.type == QUIT:
                    raise SystemExit
                    screen.blit(background, (0, 0))
                    pygame.display.flip()
                if event.type == MOUSEBUTTONUP:
                    if yellow_rect.collidepoint(event.pos):
                        player_color = 'yellow' #fix
                    if green_rect.collidepoint(event.pos):
                        player_color = 'green' #fix
                    if blue_rect.collidepoint(event.pos):
                        player_color = 'blue' #fix
                    if red_rect.collidepoint(event.pos):
                        player_color = 'red' #fix
                    if purple_rect.collidepoint(event.pos):
                        player_color = 'purple' #fix
                    if orange_rect.collidepoint(event.pos):
                        player_color = 'orange' #fix
                    #cant play with only 1 player
                    
                    if p2_rect.collidepoint(event.pos):
                        num_players = 2 #fix
                    if p3_rect.collidepoint(event.pos):
                        num_players = 3 #fix
                    if p4_rect.collidepoint(event.pos):
                        num_players = 4 #fix
                    if b6_rect.collidepoint(event.pos):
                        BOARD_SIZE = 6 #fix
                    if b7_rect.collidepoint(event.pos):
                        BOARD_SIZE = 7 #fix
                    if b8_rect.collidepoint(event.pos):
                        BOARD_SIZE = 8 #fix
                    if b9_rect.collidepoint(event.pos):
                        BOARD_SIZE = 9 #fix
                    if b10_rect.collidepoint(event.pos):
                        BOARD_SIZE = 10 #fix
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.display.quit()
                        sys.exit()
                    if event.key == K_RETURN:
                        player_name = prompt(10,217,"Please enter your name:", font,screen)                        #fix^
			PLAYER = Host(player_name, player_color, None)
                        #fix^
                        state = 3
                        background.fill(green)
                        screen.blit(background, (0,0))
                        pygame.display.flip()







### join options ########################################

    #fix
    player_name = ""

    drawn_join_options = 0
    while state == 2:
        if drawn_join_options == 0:
            join_menu = pygame.Surface((600,200))
            join_menu = join_menu.convert()
            join_menu.fill((255,255,255))

            yellow_rect = pygame.Rect(0,0,100,100)
            pygame.draw.rect(join_menu, yellow, yellow_rect)
            green_rect = pygame.Rect(100,0,100,100)
            pygame.draw.rect(join_menu, green, green_rect)
            blue_rect = pygame.Rect(200,0,100,100)
            pygame.draw.rect(join_menu, blue, blue_rect)
            red_rect = pygame.Rect(300,0,100,100)
            pygame.draw.rect(join_menu, red, red_rect)
            purple_rect = pygame.Rect(400,0,100,100)
            pygame.draw.rect(join_menu, purple, purple_rect)
            orange_rect = pygame.Rect(500,0,100,100)
            pygame.draw.rect(join_menu, orange, orange_rect)
            
            background.blit(join_menu, (0,0))
            screen.blit(background, (0,0))
            pygame.display.flip()
            drawn_join_options = 1
        else:
            for event in pygame.event.get():
                if event.type == QUIT:
                    raise SystemExit
                    screen.blit(background, (0, 0))
                    pygame.display.flip()
                if event.type == MOUSEBUTTONUP:
                    if yellow_rect.collidepoint(event.pos):
                        player_color = 'yellow' #fix
                    if green_rect.collidepoint(event.pos):
                        player_color = 'green' #fix
                    if blue_rect.collidepoint(event.pos):
                        player_color = 'blue' #fix
                    if red_rect.collidepoint(event.pos):
                        player_color = 'red' #fix
                    if purple_rect.collidepoint(event.pos):
                        player_color = 'purple' #fix
                    if orange_rect.collidepoint(event.pos):
                        player_color = 'orange' #fix
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.display.quit()
                        sys.exit()
                    if event.key == K_RETURN:
                        player_name = prompt(10,140,"Please enter your name:", font,screen)
			# might have to change this VVV (ipaddr)
			PLAYER = Player(player_name, player_color, '0.0.0.0')
                        #fix ^
                 # uncomment once networking is integrated
                 # can advance once know BOARD_SIZE
                        state = 12345 # (no more menus, draw game)
                        background.fill(green)
                        screen.blit(background, (0,0))
                        pygame.display.flip()


### invite options ########################################

    drawn_invite_options = 0
    while state == 3:
        if drawn_invite_options == 0:
            #draw
            inv_menu = pygame.Surface((200,200))
            inv_menu = inv_menu.convert()
            inv_menu.fill((255,255,255))
            background.blit(inv_menu, (0,0))
            screen.blit(background, (0,0))
            pygame.display.flip()
            #
            drawn_invite_options = 1
        else:
            for event in pygame.event.get():
                if event.type == QUIT:
                    raise SystemExit
                    screen.blit(background, (0, 0))
                    pygame.display.flip()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.display.quit()
                        sys.exit()
                    if event.key == K_KP1:
                        #fix
                        p2_ip = prompt(10,100, "Please enter I.P.",font,screen)
                        if num_players == 2:
                            state = 50
                            background.fill(green)
                            screen.blit(background, (0,0))
                            pygame.display.flip()
                    if event.key == K_KP2:
                        #fix
                        p3_ip = prompt(10,100, "Please enter I.P.",font,screen)
                        if num_players == 3:
                            state = 50
                            background.fill(green)
                            screen.blit(background, (0,0))
                            pygame.display.flip()
                    if event.key == K_KP3:
                        #fix
                        p4_ip = prompt(10,100, "Please enter I.P.",font,screen)
                        if num_players == 4:
                            state = 50
                            background.fill(green)
                            screen.blit(background, (0,0))
                            pygame.display.flip()


## GENBOARD
    def genBoard(config):
        """Makes board lawl"""
        dotsleft = (config['boardSize'][0] * config['boardSize'][1]) - config['maxDots']
        board = Board(config['maxPlayers'],
                    config['boardSize'][0],
                    config['boardSize'][1],
                    config['rounds'],
                    dotsleft)

        return board


    if isinstance(PLAYER, Host):
        run_str = PLAYER.color + ":B:!" + str(PLAYER.config) + "@"
        Run(run_str)
    else:
        PLAYER.addClient()
        while PLAYER.board == None:
            PLAYER.updateBoard()
                        

### END OF MENU SHIT #####################################

    PLAYER.updateBoard()
    time.sleep(4)
    PLAYER.updateBoard()

    if isinstance(PLAYER, Host):
        PLAYER.beginDotTimer()
    """
    print "awesome1"
    if isinstance(PLAYER, Host):
        print "awesome2"
        PLAYER.beginDotTimer()
        print "awesome3"
        PLAYER.setBoard(genBoard(PLAYER.config))
    else:

    print "awesome4"
    """
   
# board draw

    #draw it
    if BOARD_SIZE == 6:
        DOT_SIZE = 100
        bar = '6.png'
    if BOARD_SIZE == 7:
        DOT_SIZE = 85
        bar = '7.png'
    if BOARD_SIZE == 8:
        DOT_SIZE = 75
        bar = '8.png'
    if BOARD_SIZE == 9:
        DOT_SIZE = 66
        bar = '9.png'
    if BOARD_SIZE == 10:
        DOT_SIZE = 60
        bar = '.png'
    LINE_WIDTH = 1

 
    BLACK_DOT=load_image('dot_black' + bar, white)
    YELLOW_DOT=load_image('dot_yellow' + bar, white)
    RED_DOT=load_image('dot_red' + bar, white)
    BLUE_DOT=load_image('dot_blue' + bar, white)
    GREEN_DOT=load_image('dot_green' + bar, white)
    PURPLE_DOT=load_image('dot_purple' + bar, white)
    ORANGE_DOT=load_image('dot_orange' + bar, white)

    DIMENSION = (BOARD_SIZE * DOT_SIZE) + (LINE_WIDTH * (BOARD_SIZE + 1))


    #vertical lines
    for i in range(BOARD_SIZE + 1):
        start_pos = ((i * DOT_SIZE) + (i * LINE_WIDTH), 0)
        end_pos = ((i * DOT_SIZE) + (i * LINE_WIDTH), DIMENSION)
        pygame.draw.line(background, black, start_pos, end_pos, LINE_WIDTH)

    #horizontal lines
    for i in range(BOARD_SIZE + 1):
        start_pos = (0, (i * DOT_SIZE) + (i * LINE_WIDTH))
        end_pos = (DIMENSION, (i * DOT_SIZE) + (i * LINE_WIDTH))
        pygame.draw.line(background, black, start_pos, end_pos, LINE_WIDTH)

    # blit everything to the screen
    screen.blit(background, (0, 0))
    pygame.display.flip()


    ###################
    # Game event loop #
    ###################
    while 1:
        time.sleep(0.5)
        PLAYER.updateBoard()
        draw_board(PLAYER.board.grid)

        for event in pygame.event.get():
            if event.type == QUIT:
                raise SystemExit
                screen.blit(background, (0, 0))
                pygame.display.flip()
            if event.type == MOUSEBUTTONUP:
                handle_ev(event.pos)
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.display.quit()
                    sys.exit()
	



if __name__ == '__main__': 
    main()
