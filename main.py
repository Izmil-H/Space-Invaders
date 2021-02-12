import os
import pygame
from pygame import mixer
import random
import math
import time

# ########################### SETUP ###################################

# ----- set to current directory ---
os.chdir(os.getcwd())

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

# ------------ audio -------------
musicState = 'on'
mixer.music.load('sounds/retroMusic2.wav')
if musicState == 'on': mixer.music.play(-1)

soundState = 'on'
menuSound = mixer.Sound('sounds/menu.wav')


# ###########################################################################################
colors = {"white":[255,255,255], "black":[0,0,0], "grey":[100,100,100]}

# ---- display text -----
def display_text(size, message, color, x, y, center):
    font = pygame.font.Font("arcadeFont.ttf", size)
    text = font.render(message, True, (color[0], color[1], color[2]))
    size = text.get_rect().size
    if center: 
        x -= size[0]/2
        y -= size[1]/2
    screen.blit(text, (x, y))

# ---- collision -------
def collision(aX, aY, aSize, bX, bY, bSize, Buffer): # b being the projectile and a being the target.
    if (aX - bSize[0] - Buffer <= bX <= aX + aSize[0]) and (aY - bSize[1] <= bY <= aY + aSize[1]):
        return True
    return False 


score = 0
shots, hits = 0, 0
def streak(x, y):
    global shots, hits
    if (shots == hits):
        display_text(17, "Streak: " + str(hits), colors['white'], x, y, False)
    else:
        shots, hits = 0, 0

highScore, highStreak = 0, 0

# ############################################################################################
# -------- player ------------
class C_player:
    img = pygame.image.load("images/playerSprite.png")
    size = img.get_rect().size
    x = screenWidth/2 - size[0]/2
    y = 5*screenHeight/6
    velX = 3
    def draw(self):
        screen.blit(self.img, (self.x, self.y))


# -------- enemy --------------
class enemy:
    img = pygame.image.load("images/enemySprite.png")
    size = img.get_rect().size
    velX = 2
    velY = .2
    x = 0
    y = size[1]/5 * -1
    dead = False
    def __init__ (self, randX, rand_velX):
        self.x = randX
        self.velX = rand_velX

    def draw(self):
        screen.blit(self.img, (self.x, self.y))


# -------- bullet -------------
class C_bullet:
    img = pygame.image.load("images/circle.png")
    size = img.get_rect().size
    sound = mixer.Sound('sounds/laser.wav')
    soundState
    x = 0
    y = C_player.y - size[0] - 10
    velY = 6
    state = "ready" # ready: can't see bullet,   fire: bullet is visible and moving
    def move(self):
        if self.state == "fire":
            screen.blit(self.img, (self.x + 16, self.y + 10))
            self.y -= self.velY



# ----------------------------------------------------------------------



def settings():
    global musicState, soundState
    running = True
    row = [ colors['white'], colors['grey'], colors['grey'] ]
    curChoice = 0
    rowY = []
    rowY.append(screenHeight/3 + 10)
    rowY.append(rowY[0] + 70)
    rowY.append(screenHeight - 70)

    while running:

        # ------------ EXITING -------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 0

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return 1
                if curChoice == 2 and event.key == pygame.K_SPACE:
                    return 2

                if event.key == pygame.K_UP:
                    menuSound.play()
                    if curChoice == 0: curChoice = 2
                    else: curChoice -= 1
                if event.key == pygame.K_DOWN:
                    menuSound.play()
                    if curChoice == 2: curChoice = 0
                    else: curChoice += 1
                row[0] = row[1] = row[2] = colors['grey']
                row[curChoice] = colors['white']

                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    if curChoice == 0: 
                        if musicState == 'off': 
                            musicState = 'on'
                            mixer.music.play()
                        else: 
                            musicState = 'off'
                            mixer.music.pause()
                    elif curChoice == 1:
                        if soundState == 'off': soundState = 'on'
                        else: soundState = 'off'


        # ***************** DRAWING *********************
        screen.blit(background, (0,0))

        display_text(15, "< back [esc]", colors['white'], 10, 10, False)
        display_text(40, "settings", colors['white'], screenWidth/2, screenHeight/6, True)

        display_text(35, "Music: ", row[0], screenWidth/10, rowY[0], False)
        display_text(35, "Sound effects:", row[1], screenWidth/10, rowY[1], False)
        display_text(35, "go to menu", row[2], screenWidth/2, rowY[2], True)
        if curChoice == 2: display_text(17, "press space", [200,200,200], screenWidth/2, rowY[2] + 30, True)

        display_text(35, '< ' + musicState + ' >', row[0], 6*screenWidth/10, rowY[0], False)
        display_text(35, '< ' + soundState + ' >', row[1], 6*screenWidth/10, rowY[1], False)
        
        #display_text(17, "press space", [200,200,200], screenWidth/2, optionsY[curChoice] + 30, True)

        
        pygame.display.update()


