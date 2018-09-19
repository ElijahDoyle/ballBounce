import pygame
import random
import math
import time


elasticity = 0.875
gravity = .35
drag = 0.999


def collide(p1, p2):
    dx = p1.x - p2.x
    dy = p1.y - p2.y

    dist = math.hypot(dx, dy)
    if dist < p1.radius + p2.radius:
        dist_x = p1.x - p2.x
        dist_y = p1.y - p2.y

        axe = math.atan2(dist_y, dist_x * -1)

        angle_to_pass = axe - math.pi * 0.5

        speed_to_collide_1 = math.cos(axe - p1.angle) * p1.speed
        speed_to_pass_1 = math.sin(axe - p1.angle) * p1.speed

        speed_to_collide_2 = math.cos(axe - p2.angle) * p2.speed
        speed_to_pass_2 = math.sin(axe - p2.angle) * p2.speed

        speed_after_1 = (speed_to_collide_1 * (p1.mass - p2.mass) + 2 * p2.mass * speed_to_collide_2) / (
                p1.mass + p2.mass)
        speed_after_2 = (speed_to_collide_2 * (p2.mass - p1.mass) + 2 * p1.mass * speed_to_collide_1) / (
                p1.mass + p2.mass)

        (p1.angle, p1.speed) = addVectors(axe, speed_after_1, angle_to_pass, speed_to_pass_1)
        (p2.angle, p2.speed) = addVectors(axe, speed_after_2, angle_to_pass, speed_to_pass_2)

        # prevents particles from overlapping
        overlap = 0.5 * (p1.radius + p2.radius - math.hypot(dist_x, dist_y) + 1)
        p1.x -= math.cos(axe) * overlap
        p2.x += math.cos(axe) * overlap
        p1.y += math.sin(axe) * overlap
        p2.y -= math.sin(axe) * overlap


def addVectors(angle1, length1, angle2, length2):
    x = math.sin(angle1) * length1 + math.sin(angle2) * length2
    y = math.cos(angle1) * length1 + math.cos(angle2) * length2

    angle = 0.5 * math.pi - math.atan2(y, x)
    length = math.hypot(x, y)
    return angle, length



class Ball:
    def __init__(self,x,y,radius, angle, speed):
        self.x = x
        self.y = y
        self.radius = radius
        self.speed = speed
        self.angle = angle
        self.vx = math.sin(self.angle) * self.speed
        self.vy = math.cos(self.angle) * self.speed
        self.clicked = False
        self.mass = self.radius ** 2

    def display(self,screen,showVectors):
        pygame.draw.circle(screen,(250,250,250),(int(self.x),int(self.y)),int(self.radius),0)
        if showVectors:
            pygame.draw.line(screen, (0, 0, 225), (self.x, self.y), (self.x + math.sin(self.angle) * self.speed * 15, self.y), 5)
            pygame.draw.line(screen, (255,0, 0), (self.x, self.y), (self.x, self.y - math.cos(self.angle) * self.speed * 15), 5)
            pygame.draw.line(screen, (200, 50, 255), (self.x, self.y), ((self.x + math.sin(self.angle) * self.speed * 15) , self.y - math.cos(self.angle) * self.speed * 15), 5)

    def move(self):
        self.speed *= drag
        (self.angle,self.speed) = addVectors(self.angle, self.speed,  math.pi, gravity)
        # this is gravity, bc no tuple unpacking ):
        self.vx = math.sin(self.angle) * self.speed
        self.vy = math.cos(self.angle) * self.speed
        if not self.clicked:
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_LEFT]:
                (self.angle, self.speed) = addVectors(self.angle, self.speed, (3 * math.pi) / 2, 0.1)

            if pressed[pygame.K_RIGHT]:
                (self.angle, self.speed) = addVectors(self.angle, self.speed, (math.pi) / 2, 0.1)

            if pressed[pygame.K_UP]:
                (self.angle, self.speed) = addVectors(self.angle, self.speed, 0, 0.4)

            if pressed[pygame.K_DOWN]:
                (self.angle, self.speed) = addVectors(self.angle, self.speed, (math.pi), 0.1)
            self.x += self.vx
            self.y -= self.vy

    def bounce(self, width, height, surfaceList):
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

        for surface in surfaceList:

            if self.y + self.radius*2 >= surface.yMin and surface.xMin - self.radius / 2 <= self.x <= surface.xMax + self.radius / 2 and self.y <= self.x * surface.slope + surface.intercept + self.radius <= self.y + self.radius*2:

                if self.y >= self.x*surface.slope + surface.intercept:
                    self.y += 1
                else:
                    self.y -= 1

                if surface.slantDown == True:
                    self.x += 1
                    if self.angle > math.pi:
                        newAngle = self.angle - math.pi
                        otherAngle = math.pi - (math.atan(abs(surface.x1-surface.x2)/abs(surface.y1-surface.y2))+ newAngle)
                        self.angle += 2*otherAngle
                        self.speed *= elasticity
                    elif self.angle <= math.pi:
                        newAngle = math.pi - self.angle
                        otherAngle = math.pi - ((math.pi - math.atan(abs(surface.x1 - surface.x2) / abs(surface.y1 - surface.y2))) + newAngle)
                        self.angle -= 2*otherAngle
                        self.speed *= elasticity
                else:
                    self.x -=1
                    if self.angle > math.pi:
                        newAngle = self.angle - math.pi
                        otherAngle = math.pi - ((math.pi - math.atan(abs(surface.x1-surface.x2)/abs(surface.y1-surface.y2)))+ newAngle)
                        self.angle += 2*otherAngle
                        self.speed *= elasticity
                    elif self.angle <= math.pi:
                        newAngle = math.pi - self.angle
                        otherAngle = math.pi - (math.atan(abs(surface.x1 - surface.x2) / abs(surface.y1 - surface.y2)) + newAngle)
                        self.angle -= 2*otherAngle
                        self.speed *= elasticity


                  #  print("a")


