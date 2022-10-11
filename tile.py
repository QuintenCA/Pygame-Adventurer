import pygame

class Tile(pygame.Rect):
    def __init__(self, left, top, width, height):
        super().__init__(left, top, width, height)

        self.position = [left, top]
        self.image = pygame.Surface([self.width, self.height])
        self.animated = False
        self.framecounter = 0
        self.framerate = 20
        
    def flip(self):
        self.image = pygame.transform.flip(self.image, True, False)

        return self.image

    def flop(self):
        self.image = pygame.transform.flip(self.image, False, True)

        return self.image

    def show(self, surface : pygame.Surface):
        surface.blit(self.image, self.position)

        if self.animated and self.framecounter % self.framerate == 0:
            self.flip()
            self.framecounter = 0
        
        self.framecounter += 1

