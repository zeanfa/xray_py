from PIL import Image, ImageDraw
import numpy
import math
import xray_compute as cmp
import xray_painter as pnt
import xray_filter as flt
import xray_saturation as sat

folder_name = input("\nВведите название рабочей папки\n")
file_name = 0
linear_file_name = 0
param = 0

while(1):
    cmd = input("\nВыберите опцию:\n -помощь (help) \n -шкала(scale) \n -эквализация гистограммы(equal) \n -градации насыщенности(grade)\n")
    #print(cmd)
    if cmd.find("help") == 0:
       print("\nЭта программа предназначена для раскраски рентгенограмм.")
       print("Шкала (scale) - выберите шкалу, в соответствии с которой Вы хотите раскрасить изображение")
       print("Эквализация гистограммы (equal) - применить фильтр выравнивания гистограммы к изображению")
       print("Градации насыщенности (grade) - создать набор изображений с различными градациями насыщенности\n")
       continue

    if cmd.find("scale") == 0:
        print("\nВозможные значения цветового ряда: k b r m g c y w")
        print("k - черный")
        print("b - синий")
        print("r - красный")
        print("m - пурпурный (magenta)")
        print("g - зеленый")
        print("c - голубой (cyan)")
        print("y - yellow")
        print("w - white")
        print("k must be the first and w must be the last\n")
        
        if param != 0:
            if input("use previous scale? y/n\n").find("n") == 0:
                param = input("\nenter scale\n")
        else:
            param = input("enter scale\n")
        red_scale, green_scale, blue_scale = cmp.get_scale(param, folder_name + "/" + param)
        print("\nscale is saved")
        file_name = input("\nenter file name to paint\n")
        flt.linear(folder_name + "/" + file_name)
        linear_file_name = file_name[0:(len(file_name)-4)] + "_linear.bmp"
        pnt.convert(red_scale, green_scale, blue_scale, folder_name + "/" + linear_file_name, param)
        print("painting done")
        
    elif cmd.find("equal") == 0:
        print("\nequalizing may take some time, you'll have to wait")
        file_name = input("\nenter file name to filter\n")
        flt.equalize(folder_name + "/" + file_name)
        print("filtering done\n")
        
    elif cmd.find("grade") == 0:
        print("\nmake sure you have already got a colour image!\n")
        if param != 0 and linear_file_name != 0:
            if input("use previous file and scale? y/n\n").find("n") == 0:
                linear_file_name = input("enter file name to be graded\n")
                param = input("\nenter scale\n")
        else:
            linear_file_name = input("enter file name to be graded\n")
            param = input("\nenter scale\n")
        grade = input("\nenter begin, end, step of saturation\n")
        begin, end, step = map(int, grade.split())
        sat.grade(folder_name + "/" + linear_file_name, param, begin, end, step)
        print("grading done\n")

    else:
        print("\nno command found\n")

    if input("\ncontinue? y/n\n").find("n") == 0:
        print("\nBye!\n")
        break
    
