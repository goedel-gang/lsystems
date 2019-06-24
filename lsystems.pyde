# vim: ft=python

from fractals import FRACTAL_REGISTRY, draw_fractal

PER_FRAME = 1000

def setup():
    global cur_fractal
    size(1000, 1000)
    background(0)
    colorMode(HSB, 255, 255, 255)
    noFill()
    cur_fractal = draw_fractal(FRACTAL_REGISTRY[0])
    print("Available fractals:")
    print("\n".join(
        "{}: {}".format(ind, i.name)
        for ind, i in enumerate(FRACTAL_REGISTRY, 1)))

def draw():
    translate(width * 0.1, height * 0.1)
    scale(0.8, 0.8)
    try:
        for _ in xrange(PER_FRAME):
            next(cur_fractal)
    except StopIteration:
        pass

def keyPressed():
    global cur_fractal
    n = keyCode - ord('1')
    if 0 <= n < len(FRACTAL_REGISTRY):
        background(0)
        cur_fractal = draw_fractal(FRACTAL_REGISTRY[n])