def difficulty():
    running = True
    options = [ colors['grey'], colors['white'], colors['grey'] ]
    curChoice = 1
    optionsY = []
    optionsY.append(screenHeight/3 + 50)
    optionsY.append(optionsY[0] + 120)
    optionsY.append(optionsY[1] + 120)

    while running:
        # ------------ EXITING -------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 0

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    time.sleep(.2)
                    return curChoice + 1

                if event.key == pygame.K_LEFT or event.key == pygame.K_UP:
                    menuSound.play()
                    if curChoice == 0: curChoice = 2
                    else: curChoice -= 1
                if event.key == pygame.K_RIGHT or event.key == pygame.K_DOWN:
                    menuSound.play()
                    if curChoice == 2: curChoice = 0
                    else: curChoice += 1
                options[0] = options[1] = options[2] = colors['grey']
                options[curChoice] = colors['white']


        # ***************** DRAWING *********************
        screen.blit(background, (0,0))
        display_text(40, "select difficulty", colors['white'], screenWidth/2, screenHeight/6, True)

        display_text(35, "easy", options[0], screenWidth/2, optionsY[0], True)
        display_text(35, "regular", options[1], screenWidth/2, optionsY[1], True)
        display_text(35, "hard", options[2], screenWidth/2, optionsY[2], True)
        
        display_text(17, "press space", [200,200,200], screenWidth/2, optionsY[curChoice] + 30, True)

        
        pygame.display.update()

