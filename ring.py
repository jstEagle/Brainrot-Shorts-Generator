import pygame
import ball as b
pygame.init()

class Ring:
    def __init__(self, x, y, r, background_colour=(250, 250, 250), colour=(80, 80, 80), width=10):
        self.x = x
        self.y = y
        self.r = r
        self.width = width
        self.background = background_colour
        self.colour = colour
    
    def draw(self, screen):
        pygame.draw.circle(screen, self.colour, (self.x, self.y), self.r + self.width)
        pygame.draw.circle(screen, self.background, (self.x, self.y), self.r)