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
