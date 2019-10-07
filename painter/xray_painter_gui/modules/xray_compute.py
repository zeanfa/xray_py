from PIL import Image, ImageDraw, ImageOps,ImageFont
import numpy
import math

img_width = 12800
img_height = 800

def solve_sys(number, Ff, Fl, Ef, El, Ef2, El2, Mx, draw, Vr_arr, Vg_arr, Vb_arr, position):
    global img_width,img_height
    step = 1/(number)
    for i in range(0, number):
        f1 = Ff/255 + (Fl-Ff)*i/(number*255)
        f2 = i * step
        epsilon = (Ef*Ff*(1-f2)/255 + El*Fl*f2/255)/(Ff*(1-f2)/255 + Fl*f2/255)
        epsilon2 = (Ef2*Ff*(1-f2)/255 + El2*Fl*f2/255)/(Ff*(1-f2)/255 + Fl*f2/255)
        Vr = numpy.array([f1, epsilon*f1, epsilon2*f1])
        col_arr = numpy.linalg.solve(Mx, Vr)
        Vr_arr.append(int(round(255*col_arr[0])))
        Vg_arr.append(int(round(255*col_arr[1])))
        Vb_arr.append(int(round(255*col_arr[2])))

        draw_step = int(img_width/256)
        draw.rectangle(((position + i)*draw_step,0,(position + i+1)*draw_step, int(0.4*img_height)),
                   fill =(int(round(255*col_arr[0])), int(round(255*col_arr[1])), int(round(255*col_arr[2]))),
                   outline =(int(round(255*col_arr[0])), int(round(255*col_arr[1])), int(round(255*col_arr[2]))))
        bw_color = position+i+1
        draw.rectangle(((position + i)*draw_step,int(0.4*img_height),(position + i+1)*draw_step, int(0.8*img_height)),
                   fill =(bw_color, bw_color, bw_color),
                   outline =(bw_color, bw_color, bw_color))

def get_scale(param):
    
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

    image=Image.new("RGB", (img_width,img_height), (255,255,255))
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

    # draw axis
    bias = 0.1
    width_bias = int(img_width*0.5*bias/100)
    str_width = int(img_width*(100-bias)/100)
    draw.line((width_bias,int(0.825*img_height),str_width+width_bias,int(0.825*img_height)),fill=(0,0,0),width=10)
    for i in range(0,11):
        x = int(str_width*i/10+width_bias)
        draw.line((x,int(0.8*img_height),x,int(0.85*img_height)),fill="black",width=10)
        fontsize=100
        font = ImageFont.truetype("arial", fontsize)
        text_x = x - fontsize/2
        if text_x<0:
            text_x=0
        draw.text((text_x,0.85*img_height),str(i/10),fill="black",font=font)

    if len(Vr_arr)<256:
        Vr_arr.append(255)
        Vg_arr.append(255)
        Vb_arr.append(255)
    del draw
    #image.save(name + ".png", "PNG")
    #img_with_border = ImageOps.expand(image,border=int(img_width*0.001),fill='white')

    return (Vr_arr, Vg_arr, Vb_arr, image)
