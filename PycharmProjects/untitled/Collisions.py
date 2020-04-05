from Ball import Ball
from vector2 import Vector2
import math

def dot_product(vec1,vec2):
    return  vec1.x * vec2.x + vec1.y * vec2.y

# detects when two objects touch
def collisionDetect(obj1,obj2):
    distance = ((obj1.position.x - obj2.position.x)**2 + (obj1.position.y - obj2.position.y)**2)**(1/2)
    if distance < obj1.radius + obj2.radius:
        return True
    else:
        return False

# not really sure what this is but i need it as a controller of some sort
def elasticCollisions(objectList):
    for ball in objectList:
        b1 = ball
        for otherBall in objectList:
            if otherBall != ball:
                b2 = otherBall

                if collisionDetect(b1,b2):
                   # print("collision")
                   collide(b1,b2)
                else:
                    pass

# the meat of this elastic collision project, it takes in two objects as arguments and runs them through elastic collision equations
def collide(obj1,obj2):
    p1 = obj1.position
    p2 = obj2.position
    m1 = obj1.mass
    m2 = obj2.mass
    v1 = obj1.velocity
    v2 = obj1.velocity
    totalMass = m1 + m2

#usually when my variables start with a d, it means they are the difference between two things

    dv1 = obj1.velocity.sub(obj2.velocity)  # the difference between obj1's velocity and obj2's
    dv2 = obj2.velocity.sub(obj1.velocity)  # the difference between obj2's velocity and obj1's

    dp1 = p1.sub(p2)  # the difference between obj1's position vector and obj2's
    dp2 = p2.sub(p1)  # the difference between obj2's position vector and obj1's

    dp1_magnitude = dp1.get_magnitude()  # just the magnitude of dp1
    dp2_magnitude = dp2.get_magnitude()  # just the magnitude of dp2

    dv1_dp1_dotProduct = int(dot_product(dv1,dp1))  # the dot product of dv1 and dp1
    dv2_dp2_dotProduct = int(dot_product(dv2,dp2))  # the dot product of dv2 and dp2

# the next variables, v1_Prime and v2_Prime are the the new velocities of obj1 and obj2, respectively
# it uses a big physics equation that I honestly don't understand
# it outputs a velocity vector
    v1_Prime_scalar = ((2*m2)/totalMass) * (dv1_dp1_dotProduct/(dp1_magnitude ** 2))
    v2_Prime_scalar = ((2*m1)/totalMass) * (dv2_dp2_dotProduct/(dp2_magnitude ** 2))
    v1_Prime0 = dp1.mul(v1_Prime_scalar)
    v1_Prime = v1.sub(v1_Prime0)
    v2_Prime0 = dp2.mul(v2_Prime_scalar)
    v2_Prime = v2.sub(v2_Prime0)

    obj1.velocity = v1_Prime
    obj2.velocity = v2_Prime

# now I gotta fix where they overlap
# this actually works
    dx,dy = dv1.as_tuple()
    dist = math.hypot(dx, dy)
    angle = math.atan2(dy, dx) + 0.5 * math.pi
    overlap = 0.5 * (obj1.radius + obj2.radius - dist + 1)
    obj1.position.x += math.sin(angle) * overlap
    obj2.position.y -= math.cos(angle) * overlap
    obj2.position.x -= math.sin(angle) * overlap
    obj2.position.y += math.cos(angle) * overlap

