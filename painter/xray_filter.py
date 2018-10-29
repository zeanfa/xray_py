from PIL import Image, ImageDraw
import numpy
import math

def cdf(arr, x):
    y = 0
    for i in range(x, -1, -1):
        y = y + arr[i]
    return y

def find_min(arr):
    for i in range(0, 256):
        if arr[i] != 0:
            return i
    return 0

def linear(file_name):
    init_im = Image.open(file_name)

    width, height = init_im.size

    lin_im=Image.new("RGB", (width, height))
    draw=ImageDraw.Draw(lin_im)
    lin_image_pix = lin_im.load()

    max_color = 0
    min_color = 255

    for i in range(width):
        for j in range(height):
            if init_im.getpixel((i, j))[0] > max_color:
                max_color = init_im.getpixel((i, j))[0]
            if init_im.getpixel((i, j))[0] < min_color:
                min_color = init_im.getpixel((i, j))[0]

    if max_color == min_color:
        print("mono image")
        exit
        
    for i in range(width):
        for j in range(height):
            pixel = init_im.getpixel((i, j))
            lin_pixel = int(255*(pixel[0] - min_color)/(max_color - min_color))
            lin_image_pix[i, j] = (int(pixel[0]), int(pixel[0]), int(pixel[0]))
            
    
    del draw
    lin_im.save(file_name[0:(len(file_name)-4)] + "_linear.bmp", "BMP")

    init_im.close()
    

def equalize(file_name):
    hist_arr = [0]*256
    init_im = Image.open(file_name)

    width, height = init_im.size

    eq_im=Image.new("RGB", (width, height))
    draw=ImageDraw.Draw(eq_im)
    eq_pix = eq_im.load()

    num_pix = height*width

    # make histogram
    for i in range(width):
        for j in range(height):
            # Get Pixel
            pixel = init_im.getpixel((i, j))
            hist_arr[pixel[0]] += 1

    min_h = find_min(hist_arr)


    # equalize
    for i in range(width):
        for j in range(height):
            # Get Pixel
            pixel = init_im.getpixel((i, j))

            new_colour = round(((cdf(hist_arr, pixel[0]) - cdf(hist_arr, min_h))/(num_pix - 1))*255)
            #new_colour = round(((cdf(hist_arr, pixel[0]))/(num_pix - 1))*255)

            # Set Pixel in new image
            eq_pix[i, j] = (int(new_colour), int(new_colour), int(new_colour))


    del draw
    eq_im.save(file_name[0:(len(file_name)-4)] + "_equal.bmp", "BMP")

    init_im.close()
