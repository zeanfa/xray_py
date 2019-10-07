from PIL import Image, ImageDraw
import numpy
import math

def linear(init_im):

    width, height = init_im.size
    init_pix = numpy.atleast_1d(init_im)
    
    lin_f = lambda x:(x - init_pix.min())/(init_pix.max() - init_pix.min())
    lin_pix = lin_f(init_pix)*255

    lin_im = Image.fromarray(lin_pix.astype('uint8'), mode = 'L')
    return lin_im




