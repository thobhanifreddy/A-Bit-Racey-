import pygame
import time
import random 

pygame.init()

crash_sound = pygame.mixer.Sound("crash.wav")

white = (255,255,255)
black = (0,0,0)
red = (200,0,0)
blue = (0,0,200)
green = (0,200,0)
light_red = (150,0,0)
light_green = (0,150,0)

high_score = [0]
display_width = 800
display_height = 600
car_width = 73

game_display = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption("A Bit Racey")

clock = pygame.time.Clock()
carImg = pygame.image.load('racecar.png')

pause = False

def things(thingx, thingy, thingw, thingh, color):
    pygame.draw.rect(game_display,color,[thingx,thingy,thingw, thingh]) 


def car(x,y):
    game_display.blit(carImg,(x,y))


def crash():
    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(crash_sound)
    crash_font = pygame.font.SysFont("comicsansms",115)
    crash_text = crash_font.render("You Crashed!",True,black)
    game_display.blit(crash_text,((display_width/4 - 150), (display_height/4 + 100)))

    while True:
        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
    #button(x,y,w,h,ic,ac, action = None)
        button("Play Again",150,450,160,50,green,light_green,game_loop)
        button("Quit",550,450,100,50,red,light_red,quit_game)
        print_highscore()
        pygame.display.update()
        


def score(count):
    font = pygame.font.SysFont("comicsansms",25)
    text = font.render("Score: " + str(count), True, black)
    game_display.blit(text, (1,1))

def get_highscore():
    high_score = 0
    high_score_file = open('score.txt','r')
    high_score = int(high_score_file.read())
    high_score_file.close()

    return high_score

def save_highscore(count):
    high_score_file = open("score.txt","w")
    high_score_file.write(str(count))
    high_score_file.close()

def print_highscore():
    font = pygame.font.SysFont("comicsansms",25)
    text = font.render("High Score: " + str(get_highscore()), True, black)
    game_display.blit(text, (1,25))



def quit_game():
    pygame.quit()
    quit()

def button(msg,x,y,w,h,ic,ac,action = None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(game_display, ic,(x,y,w,h))

        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(game_display, ac,(x,y,w,h))


    b_font = pygame.font.SysFont("comicsansms",20)
    b_text = b_font.render(msg,True,black)
    game_display.blit(b_text,((x+w/4),(y + h/4)))
    pygame.display.update()

def unpaused():
    global pause
    pause = False
    pygame.mixer.music.unpause()


def paused():

    #game_display.fill(white)
    
    while pause:
        pygame.mixer.music.pause()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        pause_font = pygame.font.SysFont("comicsansms",115)
        pause_text = pause_font.render("Paused",True,black)
        game_display.blit(pause_text,((display_width/4 ), (display_height/4 + 50)))
        
        get_highscore()
        
        #button(x,y,w,h,ic,ac, action = None)
        button("Continue",150,450,150,50,green,light_green,unpaused)
        button("Quit",550,450,120,50,red,light_red,quit_game)

        pygame.display.update()
    
        clock.tick(15)

def intro():
    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        game_display.fill(white)
        intro_font = pygame.font.SysFont("comicsansms",115)
        intro_text = intro_font.render("A Bit Racey",True,black)
        game_display.blit(intro_text,((display_width/4 - 100), (display_height/4 + 50)))
        
        #button(x,y,w,h,ic,ac, action = None)
        button("Go!!",150,450,100,50,green,light_green,game_loop)
        button("Quit",550,450,100,50,red,light_red,quit_game)
        print_highscore()
        pygame.display.update()
    
        clock.tick(15)

def game_loop():
    pygame.mixer.music.load('music2.wav')
    pygame.mixer.music.play(-1)


    game_exit = False

    x = (display_width / 2)
    y = (display_height * 0.8)
    x_change = 0

    thing_startx = random.randrange(0, display_width)
    thing_starty  = -600
    thing_speed = 7
    thing_width = 100
    thing_height = 100

    block_color = (random.randrange(1,255),random.randrange(1,255),random.randrange(1,255))


    count = 0
    high_score = get_highscore()
    while not game_exit:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -5
                if event.key == pygame.K_RIGHT:
                    x_change = 5
                
                if event.key == pygame.K_p:
                    global pause
                    pause = True
                    paused()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0


        x += x_change
        game_display.fill(white)

        # def things(thingx, thingy, thingw, thingh, color):
        things(thing_startx, thing_starty, thing_width,thing_height,block_color)
        thing_starty += thing_speed
        car(x,y)
        score(count)

        crash_text = False

 
        if x > display_width - car_width or x < 0:
            crash()
            
        if thing_starty > display_height:
            thing_starty = 0 - thing_height
            thing_startx = random.randrange(0,display_width)
            block_color = (random.randrange(1,255),random.randrange(1,255),random.randrange(1,255))

            count += 1
            if count > 10:
                thing_speed += 0.5
            thing_width += 1.5

        if y < thing_starty+thing_height:
            if x > thing_startx and x < thing_startx + thing_width or x+car_width > thing_startx and x + car_width < thing_startx+thing_width:
                if count > high_score:
                    save_highscore(count)

                crash()
        print_highscore()
        pygame.display.update()
        clock.tick(60)

intro()
game_loop()
pygame.quit()
quit()