import pygame

class Controller():
    def __init__(self):
        self.drawing = False
        self.interval = None
        self.placingStart = False
        self.placingEnd = False
        self.leftMouseDown = False
        self.rightMouseDown = False
        self.running = False
        self.grid = None


        self.startingNode = None
        self.targetNode = None



