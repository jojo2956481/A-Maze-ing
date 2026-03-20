from mlx import Mlx
import numpy


def close_by_button(keycode, params):
    if keycode == 113:
        m.mlx_loop_exit(ptr)


def close_window(params):
    m.mlx_loop_exit(ptr)


m = Mlx()
ptr = m.mlx_init()
window = m.mlx_new_window(ptr, 400, 400, "ok")
image = m.mlx_new_image(ptr, 400, 400)
print(m.mlx_get_data_addr(image))
m.mlx_put_image_to_window(ptr, window, image, 0, 0)
m.mlx_key_hook(window, close_by_button, None)
m.mlx_hook(window, 33, 0, close_window, None)
m.mlx_loop(ptr)
tab = numpy.array([1, 2, 3])