# ######################################################### ACTUAL GAME ###########################################################
# ################################################################################################################################# 
def game(difficulty):
    # ########################## SETUP #####################
    enemySpeedRange = [1, 2.5]
    num_enems = 5
    enemy_velY = .2
    if difficulty == 2:
        enemySpeedRange = [1.2, 3]
        num_enems = 6
    elif difficulty == 3    :
        enemySpeedRange = [2.2, 3.5]
        num_enems = 8
        enemy_velY = .3

    clock = pygame.time.Clock()
    fontOpacity = 0
    backOpacity = 0
    gameOver_count = 0
    enemyThreshold = C_player.y + C_player.size[1]/4
    global score, shots, hits, soundState, highScore, highStreak

    color1 = colors['grey']
    color2 = colors['white']

    player = C_player()
    bullet = C_bullet()
    
    enemies = []
    for i in range(num_enems):
        enemies.append( enemy(random.randint(50, screenWidth-enemy.size[0]), random.uniform(enemySpeedRange[0], enemySpeedRange[1])) )
        enemies[i].velY = enemy_velY

    # #################### GAME LOOP ##########################
    running = True
    playing = True
    while running:
        # ------------ EXITING -------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 3

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    setting = settings()
                    if setting == 0:
                        return 3
                    elif setting == 2:
                        return 1

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE and fontOpacity > 254:
                    if color1 == colors['white']: return 1
                    elif color2 == colors['white']: return 2


        pressed = pygame.key.get_pressed()
        if fontOpacity > 254:
            if pressed[pygame.K_LEFT]:
                color1 = colors['white']
                color2 = colors['grey']
            elif pressed[pygame.K_RIGHT]:
                color2 = colors['white']
                color1 = colors['grey']

        # #################################################### LOGIC ########################################################

        # ************************************ player ************************************
        # ********************************************************************************
        if(playing):
            if pressed[pygame.K_LEFT]:
                player.x -= player.velX
            if pressed[pygame.K_RIGHT]:
                player.x += player.velX
            if player.x <= 0:
                player.x = 0
            if player.x >= screenWidth - 64:
                player.x = screenWidth - 64
                
            # --------- bullet -----------------
            if pressed[pygame.K_SPACE] and bullet.state == "ready":
                if soundState == 'on': bullet.sound.play()
                bullet.state = "fire"
                bullet.x = player.x + bullet.size[0]/2
            
            if  bullet.y <= 0 - bullet.size[1] :
                shots += 1
                bullet.state = "ready"
                bullet.y = player.y - bullet.size[0] - 10 


        # ********************************* enemy ****************************************
        # ********************************************************************************
        for i in range(num_enems):        
            # -------- game Over ---------
            if not enemies[i].dead and enemies[i].y + enemies[i].size[1] >= enemyThreshold:
                playing = False
                
            if(playing):

                # ---------------- dead enemy -------------------
                if enemies[i].dead:
                    # respawn
                    if(enemies[i].y >= screenHeight):
                        enemies[i] = enemy(random.randint(50, screenWidth-enemy.size[0]), random.uniform(1, 2.5))
                        enemies[i].y = -1* enemies[i].size[1]
                        continue

                    # continue falling
                    enemies[i].y += 20*enemies[i].velY
                    continue

                # ----------------- collision --------------------
                if bullet.state == "fire" and collision(enemies[i].x, enemies[i].y, enemies[i].size, bullet.x, bullet.y, bullet.size, 5):
                    hits += 1
                    shots += 1
                    score += 1
                    highScore, highStreak = max(highScore, score), max(highStreak, hits)
                    f = open('info.txt', 'w')
                    f.write(str(highScore)+'\n')
                    f.write(str(highStreak))
                    f.close()

                    enemies[i].dead = True
                    pygame.draw.rect(screen, [255,0,0], pygame.Rect(0,0, 50, 30))
                    bullet.state = "ready"
                    bullet.y = player.y - bullet.size[0] - 10
                    
                
                # ------------------ update position ------------------
                if enemies[i].x <= 0 or enemies[i].x >= screenWidth-enemies[i].size[0]:
                    enemies[i].velX *= -1
                enemies[i].x += enemies[i].velX
                enemies[i].y += enemies[i].velY

            else:
                if gameOver_count < 200: gameOver_count +=1
                else: enemies[i].y += 50*enemies[i].velY


        # ######################################################### DRAWING #############################################################
        # --------- background --------------
        screen.blit(background, (0,0))

        # --------- characters --------------
        # -- enemy threshold
        pygame.draw.rect(screen, [40, 0 ,0], (0, enemyThreshold, screenWidth, 2))
        
        # -- enemies
        for i in range(num_enems): 
            enemies[i].draw()

        # -- player & bullets
        bullet.move()
        player.draw()
    
        # -- HUD
        display_text(15, "settings [esc]", colors['white'], screenWidth -100, 20, True)
        display_text(25, "Score: " + str(score), colors['white'], 10, 12, False)
        streak(10, 50)

        # ---- Game Over
        if(not playing): 
            
            if (fontOpacity < 254): fontOpacity += 1.5
            else:
                display_text(25, "back to menu", color1, screenWidth/3, screenHeight/2 + 35, True)
                display_text(25, "play again", color2, screenWidth/3 + 300, screenHeight/2 + 35, True)
                
                if color1 == colors['white']:
                    display_text(17, "press space", [200,200,200], screenWidth/3, screenHeight/2 + 70, True)
                    player.x = screenWidth/3 - player.size[0]/2
                elif color2 == colors['white']:
                    display_text(17, "press space", [200,200,200], screenWidth/3 + 300, screenHeight/2 + 70, True)
                    player.x = screenWidth/3 - player.size[0]/2 + 300
                
            display_text(90, "GAME OVER", [fontOpacity, fontOpacity, fontOpacity], screenWidth/2, screenHeight/2 - 50, True)

        # ----- update -----
        clock.tick(90)
        pygame.display.update()
    
    return


