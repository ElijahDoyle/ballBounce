import pygame

class node():
    def __init__(self, pos, sideLength, color, parent):
        self.parent = parent;
        self.obstacle = False
        self.start = False
        self.end = False
        self.pos = pos
        self.sideLength = sideLength
        self.color = color
        self.g = 0
        self.h = 0
        self.f = 0

    def draw(self, window):
        self.pos = tuple(self.pos)

        pygame.draw.rect(window, self.color, [self.pos[0] +1 , self.pos[1] + 1, self.sideLength - 1, self.sideLength- 1], 0)

    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.sideLength, self.sideLength)