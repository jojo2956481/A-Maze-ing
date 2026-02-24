from mlx import Mlx


def mymouse():
    pass


def mykey(keynum, mystuff):
    if keynum == 32:
        m.mlx_mouse_hook(window, None, None)


def gere_close(dummy):
    m.mlx_loop_exit(ptr)


m = Mlx()
ptr = m.mlx_init()
window = m.mlx_new_window(ptr, 400, 400, "ok")
m.mlx_string_put(ptr, window, 20, 20, 255, "Hello PyMlx!")
m.mlx_string_put(ptr, window, 40, 40, 255, "Yeah")
for i in range(400):
    for j in range(400):
        if i >= 280:
            m.mlx_pixel_put(ptr, window, i, j, 0xF05E1706)
        elif i <= 120:
            m.mlx_pixel_put(ptr, window, i, j, 0xF01900A6)
        else:
            m.mlx_pixel_put(ptr, window, i, j, 0xF0FFFFFF)

m.mlx_mouse_hook(window, None, None)
m.mlx_hook(window, 33, 0, gere_close, None)
m.mlx_loop(ptr)
