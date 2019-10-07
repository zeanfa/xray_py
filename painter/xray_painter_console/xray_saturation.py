from PIL import Image, ImageDraw
import numpy

def np_get_scale(intensity, bw_name, col_name):
    bw_im = Image.open(bw_name)
    col_im = Image.open(col_name)
    bw_pix = numpy.atleast_1d(bw_im)
    col_pix = numpy.atleast_1d(col_im)

    color = intensity/100
    b_w = 1 - color
    sum_pix = bw_pix*b_w + col_pix*color
    sum_im = Image.fromarray(sum_pix.astype('uint8'), mode = 'RGB')
    sum_im.save(col_name[0:(len(col_name)-4)] + "_" + str(intensity)+ ".bmp", "BMP")
    bw_im.close()
    col_im.close()

def grade(file_name, scale_name, begin, end, step):
    if step == 0:
        step = 5
    col_file_name = file_name[0:(len(file_name) - 4)] + "_" + scale_name + ".bmp"
    for i in range(begin, end + step, step):
        np_get_scale(i, file_name, col_file_name)
