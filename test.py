from mlx import Mlx
import numpy


def close_by_button(keycode, params):
    if keycode == 113:
        m.mlx_loop_exit(ptr)


def close_window(params):
    m.mlx_loop_exit(ptr)


def create_image(data):
    for i in range(len(list(data))):
        data[i] = 0b1100001100110011


m = Mlx()
ptr = m.mlx_init()
window = m.mlx_new_window(ptr, 400, 400, "ok")
image = m.mlx_new_image(ptr, 400, 1000)
data = m.mlx_get_data_addr(image)
data = create_image(data[0])
m.mlx_put_image_to_window(ptr, window, image, 0, 0)
m.mlx_key_hook(window, close_by_button, None)
m.mlx_hook(window, 33, 0, close_window, None)
m.mlx_loop(ptr)
tab = numpy.array([1, 2, 3])
