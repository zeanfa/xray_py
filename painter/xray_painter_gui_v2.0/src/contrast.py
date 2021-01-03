import numpy as np
import numpy.random.common
import numpy.random.bounded_integers
import numpy.random.entropy
from matplotlib.colors import ListedColormap
from PIL import Image
from decimal import Decimal, ROUND_HALF_UP
from utils import jit_cast


class Contraster:
    def __init__(self, in_dtype='uint16', out_dtype='uint16'):
        self.kp = 'kw'
        self.scale_dict = dict([('k', [0, 0, 0, 0]),
                                ('b', [0.11, 0, 0, 1]),
                                ('r', [0.3, 1, 0, 0]),
                                ('m', [0.41, 1, 0, 1]),
                                ('g', [0.59, 0, 1, 0]),
                                ('c', [0.7, 0, 1, 1]),
                                ('y', [0.89, 1, 1, 0]),
                                ('w', [1, 1, 1, 1])])
        self.gs_img = None
        self.color_img_f = None
        self.color_img_int = None
        self.full_scale = None
        self.color_scale = None
        self.color_scale_begin = 0
        self.color_scale_end = 0
        self.color_scale_img = None
        self.in_dtype = np.dtype(in_dtype)
        self.in_dtype_max = np.iinfo(self.in_dtype).max
        self.out_dtype = np.dtype(out_dtype)
        self.out_dtype_max = np.iinfo(self.out_dtype).max
        self.full_grad = self.in_dtype_max + 1
        self.color_grad = self.full_grad

    def load_img(self, gs_img, window=None, level=None, normalize=False):
        self.gs_img = gs_img
        self.color_img_int = self.gs_img
        if window is not None and level is not None:
            self.color_scale_begin = int((level - window * 0.5) * (self.in_dtype_max + 1))
            self.color_scale_end = int((level + window * 0.5) * (self.in_dtype_max + 1))
            self.color_grad = self.color_scale_end - self.color_scale_begin
        elif normalize:
            self.color_scale_begin = np.min(self.gs_img)
            self.color_scale_end = np.max(self.gs_img) + 1
            self.color_grad = self.color_scale_end - self.color_scale_begin
        else:
            self.color_scale_begin = 0
            self.color_scale_end = self.in_dtype_max + 1
            self.color_grad = self.full_grad

    def create_scale_wsat(self, user_kp, sat_rate, adaptive_saturation=False):
        self.kp = self.kp[0] + user_kp + self.kp[-1]
        color_scale = np.empty((0, 3))
        # create color scale linear pieces between the keypoints
        for i in range(len(self.kp) - 1):
            begin = self.scale_dict[self.kp[i]][0]
            end = self.scale_dict[self.kp[i + 1]][0]
            num_points_f = (end - begin) * self.color_grad * 1.0
            num_points_i = int(Decimal(num_points_f).quantize(0, ROUND_HALF_UP))
            colors_begin = self.scale_dict[self.kp[i]][1:]
            colors_end = self.scale_dict[self.kp[i + 1]][1:]
            if i == len(self.kp) - 2:
                endpoint = True
                num_points_i = self.color_grad - color_scale.shape[0]
            else:
                endpoint = False
            scale_part = np.linspace(colors_begin, colors_end, num_points_i, endpoint)
            if color_scale.shape[0] is not 0:
                color_scale = np.vstack((color_scale, scale_part))
            else:
                color_scale = scale_part
        # get kw scale for saturation adjustment
        kw_scale = np.linspace([0, 0, 0], [1, 1, 1], color_scale.shape[0])
        # apply adaptive saturation
        if adaptive_saturation:
            color_scale = np.multiply(color_scale, kw_scale)
            gray_remainder = np.multiply(np.ones(color_scale.shape) - kw_scale, kw_scale)
            color_scale = color_scale + gray_remainder
        # get final scale as weighted sum of color and kw scales
        self.color_scale = (1 - sat_rate) * kw_scale + sat_rate * color_scale
        self.color_scale_img = np.vstack((kw_scale, self.color_scale)).reshape((2, self.color_scale.shape[0], 3))

    def transform_scale_wl(self):
        # creates final scale according to Window/Level
        self.full_scale = np.empty((self.full_grad, 3), dtype=np.float64)
        self.full_scale[self.color_scale_begin:self.color_scale_end] = self.color_scale
        self.full_scale[0:self.color_scale_begin] = [0, 0, 0]
        self.full_scale[self.color_scale_end:] = [1, 1, 1]

    def map_by_scale(self, wl=False):
        # mapping by a scale
        custom_cm = ListedColormap(self.full_scale)
        self.color_img_f = custom_cm(self.gs_img)[:, :, :-1]

    def get_gs_img(self):
        return self.gs_img

    def get_color_img(self):
        # cast to used out_dtype (uint16 or uint8)
        self.color_img_int = jit_cast(self.color_img_f, self.out_dtype_max, self.out_dtype)
        return self.color_img_int


if __name__ == '__main__':
    user_kp = 'brmgcy'
    contrast = Contraster(in_dtype='uint8', out_dtype='uint8')
    gs_img = np.ones((100, 100))
    contrast.load_img(gs_img, normalize=False)
    contrast.create_scale_wsat(user_kp, sat_rate=1.0, adaptive_saturation=True)
    contrast.transform_scale_wl()
    contrast.map_by_scale()
    new_color = contrast.color_img_int.copy()
    scale_img_PIL = Image.fromarray(jit_cast(contrast.color_scale_img, type_max=255, dtype=np.uint8))
    resized_scale = scale_img_PIL.resize((2000, 200))
    resized_scale.show()
