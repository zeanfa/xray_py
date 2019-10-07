from PIL import Image, ImageTk
import numpy
import math
import xray_compute as cmp
import xray_painter as pnt
import xray_filter as flt
import xray_saturation as sat
import tkinter as tk
from tkinter import filedialog as fd
from tkinter import messagebox as mb

target_image = None
normalized_image = None
scale_image = None
colored_image = None
image_change = 0
resulting_image = None
scale_width = 0

def show_image(picture, image, image_panel):
    width,height = picture.size
    if width > height:
        w_reshape=500
        h_reshape=int(height*500/width)
    else:
        h_reshape=500
        w_reshape=int(width*500/height)
    image  = ImageTk.PhotoImage(picture.resize((w_reshape, h_reshape), Image.ANTIALIAS))
    image_panel.config(image=image)
    image_panel.image = image
    return w_reshape
    

def open_im():
    file_name = fd.askopenfilename()
    if file_name:
        global target_image, image_change, scale_width
        target_image=Image.open(file_name)
        show_image(target_image,img_left,img_left_panel)
        w_reshape = show_image(target_image,img_right,img_right_panel)
        img_scale_panel.config(image=tk.PhotoImage(width=int(2*w_reshape+4), height=80))
        image_change = 1
        scale_width = int(2*w_reshape+4)

def set_saturation(saturation):
    global resulting_image
    if target_image and colored_image and not image_change:
        resulting_image = sat.np_get_scale(int(saturation),target_image,colored_image)
        show_image(resulting_image,img_right,img_right_panel)

def process():
    global target_image, normalized_image, scale_image, colored_image, image_change, resulting_image
    if target_image == None:
        mb.showwarning("Отсутствует изображение", "Загрузите изображение")
        return
    if image_change:
        normalized_image = flt.linear(target_image)
        Vr_arr, Vg_arr, Vb_arr, scale_image = cmp.get_scale(color_scale_var.get())
        img_scale = ImageTk.PhotoImage(scale_image.resize((scale_width, 80), Image.ANTIALIAS))
        img_scale_panel.config(image=img_scale)
        img_scale_panel.image = img_scale
        colored_image = pnt.convert(Vr_arr,Vg_arr,Vb_arr,normalized_image)
        image_change = 0
    resulting_image = sat.np_get_scale(saturation_scale.get(),target_image,colored_image)
    show_image(resulting_image,img_right,img_right_panel)
    


def save():
    if resulting_image:
        default_fn=str(color_scale_var.get() + "_" + str(saturation_scale.get()))
        file_name = fd.asksaveasfilename(initialfile=default_fn, defaultextension=".bmp",
                                         filetypes=(("BMP files", "*.bmp"),))
        if file_name:
            resulting_image.save(file_name,"BMP")

def upd_scale():
    global image_change
    image_change = 1
    color_scale=str("k"+b_var.get()+r_var.get()+m_var.get()+g_var.get()+c_var.get()+y_var.get()+"w")
    color_scale_var.set(color_scale)

def close():
    if target_image:
        target_image.close()
    if normalized_image:
        normalized_image.close()
    if colored_image:
        colored_image.close()
    if resulting_image:
        resulting_image.close()
    exit(0)
    

window = tk.Tk()
window.title("X-ray painter")
window.geometry("+0+0")

# img frame
img_frame = tk.Frame()
scale_img_frame = tk.Frame(img_frame)
xray_frame = tk.Frame(img_frame)

img_left  = tk.PhotoImage(width=500, height=500)
img_right = tk.PhotoImage(width=500, height=500)
img_scale = tk.PhotoImage(width=1004, height=80)

# left image
img_left_panel = tk.Label(xray_frame, image=img_left, bg="white")
img_left_panel.pack(side="left")

# right image
img_right_panel = tk.Label(xray_frame, image=img_right, bg="white")
img_right_panel.pack(side="left")

# right image
img_scale_panel = tk.Label(scale_img_frame, image=img_scale, bg="white")
img_scale_panel.pack()

xray_frame.pack(side="top")
scale_img_frame.pack(side="bottom")
img_frame.pack(side="top")

# check frame
check_frame = tk.Frame(bd=5)
placing='nw'
color_scale_label = tk.Label(check_frame,text=u"Выберите цвета шкалы", height=0, compound="c")
color_scale_label.pack(anchor=placing)

b_var = tk.StringVar()
b_var.set("")
c1 = tk.Checkbutton(check_frame,text="B - Синий", variable=b_var, onvalue="b", offvalue="", command=upd_scale)
c1.pack(anchor=placing)
 
r_var = tk.StringVar()
r_var.set("")
c2 = tk.Checkbutton(check_frame,text="R - Красный", variable=r_var, onvalue="r", offvalue="", command=upd_scale)
c2.pack(anchor=placing)

m_var = tk.StringVar()
m_var.set("")
c1 = tk.Checkbutton(check_frame,text="M - Пурпурный", variable=m_var, onvalue="m", offvalue="", command=upd_scale)
c1.pack(anchor=placing)
 
g_var = tk.StringVar()
g_var.set("")
c2 = tk.Checkbutton(check_frame,text="G - Зеленый", variable=g_var, onvalue="g", offvalue="", command=upd_scale)
c2.pack(anchor=placing)

c_var = tk.StringVar()
c_var.set("")
c1 = tk.Checkbutton(check_frame,text="C - Голубой", variable=c_var, onvalue="c", offvalue="", command=upd_scale)
c1.pack(anchor=placing)
 
y_var = tk.StringVar()
y_var.set("")
c2 = tk.Checkbutton(check_frame,text="Y - Желтый", variable=y_var, onvalue="y", offvalue="", command=upd_scale)
c2.pack(anchor=placing)

check_frame.pack(side="left")

color_scale_var = tk.StringVar()
color_scale_var.set("kw")

#l = tk.Label(textvariable=color_scale_var,bg='white', fg='black', width=20)
        
scale_frame = tk.Frame(bd=5)
saturation_frame = tk.Frame(scale_frame)
saturation_scale = tk.Scale(saturation_frame, label="Выберите насыщенность", orient=tk.HORIZONTAL,length=495,
                            from_=0,to=100,tickinterval=100, resolution=1,command=set_saturation)
saturation_scale.pack(side="bottom",anchor="s",pady=30)
saturation_frame.pack(side="bottom")
scale_frame.pack(side="right",anchor="n")

button_frame = tk.Frame(scale_frame)
open_button = tk.Button(button_frame,text="Открыть снимок",
              command=lambda:open_im())
open_button.pack(side="left")

process_button = tk.Button(button_frame,text="Раскрасить",
              command=lambda:process())
process_button.pack(side="left")

save_button = tk.Button(button_frame,text="Сохранить снимок",
              command=lambda:save())
save_button.pack(side="left")

close_button = tk.Button(button_frame,text="Закрыть",
              command=lambda:close())
close_button.pack(side="right",padx=70)
button_frame.pack(side="top",anchor="nw")


window.mainloop()
