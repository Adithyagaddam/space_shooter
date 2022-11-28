import pygame
import os

pygame.font.init()
pygame.mixer.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

WIDTH, HEIGHT = 900, 500
BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

#BULLET_HIT_SOUND = pygame.mixer.Sound('Assets/Grenade+1.mp3')
#BULLET_FIRE_SOUND = pygame.mixer.Sound('Assets/Gun+Silencer.mp3')

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

VEL = 5
BULLET_VEL = 7

class Player:
    def __init__(self,SPACESHIP_WIDTH, SPACESHIP_HEIGHT,IMAGE_URL,rotate,health,bullets,hit,x,y,player_id):
        self.SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', str(IMAGE_URL)))
        self.SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
            self.SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), rotate)
            
        self.health = health
        self.bullets = bullets
        self.HIT = pygame.USEREVENT + hit
        self.x = x
        self.y = y
        self.rotate=rotate
        self.width=SPACESHIP_WIDTH
        self.height=SPACESHIP_HEIGHT
        self.rect = pygame.Rect(self.x,self.y,self.width,self.height)
        self.id=player_id
        self.update()

    def update(self):
        self.rect.x,self.rect.y = (self.x, self.y)

    def draw_window(self,SPACE,WIN,player2,player_number):
        WIN.blit(SPACE, (0, 0))
        pygame.draw.rect(WIN, BLACK, BORDER)

        yellow_health_text = HEALTH_FONT.render(
            "Health: " + str(self.health), 1, WHITE)
        
        red_health_text = HEALTH_FONT.render(
            "Health: " + str(player2.health), 1, WHITE)
        
        if(not int(player_number)):
            WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
            WIN.blit(yellow_health_text, (10, 10))
        else:
            WIN.blit(yellow_health_text,(WIDTH - yellow_health_text.get_width() - 10, 10))
            WIN.blit(red_health_text,(10, 10))


        WIN.blit(self.SPACESHIP, (self.x, self.y))
        WIN.blit(player2.SPACESHIP, (player2.x, player2.y))

        for bullet in player2.bullets:
            pygame.draw.rect(WIN, RED, bullet)

        for bullet in self.bullets:
            pygame.draw.rect(WIN, RED, bullet)


        pygame.display.update()
    
    def handle_movement(self,keys_pressed):
        if self.id == 0:
            if keys_pressed[pygame.K_a] and self.x - VEL > 0:  # LEFT
                self.x -= VEL
            if keys_pressed[pygame.K_d] and self.x + VEL + self.width < BORDER.x:  # RIGHT
                self.x += VEL
            if keys_pressed[pygame.K_w] and self.y - VEL > 0:  # UP
                self.y -= VEL
            if keys_pressed[pygame.K_s] and self.y + VEL + self.height < HEIGHT - 15:  # DOWN
               self.y += VEL
        elif self.id == 1:
            if keys_pressed[pygame.K_LEFT] and self.x - VEL > BORDER.x + BORDER.width:  # LEFT
                self.x -= VEL
            if keys_pressed[pygame.K_RIGHT] and self.x + VEL + self.width < WIDTH:  # RIGHT
                self.x += VEL
            if keys_pressed[pygame.K_UP] and self.y - VEL > 0:  # UP
                self.y -= VEL
            if keys_pressed[pygame.K_DOWN] and self.y + VEL + self.height < HEIGHT - 15:  # DOWN
                self.y += VEL
        self.update()
    
    
    def handle_movement_arrow(self,keys_pressed):
        if keys_pressed[pygame.K_LEFT] and self.x - VEL > BORDER.x + BORDER.width:  # LEFT
            self.x -= VEL
        if keys_pressed[pygame.K_RIGHT] and self.x + VEL + self.width < WIDTH:  # RIGHT
            self.x += VEL
        if keys_pressed[pygame.K_UP] and self.y - VEL > 0:  # UP
            self.y -= VEL
        if keys_pressed[pygame.K_DOWN] and self.y + VEL + self.height < HEIGHT - 15:  # DOWN
            self.y += VEL
        self.update()

    def handle_bullets(self,player2):
        if self.id == 0:
            for bullet in self.bullets:
                bullet.x += BULLET_VEL
                if player2.rect.colliderect(bullet):
                    pygame.event.post(pygame.event.Event(self.HIT))
                    self.bullets.remove(bullet)
                elif bullet.x > WIDTH:
                    self.bullets.remove(bullet)
        elif self.id == 1:
            for bullet in self.bullets:
                bullet.x -= BULLET_VEL
                if player2.rect.colliderect(bullet):
                    pygame.event.post(pygame.event.Event(self.HIT))
                    self.bullets.remove(bullet)
                elif bullet.x < 0:
                    self.bullets.remove(bullet)

    @staticmethod
    def draw_winner(WIN,text):
        draw_text = WINNER_FONT.render(text, 1, WHITE)
        WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width() /
                             2, HEIGHT/2 - draw_text.get_height()/2))
        pygame.display.update()
        pygame.time.delay(5000)
    