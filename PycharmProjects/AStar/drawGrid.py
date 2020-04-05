import pygame
from gridSquare import node

def createGrid(columns, rows, width, height, interval, surface):

    x = 0
    y = 0
    gridList=[]
    for c in range(0, columns):
        x += interval
        pygame.draw.line(surface, (0,0,0), (x,0), (x, height), 1)
        for r in range (0, rows):
            tempSquare = node((x-interval ,r * interval ), interval , (255,255,255), None)
            tempSquare.draw(surface)
            gridList.append(tempSquare)

    for r in range(0, rows):
        y += interval
        pygame.draw.line(surface, (0,0,0), (0,y), (width, y), 1)

    return gridList