# vim: ft=python

"""
Provides the Processing interface. Has several global flags to tweak the
rendering mode. Ideally I'd just use a PGraphics everywhere, but that's
incurring a significant slowdown, and I'm already slow enough because I'm using
Python.
"""

VIDEO = True
CYCLE_PAUSE = 300

from collections import deque
from itertools import islice

from fractals import FRACTAL_REGISTRY
from drawing import draw_fractal

def setup():
    global render_to_buffer, render_fullscreen, cycle, cycling, depth_delta, frames_per_draw
    size(1920 if VIDEO else 1000, 1080 if VIDEO else 1000)
    cycling = -1
    depth_delta = 0
    if VIDEO:
        render_to_buffer = False
        render_fullscreen = False
        cycle = True
        frames_per_draw = 600
    else:
        render_to_buffer = False
        render_fullscreen = False
        cycle = False
        frames_per_draw = 600
    set_fractal_drawer(0)
    colorMode(HSB, 255, 255, 255)
    noFill()
    print "Available fractals:"
    print "\n".join(
        "{}: {}".format(ind, i.name)
        for ind, i in enumerate(FRACTAL_REGISTRY, 1))

def set_fractal_drawer(n):
    global cur_fractal_drawer, fractal_graphics, cycling, projected_steps, cur_fractal_n
    cur_fractal_n = n
    fractal = FRACTAL_REGISTRY[n]
    fractal_depth = max(fractal.iterations + depth_delta, 1)
    cycling = -1
    if render_to_buffer:
        fractal_graphics = createGraphics(*(min(width, height),) * 2)
        fractal_graphics.beginDraw()
        fractal_graphics.colorMode(HSB, 255, 255, 255)
        fractal_graphics.noFill()
        fractal_graphics.endDraw()
    else:
        background(0)
        fractal_graphics = g
    cur_fractal_drawer = draw_fractal(fractal_graphics, fractal,
            min(fractal_graphics.width, fractal_graphics.height),
            fractal_depth)
    projected_steps = fractal.steps_func(fractal_depth)
    print "set to {}".format(fractal.name)

def advance():
    global cycling
    if cycling < 1 and render_to_buffer:
        fractal_graphics.beginDraw()
    # consume `iterations_per_frame` number of items from cur_fractal_drawer
    d = deque(islice(cur_fractal_drawer,
                     max(1, projected_steps // frames_per_draw)), maxlen=1)
    if not d:
        if cycle:
            print("preparing to cycle")
            cycling = CYCLE_PAUSE
        else:
            cycling = 0
    if cycling < 1 and render_to_buffer:
        fractal_graphics.endDraw()

def draw():
    global cur_fractal_n, cycling
    translate(width / 2 - height / 2, 0)
    if cycle and cycling != -1:
        cycling -= 1
        if cycling == 0:
            cycling = -1
            cur_fractal_n += 1
            if cur_fractal_n < len(FRACTAL_REGISTRY):
                set_fractal_drawer(cur_fractal_n)
            else:
                exit()
    else:
        if render_to_buffer:
            background(0)
        translate(0, height)
        scale(1, -1)
        if not render_fullscreen:
            translate(width * 0.1, height * 0.1)
            scale(0.8, 0.8)
        advance()
        if render_to_buffer:
            image(fractal_graphics, 0, 0)
        if VIDEO:
            saveFrame("frames/lsystems-#############.png")

def keyPressed():
    global iterations_per_frame, depth_delta
    if not VIDEO:
        n = keyCode - ord('1')
        if 0 <= n < len(FRACTAL_REGISTRY):
            set_fractal_drawer(n)
        elif keyCode == LEFT:
            iterations_per_frame = max(1, iterations_per_frame // 2)
        elif keyCode == RIGHT:
            iterations_per_frame *= 2
        elif keyCode == DOWN:
            depth_delta -= 1
        elif keyCode == UP:
            depth_delta += 1
    else:
        print "bro ur killin my flow"
