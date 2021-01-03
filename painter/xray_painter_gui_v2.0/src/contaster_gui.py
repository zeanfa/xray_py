import os
import numpy as np
import tkinter as tk
from tkinter import filedialog as fd, ttk
from PIL import ImageTk, Image
from contrast import Contraster
import utils


class ContrasterGUI:
    def __init__(self):
        self.target_image = None
        self.resulting_image = None
        self.scale_image = None
        self.scale_change = 0
        self.contraster = None
        self.in_dtype = 'uint8'

        self.scale_width = 0
        self.filetypes = (("BMP files", "*.bmp"),
                          ("JPG files", "*.jpg *.jpeg"),
                          ("PNG files", "*.png"),
                          ("TIFF files", "*.tiff *.tif"),)
        self.window = tk.Tk()
        self.window.title("X-ray painter")
        self.window.geometry("+0+0")
        self.img_left_panel = None
        self.img_right_panel = None
        self.img_scale_panel = None
        self.screen_width = self.window.winfo_screenwidth()
        self.screen_height = self.window.winfo_screenheight()
        self.image_size = int(self.screen_height - 350)
        self.color_scale = ''
        self.b_var = None
        self.r_var = None
        self.m_var = None
        self.g_var = None
        self.c_var = None
        self.y_var = None
        self.adaptive_saturation_var = None
        self.scale_preset_var = None
        self.saturation_scale = None

    def setup_window(self):
        # img frame
        img_frame = tk.Frame()
        scale_img_frame = tk.Frame(img_frame)
        xray_frame = tk.Frame(img_frame)

        img_left = tk.PhotoImage(width=self.image_size, height=self.image_size)
        img_right = tk.PhotoImage(width=self.image_size, height=self.image_size)
        img_scale = tk.PhotoImage(width=self.image_size * 2 + 4, height=int(80 / 0.825))

        # left image
        self.img_left_panel = tk.Label(xray_frame, image=img_left, bg="white")
        self.img_left_panel.pack(side="left")

        # right image
        self.img_right_panel = tk.Label(xray_frame, image=img_right, bg="white")
        self.img_right_panel.pack(side="left")

        # scale image
        self.img_scale_panel = tk.Label(scale_img_frame, image=img_scale, bg="white")
        self.img_scale_panel.pack()

        xray_frame.pack(side="top")
        scale_img_frame.pack(side="bottom")
        img_frame.pack(side="top")

        # options frame
        check_frame = tk.Frame(bd=5)
        placing = 'nw'
        color_scale_label = tk.Label(check_frame, text=u"Выберите цвета шкалы", height=0, compound="c")
        color_scale_label.pack(anchor=placing)

        self.b_var = tk.BooleanVar()
        self.b_var.set(False)
        c1 = tk.Checkbutton(check_frame, text="B - Синий", variable=self.b_var, onvalue=True, offvalue=False,
                            command=self.upd_scale)
        c1.pack(anchor=placing)

        self.r_var = tk.BooleanVar()
        self.b_var.set(False)
        c2 = tk.Checkbutton(check_frame, text="R - Красный", variable=self.r_var, onvalue=True, offvalue=False,
                            command=self.upd_scale)
        c2.pack(anchor=placing)

        self.m_var = tk.BooleanVar()
        self.b_var.set(False)
        c1 = tk.Checkbutton(check_frame, text="M - Пурпурный", variable=self.m_var, onvalue=True, offvalue=False,
                            command=self.upd_scale)
        c1.pack(anchor=placing)

        self.g_var = tk.BooleanVar()
        self.b_var.set(False)
        c2 = tk.Checkbutton(check_frame, text="G - Зеленый", variable=self.g_var, onvalue=True, offvalue=False,
                            command=self.upd_scale)
        c2.pack(anchor=placing)

        self.c_var = tk.BooleanVar()
        self.b_var.set(False)
        c1 = tk.Checkbutton(check_frame, text="C - Голубой", variable=self.c_var, onvalue=True, offvalue=False,
                            command=self.upd_scale)
        c1.pack(anchor=placing)

        self.y_var = tk.BooleanVar()
        self.b_var.set(False)
        c2 = tk.Checkbutton(check_frame, text="Y - Желтый", variable=self.y_var, onvalue=True, offvalue=False,
                            command=self.upd_scale)
        c2.pack(anchor=placing)

        check_frame.pack(side="left")

        options_frame = tk.Frame(bd=5)
        # label
        preset_label = ttk.Label(options_frame, text="Предустановка шкалы:")
        preset_label.pack(anchor='nw')

        # Combobox creation
        self.scale_preset_var = tk.StringVar()
        self.scale_preset_var.set('None')
        scale_preset = ttk.Combobox(options_frame, width=27, textvariable=self.scale_preset_var)
        scale_preset.bind('<<ComboboxSelected>>', self.upd_scale)

        # Adding combobox drop down list
        scale_preset['values'] = ('None',
                                  'full',
                                  'warm',
                                  'cold',
                                  'compRC',
                                  'compMG',
                                  'compBY')
        scale_preset.pack(anchor='nw')

        self.adaptive_saturation_var = tk.BooleanVar()
        self.adaptive_saturation_var.set(False)
        c1 = tk.Checkbutton(options_frame, text="Использовать адаптивную насыщенность",
                            variable=self.adaptive_saturation_var, onvalue=True, offvalue=False, command=None)
        c1.pack(anchor='nw')
        options_frame.pack(side='left')

        scale_frame = tk.Frame(bd=5)
        saturation_frame = tk.Frame(scale_frame)
        self.saturation_scale = tk.Scale(saturation_frame, label="Выберите насыщенность", orient=tk.HORIZONTAL,
                                         length=495, from_=0, to=100, tickinterval=100, resolution=1,
                                         command=self.process)
        self.saturation_scale.pack(side="bottom", anchor="s", pady=30)
        saturation_frame.pack(side="bottom")
        scale_frame.pack(side="right", anchor="n")

        button_frame = tk.Frame(scale_frame)
        open_button = tk.Button(button_frame, text="Открыть снимок", command=self.open_im)
        open_button.pack(side="left")

        process_button = tk.Button(button_frame, text="Раскрасить", command=self.process)
        process_button.pack(side="left")

        save_button = tk.Button(button_frame, text="Сохранить снимок", command=self.save)
        save_button.pack(side="left")

        button_frame.pack(side="top", anchor="nw")

        self.window.mainloop()

    def show_image(self, picture, image_panel):
        width, height = picture.size
        if width > height:
            w_reshape = int(0.9 * self.screen_width / 2)
            h_reshape = int(height * w_reshape / width)
            if h_reshape > self.image_size:
                h_reshape = self.image_size
                w_reshape = int(width * self.image_size / height)
        else:
            h_reshape = self.image_size
            w_reshape = int(width * self.image_size / height)
        image = ImageTk.PhotoImage(picture.resize((w_reshape, h_reshape), Image.ANTIALIAS))
        image_panel.config(image=image)
        image_panel.image = image
        return w_reshape

    def open_im(self):
        path = fd.askopenfilename(defaultextension=".bmp", filetypes=self.filetypes)
        if path:
            filename, file_extension = os.path.splitext(path)
            if file_extension in ['.tif', '.tiff']:
                self.target_image = Image.open(path)
                self.in_dtype = 'uint16'
            else:
                self.target_image = Image.open(path).convert('L')
                self.in_dtype = 'uint8'
            img_array = np.array(self.target_image)
            norm_array = 255*((img_array - np.min(img_array)) / (np.max(img_array) - np.min(img_array)))
            display_img = Image.fromarray(norm_array.astype('uint8'))
            self.show_image(display_img, self.img_left_panel)
            w_reshape = self.show_image(display_img, self.img_right_panel)
            self.img_scale_panel.config(image=tk.PhotoImage(width=int(2 * w_reshape + 4), height=int(80 / 0.825)))
            self.scale_width = int(2 * w_reshape + 4)

    def process(self, *other):
        if self.target_image is not None:
            self.contraster = Contraster(in_dtype=self.in_dtype, out_dtype='uint8')
            self.contraster.load_img(np.array(self.target_image), normalize=True)
            self.contraster.create_scale_wsat(self.color_scale, sat_rate=self.saturation_scale.get() / 100,
                                              adaptive_saturation=self.adaptive_saturation_var.get())
            self.contraster.transform_scale_wl()
            self.contraster.map_by_scale()
            scale_img_pil = Image.fromarray(utils.jit_cast(self.contraster.color_scale_img,
                                                           type_max=255, dtype=np.uint8))
            resized_scale_img = scale_img_pil.resize((self.scale_width, 80))
            scale_waxis = utils.draw_axis(resized_scale_img)
            tk_scale_img = ImageTk.PhotoImage(scale_waxis)
            self.img_scale_panel.config(image=tk_scale_img)
            self.img_scale_panel.image = tk_scale_img
            self.resulting_image = Image.fromarray(self.contraster.get_color_img())
            self.show_image(self.resulting_image, self.img_right_panel)
            self.scale_change = 0

    def save(self):
        if self.resulting_image:
            default_fn = str(self.color_scale + "_" + str(self.saturation_scale.get()))
            file_name = fd.asksaveasfilename(initialfile=default_fn, defaultextension=".bmp",
                                             filetypes=self.filetypes)
            if file_name:
                self.resulting_image.save(file_name)

    def upd_scale(self, *other):
        self.scale_change = 1
        self.color_scale = utils.get_user_kp(preset=self.scale_preset_var.get(),
                                             blue=self.b_var.get(),
                                             red=self.r_var.get(),
                                             magenta=self.m_var.get(),
                                             green=self.g_var.get(),
                                             cyan=self.c_var.get(),
                                             yellow=self.y_var.get())


if __name__ == '__main__':
    gui = ContrasterGUI()
    gui.setup_window()
