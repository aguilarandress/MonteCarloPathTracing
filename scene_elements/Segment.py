import scene_elements.Point


class Segment:
    """Clase para representar un segmento en la imagen
    """

    def __init__(self, point1, point2, especularidad=False):
        self.point1 = point1
        self.point2 = point2
        self.especularidad = especularidad

    def getPoint1(self):
        return self.point1

    def getPoint2(self):
        return self.point2
