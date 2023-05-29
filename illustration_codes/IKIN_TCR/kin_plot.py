import math
import numpy as np


class kin_plot():
    def __init__(self, canvas, height = 500, width = 500):
        self.height = height
        self.width = width
        self.canvas = canvas
        self.arrows = np.array([])
        self.color = "blue"
        self.penwidth = 1
        self.raster()
        self.canvas.pack()
        pass

    def c2t(self, x, y):
        x, y = int(x+self.width/2),int(self.height/2-y)

        return x, y

    def plot_robot(self, x1, y1, x2, y2, color):
        x0, y0 = self.c2t(0, 0)
        x1, y1 = self.c2t(x1, y1)
        x2, y2 = self.c2t(x2, y2)

        line = self.canvas.create_line(x0, y0, x1, y1, fill=color, width=self.penwidth)
        line = self.canvas.create_line(x1, y1, x2, y2, fill=color, width=self.penwidth)
        return 0
    
    def raster(self):
        print(self.width)
        print(self.height)
        x0_x, y0_x = self.c2t(-self.width/2, 0)
        x1_x, y1_x = self.c2t(self.width/2, 0)
        line_x = self.canvas.create_line(x0_x, y0_x, x1_x, y1_x, fill="green", width=1)

        x0_y, y0_y = self.c2t(0, self.height/2)
        x1_y, y1_y = self.c2t(0, -self.height/2)
        line_y = self.canvas.create_line(x0_y, y0_y, x1_y, y1_y, fill="green", width=1)
        #print(x0_x, y0_x, x1_x, y1_x)
        #print(x0_y, y0_y, x1_y, y1_y)

        return line_x, line_y


