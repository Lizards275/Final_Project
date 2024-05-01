import pygame
import random

pygame.init()

WIDTH, HEIGHT = 800, 600

wn = pygame.display.set_mode((WIDTH, HEIGHT))

FPS = 60
clock = pygame.time.Clock()

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

all_sprites = pygame.sprite.Group()




class Entity(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image):
        super().__init__()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = image
        self.xVel = 0
        self.yVel = 0
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

class Player(Entity):
    pgroup = pygame.sprite.Group()
    def __init__(self):
        super().__init__(100, 100, 50, 100, None)
        self.grounded = False
        self.double_jumped = False
        self.health = 100
        Player.pgroup.add(self)

    def update(self):
        if self.image == None:
            pygame.draw.rect(wn, BLUE, (self.rect))
        else:
            pass
        # player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.yVel = -1
        if keys[pygame.K_s]:
            self.yVel += 1
        if keys[pygame.K_a]:
            if self.xVel > -5:
                self.xVel += -1
        if keys[pygame.K_d]:
            if self.xVel < 5:
                self.xVel += 1
        #Jumpinh
        if keys[pygame.K_SPACE]:
            current_time = pygame.time.get_ticks()
            if self.grounded == True:
                self.yVel -= 20
                self.grounded = False
                self.jump_delay = 300
                self.last_jump = current_time
            elif self.double_jumped == False and current_time - self.last_jump > self.jump_delay:
                self.yVel -= 15
                self.double_jumped = True
            else:
                # add a negative sound effect later
                pass
        
        






        
        #Barriers
        #X
        if self.rect.x < 1:
            self.xVel = 0
        elif self.rect.x > WIDTH - self.width:
            self.xVel = 0
            self.rect.x -= 1
        else: 
            self.rect.x += self.xVel
        # X Friction
        if self.xVel > 0:
            self.xVel -= .5
        if self.xVel < 0:
            self.xVel += .5

        
        #Y
        
        if self.rect.x > 0 and self.x < WIDTH - self.width:
            self.rect.x += self.xVel
        else:
            self.rect.x += 10

        if self.rect.y < HEIGHT - self.height:
            self.rect.y += self.yVel
      
        #GRAVITY

        if pygame.sprite.spritecollide(self, Platform.plats, False):
            self.yVel = 0
            cols = pygame.sprite.spritecollide(self, Platform.plats, False)
            for col in cols:
                if self.rect.y < col.rect.y:        
                    self.rect.y = col.rect.y - self.height
                    self.double_jumped = False
                    self.grounded = True
                if self.rect.y > col.rect.y:
                    self.rect.y = col.rect.y + col.height
                    
        else:
            self.yVel += 1

        enemy_hits = pygame.sprite.spritecollide(self, Enemy.enemies, False)

        for col in enemy_hits:
            if self.rect.y < col.rect.y + self.rect.height - 5:
                col.alive = False
                self.yVel = -15



class Platform(Entity):
    plats = pygame.sprite.Group()
    def __init__(self, x, y, width, height, image):
        super().__init__(x, y, 50, 50, None)
        Platform.plats.add(self)
    def update(self):
        pygame.draw.rect(wn, GREEN, (self.rect))

class Enemy(Entity):
    enemies = pygame.sprite.Group()
    def __init__(self, x, y, width, height, image):
        super().__init__(x,y,width,height,image)
        self.alive = True
        self.dir = 1
        self.timer = 0
        self.turn_time = 1000
        self.yVel = 0
        self.enemies.add(self)
        if self.image == None:
            self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        else:
            self.rect = self.image.get_rect()

    def update(self):
        if self.alive:
            #Move back and forth
            if self.dir == 1 and self.timer < self.turn_time:
                self.rect.x += 1
            else:
                self.rect.x -= 1
            
            if self.timer < self.turn_time:
                self.timer = pygame.time.get_ticks()
            else:
                self.dir *= -1
                self.timer = pygame.time.get_ticks()
                self.turn_time = pygame.time.get_ticks() + 1000
            
        else:
            Enemy.enemies.remove(self)
            self.yVel += 1

            if self.rect.y > HEIGHT:
                self.kill()
        #Draw enemy
        self.rect.y += self.yVel
        if self.image == None:
            pygame.draw.rect(wn, RED, self.rect)

        

class Bullet(Entity):
    bullets = pygame.sprite.Group()
    def __init__(self):
        super().__init__((175,0,175), 5, 20, player.rect.x + 25, player.rect.y + 25)
        Bullet.bullets.add(self)
    def update(self):
        self.rect.x += 10
        if self.rect.x > WIDTH:
            self.kill()
        if pygame.sprite.spritecollide(self, Enemy.enemies, True):
            self.kill()


        pygame.draw.rect(wn, self.color, self.rect)



class En_Bullet(Entity):
    bullets = pygame.sprite.Group()
    def __init__(self,x,y):
        super().__init__((0,200,200), 5, 20, x, y + 12)
        En_Bullet.bullets.add(self)
    def update(self):
        self.rect.x -= 7
        if self.rect.x < 0:
            self.kill()
        if pygame.sprite.spritecollide(self, Player.pgroup, False):
            self.kill()
        pygame.draw.rect(wn, self.color, self.rect)






# Instantiate objects
player = Player()

enemy = Enemy(600,375,25,25,None)



#Make platforms, later we will move this to a level class
for i in range(10):
    Platform(i * 50, HEIGHT - 50, 50, 50, None)

startX = 600
for i in range(10):
    Platform(startX, 400,50,50,None)
    startX += 50

Platform(300, 350, 50, 50, None)


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if Bullet.bullets.__len__() < 5:
                    Bullet()
    wn.fill(WHITE)
    player.update()
    enemy.update()
    for plat in Platform.plats:
        plat.update()


    pygame.display.flip()
    clock.tick(FPS)

