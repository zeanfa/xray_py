from PIL import Image, ImageDraw
import numpy
import math
import xray_compute as cmp
import xray_painter as pnt
import xray_filter as flt
import xray_saturation as sat

folder_name = input("\nHello! enter workspace folder name\n")
file_name = 0
param = 0

while(1):
    cmd = input("\nChoose option:\nhelp scale filter grade\n")
    #print(cmd)
    if cmd.find("help") == 0:
       print("\nThis app helps you to colour Xray photographs")
       print("scale - choose a scale you whant your image be painted to")
       print("filter - apply histogram equalization filter to the image")
       print("grade - make a set of saturation graded images\n")
       continue

    if cmd.find("scale") == 0:
        print("\nparameters that can be used: k b r m g c y w")
        print("k - black")
        print("b - blue")
        print("r - red")
        print("m - purple (magenta)")
        print("g - green")
        print("c - cyan (light blue)")
        print("y - yellow")
        print("w - white")
        print("k must be the first and w must be the last\n")
        param = input("enter scale\n")
        red_scale, green_scale, blue_scale = cmp.get_scale(param, folder_name + "/" + param)
        print("\nscale is saved")
        file_name = input("\nenter file name to paint\n")
        pnt.convert(red_scale, green_scale, blue_scale, folder_name + "/" + file_name, param)
        print("painting done")
        
    elif cmd.find("filter") == 0:
        print("\nequalizing may take some time, you'll have to wait")
        file_name = input("\nenter file name to filter\n")
        flt.equalize(folder_name + "/" + file_name)
        print("filtering done\n")
        
    elif cmd.find("grade") == 0:
        print("\nmake sure you have already got a colour image!\n")
        if param != 0 and file_name != 0:
            if input("\nuse previous file and scale? y/n\n").find("n") == 0:
                file_name = input("enter file name to be graded\n")
                param = input("\nenter scale\n")
        else:
            file_name = input("enter file name to be graded\n")
            param = input("\nenter scale\n")
        grade = input("\nenter begin, end, step of saturation\n")
        begin, end, step = map(int, grade.split())
        sat.grade(folder_name + "/" + file_name, param, begin, end, step)
        print("grading done\n")

    else:
        print("\nno command found\n")

    if input("\ncontinue? y/n\n").find("n") == 0:
        print("\nBye!\n")
        break
    
