SOGL=None

def clear_color(r:int, g:int, b:int, a:int) -> None:
    SOGL.sgClearColor(r, g, b, a)

def clear() -> None:
    SOGL.sgClear()

def buffer_swap(win) -> None:
    SOGL.sgBufferSwap(win)


