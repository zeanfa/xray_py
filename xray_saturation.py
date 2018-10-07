from PIL import Image, ImageDraw

def get_scale(intensity, bw_name, col_name):
    bw_im = Image.open(bw_name)
    col_im = Image.open(col_name)

    width, height = bw_im.size
    sum_im=Image.new("RGB", (width, height))
    draw=ImageDraw.Draw(sum_im)

    color = intensity/100
    b_w = 1-color


    sum_pix = sum_im.load()

    # Transform to grayscale
    for i in range(width):
        for j in range(height):
            # Get Pixel
            bw_pixel = bw_im.getpixel((i, j))
            col_pixel = col_im.getpixel((i, j))

            # Get R, G, B values (This are int from 0 to 255)
            #grey =   pixel[0]

            # Set Pixel in new image
            sum_pix[i, j] = (int(round(bw_pixel[0]*b_w + col_pixel[0]*color)),
                             int(round(bw_pixel[1]*b_w + col_pixel[1]*color)),
                             int(round(bw_pixel[2]*b_w + col_pixel[2]*color)))


    bw_im.close()

    del draw
    sum_im.save(col_name[0:(len(col_name)-4)] + "_" + str(intensity)+ ".bmp", "BMP")

def grade(file_name, scale_name, begin, end, step):
    col_file_name = file_name[0:(len(file_name) - 4)] + "_" + scale_name + ".bmp"
    for i in range(begin, end + step, step):
        get_scale(i, file_name, col_file_name)
