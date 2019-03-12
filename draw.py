from display import *
from matrix import *


def add_circle( points, cx, cy, cz, r, step ):
    dtheta = 2 * math.pi/step
    theta = 0
    for i in range(step):
        x1 = cx + r * math.cos(theta)
        y1 = cy + r * math.sin(theta)
        theta += dtheta
        x2 = cx + r * math.cos(theta)
        y2 = cy + r * math.sin(theta)
        add_edge(points, x1, y1, cz, x2, y2, cz)

def add_curve( points, x0, y0, x1, y1, x2, y2, x3, y3, step, curve_type ):
    if curve_type == 'hermite':
        rx0 = x2
        ry0 = y2
        rx1 = x3
        ry1 = y3
        Cx, Cy = make_hermite(x0, y0, x1, y1, rx0, ry0, rx1, ry1)
        dt = float(1 / float(step))
        t = 0.0
        for i in range(step):
            x1 = cubic(t, Cx)
            y1 = cubic(t, Cy)
            t += dt
            x2 = cubic(t, Cx)
            y2 = cubic(t, Cy)
            add_edge(points, x1, y1, 0, x2, y2, 0)
    if curve_type == 'bezier':
        xcoefs, ycoefs = make_bezier(x0, y0, x1, y1, x2, y2, x3, y3)
        dt = float(1 / float(step))
        t = 0.0
        for i in range(step):
            x1 = cubic(t, xcoefs)
            y1 = cubic(t, ycoefs)
            t += dt
            x2 = cubic(t, xcoefs)
            y2 = cubic(t, ycoefs)
            add_edge(points, x1, y1, 0, x2, y2, 0)

def cubic(t, coefs):
    return coefs[0] * math.pow(t, 3) + coefs[1] * math.pow(t, 2) + coefs[2] * t + coefs[3]

def draw_lines( matrix, screen, color ):
    if len(matrix) < 2:
        print('Need at least 2 points to draw')
        return

    point = 0
    while point < len(matrix) - 1:
        draw_line( int(matrix[point][0]),
                   int(matrix[point][1]),
                   int(matrix[point+1][0]),
                   int(matrix[point+1][1]),
                   screen, color)
        point+= 2

def add_edge( matrix, x0, y0, z0, x1, y1, z1 ):
    add_point(matrix, x0, y0, z0)
    add_point(matrix, x1, y1, z1)

def add_point( matrix, x, y, z=0 ):
    matrix.append( [x, y, z, 1] )




def draw_line( x0, y0, x1, y1, screen, color ):

    #swap points if going right -> left
    if x0 > x1:
        xt = x0
        yt = y0
        x0 = x1
        y0 = y1
        x1 = xt
        y1 = yt

    x = x0
    y = y0
    A = 2 * (y1 - y0)
    B = -2 * (x1 - x0)

    #octants 1 and 8
    if ( abs(x1-x0) >= abs(y1 - y0) ):

        #octant 1
        if A > 0:
            d = A + B/2

            while x < x1:
                plot(screen, color, x, y)
                if d > 0:
                    y+= 1
                    d+= B
                x+= 1
                d+= A
            #end octant 1 while
            plot(screen, color, x1, y1)
        #end octant 1

        #octant 8
        else:
            d = A - B/2

            while x < x1:
                plot(screen, color, x, y)
                if d < 0:
                    y-= 1
                    d-= B
                x+= 1
                d+= A
            #end octant 8 while
            plot(screen, color, x1, y1)
        #end octant 8
    #end octants 1 and 8

    #octants 2 and 7
    else:
        #octant 2
        if A > 0:
            d = A/2 + B

            while y < y1:
                plot(screen, color, x, y)
                if d < 0:
                    x+= 1
                    d+= A
                y+= 1
                d+= B
            #end octant 2 while
            plot(screen, color, x1, y1)
        #end octant 2

        #octant 7
        else:
            d = A/2 - B;

            while y > y1:
                plot(screen, color, x, y)
                if d > 0:
                    x+= 1
                    d+= A
                y-= 1
                d-= B
            #end octant 7 while
            plot(screen, color, x1, y1)
        #end octant 7
    #end octants 2 and 7
#end draw_line
