import pygame
import os
from network import Network
from player import Player

pygame.font.init()
pygame.mixer.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

WIDTH, HEIGHT = 900, 500
MAX_BULLETS = 3
FPS = 60
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("First Game!")

SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40
SPACE = pygame.transform.scale(pygame.image.load(
        os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))

WIDTH, HEIGHT = 900, 500
BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

#BULLET_HIT_SOUND = pygame.mixer.Sound('Assets/Grenade+1.mp3')
#BULLET_FIRE_SOUND = pygame.mixer.Sound('Assets/Gun+Silencer.mp3')

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)


players=[Player(SPACESHIP_WIDTH,SPACESHIP_HEIGHT,'spaceship_yellow.png',90,10,[],1,100,300,0),Player(SPACESHIP_WIDTH,SPACESHIP_HEIGHT,'spaceship_red.png',270,10,[],2,700,300,1)]

def read_pos(str):
    str = str.split(",")
    return int(str[0]), int(str[1]) ,int(str[2]),int(str[3]), int(str[4])


def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1]) + "," + str(tup[2]) + "," + str(tup[3]) + "," + str(tup[4])  


def bullets_read(str):
    str=str.split(",")
    return str

def bullets_make(tup):
    str_ans=""
    for i in range(len(tup)):
        str_ans+=str(tup[i]) + ","
    return str_ans

def main():  
    clock = pygame.time.Clock()
    run = True
    n=Network()
    player_number=n.getP()
    player1=players[int(player_number)]
    player2=players[int(not int(player_number))]
    while run:
        clock.tick(FPS)
        if int(player_number)==0:
            p2Pos = read_pos(n.send(make_pos((player_number,player1.x, player1.y,player1.health,player2.health))))
        else:
            p2Pos = read_pos(n.send(make_pos((player_number,player1.x, player1.y,player2.health,player1.health))))
    
        player2.x = p2Pos[1]
        player2.y = p2Pos[2]
        if int(player_number)==0:
            player1.health=min(player1.health,p2Pos[3])
            player2.health=min(player2.health,p2Pos[4])
        else:
            player1.health=min(player1.health,p2Pos[4])
            player2.health=min(player2.health,p2Pos[3])
        player2.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(player1.bullets) < MAX_BULLETS:
                    if(not int(player_number)):
                        bullet = pygame.Rect(
                            player1.x + player1.width, player1.y + player1.height//2 - 2, 10, 5)
                    else:
                        bullet = pygame.Rect(
                            player1.x, player1.y + player1.height//2 - 2, 10, 5)
                    player1.bullets.append(bullet)
                    #BULLET_FIRE_SOUND.play()
                

            if event.type == player1.HIT:
                player2.health-=1
                #BULLET_HIT_SOUND.play()
        
        winner_text = ""
        if player1.health <= 0:
            if(not int(player_number)):
                winner_text = "Player 1 Wins!"
            else:
                winner_text = "Player 2 Wins!"

        if player2.health <= 0:
            if(not int(player_number)):
                winner_text = "Player 1 Wins!"
            else:
                winner_text = "Player 2 Wins!"
        

        if winner_text != "":
            player1.draw_window(SPACE,WIN,player2,player_number)
            Player.draw_winner(WIN,winner_text)
            return 1

        keys_pressed = pygame.key.get_pressed()
        player1.handle_bullets(player2)
        player1.handle_movement(keys_pressed)
        player1.draw_window(SPACE,WIN,player2,player_number)

main()