class Surface:
    def __init__(self,x1,y1,x2,y2,color):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
#basically a pair of x,y coords
        self.slope = (self.y2-self.y1)/(self.x2-self.x1)
        if self.slope == 0:
            self.slope = 1

        self.angle = math.atan(abs(self.y1-self.y2)/abs(self.x1-self.x2))
        self.color = color
        self.intercept = self.y1 - (self.x1 * self.slope)

        if self.x1 > self.x2:
            self.xMax = self.x1
            self.xMin = self.x2
        else:
            self.xMax = self.x2
            self.xMin = self.x1

        if self.y1 < self.y2:
            self.yMin = self.y1
            self.slantDown = True
            self.yMax = self.y2
        else:
            self.yMin = self.y2
            self.yMax = self.y1
            self.slantDown = False
    def display(self, displaySurface):
        pygame.draw.line(displaySurface, self.color, (self.x1, self.y1), (self.x2, self.y2),5)


screenWidth = 1000
screenHeight = 500

line1 = Surface(60, 100,450,350,(0,255,0))
line2 = Surface(600,350 ,900, 200,(255,0,0))
lineList = [line1,line2]

thing = Ball(random.randint(50,screenWidth - 50),random.randint(50,screenHeight - 50),30,random.uniform(0, math.pi * 2), random.uniform(2,6))
ballList = [thing]
pygame.init()
screen = pygame.display.set_mode((screenWidth,screenHeight))
done = False
clock = pygame.time.Clock()
clicked = None
alreadyClicked = False
lastTime = 0
paused = False
showVectors = False
Ygravity = True
Ydrag = True
Yelasticity = True
mcount = 0
momentumList = []
avgMomentumList = []
#for n in range(0):
 #   ball = Ball(random.randint(50,500),random.randint(50,500),random.randint(20,50), random.uniform(0, math.pi * 2), random.uniform(6,20))
  #  ballList.append(ball)


while not done:

    (a, b) = pygame.mouse.get_pos()
    clickBox = pygame.Rect(a, b, 2, 2)
    screen.fill((0,0,0))
    for line in lineList:
        #      pressed = pygame.key.get_pressed()
        #
        #       if pressed[pygame.K_LEFT]:
        #          ball.vx -= 8
        #         ball.x += ball.vx
        #    if pressed[pygame.K_RIGHT]:
        #       ball.vx += 8
        #      ball.x += ball.vx
        line.display(screen)

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            clicked = True
        elif event.type == pygame.MOUSEBUTTONUP:
            clicked = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                ball = Ball(random.randint(50,screenWidth - 50),random.randint(50,screenHeight - 50),random.randint(5,50),random.uniform(0, math.pi * 2), random.uniform(2,6))
                ballList.append(ball)
            if event.key == pygame.K_p:
                paused = True
                while paused:
                    pygame.time.wait(100)
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN and event.key == pygame.K_u:
                            paused = False
            if event.key == pygame.K_s:
                if showVectors:
                    showVectors = False
                else:
                    showVectors = True
            if event.key == pygame.K_g:
                if Ygravity:
                    Ygravity = False
                    gravity = 0
                else:
                    Ygravity = True
                    gravity = 0.35
            if event.key == pygame.K_r:
                if Ydrag:
                    drag = 1
                    Ydrag = False
                else:
                    Ydrag = True
                    drag = 0.999
            if event.key == pygame.K_e:
                if Yelasticity:
                    Yelasticity = False
                    elasticity = 1
                else:
                    Yelasticity = True
                    elasticity = .875
            if event.key == pygame.K_d:
                if len(ballList) > 1:
                    index = random.randint(0,len(ballList) - 1)
                    if ballList[index].clicked:
                        alreadyClicked = False
                        clicked = False
                    ballList.remove(ballList[index])
        if event.type == pygame.QUIT:
            done = True
    velocity = 0


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
            ball.speed = math.hypot(dx, dy) * 0.5
  #      pressed = pygame.key.get_pressed()
#
 #       if pressed[pygame.K_LEFT]:
  #          ball.vx -= 8
   #         ball.x += ball.vx
    #    if pressed[pygame.K_RIGHT]:
     #       ball.vx += 8
      #      ball.x += ball.vx

        ball.move()
        ball.bounce(screenWidth, screenHeight,lineList)
        ball.display(screen,showVectors)

        for otherBall in ballList:

            if otherBall is not ball:
                collide(ball, otherBall)

        momentum = ball.speed * ball.mass
        momentumList.append(momentum)

    if pygame.time.get_ticks() > lastTime + 1000:
        momen = 0
        for value in momentumList:
            momen += value
        avgMomentumList.append(momen)
        for line in range(10):
            print("")
        print("Drag: " + str(drag))
        print("Momentum: " + str(momen))
        print("Elasticity: " + str(elasticity))
        print("Gravity : " + str(gravity))
        print("showVectors: " + str(showVectors))
        lastTime = pygame.time.get_ticks()
        mcount += 1
        momentumList = []
        if mcount == 10:
            mcount = 0
            avgmomen = 0
            for val in avgMomentumList:
                avgmomen += val
            avgmomen = avgmomen / 10
            print("Average Momentum: " + str(avgmomen))
            avgMomentumList = []


    pygame.display.update()
    clock.tick(60)