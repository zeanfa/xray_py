from PIL import Image, ImageDraw

def convert(red_array, green_array, blue_array, bw_im):

    width, height = bw_im.size
    col_im=Image.new("RGB", (width, height))
    draw=ImageDraw.Draw(col_im)

    colour_pix = col_im.load()
    bw_pix = bw_im.load()

    for i in range(width):
        for j in range(height):
            pixel = bw_pix[i, j]
            colour_pix[i, j] = (int(red_array[pixel]), int(green_array[pixel]), int(blue_array[pixel]))

    del draw

    return col_im
