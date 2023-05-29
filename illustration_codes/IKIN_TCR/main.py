import tkinter as tk
import numpy as np
from math import acos, atan, sin, cos, pi
import numpy as np
from kin import *
from kin_plot import kin_plot
from heatmap_calculator import *



scale = 1100
a1 = 0.29 #0.29 #1-es tag hossza
a2 = 0.26 #0.26 #2-es tag hossza

def plot_points(kin):
    x_range = np.arange(0.1, 0.4, 0.05)
    y_range = np.arange(-0.4, 0.4, 0.05)
    sum = len(x_range)*len(y_range)
    i = 0
    for x in x_range:
        for y in y_range:
            #x = -0.1
            #y = 0.30
            print(x, y)
            q1, q2, ok = IKIN(x*scale, y*scale, a1*scale, a2*scale)
            if ok:
                x1, y1, x2, y2 = FKIN(q1, q2, a1*scale, a2*scale)
                kin.plot_robot(x1, y1, x2, y2, heatmap(i/sum))
            else:
                print("Messzebb akarunk elnyúlni")
            i += 1


def joint_interplate(kin, x1, y1, x2, y2, step = 30):
    q11, q21, ok1 = IKIN(x1*scale, y1*scale, a1*scale, a2*scale)
    q12, q22, ok2 = IKIN(x2*scale, y2*scale, a1*scale, a2*scale)

    if (ok1 == 1 & ok2 == 1):
        for i in range(0, step+1):
            x1, y1, x2, y2 = FKIN(q11 + (i/step)*(q12-q11), q21 + (i/step)*(q22-q21), a1*scale, a2*scale)
            kin.plot_robot(x1, y1, x2, y2, heatmap(i/(step+1)))
    else:
        print("Nem elérhető pont")

def linear_interpolate(kin, x1, y1, x2, y2, step = 30):
    q11, q21, ok1 = IKIN(x1*scale, y1*scale, a1*scale, a2*scale)
    q12, q22, ok2 = IKIN(x2*scale, y2*scale, a1*scale, a2*scale)

    if (ok1 == 1 & ok2 == 1):
        for i in range(0, step+1):
            x_ = (i/step)*(x2-x1)+x1
            y_ = (i/step)*(y2-y1)+y1
            q1, q2, ok = IKIN(x_*scale, y_*scale, a1*scale, a2*scale)
            x1_, y1_, x2_, y2_ = FKIN(q1, q2, a1*scale, a2*scale)
            kin.plot_robot(x1_, y1_, x2_, y2_, heatmap(i/(step+1)))
    else:
        print("Nem elérhető pont")


def main():
    H, W = 900,900 #for Full HD
    top = tk.Tk()
    top.title("Kin plot")
    C = tk.Canvas(top, bg="black", height=H, width=W)
    kin = kin_plot(C, H, W)
    #plot_points(kin)
    x0, y0, x1, y1 = -0.35, 0.05, 0.3, 0.25
    step = 100
    
    joint_interplate(kin, x0, y0, x1, y1, step = step)
    linear_interpolate(kin, x0, y0, x1, y1, step = step)
    
    top.mainloop()




if __name__ == "__main__":
    main()


