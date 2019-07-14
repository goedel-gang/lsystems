"""
Provides the Processing interface. Has several global flags to tweak the
rendering mode. Ideally I'd just use a PGraphics everywhere, but that's
incurring a significant slowdown, and I'm already slow enough because I'm using
Python.
"""

# TODO: shuffle mode

# Record each frame, and set other values to be suitable for video recording
VIDEO = False
# Don't actually save any frames, but still set video default graphics options
VIDEO_MOCK = False

# When automatically cycling, pause for this many frames
CYCLE_PAUSE = 300

# Take a screenshot of each fractal when it completes
SCREENSHOT = True

# draw some lines to work out where the centre is. Turns out I don't have the
# requisite IQ and understanding of geometry to reliably see if things are
# centred right.
GUIDELINES = False

from collections import deque
from itertools import islice, izip
from textwrap import dedent

from fractals import fractal_registry
from drawing import ProcessingTurtle

# The order in which to assign keys to fractals from fractal_registry.
FRACTAL_KEYS = "1234567890QWERTYUIOPASDFGHJKLZXCVBNM"

assert len(FRACTAL_KEYS) >= len(fractal_registry)

FRACTAL_KEYMAP = dict((ord(key), ind) for ind, key in
        islice(enumerate(FRACTAL_KEYS), len(fractal_registry)))

def helptext():
    print dedent("""\
            This is an L-system drawing program. You can directly draw a fractal
            by pressing a key, or you can let it cycle by itself. Press '?' to
            re-print this menu.
            Available fractals:""")
    print "\n".join(
        "{}: {}".format(key, i.name)
        for key, i in izip(FRACTAL_KEYS, fractal_registry))

def setup():
    global render_to_buffer, render_fullscreen, cycle, cycling, depth_delta, \
           frames_per_draw
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
        cycle = True
        frames_per_draw = 600
    set_fractal_drawer(0)
    colorMode(HSB, 255, 255, 255)
    noFill()
    helptext()

def set_fractal_drawer(n):
    global cur_fractal_drawer, fractal_graphics, cycling, projected_steps, \
           cur_fractal_n, has_screenshot
    has_screenshot = False
    cur_fractal_n = n
    fractal = fractal_registry[n]
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
    cur_fractal_drawer = fractal.draw(ProcessingTurtle(fractal_graphics),
            fractal_depth,
            min(fractal_graphics.width, fractal_graphics.height))
    projected_steps = fractal.project_steps(fractal_depth)
    print "set to {}".format(fractal.name)

def advance():
    global cycling, has_screenshot, depth_delta
    if cycling < 1 and render_to_buffer:
        fractal_graphics.beginDraw()
    # consume `iterations_per_frame` number of items from cur_fractal_drawer
    d = deque(islice(cur_fractal_drawer,
                     max(1, projected_steps // frames_per_draw)), maxlen=1)
    if not d:
        if (not GUIDELINES and not has_screenshot and SCREENSHOT
                and depth_delta == 0):
            scrot_name = "screenshots/{:02}_{}.png".format(cur_fractal_n,
                    "".join(c for c in
                    fractal_registry[cur_fractal_n]
                        .name.lower().replace(" ", "_")
                    if c == "_" or c.isalnum()))
            print("saving {}".format(scrot_name))
            save(scrot_name)
            has_screenshot = True
        if cycle:
            print("preparing to cycle")
            cycling = max(CYCLE_PAUSE, 1)
        else:
            cycling = 0
    if cycling < 1 and render_to_buffer:
        fractal_graphics.endDraw()

def draw():
    global cur_fractal_n, cycling
    if GUIDELINES:
        line(0, 0, width, height)
        line(0, height, width, 0)
    translate(width / 2 - height / 2, 0)
    if cycle and cycling != -1:
        cycling -= 1
        if cycling == 0:
            cycling = -1
            cur_fractal_n += 1
            if cur_fractal_n < len(fractal_registry):
                depth_delta = 0
                set_fractal_drawer(cur_fractal_n)
            else:
                if VIDEO:
                    exit()
                else:
                    set_fractal_drawer(0)
    else:
        if render_to_buffer:
            background(0)
        translate(0, height)
        scale(1, -1)
        if not render_fullscreen:
            # Assume height is less than width
            translate(height * 0.1, height * 0.1)
            scale(0.8, 0.8)
        advance()
        if render_to_buffer:
            image(fractal_graphics, 0, 0)
    if VIDEO:
        if not VIDEO_MOCK:
            saveFrame("frames/lsystems-#############.png")

def keyPressed():
    global frames_per_draw, depth_delta, cycle
    if not VIDEO:
        if keyCode in FRACTAL_KEYMAP:
            depth_delta = 0
            set_fractal_drawer(FRACTAL_KEYMAP[keyCode])
        elif keyCode == LEFT:
            frames_per_draw = max(1, frames_per_draw * 9 // 10)
            print "frames per draw: {}".format(frames_per_draw)
        elif keyCode == RIGHT:
            frames_per_draw = frames_per_draw * 10 // 9
            print "frames per draw: {}".format(frames_per_draw)
        elif keyCode == DOWN:
            depth_delta -= 1
            set_fractal_drawer(cur_fractal_n)
            print "depth delta: {}".format(depth_delta)
        elif keyCode == UP:
            depth_delta += 1
            set_fractal_drawer(cur_fractal_n)
            print "depth delta: {}".format(depth_delta)
        elif key == "?":
            helptext()
        elif key == ".":
            cycle = not cycle
            print "cycle is set to {}".format(cycle)
        elif isinstance(key, unicode):
            print "I don't know what to do with {!r}".format(key)
    else:
        print "bro ur killin my flow"
