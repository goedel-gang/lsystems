from hilbert import draw_hil
from dragon import draw_drg
from levy import draw_lev
from koch import draw_koc

FUNS = [(draw_hil, {"depth": 9}),
        (draw_drg, {"depth": 18}),
        (draw_lev, {"depth": 18}),
        (draw_koc, {"depth": 8}),]

PER_FRAME = 100
CFUN = 0

def setup():
    global fun, FUNS
    size(1000, 1000)
    background(0)
    colorMode(HSB, 255, 255, 255)
    f, a = FUNS[CFUN]
    fun = f(width=height, **a)

def draw():
    try:
        for _ in xrange(PER_FRAME):
            next(fun)
    except StopIteration:
        pass

def keyPressed():
    global CFUN
    n = keyCode - ord('1')
    if 0 <= n < len(FUNS):
        CFUN = n
        setup()