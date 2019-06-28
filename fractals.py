"""
Instances of L-system fractals. See

- https://en.wikipedia.org/wiki/L-system
- http://paulbourke.net/fractals/lsys/
- https://youtu.be/E1B4UoSQMFw
"""

# TODO: implement Bourke's length factor for eg the "L system leaf"
#       implement some of the HUGE ones like the algae
#       Most critically, get all of the guesswork sorted out

from fractal_base import LSystemFractal

def draw(*args):
    """
    Dummy function that returns True, for nicer semantics in defining L systems.
    You pass each thing you want to be executed as an argument. Generally I've
    favoured lambda functions over functools.partial because I think they're
    cooler.
    """
    return True

def nodraw(*args):
    """
    Similar to draw(). With no arguments, can act as a no-op
    """
    return False

def standard_rules(t, angle=90, initial_pos=(0, 0), initial_heading=0,
        additions={}):
    """
    Provide the "standard" rule set, given the angle and the turtle and depth
    arguments. Can also append further rules, which may override standard rules.
    Also defines a "0" symbol, the function of which can be modified with the
    `initial_pos` and `initial_heading` parameters.

    This is basically a nonstandard helper function to hugely shorten the
    definition of each fractal.
    """
    rules = {"F": lambda: draw(t.forward(1)),
             "G": lambda: draw(t.forward(1)),
             "f": lambda: nodraw(t.fjump(1)),
             "-": lambda: nodraw(t.turn_degrees(-angle)),
             "+": lambda: nodraw(t.turn_degrees(angle)),
             "|": lambda: nodraw(t.turn_degrees(180)),
             "[": lambda: nodraw(t.save_state()),
             "]": lambda: nodraw(t.restore_state()),
             "X": nodraw,
             "Y": nodraw,
             "0": lambda: nodraw(t.jump(*initial_pos),
                                 t.setheading_degrees(initial_heading))}
    rules.update(additions)
    return rules

sierpinski = LSystemFractal(
    "Sierpinski's Gasket",
    "F+G+G",
    lambda d: 2 ** d,
    {"F": "F+G-F-G+F",
     "G": "GG"},
    lambda t, d: standard_rules(t, 120),
    9)

dragon = LSystemFractal(
    "The Dragon Curve",
    "0[FX]+[FX]+[FX]+FX",
    lambda d: 2 * 2 ** (d / 2.0),
    {"X": "X-YF-",
     "Y": "+FX+Y"},
    lambda t, d: standard_rules(t, 90, (0.5, 0.5), 45 * (d + 1)),
    15)

fern = LSystemFractal(
    "A Lindenmayer Fern",
    "0X",
    # This is basically just noting that it doubles its dimension along each
    # branch, and that it has some limit it approaches at infinity, found
    # by trial and error. It would be nice to find this more exactly in terms of
    # trigonometric functions of 25 degrees. (TODO)
    lambda d: 2.718281828 * 2 ** d,
    {"X": "F-[[X]+X]+F[+FX]-X",
     "F": "FF"},
    lambda t, d: standard_rules(t, 25, (0.5, 0), 90),
    9)

levy_c = LSystemFractal(
    "The Levy C Curve",
    "0F",
    lambda d: 2 * 2 ** (d / 2.0),
    {"F": "+F--F+"},
    lambda t, d: standard_rules(t, 45, additions=
                {"0": lambda: nodraw(t.jump(0.25, 0.25))}),
    16)

hilbert = LSystemFractal(
    "Hilbert's Space-Filling Curve",
    "X",
    lambda d: 2 ** d - 1,
    {"X": "+YF-XFX-FY+",
     "Y": "-XF+YFY+FX-"},
    lambda t, d: standard_rules(t),
    8)

sierp_hex = LSystemFractal(
    "Sierpinski's Gasket Hexagonal Variant",
    "F",
    lambda d: 2 ** d,
    {"F": "G-F-G",
     "G": "F+G+F"},
    lambda t, d: standard_rules(t, (-1) ** d * 60),
    8)

koch = LSystemFractal(
    "Koch Snowflake",
    "0F++F++F",
    lambda d: 2 * sqrt(3) / 3 * 3 ** d,
    {"F": "F-F++F-F"},
    lambda t, d: standard_rules(t, 60, additions=
            {"0": lambda: nodraw(t.jump(0.5 * (1 - 3 / (2 * sqrt(3))), 0.25))}),
    6)

koch_square = LSystemFractal(
    "Square Koch Curve",
    "0F-F-F-F",
    lambda d: 2 * 3 ** d,
    {"F": "F+F-F-F+F"},
    lambda t, d: standard_rules(t, 90, (0.25, 0.75)),
    6)

