from PIL import Image, ImageDraw
import numpy

def np_get_scale(intensity, bw_im, col_im):
    bw_pix = numpy.atleast_3d(bw_im)
    col_pix = numpy.atleast_1d(col_im)

    color = intensity/100
    b_w = 1 - color
    sum_pix = bw_pix*b_w + col_pix*color
    sum_im = Image.fromarray(sum_pix.astype('uint8'), mode = 'RGB')
    return sum_im
