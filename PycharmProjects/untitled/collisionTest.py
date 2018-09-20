from Ball import Ball
from Collisions import collide, collisionDetect, elasticCollisions, dot_product

testBall = Ball(676.178, 415.806, 50, -1.431, -0.166)
testBall2 = Ball(602.631, 408.189, 24, 2.412, 5.467)

collide(testBall, testBall2)
