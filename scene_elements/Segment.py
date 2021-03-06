class Segment:
    """Clase para representar un segmento en la imagen
    """

    def __init__(self, point1, point2, horizontal, transparencia=False, especularidad=False):
        self.point1 = point1
        self.point2 = point2
        self.transparencia = transparencia
        self.horizontal = horizontal
        self.especularidad = especularidad

    def get_point1(self):
        return self.point1

    def get_point2(self):
        return self.point2


    def determinar_pendiente(self):
        """Determina la pendiente del segmento

        :return: La pendiente del segmento
        """
        return (self.point1.y - self.point2.y) / (self.point1.x - self.point2.x)
