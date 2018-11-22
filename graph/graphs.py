from PIL import Image, ImageDraw
import numpy
import math
import matplotlib.pyplot as plt
import pylab
from mpl_toolkits.mplot3d import Axes3D
from itertools import product, combinations


#draw cube
def draw_cube(axes):
        r = [0, 1]
        for s, e in combinations(numpy.array(list(product(r, r, r))), 2):
            if numpy.sum(numpy.abs(s-e)) == r[1]-r[0]:
                axes.plot3D(*zip(s, e), "k:")

def solve_sys(number, Ff, Fl, Ef, El, Ef2, El2, Mx, draw, Vr_arr, Vg_arr, Vb_arr, position):
    step = 1/(number)
    for i in range(0, number):
        f1 = Ff/255 + (Fl-Ff)*i/(number*255)
        f2 = i* step
        epsilon = (Ef*Ff*(1-f2)/255 + El*Fl*f2/255)/(Ff*(1-f2)/255 + Fl*f2/255)
        epsilon2 = (Ef2*Ff*(1-f2)/255 + El2*Fl*f2/255)/(Ff*(1-f2)/255 + Fl*f2/255)
        Vr = numpy.array([f1, epsilon*f1, epsilon2*f1])
        col_arr = numpy.linalg.solve(Mx, Vr)
        Vr_arr.append(int(255*col_arr[0]))
        Vg_arr.append(int(255*col_arr[1]))
        Vb_arr.append(int(255*col_arr[2]))

        draw.rectangle(((position + i)*50,0,(position + i+1)*50, 1000),
                   fill =(int(round(255*col_arr[0])), int(round(255*col_arr[1])), int(round(255*col_arr[2]))),
                   outline =(int(round(255*col_arr[0])), int(round(255*col_arr[1])), int(round(255*col_arr[2]))))

def get_scale(param, name, bd_graphs, td_graphs, other):
    
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
    f_arr = []

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

    if bd_graphs:
        # 2D graph
        Rel_red_arr = list(map(lambda x: x/255, Vr_arr))
        Rel_green_arr = list(map(lambda x: x/255, Vg_arr))
        Rel_blue_arr = list(map(lambda x: x/255, Vb_arr))

        for i in range(0, 256):
            f_arr.append(i*1/255)

        f, (ax1, ax2, ax3) = plt.subplots(3, sharex=True, sharey=True)
        
        ax1.plot(f_arr, Rel_red_arr, "r")
        ax1.set_ylabel("R", fontsize = 15, rotation = 0, labelpad = 10)
        ax1.plot((0, 1), (1, 1), 'k--')
        ax2.plot(f_arr, Rel_green_arr, "g")
        ax2.set_ylabel("G", fontsize = 15, rotation = 0, labelpad = 10)
        ax2.plot((0, 1), (1, 1), 'k--')
        ax3.plot(f_arr, Rel_blue_arr, "b")
        ax3.set_ylabel("B", fontsize = 15, rotation = 0, labelpad = 10)
        ax3.plot((0, 1), (1, 1), 'k--')
        plt.xlabel("Относительная яркость исходной рентгенограммы")
        plt.xticks([0, 0.11, 0.3, 0.41, 0.59, 0.7, 0.89, 1])
        plt.savefig(name + "_plot.png")

    if td_graphs:
        # 3D graph eng
        fig = pylab.figure()
        axes = Axes3D(fig)
        
        Rel_red_arr = list(map(lambda x: x/255, Vr_arr))
        Rel_green_arr = list(map(lambda x: x/255, Vg_arr))
        Rel_blue_arr = list(map(lambda x: x/255, Vb_arr))
        axes.plot3D(Rel_red_arr, Rel_blue_arr, Rel_green_arr, "b", label = "full")
        axes.legend()
        axes.set_xlabel('R')
        axes.set_ylabel('B')
        axes.set_zlabel('G')
        draw_cube(axes)

        satur = 0.3
        Sat_red_arr3 = list(map(lambda ix: ix[1]*satur + ix[0]*(1-satur)/255, enumerate(Rel_red_arr)))
        Sat_green_arr3 = list(map(lambda ix: ix[1]*satur + ix[0]*(1-satur)/255, enumerate(Rel_green_arr)))
        Sat_blue_arr3 = list(map(lambda ix: ix[1]*satur + ix[0]*(1-satur)/255, enumerate(Rel_blue_arr)))
        axes.plot3D(Sat_green_arr3, Sat_red_arr3, Sat_blue_arr3, "r", label = "30%")

        axes.plot3D([0, 1], [0, 1], [0, 1], "k--", label = "BW")

        axes.legend()
        
        fig.savefig(name + "_plot3D_eng.png")

        if other:
            # 3D graph full
            fig = pylab.figure()
            axes = Axes3D(fig)
            axes.plot3D(Rel_red_arr, Rel_blue_arr, Rel_green_arr, "b", label = "full")
            axes.legend()
            axes.set_xlabel('R')
            axes.set_ylabel('B')
            axes.set_zlabel('G')
            draw_cube(axes)
            
            fig.savefig(name + "_plot3D.png")

            # 3D graph saturation
            satur = 0.1
            Sat_red_arr = list(map(lambda ix: ix[1]*satur + ix[0]*(1-satur)/255, enumerate(Rel_red_arr)))
            Sat_green_arr = list(map(lambda ix: ix[1]*satur + ix[0]*(1-satur)/255, enumerate(Rel_green_arr)))
            Sat_blue_arr = list(map(lambda ix: ix[1]*satur + ix[0]*(1-satur)/255, enumerate(Rel_blue_arr)))

            satur = 0.2
            Sat_red_arr2 = list(map(lambda ix: ix[1]*satur + ix[0]*(1-satur)/255, enumerate(Rel_red_arr)))
            Sat_green_arr2 = list(map(lambda ix: ix[1]*satur + ix[0]*(1-satur)/255, enumerate(Rel_green_arr)))
            Sat_blue_arr2 = list(map(lambda ix: ix[1]*satur + ix[0]*(1-satur)/255, enumerate(Rel_blue_arr)))

            satur = 0.5
            Sat_red_arr3 = list(map(lambda ix: ix[1]*satur + ix[0]*(1-satur)/255, enumerate(Rel_red_arr)))
            Sat_green_arr3 = list(map(lambda ix: ix[1]*satur + ix[0]*(1-satur)/255, enumerate(Rel_green_arr)))
            Sat_blue_arr3 = list(map(lambda ix: ix[1]*satur + ix[0]*(1-satur)/255, enumerate(Rel_blue_arr)))
            
            fig_satur = pylab.figure()
            axes_sat = Axes3D(fig_satur)
            axes_sat.plot3D(Sat_red_arr, Sat_green_arr, Sat_blue_arr, "r--", label = "10%")
            axes_sat.plot3D(Sat_red_arr2, Sat_green_arr2, Sat_blue_arr2, "g-.", label = "20%")
            axes_sat.plot3D(Sat_red_arr3, Sat_green_arr3, Sat_blue_arr3, "b-", label = "30%")
            axes_sat.legend()
            axes_sat.set_xlabel('R')
            axes_sat.set_ylabel('G')
            axes_sat.set_zlabel('B')
            draw_cube(axes_sat)
                    
            fig_satur.savefig(name + "_plot3D_sat.png")
        pylab.show()

    
    return (Vr_arr, Vg_arr, Vb_arr)