# TODO: ParametrisedLSystemFractal
binary_tree = LSystemFractal(
    "Binary Tree",
    "0++F",
    # A messy, but not intrinsically hugely complicated pair of interlaced
    # geometric progressions
    # TODO: scale with depth, rather than assume infinity. Remember leaves are
    #       weird
    lambda d: 1 + 2 ** (d - 1) * 4 / 3 * (1 + 0.25 * sqrt(2)),
    {"G": "GG",
     "F": "G[+F]-F"},
    lambda t, d: standard_rules(t, 45, additions=
            {"0": lambda: nodraw(t.jump(0.5, 0))}),
    10)

# TODO: some proper names here
#       Also, basically all of these are total guesswork as to the dimensions.

crystal = LSystemFractal(
    "Crystal",
    "F+F+F+F",
    lambda d: 3 ** d,
    {"F": "FF+F++F+F"},
    lambda t, d: standard_rules(t),
    6)

peano = LSystemFractal(
    "Peano Curve",
    "X",
    lambda d: 3 ** d - 1,
    {"X": "XFYFX+F+YFXFY-F-XFYFX",
     "Y": "YFXFY-F-XFYFX+F+YFXFY"},
    lambda t, d: standard_rules(t),
    5)

krishna_anklets = LSystemFractal(
    "Krishna Anklets",
    "0-X--X",
    lambda d: sqrt(2) * (2 ** d - 1),
    {"X": "XFX--XFX"},
    lambda t, d: standard_rules(t, 45, (0.5, 1)),
    7)

mango = LSystemFractal(
    "Mango",
    "0_Y---Y",
    lambda d: sqrt(3) * (3 * d - 2),
    {"X": "F-FF-F--[--X]F-FF-F--F-FF-F--",
     "Y": "f-F+X+F-fY"},
    lambda t, d: standard_rules(t, 60, (0.5, 0.5), additions=
        # black magic
        {"_": lambda: nodraw(t.fjump(-1.5 * d))}),
    22)

board = LSystemFractal(
    "Board",
    "F+F+F+F",
    lambda d: 3 ** d,
    {"F": "FF+F+F+F+FF"},
    lambda t, d: standard_rules(t),
    5)

square_sierpinski = LSystemFractal(
    "Square Sierpinski",
    "0_F+XF+F+XF",
    lambda d: 4 * (2 ** d) - 3,
    {"X": "XF-F+F-XF+F+XF-F+F-X"},
    lambda t, d: standard_rules(t, 90, (0.5, 0), additions=
        {"_": lambda: nodraw(t.fjump(-0.5))}),
    6)

# A weird one - it becomes idempotent after the third iteration.
# TODO: can this be made to generate further?
kolam = LSystemFractal(
    "Kolam",
    "0-D--D",
    lambda d: 19 * sqrt(2),
    {"A": "F++FFFF--F--FFFF++F++FFFF--F",
     "B": "F--FFFF++F++FFFF--F--FFFF++F",
     "C": "BFA--BFA",
     "D": "CFC--CFC"},
    lambda t, d: standard_rules(t, 45, (0.5, 1), additions=
        {"A": nodraw, "B": nodraw, "C": nodraw, "D": nodraw}),
    3)

bourke_bush_1 = LSystemFractal(
    "Bourke's first Bush",
    "0Y",
    lambda d: 2 * 2 ** d,
    {"X": "X[-FFF][+FFF]FX",
     "Y": "YFX[+Y][-Y]"},
    lambda t, d: standard_rules(t, 25.7, (0.5, 0), 90),
    7)

bourke_bush_2 = LSystemFractal(
    "Bourke's second Bush",
    "0F",
    lambda d: 4 * 2 ** d,
    {"F": "FF+[+F-F-F]-[-F+F+F]"},
    lambda t, d: standard_rules(t, 22.5, (0.5, 0), 90),
    6)

bourke_bush_3 = LSystemFractal(
    "Bourke's third Bush",
    "0F",
    lambda d: 3 ** d,
    {"F": "F[+FF][-FF]F[-F][+F]F"},
    lambda t, d: standard_rules(t, 35, (0.5, 0), 90),
    5)

saupe_bush = LSystemFractal(
    "Saupe's Bush",
    "0VZFFF",
    # TODO: i am truly lost
    lambda d: 2.5 * 3 * d,
    {"V": "[+++W][---W]YV",
     "W": "+X[-W]Z",
     "X": "-W[+X]Z",
     "Y": "YZ",
     "Z": "[-FFF][+FFF]F"},
    lambda t, d: standard_rules(t, 20, (0.5, 0.2), 90, additions=
        {"Z": nodraw, "V": nodraw, "W": nodraw}),
    13)

