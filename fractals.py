"""
Using Python turtle to draw L-system fractals
It uses layered lazy generators so it is very memory-efficient - effectively
using a call-stack of the size of the number of iterations. See [1].

[1]: https://en.wikipedia.org/wiki/L-system
"""

from collections import namedtuple
from math import cos, pi

_LSystemFractal = namedtuple("LSystemFractal",
                             """name start size_func rules draw_rules
                                iterations""")

FRACTAL_REGISTRY = []

def LSystemFractal(*args, **kwargs):
    lsf = _LSystemFractal(*args, **kwargs)
    FRACTAL_REGISTRY.append(lsf)
    return lsf

def substitute(sequence, rules):
    for symbol in sequence:
        if symbol not in rules:
            yield symbol
        else:
            for sym in rules[symbol]:
                yield sym

class ProcessingTurtle:
    def __init__(self, x=0, y=0, heading=0, pendown=True):
        self.x = x
        self.y = y
        self.heading = heading
        self._pendown = True
        self.times_moved = 0
        self.state_stack = []

    def setpos(self, nx, ny):
        if self._pendown:
            line(self.x, self.y, nx, ny)
        self.jump(nx, ny)

    def jump(self, nx, ny):
        self.x = nx
        self.y = ny

    def setheading_degrees(self, heading):
        self.heading = radians(heading)

    def forward(self, steps):
        self.setpos(self.x + steps * cos(self.heading),
                    self.y + steps * sin(self.heading))
        self.times_moved += 1

    def turn_degrees(self, angle):
        self.heading += radians(angle)
        self.heading %= 2 * pi

    def penup(self):
        self._pendown = False

    def pendown(self):
        self._pendown = True

    def save_state(self):
        self.state_stack.append(
                (self.x, self.y, self.heading, self._pendown))

    def restore_state(self):
        self.x, self.y, self.heading, self._pendown = self.state_stack.pop()

def nop():
    pass

sierpinski = LSystemFractal(
    "Sierpinski's Gasket",
    "F-G-G",
    lambda depth: 3 ** depth * 3,
    {"F": "F-G+F+G-F",
     "G": "GG"},
    lambda t, depth: {"F": lambda: t.forward(width * 2 ** -depth),
                      "G": lambda: t.forward(width * 2 ** -depth),
                      "-": lambda: t.turn_degrees(+120),
                      "+": lambda: t.turn_degrees(-120)},
    9)

dragon = LSystemFractal(
    "The Dragon Curve",
    "0FX",
    lambda depth: 2 ** depth,
    {"X": "X+YF+",
     "Y": "-FX-Y"},
    lambda t, depth: {"F": lambda: t.forward(width * 0.5 * 2 ** -(depth / 2)),
                      "-": lambda: t.turn_degrees(+90),
                      "+": lambda: t.turn_degrees(-90),
                      "0": lambda: (t.turn_degrees(45 + 45 * depth),
                                    t.jump(width * 0.35, height * 0.25)),
                      "X": nop,
                      "Y": nop},
    15)

def fern_steps(depth):
    """
    Helper function to calculate the number of steps for a Lindenmayer fern.
    Very much ungraceful.

    TODO: matrices logarithmic in number of iterations.
    """
    F = 0
    X = 1
    for _ in xrange(depth):
        F, X = X * 3 + F * 2, X * 4
    return F

fern = LSystemFractal(
    "A Lindenmayer Fern",
    "0X",
    fern_steps,
    {"X": "F+[[X]-X]-F[-FX]+X",
     "F": "FF"},
    # TODO: better approach to this
    lambda t, depth: {"F": lambda: t.forward(width * 10 * 3 ** -(depth)),
                      "-": lambda: t.turn_degrees(+25),
                      "+": lambda: t.turn_degrees(-25),
                      "X": nop,
                      "[": t.save_state,
                      "]": t.restore_state,
                      "0": lambda: (t.jump(width / 2, 0),
                                    t.setheading_degrees(90))},
    8)

levy_c = LSystemFractal(
    "The Levy C Curve",
    "0F",
    lambda depth: 2 ** depth,
    {"F": "+F--F+"},
    lambda t, depth: {"F": lambda: t.forward(width * 0.5 * 2 ** -(depth / 2)),
                      "-": lambda: t.turn_degrees(-45),
                      "+": lambda: t.turn_degrees(+45),
                      "0": lambda: t.jump(0.25 * width, 0.25 * height)},
    14)

hilbert = LSystemFractal(
    "Hilbert's Space-Filling Curve",
    "A",
    lambda depth: 4 ** depth,
    {"A": "-BF+AFA+FB-",
     "B": "+AF-BFB-FA+"},
    lambda t, depth: {"F": lambda: t.forward(width * 2 ** -(depth)),
                      "A": nop,
                      "B": nop,
                      "-": lambda: t.turn_degrees(+90),
                      "+": lambda: t.turn_degrees(-90)},
    8)

sierp_hex = LSystemFractal(
    "Sierpinski's Gasket Hexagonal Variant",
    "A",
    lambda depth: 3 ** depth,
    {"A": "B-A-B",
     "B": "A+B+A"},
    lambda t, depth: {"A": lambda: t.forward(width * 2 ** -depth),
                      "B": lambda: t.forward(width * 2 ** -depth),
                      "-": lambda: t.turn_degrees(+60),
                      "+": lambda: t.turn_degrees(-60)},
    9)

koch = LSystemFractal(
    "Koch Snowflake",
    "0F--F--F",
    lambda depth: 3 * 4 ** depth,
    {"F": "F+F--F+F"},
    lambda t, depth: {"F": lambda: t.forward(3 / (2 * sqrt(3))
                                           * width * 3 ** -depth),
                      "-": lambda: t.turn_degrees(60),
                      "+": lambda: t.turn_degrees(-60),
                      "0": lambda: t.jump(0.5 * (1 - 3 / (2 * sqrt(3))) * width,
                                          0.25 * width)},
    7)

koch_square = LSystemFractal(
    "Square Koch Curve",
    "F",
    lambda depth: 5 ** depth,
    {"F": "F+F-F-F+F"},
    lambda t, depth: {"F": lambda: t.forward(width * 3 ** -depth),
                      "-": lambda: t.turn_degrees(-90),
                      "+": lambda: t.turn_degrees(+90)},
    7)

def draw_fractal(fractal):
    t = ProcessingTurtle(0, 0, 0)
    background(0)
    path = fractal.start
    expected_steps = fractal.size_func(fractal.iterations)
    draw_rules = fractal.draw_rules(t, fractal.iterations)
    for _ in xrange(fractal.iterations):
        path = substitute(path, fractal.rules)
    for symbol in path:
        stroke(255.0 * t.times_moved / expected_steps, 255, 255)
        draw_rules[symbol]()
        yield
