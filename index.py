import pygame
import time
import sys
from pygame import mixer
from fighter import Fighter

mixer.init()
pygame.init()

width = 1000
height = 600

win = pygame.display.set_mode((width,height))
pygame.display.set_caption('Multiplayer Street Fighter')
clock = pygame.time.Clock()

# fps
FPS = 30
# color
white = (255,255,255)
yellow = (255,255,0)
red = (255,0,0)
#define game variables
intro_count = 4
last_count_update = pygame.time.get_ticks()
score = [0,0] # player scores
round_over = False
round_over_cooldown =  2000
# define fighter variables
WARRIOR_SIZE = 162
WARRIOR_SCALE = 4
WARRIOR_OFFSET = [72,56]
WARRIOR_DATA = [WARRIOR_SIZE,WARRIOR_SCALE,WARRIOR_OFFSET]
WIZARD_SIZE = 250
WIZARD_SCALE = 3
WIZARD_OFFSET = [112,107]
WIZARD_DATA = [WIZARD_SIZE,WIZARD_SCALE,WIZARD_OFFSET]

# load music or sounds
pygame.mixer.music.load('./audio/music.mp3')
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1, 0.0, 5000)
# sound effects 
sword_fx = pygame.mixer.Sound('./audio/sword.wav')
sword_fx.set_volume(0.5)
magic_fx = pygame.mixer.Sound('./audio/magic.wav')
magic_fx.set_volume(0.5)
# multiple images
bg1 = pygame.image.load('./assets/images/background/background.jpg').convert_alpha()
# victory image
victory_img = pygame.image.load('./victory.png').convert_alpha()
# warrior
warrior_sheet = pygame.image.load('./assets/images/warrior/Sprites/warrior.png').convert_alpha()
wizard_sheet = pygame.image.load('./assets/images/wizard/Sprites/wizard.png').convert_alpha()

# define the nomber of steps in each animation
WARRIOR_ANIMATION_STEPS = [10,8,1,7,7,3,7]
WIZARD_ANIMATION_STEPS   = [8,8,1,8,8,3,7]




# font display
# count_font = pygame.font.SysFont("bytes",80,bold=True)
count_font = pygame.font.Font('./turok.ttf',80)
score_font = pygame.font.Font('./turok.ttf',30)
again_play_font = pygame.font.Font('./turok.ttf',30)
# display text
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    win.blit(img, (x, y))
# background
def draw_bg():
    scaled_bg = pygame.transform.scale(bg1,(width,height))
    win.blit(scaled_bg,(0,0))
def draw_health_bar(health,x,y):
    ratio = health/100
    pygame.draw.rect(win,white,(x - 2,y - 2,404,24))
    pygame.draw.rect(win,red,(x,y,400,20))
    pygame.draw.rect(win,yellow,(x,y,400*ratio,20))

# fighters
fighter1 = Fighter(1, 200,310,False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx)
fighter2 = Fighter(2, 700,310, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx)


run = True
# game loop
while run:
    clock.tick(FPS)
    draw_bg()
    # draw healthbar 
    draw_health_bar(fighter1.health,20,20)
    draw_health_bar(fighter2.health,580,20)
    draw_text('P1: ' + str(score[0]), score_font, red, 20,60)
    draw_text('P2: ' + str(score[1]), score_font, red, 580,60)
    # update countdown
    if intro_count <= 0:
        #move fighters
        fighter1.move(width, height, win, fighter2, round_over)
        fighter2.move(width, height, win, fighter1, round_over)
    else:
        #displaye count timer
        draw_text(str(intro_count), count_font, red, width / 2, height / 3)
        #update count timer
        if (pygame.time.get_ticks() - last_count_update) >= 1000:
            intro_count -= 1
            last_count_update = pygame.time.get_ticks()


    # update fighters
    fighter1.update()
    fighter2.update()

    # draw fighters
    fighter1.draw(win)
    fighter2.draw(win)

    # check for player defeat
    if round_over == False:
        if fighter1.alive == False:
            score[1] += 1
            round_over = True
            round_over_time = pygame.time.get_ticks()
        elif fighter2.alive == False:
            score[0] += 1
            round_over = True
            round_over_time = pygame.time.get_ticks()
    else:
        # display victory image
        win.blit(victory_img, (360, 150))
        if pygame.time.get_ticks() - round_over_time > round_over_cooldown:
            round_over = False
            intro_count = 4
            fighter1 = Fighter(1, 200,310,False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx)
            fighter2 = Fighter(2, 700,310, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx)


    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()
            run = False
            quit()



    pygame.display.update()
