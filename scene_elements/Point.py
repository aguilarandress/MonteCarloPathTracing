class Point:
    """Clase para representar un punto en la imagen
    """

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def __add__(self, other):
        return Point(self.x+other.x, self.y+other.y)

    def __sub__(self, other):
        return Point(self.x-other.x, self.y-other.y)

    def __mul__(self, other):
        return Point(self.x*other, self.y*other)

    def __truediv__(self, other):
        return Point(self.x/other, self.y/other)

    def dot(self, p2):
        return (self.x*p2.x) + (self.y*p2.y)

    def cross(self, p2):
        return (self.x*p2.y) - (self.y*p2.x)

    def __str__(self):
        return "[ {}, {}]".format(self.x, self.y)
