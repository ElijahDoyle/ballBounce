import pygame
import random
import math

drag = 1
elasticity = 1
gravity = .2

def collide(ball, otherBall):
    dx = ball.x - otherBall.x
    dy = ball.y - otherBall.y
    angle = math.atan2(dy, dx) + 0.5 * math.pi
    dist = math.hypot(dx, dy)
    if dist < ball.radius + otherBall.radius:
        bvx = math.sin(ball.angle) * ball.speed
        bvy = math.cos(ball.angle) * ball.speed
        ovx = math.sin(otherBall.angle) * otherBall.speed
        ovy = math.cos(otherBall.angle) * otherBall.speed

        ball.vx = (bvx * (ball.mass - otherBall.mass) + (2 * otherBall.mass * ovx)) / (ball.mass + otherBall.mass)
        ball.vy = (bvy * (ball.mass - otherBall.mass) + (2 * otherBall.mass * ovy)) / (ball.mass + otherBall.mass)
        otherBall.vx = (ovx * (otherBall.mass - ball.mass) + (2 * ball.mass * bvx)) / (ball.mass + otherBall.mass)
        otherBall.vy = (ovy * (otherBall.mass - ball.mass) + (2 * ball.mass * bvy)) / (ball.mass + otherBall.mass)

        overlap = 0.5 * (ball.radius + otherBall.radius - dist + 1)
        ball.x += math.sin(angle) * overlap
        ball.y -= math.cos(angle) * overlap
        otherBall.x -= math.sin(angle) * overlap
        otherBall.y += math.cos(angle) * overlap

        ball.speed = math.hypot(ball.vx, ball.vy) * elasticity
        otherBall.speed = math.hypot(otherBall.vx, otherBall.vy) * elasticity
        ball.angle = math.atan2(ball.vx, ball.vy)
        otherBall.angle = math.atan2(otherBall.vx, otherBall.vy)


def addVectors(angle1, length1, angle2, length2):
    x = math.sin(angle1) * length1 + math.sin(angle2) * length2
    y = math.cos(angle1) * length1 + math.cos(angle2) * length2

    angle = 0.5 * math.pi - math.atan2(y, x)
    length = math.hypot(x, y)
    return (angle, length)

class Ball:
    def __init__(self,x,y,radius, angle, speed, hangingPoint):
        self.x = x
        self.y = y
        self.radius = radius
        self.speed = speed
        self.angle = angle
        self.xv = math.sin(self.angle)
        self.clicked = False
        self.mass = self.radius ** 2
        self.hangingPoint = hangingPoint
        self.fullLength = False

    def move(self):
        self.speed *= drag
        if not self.fullLength:
            (self.angle,self.speed) = addVectors(self.angle, self.speed,  math.pi,gravity) # this is gravity, bc no tuple unpacking ):
        if not self.clicked:
            self.x += math.sin(self.angle) * self.speed
            self.y -= math.cos(self.angle) * self.speed

    def bounce(self, width, height):
        if self.x > width - self.radius:
            self.x = width - self.radius
            self.angle = - self.angle
            self.speed *= elasticity

        elif self.x < self.radius:
            self.x = self.radius
            self.angle = - self.angle
            self.speed *= elasticity

        if self.y > height - self.radius:
            self.y = height - self.radius
            self.angle = math.pi - self.angle
            self.speed *= elasticity

        elif self.y < self.radius:
            self.y = self.radius
            self.angle = math.pi - self.angle
            self.speed *= elasticity


    def display(self,screen):
        pygame.draw.circle(screen,(200,200,200),(int(self.x),int(self.y)),int(self.radius),0)
       # pygame.draw.line(screen, (0, 0, 225), (self.x, self.y), (self.x + math.sin(self.angle) * self.speed * 10, self.y), 3)
       # pygame.draw.line(screen, (255,0, 0), (self.x, self.y), (self.x, self.y - math.cos(self.angle) * self.speed * 10), 3)
       # pygame.draw.line(screen, (200, 50, 255), (self.x, self.y), ((self.x + math.sin(self.angle) * self.speed * 10) , self.y - math.cos(self.angle) * self.speed * 10), 3)


thing = Ball(200, 200,30,math.pi, 0, (200, 0))
otherThing = Ball(260, 200,30,math.pi, 0, (260, 0))
anotherThing = Ball(320, 200,30,math.pi, 0, (320, 0))
ballList = [thing, otherThing,anotherThing]
screenWidth = 600
screenHeight = 400
pygame.init()
screen = pygame.display.set_mode((screenWidth,screenHeight))
done = False
clock = pygame.time.Clock()
clicked = None
alreadyClicked = False
lastTime = 0



while not done:
    (a, b) = pygame.mouse.get_pos()
    clickBox = pygame.Rect(a, b, 2, 2)
    screen.fill((0,0,0))
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            clicked = True
        elif event.type == pygame.MOUSEBUTTONUP:
            clicked = False
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                paused = True
                while paused:
                    pygame.time.wait(100)
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN and event.key == pygame.K_u:
                            paused = False
    momentum = 0

    for ball in ballList:

        ball.hitbox = pygame.Rect(ball.x - ball.radius, ball.y - ball.radius, ball.radius * 2, ball.radius * 2)
        if ball.hitbox.colliderect(clickBox) and clicked and not alreadyClicked:
            alreadyClicked = True
            ball.clicked = True


        if ball.clicked and clicked:
            ball.x, ball.y = a, b
            ball.speed = 0

        elif ball.clicked and not clicked:
            clicked = False
            alreadyClicked = False
            ball.clicked = False
            (mouseX, mouseY) = pygame.mouse.get_pos()
            dx = mouseX - ball.x
            dy = mouseY - ball.y
            ball.angle = 0.5 * math.pi + math.atan2(dy, dx)
            ball.speed = math.hypot(dx, dy)

        dy = ball.y - ball.hangingPoint[1]
        dx = ball.x - ball.hangingPoint[0]
        angle = math.atan2(dy, dx)
        dist = math.hypot(dx, dy)
        length = 200
        if dist > length:
            ball.x = ball.hangingPoint[0] + math.cos(angle) * length
            ball.y = ball.hangingPoint[1] + math.sin(angle) * length
            if ball.x > ball.hangingPoint[0] + 5:
                ball.angle,ball.speed = addVectors(ball.angle,ball.speed, (ball.angle + math.pi / 2), gravity)
            elif ball.hangingPoint[0] + 5 > ball.x > ball.hangingPoint[0]:
                ball.angle, ball.speed = addVectors(ball.angle, ball.speed, (ball.angle + math.pi / 2), 0.1)

            elif ball.x < ball.hangingPoint[0] - 5:
                ball.angle,ball.speed = addVectors(ball.angle,ball.speed, (ball.angle + math.pi / 2), -gravity)
            elif ball.hangingPoint[0] - 5 < ball.x < ball.hangingPoint[0]:
                ball.angle, ball.speed = addVectors(ball.angle, ball.speed, (ball.angle + math.pi / 2), -0.1)
            ball.fullLength = True
        else:
            ball.fullLength = False




        for otherBall in ballList:
            if otherBall is not ball:
                collide(ball, otherBall)

        momentum += (ball.speed * ball.mass)
        ball.move()
        ball.bounce(screenWidth, screenHeight)
        ball.display(screen)
        pygame.draw.line(screen, (20, 255, 20), (ball.x, ball.y), ball.hangingPoint, 3)

    if pygame.time.get_ticks() > lastTime + 1000:
        for line in range(10):
            print("")
        print("Momentum: " + str(momentum))
        lastTime = pygame.time.get_ticks()

    pygame.display.update()
    clock.tick(60)