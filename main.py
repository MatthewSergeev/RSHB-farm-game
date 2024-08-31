import pygame
import sys

pygame.init()
win = pygame.display.set_mode((1024, 768))

pygame.display.set_caption("RSHB")

walkRight = [pygame.image.load('farmer_right-1.png'),  pygame.image.load('farmer_right-2.png'), pygame.image.load('farmer_right-3.png'), pygame.image.load('farmer_right-4.png')]
walkLeft = [pygame.image.load('farmer_left-1.png'),  pygame.image.load('farmer_left-2.png'), pygame.image.load('farmer_left-3.png'), pygame.image.load('farmer_left-4.png')]
playerStand = pygame.image.load('farmer_front.png')
sea = pygame.image.load('back.png')

farmerStand = [pygame.image.load('carrot-1.png'), pygame.image.load('carrot-2.png'), pygame.image.load('carrot-3.png'), pygame.image.load('carrot-4.png'), pygame.image.load('carrot-5.png')]
farmerRight = farmerStand
farmerLeft = farmerStand

r_lopata = [pygame.image.load('lopata-1.png'), pygame.image.load('lopata-2.png'), pygame.image.load('lopata-3.png'), pygame.image.load('lopata-4.png'), pygame.image.load('lopata-5.png'), pygame.image.load('lopata-6.png')]
l_lopata = [pygame.image.load('lopata-1 (1).png'), pygame.image.load('lopata-2 (1).png'), pygame.image.load('lopata-3 (1).png'), pygame.image.load('lopata-4 (1).png'), pygame.image.load('lopata-5 (1).png'), pygame.image.load('lopata-6 (1).png'),]

clock = pygame.time.Clock()

x = 50
y = 40

x1 = 500
y1 = 550
speed = 5
isJump = False
jumpCount = 10

r = 0
left = False
right = False
lastMove = "right"
class player():
    def __init__(self, x1, y1, t):
        self.x1 = x1
        self.y1 = y1
        self.t = t
    def draw(self, win):
        if self.t + 1 >= 9:
            self.t = 0
        if left:
            win.blit(walkLeft[self.t // 3], (self.x1, self.y1))
            self.t += 1
        elif right:
            win.blit(walkRight[self.t // 3], (self.x1, self.y1))
            self.t += 1
        else:
            win.blit(playerStand, (self.x1, self.y1))

        for bullet in bullets:
            bullet.draw(win)

class farmer():
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.t = 0
        self.r = r
    def draw(self, win):
        if self.t + 1 >= 25:
            self.t = 0
        if self.r == 0:
            win.blit(farmerStand[self.t // 5], (self.x, self.y))
        if self.r == 1:
            win.blit(farmerRight[self.t // 5], (self.x, self.y))
        if self.r == -1:
            win.blit(farmerLeft[self.t // 5], (self.x, self.y))
        self.t += 1

class lopata():
    def __init__(self, x1, y1, facing):
        self.x1 = x1
        self.y1 = y1
        self.facing = facing
        self.vel = 12 * facing
        self.t = 0
    def draw(self, win):
        if self.t + 1 >= 30:
            self.t = 0
        if self.facing == 1 or self.facing == 0:
            win.blit(r_lopata[self.t // 5], (self.x1, self.y1))
            self.t += 1
        if self.facing == -1:
            win.blit(l_lopata[self.t // 5], (self.x1, self.y1))
            self.t += 1
def drawWindow():

    win.blit(sea, (0, 0))

    player.draw(win)

    myfarmer.draw(win)

    pygame.display.update()

run = True
bullets = []
myfarmer = farmer(x, y, r)
player = player(x1, y1, 0)
while run:
    clock.tick(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    for bullet in bullets:
        if bullet.x1 < 1024 and bullet.x1 > -40:
            bullet.x1 += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))
        if abs(bullet.x1 - myfarmer.x) < 15 and abs(bullet.y1 - myfarmer.y) < 15:
            game_win_text = pygame.font.SysFont('arial', 36).render("YOU WIN", 1, (255, 0, 0))
            game_win_rect = game_win_text.get_rect(center=(525, 425))
            win.blit(game_win_text, game_win_rect)
            pygame.display.update()
            pygame.time.delay(2000)
            pygame.quit()
            sys.exit(0)

    if ((player.x1-myfarmer.x)**2+(player.y1-myfarmer.y)**2) <= 40**2:
        myfarmer.r = 0
        game_over_text = pygame.font.SysFont('arial', 36).render("GAME OVER", 1, (255, 0, 0))
        game_over_rect = game_over_text.get_rect(center=(525, 425))
        win.blit(game_over_text, game_over_rect)
        pygame.display.update()
        pygame.time.delay(2000)
        pygame.quit()
        sys.exit(0)
    else:
        if myfarmer.x >= player.x1:
            myfarmer.r = -1
            myfarmer.x -= 2
        if myfarmer.x < player.x1:
            myfarmer.r = 1
            myfarmer.x += 2
        if myfarmer.y < player.y1:
            myfarmer.y += 1
        if myfarmer.y >= player.y1:
            myfarmer.y -= 1

    keys = pygame.key.get_pressed()

    if keys[pygame.K_f]:
        if lastMove == "right":
            facing = 1
        else:
            facing = -1
        if len(bullets) < 1:
            bullets.append(lopata(player.x1, player.y1-15, facing))

    if keys[pygame.K_LEFT] and player.x1 > -115:
        player.x1 = player.x1 - speed
        left = True
        right = False
        lastMove = "left"
    elif keys[pygame.K_RIGHT] and player.x1 < 1000 - 40:
        player.x1 = player.x1 + speed
        left = False
        right = True
        lastMove = "right"
    else:
        left = False
        right = False
        player.t = 0
    if not(isJump):
        if keys[pygame.K_UP] and player.y1 > 350:
            player.y1 = player.y1 - speed
        if keys[pygame.K_DOWN] and player.y1 < 600:
            player.y1 = player.y1 + speed
        if keys[pygame.K_SPACE]:
            isJump = True
    else:
        if jumpCount >= -10:
            if jumpCount < 0:
                player.y1 = player.y1 + (jumpCount**2)//2
            else:
                player.y1 = player.y1 - (jumpCount**2)//2
            jumpCount = jumpCount - 1
        else:
            isJump = False
            jumpCount = 10

    drawWindow()

pygame.quit()
sys.exit(0)
