import pygame
from vector2 import Vector2
import math
import random

class Ball:
    def __init__(self,x,y,radius, vx,vy):
        self.position = Vector2(x,y)
        self.velocity = Vector2(vx,vy)
        self.clicked = False
        self.radius = radius
        self.mass = self.radius ** 2
        self.drag = .999
        self.gravity = Vector2(0, .35)
        self.elasticity = 0.875
        self.angle = math.atan2(self.velocity.y, self.velocity.x)
        self.magnitude = self.velocity.get_magnitude()
        self.color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))

    def display(self,screen, showVectors):
        pygame.draw.circle(screen,self.color,(int(self.position.x), int(self.position.y)),int(self.radius),0)
        if showVectors:
            pygame.draw.line(screen, (0, 0, 225), (self.position.x, self.position.y),
                             (self.position.x + math.cos(self.angle) * self.magnitude * 10, self.position.y), 5)
            pygame.draw.line(screen, (255, 0, 0), (self.position.x, self.position.y),
                             (self.position.x, self.position.y + math.sin(self.angle) * self.magnitude * 10), 5)
            pygame.draw.line(screen, (200, 50, 255), (self.position.x, self.position.y), (
            (self.position.x + math.cos(self.angle) * self.magnitude * 10), self.position.y + math.sin(self.angle) * self.magnitude * 10), 5)

    def update(self, seconds):

        if not self.clicked:
            self.magnitude = self.velocity.get_magnitude()
            self.angle = math.atan2(self.velocity.y, self.velocity.x)
            self.position = self.position.add(self.velocity) #changes the ball's position based on its velocity
            self.position = self.position.mul(seconds)
            self.velocity = self.velocity.mul(self.drag) #multiplies the velocity vector by the drag scalar
            self.velocity = self.velocity.add(self.gravity) #applies gravity to the ball
        else:
            self.magnitude = 0
            self.velocity = Vector2(math.cos(self.angle) * (self.magnitude * 0.95), math.sin(self.angle) *
                                    (self.magnitude * self.elasticity))

    def bounce(self, width, height):
        if self.position.x > width - self.radius:
            self.position.x = width - self.radius
            self.angle = math.pi - self.angle
            self.magnitude *= self.elasticity
            self.velocity = Vector2(math.cos(self.angle) * self.magnitude, math.sin(self.angle) * self.magnitude)


        elif self.position.x < self.radius:
            self.position.x = self.radius
            self.angle = math.pi - self.angle
            self.magnitude *= self.elasticity
            self.velocity = Vector2(math.cos(self.angle) * self.magnitude, math.sin(self.angle) * self.magnitude)


        if self.position.y > height - self.radius:

            if self.velocity.y > 2 or self.clicked:
                self.position.y = height - self.radius
                self.angle = - self.angle
                self.magnitude *= self.elasticity
                self.velocity = Vector2(math.cos(self.angle) * self.magnitude, math.sin(self.angle) * self.magnitude)
                if self.velocity.y <= 3:

                    self.velocity = Vector2(math.cos(self.angle) * (self.magnitude * 0.98), math.sin(self.angle) *
                                            (self.magnitude * self.elasticity))

            else:
                self.angle = - self.angle
                self.velocity = Vector2(math.cos(self.angle) * (self.magnitude * 0.95), math.sin(self.angle) *
                                        (self.magnitude* self.elasticity))




        elif self.position.y < self.radius:
            self.position.y = self.radius
            self.angle = - self.angle
            self.magnitude *= self.elasticity
            self.velocity = Vector2(math.cos(self.angle) * self.magnitude, math.sin(self.angle) * self.magnitude)

