import pygame

class Level:
    """This class will load our levels from a file so we can use them in our game"""
    def __init__(self, filename):
        self.filename = filename
        self.tiles = []
        self.load()

    def load(self):
        if self.filename == None:
            self.tiles = [[0 if j < 11 else 1 for i in range(16)] for j in range(12)]
            # save this to a file called default.txt
            with open('default.txt', 'w') as f:
                for row in self.tiles:
                    f.write("".join(str(i) for i in row) + "\n")
            self.filename = 'default.txt'
        # if they do have a file
        else:
            with open(self.filename, 'r') as f:
                for row in f:
                    self.tiles.append([int(row[i]) for i in range(len(row)) if row[i] != '\n'])
    

    def draw(self, surface):
        for y in range(len(self.tiles)):
            for x in range(len(self.tiles[0])):
                    if self.tiles[y][x] == 1:
                        pygame.draw.rect(surface, (0,255,0), (x * 50, y * 50, 50, 50) )



pygame.init()
screen = pygame.display.set_mode((800,600))


level = Level('default.txt')
print(level.tiles)
level.draw(screen)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.flip()