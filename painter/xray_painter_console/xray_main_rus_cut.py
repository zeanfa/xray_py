import time
import xray_compute as cmp
import xray_painter as pnt
import xray_filter as flt
import xray_saturation as sat

scale_set = {
    '1': 'kbgcw',
    '2': 'kbcw',
    '3': 'krmyw',
    '4': 'kryw',
    }
folder_name = input("\nВведите название рабочей папки:\n")
file_name = input("\nВведите имя файла для раскраски:\n")
print("\nШкалы для раскраски:")
print("1 - холодные цвета, полная (kbgcw)")
print("2 - холодные цвета, усеченная (kbcw)")
print("3 - теплые цвета, полная (krmyw)")
print("4 - теплые цвета, усеченная (kryw)")
scale = input("\nВыберите шкалу:\n")
grade = input("\nВведите начало, конец и шаг градации насыщенности (через пробел):\n")
timestamp = time.time()
param = scale_set[scale]
red_scale, green_scale, blue_scale = cmp.get_scale(param, folder_name + "/" + param)
flt.linear(folder_name + "/" + file_name)
linear_file_name = file_name[0:(len(file_name)-4)] + "_linear.bmp"
pnt.convert(red_scale, green_scale, blue_scale, folder_name + "/" + linear_file_name, param)
begin, end, step = map(int, grade.split())
sat.grade(folder_name + "/" + linear_file_name, param, begin, end, step)
print("\nРаскраска завершена")
print("Затраченное время ", round(time.time() - timestamp, 3))
