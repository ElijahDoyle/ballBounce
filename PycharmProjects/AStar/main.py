import pygame
import tkinter as tk
from tkinter import *
import tkinter.font as tkFont
import os
from drawGrid import createGrid
from controller import Controller
from findLowest import lowestFcost

root = tk.Tk()
times = tkFont.Font(family="Times", size=20)
embed = tk.Frame(root, width = 500, height = 500) #creates embed frame for pygame window
embed.grid(columnspan = (500), rowspan = 500) # Adds grid
embed.pack(side = LEFT) #packs window to the left
buttonwin = tk.Frame(root, width = 100, height = 500)
buttonwin.pack(side = RIGHT)
os.environ['SDL_WINDOWID'] = str(embed.winfo_id())
os.environ['SDL_VIDEODRIVER'] = 'windib'
screen = pygame.display.set_mode((500,500))
screen.fill(pygame.Color(255,255,255))
pygame.display.init()
clock = pygame.time.Clock()

MainControl = Controller()

MainControl.grid = createGrid( 25,25, 500, 500, 20, screen)

def distBetween(pos1,pos2, interval):
    xDiff = abs((pos1[0] - pos2[0])) / interval
    yDiff = abs((pos1[1] - pos2[1])) / interval
    if xDiff < yDiff:
        return 14*xDiff + 10 *(yDiff - xDiff)
    return 14*yDiff + 10 * (xDiff- yDiff)

def setDraw():
    MainControl.placingStart = False
    MainControl.placingEnd = False
    MainControl.drawing = True
def reset():
    MainControl.startingNode = None
    MainControl.targetNode = None
    MainControl.grid = createGrid(25, 25, 500, 500, 20, screen)
    for square in MainControl.grid:
        square.start = False
        square.end = False
        square.draw(screen)
        pygame.display.update()
        root.update()
    print('gamer')
def setStart():
    MainControl.placingStart = True
    MainControl.placingEnd = False
    MainControl.drawing = False
def setEnd():
    MainControl.placingStart = False
    MainControl.placingEnd = True
    MainControl.drawing = False
def run():
    for square in MainControl.grid:
        if square.start:
            MainControl.interval = square.sideLength
            MainControl.startingNode = square
        elif square.end:
            MainControl.targetNode = square
    if(MainControl.startingNode != None and MainControl.targetNode != None):
        MainControl.running = True
        MainControl.placingStart = False
        MainControl.placingEnd = False
        MainControl.drawing = False

button1 = Button(buttonwin, text='Draw', command=setDraw, width=5, height=2,font=times)
button2 = Button(buttonwin, text = 'Reset', command=reset, width=5, height=2,font=times)
button3 = Button(buttonwin, text = 'Place\nstart', command=setStart, width=5, height=2,font=times)
button4 = Button(buttonwin, text = 'Place\n target', command=setEnd, width=5, height=2,font=times)
button5 = Button(buttonwin, text = 'Run', command=run, width=5, height=2, font=times)
button1.pack(side=TOP)
button5.pack(side=BOTTOM)
button2.pack(side=BOTTOM)
button4.pack(side=BOTTOM)
button3.pack(side=BOTTOM)



done = False
while not done:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                MainControl.leftMouseDown = True
            elif event.button == 3:
                MainControl.rightMouseDown = True
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                MainControl.leftMouseDown = False
            elif event.button == 3:
                MainControl.rightMouseDown = False

        if MainControl.leftMouseDown:
            if MainControl.drawing:
                for square in MainControl.grid:
                    tempRect = square.rect()
                    if tempRect.collidepoint(pygame.mouse.get_pos()):
                        square.obstacle = True
                        square.color = (0, 0, 0)
                        square.draw(screen)
            elif MainControl.placingStart:
                for square in MainControl.grid:
                    tempRect = square.rect()
                    if square.start == True:
                        square.start = False
                        square.color = (255,255,255)
                        square.draw(screen)
                    if tempRect.collidepoint(pygame.mouse.get_pos()) and square.end == False:
                        square.start = True
                        square.color = (0, 255, 0)
                        square.draw(screen)
            elif MainControl.placingEnd:
                for square in MainControl.grid:
                    tempRect = square.rect()
                    if square.end == True:
                        square.end = False
                        square.color =(255, 255, 255)
                        square.draw(screen)
                    if tempRect.collidepoint(pygame.mouse.get_pos()) and square.start == False:
                        square.end = True
                        square.color = (255, 0, 0)
                        square.draw(screen)
        if MainControl.rightMouseDown:
            if MainControl.drawing:
                for square in MainControl.grid:
                    tempRect = square.rect()
                    if tempRect.collidepoint(pygame.mouse.get_pos()):
                        square.obstacle = False
                        square.color = (255, 255, 255)
                        square.draw(screen)

    currentNode = None
    open = []
    closed = []
    while MainControl.running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                MainControl.running = False
                break
                done = True
                quit()
                exit()

        if open == []:
            open.append(MainControl.startingNode)

        currentNodeIndex = lowestFcost(open)
        currentNode = open[currentNodeIndex]
        if currentNode != MainControl.startingNode and currentNode != MainControl.targetNode:
            currentNode.color = (200,200,200)
        currentNode.draw(screen)
        pygame.display.update()
        closed.append(currentNode)
        open.pop(currentNodeIndex)

        if currentNode == MainControl.targetNode:
            print("done")
            tempNode = currentNode
            while tempNode != MainControl.startingNode :
                tempNode.parent.color = (255,255,0)
                tempNode.draw(screen)
                pygame.display.update()
                tempNode = tempNode.parent

            MainControl.running = False


        for direction in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
            tempAdjacentPosition = (currentNode.pos[0] + (direction[0] * MainControl.interval), currentNode.pos[1] + (direction[1] * MainControl.interval))
            for node in MainControl.grid:
                if (node in closed or node.obstacle):
                    continue
                elif node.pos == tempAdjacentPosition and 500 >= node.pos[0] >= 0 and 500 >= node.pos[1] >= 0:

                    if node != MainControl.targetNode:
                        node.color = (0,255,255)
                    node.g = currentNode.g + distBetween(currentNode.pos, node.pos, MainControl.interval)
                    node.h = distBetween(node.pos, MainControl.targetNode.pos, MainControl.interval)
                    node.f = node.g + node.h
                    node.draw(screen)
                    pygame.display.update()

                    if(node in open):
                        if node.g > currentNode.g:
                            continue
                    node.parent = currentNode
                    open.append(node)
        clock.tick(60)


    clock.tick(60)
    pygame.display.update()
    if done ==False:
        root.update()