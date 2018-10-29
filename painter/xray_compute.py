from PIL import Image, ImageDraw
import numpy
import math

def solve_sys(number, Ff, Fl, Ef, El, Ef2, El2, Mx, draw, Vr_arr, Vg_arr, Vb_arr, position):
    step = 1/(number)
    for i in range(0, number):
        f1 = Ff/255 + (Fl-Ff)*i/(number*255)
        f2 = i* step
        epsilon = (Ef*Ff*(1-f2)/255 + El*Fl*f2/255)/(Ff*(1-f2)/255 + Fl*f2/255)
        epsilon2 = (Ef2*Ff*(1-f2)/255 + El2*Fl*f2/255)/(Ff*(1-f2)/255 + Fl*f2/255)
        Vr = numpy.array([f1, epsilon*f1, epsilon2*f1])
        col_arr = numpy.linalg.solve(Mx, Vr)
        Vr_arr.append(int(round(255*col_arr[0])))
        Vg_arr.append(int(round(255*col_arr[1])))
        Vb_arr.append(int(round(255*col_arr[2])))

        draw.rectangle(((position + i)*50,0,(position + i+1)*50, 1000),
                   fill =(int(round(255*col_arr[0])), int(round(255*col_arr[1])), int(round(255*col_arr[2]))),
                   outline =(int(round(255*col_arr[0])), int(round(255*col_arr[1])), int(round(255*col_arr[2]))))

def get_scale(param, name):
    
    lr = 0.3
    lg = 0.59
    lb = 0.11

    Ered = 1.59
    Egreen = 1.91
    Eblue = 2.14

    Ered2 = 2.54
    Egreen2 = 3.69
    Eblue2 = 4.6

    Ewhite = 1.8393
    Ewhite2 = 3.4451

    Fblack = 1
    Fblue = int(lb*255)
    Fred = int(lr*255)
    Fmagenta = Fblue + Fred
    Fgreen = int(lg*255)
    Fcyan = Fblue + Fgreen
    Fyellow = Fred + Fgreen
    Fwhite = 255

    Emagenta = (Ered*Fred + Eblue*Fblue)/(Fred + Fblue)
    Ecyan = (Egreen*Fgreen + Eblue*Fblue)/(Fgreen + Fblue)
    Eyellow = (Ered*Fred + Egreen*Fgreen)/(Fred + Fgreen)

    Emagenta2 = (Ered2*Fred + Eblue2*Fblue)/(Fred + Fblue)
    Ecyan2 = (Egreen2*Fgreen + Eblue2*Fblue)/(Fgreen + Fblue)
    Eyellow2 = (Ered2*Fred + Egreen2*Fgreen)/(Fred + Fgreen)

    Ewhite = 1.8393
    Ewhite2 = 3.4451

    Eblack = Ewhite
    Eblack2 = Ewhite2

    param_set = {
    'w': (Fwhite, Ewhite, Ewhite2),
    'k': (Fblack, Eblack, Eblack2),
    'r': (Fred, Ered, Ered2),
    'g': (Fgreen, Egreen, Egreen2),
    'b': (Fblue, Eblue, Eblue2),
    'c': (Fcyan, Ecyan, Ecyan2),
    'm': (Fmagenta, Emagenta, Emagenta2),
    'y': (Fyellow, Eyellow, Eyellow2)
    }

    image=Image.new("RGB", (12700,1000), (0,0,0))
    draw=ImageDraw.Draw(image)
    
    Vr_arr = [0]
    Vg_arr = [0]
    Vb_arr = [0]

    Mx=numpy.array([[lr, lg, lb],[lr*Ered, lg*Egreen, lb*Eblue],[lr*Ered2, lg*Egreen2, lb*Eblue2]])
    gap = 0


    for i in range(len(param) - 1):
        Fleft = param_set[param[i]][0]
        Eleft = param_set[param[i]][1]
        E2left = param_set[param[i]][2]
        Fright = param_set[param[i+1]][0]
        Eright = param_set[param[i+1]][1]
        E2right = param_set[param[i+1]][2]
        solve_sys(Fright-Fleft, Fleft, Fright, Eleft, Eright, E2left, E2right, Mx, draw, Vr_arr, Vg_arr, Vb_arr, gap)
        gap += Fright-Fleft

    if len(Vr_arr)<256:
        Vr_arr.append(255)
        Vg_arr.append(255)
        Vb_arr.append(255)
    
    del draw
    image.save(name + ".png", "PNG")

    return (Vr_arr, Vg_arr, Vb_arr)
