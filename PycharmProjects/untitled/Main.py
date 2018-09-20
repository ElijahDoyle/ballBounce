import pygame
from vector2 import Vector2
from Ball import Ball
import random
from Collisions import elasticCollisions


#initializing some variables
screenWidth = 750
screenHeight = 500
done = False
clock = pygame.time.Clock()
ballList = []
clicked = None
alreadyClicked = False
showVectors = False
gravityOn = True


#ball objects
testBall = Ball(screenWidth/2,screenHeight/2, 50, 3, -2)
ballList.append(testBall)


pygame.init()
screen = pygame.display.set_mode((screenWidth,screenHeight)) #sets the screen up

while not done: #this is the main loop
    screen.fill((0,0,0))
    (a, b) = pygame.mouse.get_pos()
    clickBox = pygame.Rect(a, b, 2, 2)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            clicked = True
        elif event.type == pygame.MOUSEBUTTONUP:
            clicked = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                newBall = Ball(random.randint(60,screenWidth - 60),random.randint(60,screenHeight - 60),
                               random.randint(10,60), random.randint(-10, 10), random.randint(-10, 10))
                ballList.append(newBall)
            if event.key == pygame.K_s:
                if showVectors:
                    showVectors = False
                else:
                    showVectors = True
            elif event.key == pygame.K_g:
                if gravityOn:
                    gravityOn = False
                else:
                    gravityOn = True


    elasticCollisions(ballList)
    for ball in ballList:
        if gravityOn:
            ball.gravity = Vector2(0, 0.35)
        else:
            ball.gravity = Vector2(0,0)
        ball.bounce(screenWidth,screenHeight)
        ball.update(1)
        ball.display(screen, showVectors)

        ball.hitbox = pygame.Rect(ball.position.x - ball.radius, ball.position.y - ball.radius, ball.radius * 2, ball.radius * 2)
        if ball.hitbox.colliderect(clickBox) and clicked and not alreadyClicked:
            alreadyClicked = True
            ball.clicked = True

        if ball.clicked and clicked:
            ball.position.x, ball.position.y = a, b
            ball.speed = 0
        elif ball.clicked and not clicked:
            clicked = False
            alreadyClicked = False
            ball.clicked = False
            (mouseX, mouseY) = pygame.mouse.get_pos()
            dx = mouseX - ball.position.x
            dy = mouseY - ball.position.y
            ball.velocity = Vector2(dx, dy)

    pygame.display.update()
    clock.tick(60)

