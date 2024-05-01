'''
In Pygame sprites are the things that move
Players, enemies, bullets, ships, powerups, etc.
Sprites are usually represented by a rectangle
We can add images to the rectangle to make it look like something
The sprite class has a few extra methods that make it easier to work with
'''

import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
wn = pygame.display.set_mode((WIDTH, HEIGHT))


FPS = 60
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()





# MARK: Player Class
# defining a class to inherit from the sprite class
class Box(pygame.sprite.Sprite):
    def __init__(self, color, height, width, x, y):
        super().__init__()
        self.color = color
        self.rect = pygame.Rect(x, y, width, height)
        # add to the all sprites group
        all_sprites.add(self)
    
    # override the update method    
    def update(self):
        pygame.draw.rect(wn, self.color, self.rect)
        
print(Box.__bases__)
blue_box = Box((0, 0, 255), 50, 50, 150, 150)

class Player(Box):
    pgroup = pygame.sprite.Group()
    def __init__(self):
        super().__init__((200,200,0), 50, 50 , 200, 200)
        print(Player.__bases__)
        print(isinstance(self, Box)) # True because it inherits from Box
        print(isinstance(self, pygame.sprite.Sprite)) # True because Box inherits from Sprite
        Player.pgroup.add(self)
        self.health = 100


    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_s]:
            # Move in place method allows you to change x and y in the same line
            self.rect.y += 5
        if keys[pygame.K_w]:
            self.rect.y -= 5
        if keys[pygame.K_a]:
            self.rect.x -= 5
        if keys[pygame.K_d]:
            self.rect.x += 5

        
        if pygame.sprite.spritecollide(self, enemies, True):
            self.rect.x = 200
            self.rect.y = 200

        if pygame.sprite.spritecollide(self, En_Bullet.bullets, True):
            self.health -= 10
            print(self.health)
        
        pygame.draw.rect(wn, (255, 0, 0), (self.rect.x, self.rect.y - 10, 50, 5))
        pygame.draw.rect(wn, (0, 255, 0), (self.rect.x, self.rect.y - 10, (self.health/2) , 5))


        pygame.draw.rect(wn, self.color, self.rect)
# MARK: Enemy Class
enemies = pygame.sprite.Group()
class Enemy(Box):
    def __init__(self):
        super().__init__((100,100,100), 25,25, random.randrange(300,500), random.randrange(100,500) )
        self.dir = random.choice(['up', 'down'])
        enemies.add(self)
    def update(self):
        if self.dir == 'up':
            if self.rect.y < 0:
                self.dir = 'down'
            else:
                self.rect.y -= 5
        elif self.dir == 'down':
            if self.rect.y > HEIGHT - self.rect.height:
                self.dir = 'up'
            else:
                self.rect.y += 5
            if random.randint(1,100) < 3:
                En_Bullet(self.rect.x, self.rect.y)
        pygame.draw.rect(wn, self.color, self.rect)

class Bullet(Box):
    bullets = pygame.sprite.Group()
    def __init__(self):
        super().__init__((175,0,175), 5, 20, player.rect.x + 25, player.rect.y + 25)
        Bullet.bullets.add(self)
    def update(self):
        self.rect.x += 10
        if self.rect.x > WIDTH:
            self.kill()
        if pygame.sprite.spritecollide(self, enemies, True):
            self.kill()


        pygame.draw.rect(wn, self.color, self.rect)

class En_Bullet(Box):
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

# MARK: Instantiating obejcts
player = Player()
for i in range(10):
    Enemy()
enemy = Enemy()

print(hasattr(player, 'color')) # True
print(hasattr(player, 'rect')) # True
print(hasattr(player, 'update')) # True
print(Player.__dict__)
print(player.__dict__)
# MARK: Game loop
running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if Bullet.bullets.__len__() < 5:
                    Bullet()

    if enemies.__len__() == 0:
        for i in range(10):
            Enemy()
    # Update Screen
    wn.fill((255, 255, 255))
    
    # draw sprites
    for sprite in all_sprites:
        sprite.update()
    
    
    pygame.display.update()