bourke_stick = LSystemFractal(
    "Bourke Stick",
    "0X",
    lambda d: 2.3 * 2 ** d,
    {"F": "FF",
     "X": "F[+X]F[-X]+X"},
    lambda t, d: standard_rules(t, 20, (0.5, 0), 90),
    9)

bourke_weed = LSystemFractal(
    "Bourke Weed",
    "0F",
    lambda d: 2.3 * 2 ** d,
    {"F": "FF-[XY]+[XY]",
     "X": "+FY",
     "Y": "-FX"},
    lambda t, d: standard_rules(t, 22.5, (0.5, 0), 90),
    8)

bourke_triangle = LSystemFractal(
    "Bourke Triangle",
    "0[G]+[G]+[G]",
    lambda d: 2 * 3 ** (d / 2.0),
    {"F": "F-F+F",
     "G": "F+F+F"},
    lambda t, d: standard_rules(t, 120, (0.5, 0.5)),
    8)

koch_island_1 = LSystemFractal(
    "Koch Island 1",
    "0F+F+F+F",
    # TODO: total bodge here
    lambda d: 2 * 4 ** d,
    {"F": "F+F-F-FFF+F+F-F"},
    lambda t, d: standard_rules(t, 90, (0.1, 0.6), 15),
    5)

koch_island_2 = LSystemFractal(
    "Koch Island 2",
    "0F+F+F+F",
    # TODO: this is even worse
    lambda d: 1.2 * 7 ** d,
    {"F": "F-FF+FF+F+F-F-FF+F+F-F-FF-FF+F"},
    lambda t, d: standard_rules(t, 90, (0.15, 0.4), -25),
    3)

koch_island_3 = LSystemFractal(
    "Koch Island 3",
    "0X+X+X+X+X+X+X+X",
    # TODO: aaaaaaaaaaaaaaaaaaaa
    lambda d: 0.6 * 7 ** d,
    {"X": "X+YF++YF-FX--FXFX-YF+X",
     "Y": "-FX+YFYF++YF+FX--FX-YF"},
    lambda t, d: standard_rules(t, 45, (0.05, 0.5), -150),
    4)

koch_island_4 = LSystemFractal(
    "Koch Island 4",
    "0F+F+F+F",
    # TODO y u c k
    lambda d: 0.17 * 7 ** d,
    {"F": "F+F-F-FF+F+F-F"},
    lambda t, d: standard_rules(t, 90, (0.1, 0.6), -60),
    4)

pentaplexity = LSystemFractal(
    "Pentaplexity",
    "0F++F++F++F++F",
    # TODO: figure out actual geometry
    lambda d: 3 ** d,
    {"F": "F++F++F|F-F++F"},
    lambda t, d: standard_rules(t, 36, (0.2, 0)),
    4)

bourke_rings = LSystemFractal(
    "Bourke Rings",
    "0F+F+F+F",
    # TODO TODO TODO
    lambda d: 2 * 3 ** d,
    {"F": "FF+F+F+F+F+F-F"},
    lambda t, d: standard_rules(t, 90, (0.05, 0.5), -140),
    5)

bourke_2 = LSystemFractal(
    "Bourke 2",
    "0F+F+F+F",
    lambda d: 5 + d + 3 ** d,
    {"F": "FF+F-F+F+FF"},
    lambda t, d: standard_rules(t, 90, (0.5, 0.5)),
    4)

hexagonal_gosper = LSystemFractal(
    "Hexagonal Gosper",
    "0XF",
    # TODO gnhhhhhhhhh
    lambda d: 5 * 2 ** d,
    {"X": "X+YF++YF-FX--FXFX-YF+",
     "Y": "-FX+YFYF++YF+FX--FX-Y"},
    lambda t, d: standard_rules(t, 60, (0.5, 0), -7.5 * d),
    5)

quadratic_gosper = LSystemFractal(
    "Quadratic Gosper",
    "YF",
    # TODO; this scales wrong
    lambda d: 2 * 4 ** d,
    {"X": "XFX-YF-YF+FX+FX-YF-YFFX+YF+FXFXYF-FX+YF+FXFX+YF-FXYF-YF-FX+FX+YFYF-",
     "Y": "+FXFX-YF-YF+FX+FXYF+FX-YFYF-FX-YF+FXYFYF-FX-YFFX+FX+YF-YF-FX+FX+YFY",
     },
    lambda t, d: standard_rules(t),
    3)
