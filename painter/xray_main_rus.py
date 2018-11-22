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
    cmd = input("\nВыберите опцию:\n (1) помощь \n (2) шкала \n (3) эквализация гистограммы \n (4) градации насыщенности\n")
    #print(cmd)
    if cmd.find("1") == 0:
       print("\nЭта программа предназначена для раскраски рентгенограмм.")
       print("Шкала (2) - выберите шкалу, в соответствии с которой Вы хотите раскрасить изображение")
       print("Эквализация гистограммы (3) - применить фильтр выравнивания гистограммы к изображению")
       print("Градации насыщенности (4) - создать набор изображений с различными градациями насыщенности\n")
       continue

    if cmd.find("2") == 0:
        print("\nВозможные значения цветового ряда: k b r m g c y w")
        print("k - черный")
        print("b - синий")
        print("r - красный")
        print("m - пурпурный")
        print("g - зеленый")
        print("c - голубой")
        print("y - желтый")
        print("w - белый")
        print("Черный должен быть первым, а белый последним")
        print("Промежуточные цвета должны быть указаны в порядке ряда\n")
        
        if param != 0:
            if input("Использовать предыдущую шкалу? д/н\n").find("н") == 0:
                param = input("\nВведите шкалу:\n")
        else:
            param = input("Введите шкалу:\n")
        red_scale, green_scale, blue_scale = cmp.get_scale(param, folder_name + "/" + param)
        print("\nШкала сохранена")
        file_name = input("\nВведите название файла для раскраски:\n")
        flt.linear(folder_name + "/" + file_name)
        linear_file_name = file_name[0:(len(file_name)-4)] + "_linear.bmp"
        pnt.convert(red_scale, green_scale, blue_scale, folder_name + "/" + linear_file_name, param)
        print("Раскраска завершена")
        
    elif cmd.find("3") == 0:
        print("\nЭквализация может занять некоторое время, пожалуйста, подождите")
        file_name = input("\nВведите название файла для эквализации гистограммы:\n")
        flt.equalize(folder_name + "/" + file_name)
        print("Эквализация завершена\n")
        
    elif cmd.find("4") == 0:
        print("\nПожалуйста, убедитесь в наличии цветного изображения максимальной насыщенности!\n")
        if param != 0 and linear_file_name != 0:
            if input("Использовать предыдущую шкалу и файл? д/н\n").find("н") == 0:
                linear_file_name = input("Введите имя файла для градуировки насыщенности:\n")
                param = input("\nВведите шкалу:\n")
        else:
            linear_file_name = input("Введите имя файла для градуирования насыщенности:\n")
            param = input("\nВведите шкалу:\n")
        grade = input("\nВведите начало, конец и шаг градации насыщенности (через пробел):\n")
        begin, end, step = map(int, grade.split())
        sat.grade(folder_name + "/" + linear_file_name, param, begin, end, step)
        print("Градуирование завершено\n")

    else:
        print("\nКоманда не найдена\n")

    if input("\nПродолжить? д/н\n").find("н") == 0:
        print("\nЗавершено!\n")
        break
    
