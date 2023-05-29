from math import acos, sin, cos, atan2, sqrt

def IKIN(x, y, a1, a2):
    if(sqrt(x**2 + y**2) < a1 + a2):
        q2 = acos((x**2+y**2-a1**2-a2**2)/(2*a1*a2))
        q1 = atan2(y,x)-atan2((a2*sin(q2)),(a1+a2*cos(q2)))
        return q1, q2, 1
    return 0, 0, 0


def FKIN(q1, q2, a1, a2):
    x1, y1 = a1*cos(q1), a1*sin(q1)
    x2, y2 = x1 + a2*cos(q1+q2), y1 + a2*sin(q1+q2)
    return x1, y1, x2, y2