def howToPlay():
    clock = pygame.time.Clock()
    running = True
    
    enemies = enemy(0,0)
    enemies.x, enemies.y = 800, 300
    count = 0
    while running:
        # ------------ EXITING -------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 0
            
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RETURN: return 1
        
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_ESCAPE]:
            return 1
        
        limit, speed = 100, .3
        if count < limit: enemies.y -= speed
        elif limit <= count < 2*limit: enemies.y += speed
        else: count = 0
        count += 1


        # ***************** DRAWING *********************
        screen.blit(background, (0,0))
        screen.fill((0,0,0))

        display_text(15, "<-- Back to menu [esc]", colors['white'], 10, 10, False) 

        display_text(35, "How to play Space Invaders:", colors['white'], screenWidth/2, 100, True)
        
        display_text(22, " 1. Use the arrow keys to move left and right.", colors['white'], 10, screenHeight/7 + 110, False)
        display_text(22, " 2. Press space to shoot.", colors['white'], 10, 2*screenHeight/7 + 110, False)
        display_text(22, " 3. Shoot down as many aliens as you can.", colors['white'], 10, 3*screenHeight/7 + 110, False)
        display_text(22, " 4. You lose when an alien reaches the red line.", colors['white'], 10, 4*screenHeight/7 + 110, False)

        enemies.draw()

        clock.tick(90)
        pygame.display.update()
        

def menu():
    global highScore, highStreak
    f = open("info.txt", 'r')
    highScore, highStreak = int(f.readline()), int(f.readline())
    f.close()

    running = True
    color1 = colors['grey']
    color2 = colors['white']

    player = C_player()
    bullet = C_bullet()

    enemies = []
    for i in range(3):
        enemies.append(enemy(0, 0))

    enemies[0].x, enemies[0].y = 50, 390
    enemies[1].x, enemies[1].y = 350, 500
    enemies[2].x, enemies[2].y = 750, 400
    count = 0

    player = C_player()
    player.y = screenHeight - 50 - player.size[1]/2

    while running:
        # ------------ EXITING -------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    setting = settings()
                    if setting == 0:
                        return 3

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and bullet.state == "ready":
                    bullet.sound.play()
                    bullet.state = "fire"
                    bullet.x = player.x + bullet.size[0]/2
                    if color1 == colors['white']: return 2
                    elif color2 == colors['white']: return 1

                    
        if  bullet.y <= screenHeight/2 + 35 - bullet.size[0]:
            bullet.state = "ready"
            bullet.y = player.y - bullet.size[0] - 10 
        
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_LEFT] and color1 == colors['grey']:
            menuSound.play()
            color1 = colors['white']
            color2 = colors['grey']
        if pressed[pygame.K_RIGHT] and color2 == colors['grey']:
            menuSound.play()
            color2 = colors['white']
            color1 = colors['grey']

        limit, speed = 350, .15
        for i in range(3):
            if count < limit: enemies[i].y -= speed
            elif limit <= count < 2*limit: enemies[i].y += speed
            else: count = 0
            count += 1


        # ***************** DRAWING *********************
        screen.blit(background, (0,0))
        display_text(65, "Space Invaders", colors['white'], screenWidth/2, screenHeight/4, True)
        display_text(30, "High Score:"+ str(highScore), [174, 197, 255], screenWidth/2, 3*screenHeight/7 - 25, True)
        display_text(30, "Streak:"+ str(highStreak), [174, 197, 255], screenWidth/2, 3*screenHeight/7 + 20, True)
        display_text(15, "settings [esc]", colors['white'], screenWidth-100, 20, True)


        display_text(25, "How to play", color1, screenWidth/3, 4*screenHeight/7 + 20, True)
        display_text(25, "Play", color2, screenWidth/3 + 300, 4*screenHeight/7 + 20, True)
        
        if color1 == colors['white']:
            display_text(17, "press space", [200,200,200], screenWidth/3, 4*screenHeight/7 + 55, True)
            player.x = screenWidth/3 - player.size[0]/2
        elif color2 == colors['white']:
            display_text(17, "press space", [200,200,200], screenWidth/3 + 300, 4*screenHeight/7 + 55, True)
            player.x = screenWidth/3 - player.size[0]/2 + 300
        
        player.draw()
        bullet.move()

        for i in range(3):
            enemies[i].draw()
        
        pygame.display.update()

# MENU:
#   1: game, 2: how to play, 3: quit

# GAME:
#   1: menu, 2: replay, 3: quit

quit = False
while True:
    men = menu()
    if men == 1:
        dif = difficulty()
        if dif == 0: break
        gam = game(dif)
        if gam == 1:
            pass
        elif gam == 2:
            while game(dif) == 2:
                pass
        else:
            quit = True
    elif men == 2:
        if not howToPlay():
            break
    else:
        quit = True
    
    if quit:
        info.close()


