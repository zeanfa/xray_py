import numpy as np
from numba import njit
from PIL import Image, ImageDraw, ImageFont


@njit(cache=True)
def jit_cast(img, type_max=65535, dtype=np.uint16):
    # casting to set dtype
    return (type_max * img).astype(dtype)


def get_user_kp(preset, blue, red, magenta, green, cyan, yellow):
    # check if a preset is chosen
    if preset == 'None':
        # construct scale from single colors
        kp_full = 'brmgcy'
        kp_bool = [blue, red, magenta, green, cyan, yellow]
        user_kp = ''.join([a for a, b in zip(kp_full, kp_bool) if b is True])
    else:
        # process the preset
        preset_dict = dict([('full',    'brmgcy'),
                            ('warm',    'ry'),
                            ('cold',    'bg'),
                            ('compBY',  'by'),
                            ('compRC',  'rc'),
                            ('compMG',  'mg')])
        user_kp = preset_dict[preset]
    return user_kp


def draw_axis(image):
    img_width = image.width
    img_height = image.height
    res_image = Image.new("RGB", (img_width, int(img_height / 0.825)), (255, 255, 255))
    res_image.paste(image, (0, 0))
    draw = ImageDraw.Draw(res_image)
    bias = 0.1
    width_bias = int(img_width * 0.5 * bias / 100)
    str_width = int(img_width * (100 - bias) / 100)
    draw.line((width_bias, int(img_height), str_width + width_bias, int(img_height)), fill=(0, 0, 0), width=2)
    for i in range(0, 11):
        x = int(str_width * i / 10 + width_bias)
        draw.line((x, int(0.95 * img_height), x, int(1.05 * img_height)), fill="black", width=2)
        fontsize = 12
        font = ImageFont.truetype("arial", fontsize)
        text_x = x - fontsize / 2
        if text_x < 0:
            text_x = 0
        draw.text((text_x, 1.05 * img_height), str(i / 10), fill="black", font=font)
    return res_image
