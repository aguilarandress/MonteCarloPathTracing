class Segment:
    """Clase para representar un segmento en la imagen
    """

    def __init__(self, point1, point2, horizontal,transparencia=False):
        self.point1 = point1
        self.point2 = point2
        self.transparencia = transparencia
        self.horizontal = horizontal

    def get_point1(self):
        return self.point1

    def get_point2(self):
        return self.point2
