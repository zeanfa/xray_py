from PIL import Image, ImageDraw

def convert(red_array, green_array, blue_array, file_name, scale_name):

    bw_im = Image.open(file_name)

    width, height = bw_im.size
    col_im=Image.new("RGB", (width, height))
    draw=ImageDraw.Draw(col_im)

    colour_pix = col_im.load()

    for i in range(width):
        for j in range(height):
            pixel = bw_im.getpixel((i, j))
            colour_pix[i, j] = (int(red_array[pixel[0]]), int(green_array[pixel[0]]), int(blue_array[pixel[0]]))

    bw_im.close()

    del draw
    col_im.save(file_name[0:(len(file_name)-4)] + "_" + scale_name + ".bmp", "BMP")
