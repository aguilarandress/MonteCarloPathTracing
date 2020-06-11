import tkinter
import numpy as np
from scene_elements.Point import Point
from scene_elements.Segment import Segment
from tkinter import *


def main():
    """Funcion principal de la aplicacion
    """
    # Crear main window
    root_window = tkinter.Tk()
    root_window.title('Proyecto #2 Analisis de Algoritmos - 2D Path Tracing')
    arr = np.array([2, 3, 4])
    print(arr)
    root_window.mainloop()


if __name__ == "__main__":
    main()
