import math

def TempMap(T):
    R, G, B = 0, 0, 0
    #Blue
    if (T < 0.1):
        B = (255.0/0.15) * (T+0.05)
    elif (T >= 0.1 and T <= 0.4):
        B = 255
    elif (T > 0.4 and T < 0.5):
        B = -(255.0/0.1) * (T - 0.5)
    else:
        B = 0
    #Green
    if (T > 0.1 and T < 0.4):
        G = (255.0/0.3) * (T - 0.1)
    elif (T >= 0.4 and T <= 0.6):
        G = 255
    elif (T > 0.6 and T < 0.9):
        G = -(255.0/0.3) * (T-0.9)
    else:
        G = 0

    #Red
    if (T > 0.5 and T < 0.6):
        R = (255.0/0.1) * (T - 0.5)
    elif (T >= 0.6 and T <= 0.9):
        R = 255
    elif (T > 0.9):
        R = -(255.0/0.15) * (T - 1.05)
    else:
        R = 0

    return int(R),int(G),int(B)

def heatmap(input):
    r, g, b = TempMap(input)
    return '#' + '{:02x}'.format(r) + '{:02x}'.format(g) + '{:02x}'.format(b)