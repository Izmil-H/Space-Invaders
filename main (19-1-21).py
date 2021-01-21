import os
import pygame
import random
import math

# ########################### SETUP ###################################

# ----- set to current directory ---
os.chdir("C:/Users/Ismail/Desktop/Productive/pythoning/game")

# ------ initialize pygame ---------
pygame.init()

# ------- create screen ------------
screenWidth = 900
screenHeight = 600
screen = pygame.display.set_mode((screenWidth, screenHeight))
background = pygame.image.load("images/background.jpg")

# ------- customize window ---------
pygame.display.set_caption("Ismail's Game")
icon = pygame.image.load("images/icon.png")
pygame.display.set_icon(icon)

# ------- texts and fontss ----------
font = pygame.font.Font("arcadeFont.TTF", 25)

# ########################## SYSTEMS ################################
# ------ score -------
score = 0
def draw_score(x, y):
    text = font.render("Score: " + str(score), True, [255, 255, 255])
    screen.blit(text, (x, y))

# ########################### ASSETS ################################

# -------- player ------------
playerImg = pygame.image.load("images/playerSprite.png")
playerSize = playerImg.get_rect().size
playerX = screenWidth/2 - playerSize[0]/2
playerY = 5*screenHeight/6
P_velX = .3


# -------- enemy --------------
class enemy:
    img = pygame.image.load("images/enemySprite.png")
    size = img.get_rect().size
    velX = .2
    velY = .02
    x = 0
    y = screenHeight/6
    def __init__ (self, randX, rand_velX):
        self.x = randX
        self.velX = rand_velX

    def draw(self):
        screen.blit(self.img, (self.x, self.y))

num_enems = 5
enemies = []
for i in range(num_enems):
    enemies.append( enemy(random.randint(50, screenWidth-enemy.size[0]), random.uniform(0.1, 0.25)) )


# -------- bullet -------------
bulletImg = pygame.image.load("images/circle.png")
bulletSize = bulletImg.get_rect().size
bulletX = 0
bulletY = playerY - bulletSize[0] - 10
B_velY = .6
bulletState = "ready" # ready: can't see bullet,   fire: bullet is moving

def bullet(x, y): 
    global bulletState
    global bulletY
    global B_vel
    if bulletState == "fire":
        screen.blit(bulletImg, (x + 16, y + 10))
        bulletY -= B_velY
    if bulletY <= 0 - bulletSize[1]:
        bulletState = "ready"
        bulletY = playerY - bulletSize[0] - 10 

def collision(eX, eY, bX, bY):
    if (eX - bulletSize[0] - 5 <= bX <= eX + enemy.size[0] + 5) and (eY - bulletSize[1] - 5 <= bY <= eY + enemy.size[1] + 5):
        return True
    return False
  

# ################################## GAME LOOP ################################### 

running = True
while running:
    
    # ------------ EXITING -------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
   # ********************* MOVEMENT ***************************
    # ----- player ---------
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_LEFT]:
        playerX -= P_velX
    if pressed[pygame.K_RIGHT]:
        playerX += P_velX
    if playerX <= 0:
        playerX = 0
    if playerX >= screenWidth - 64:
        playerX = screenWidth - 64
    
    # ----- bullet ----------
    if pressed[pygame.K_SPACE] and bulletState == "ready":
        bulletState = "fire"
        bulletX = playerX + bulletSize[0]/2

    # ----- enemy -----------
    for i in range(num_enems):
        if enemies[i].x <= 0 or enemies[i].x >= screenWidth-enemies[i].size[0]:
            enemies[i].velX *= -1
        
        enemies[i].x += enemies[i].velX
        enemies[i].y += enemies[i].velY

        
        
    # ******************* COLLISION ******************************
    for i in range(num_enems):
        if bulletState == "fire" and collision(enemies[i].x, enemies[i].y, bulletX, bulletY):
            pygame.draw.rect(screen, [255,0,0], pygame.Rect(0,0, 50, 30))
            score += 1
            print(score)
            bulletState = "ready"
            bulletY = playerY - bulletSize[0] - 10
            enemies[i] = enemy(random.randint(50, screenWidth-enemy.size[0]), random.uniform(0.1, 0.25))


# ************************* DRAWING *******************************

    # --------- background --------------
    screen.fill((100,100,100))
    screen.blit(background, (0,0))
   
    # --------- characters --------------
    screen.blit(playerImg, (playerX, playerY))

    for i in range(num_enems): 
        enemies[i].draw()

    bullet(bulletX, bulletY)

    draw_score(10, 10)

    # ----- update -----
    pygame.display.update()