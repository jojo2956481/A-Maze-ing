from mlx import Mlx
import numpy


def close_by_button(keycode, params):
    print(keycode)
    if keycode == 113:
        m.mlx_loop_exit(ptr)


def close_window(params):
    m.mlx_loop_exit(ptr)


def create_image(data):
    # BGRA
    for i in range(0, len(list(data)), 4):
        data[i] = 0
        data[i + 1] = 0
        data[i + 2] = 255
        data[i + 3] = 255
    return data


m = Mlx()
ptr = m.mlx_init()
window = m.mlx_new_window(ptr, 400, 400, "ok")
image = m.mlx_new_image(ptr, 400, 400)
data = m.mlx_get_data_addr(image)
print(data)
data = create_image(data[0])
# m.mlx_put_image_to_window(ptr, window, image, 0, 0)
m.mlx_string_put(ptr, window, 10, 10, 0xFFFF00FF, "A-maze-ing")
m.mlx_key_hook(window, close_by_button, None)
m.mlx_hook(window, 33, 0, close_window, None)
m.mlx_loop(ptr)
tab = numpy.array([1, 2, 3])
