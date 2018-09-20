import math


class Vector2():
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

    def str(self):
        return "(%s, %s)" % (self.x, self.y)

    def set_values(self, x, y):
        self.x = x
        self.y = y

    def as_tuple(self):
        return (self.x, self.y)

    def from_points(self, P1, P2):
        return Vector2(P2[0] - P1[0], P2[1] - P1[1])

    def get_magnitude(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def normalize(self):
        magnitude = self.get_magnitude()
        if magnitude != 0:
            self.x /= magnitude
            self.y /= magnitude

    def get_distance_to(self, entity):
        return math.sqrt((self.x - entity[0]) ** 2 + (self.y - entity[1]) ** 2)

    # rhs stands for Right Hand Side
    def add(self, rhs):
        return Vector2(self.x + rhs.x, self.y + rhs.y)

    def sub(self, rhs):
        return Vector2(self.x - rhs.x, self.y - rhs.y)

    def neg(self):
        return Vector2(-self.x, -self.y)

    def mul(self, scalar):
        return Vector2(self.x * scalar, self.y * scalar)

    def lmul(self, scalar):
        return Vector2(self.x * scalar, self.y * scalar)

    def rmul(self, scalar):
        return Vector2(self.x * scalar, self.y * scalar)

    def truediv(self, scalar):
        return Vector2(self.x / scalar, self.y / scalar)


