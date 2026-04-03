from mlx import Mlx


def close_by_button(keycode, params):
    print(keycode)
    if keycode == 113:
        m.mlx_loop_exit(ptr)


def close_window(params):
    m.mlx_loop_exit(ptr)


m = Mlx()
ptr = m.mlx_init()
window = m.mlx_new_window(ptr, 1000, 1000, "ok")
m.mlx_key_hook(window, close_by_button, None)
m.mlx_loop(ptr)
