"""
Instances of L-system fractals. See

- https://en.wikipedia.org/wiki/L-system
- http://paulbourke.net/fractals/lsys/
- https://youtu.be/E1B4UoSQMFw
"""

# TODO: implement Bourke's length factor for eg the "L system leaf"
#       implement some of the HUGE ones like the algae
#       Most critically, get all of the guesswork sorted out

from math import sqrt
from itertools import chain

from matrix import Matrix
from fractal_base import LSystemFractal

fractal_registry = []

def register_fractal(*args, **kwargs):
    """
    Dummy wrapper around LSystemFractal that also registers fractals in a list.
    """
    fractal = LSystemFractal(*args, **kwargs)
    fractal_registry.append(fractal)
    return fractal

def draw(*args):
    """
    Dummy function that returns 1, for nicer semantics in defining L systems.
    You pass each thing you want to be executed as an argument. Generally I've
    favoured lambda functions over functools.partial because I think they're
    cooler.
    """
    return 1

def nodraw(*args):
    """
    Similar to draw(). With no arguments, can act as a no-op
    """
    return 0

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

sierpinski = register_fractal(
    "Sierpinski's Gasket",
    "F+G+G",
    {"F": "F+G-F-G+F",
     "G": "GG"},
    lambda t, d: standard_rules(t, 120),
    lambda d: 2 ** d,
    9)

dragon = register_fractal(
    "The Dragon Curve",
    "0[FX]+[FX]+[FX]+FX",
    {"X": "X-YF-",
     "Y": "+FX+Y"},
    lambda t, d: standard_rules(t, 90, (0.5, 0.5), 45 * (d + 1)),
    lambda d: 2 * 2 ** (d / 2.0),
    15)

fern = register_fractal(
    "A Lindenmayer Fern",
    "0X",
    # This is basically just noting that it doubles its dimension along each
    # branch, and that it has some limit it approaches at infinity, found
    # by trial and error. It would be nice to find this more exactly in terms of
    # trigonometric functions of 25 degrees. (TODO)
    {"X": "F-[[X]+X]+F[+FX]-X",
     "F": "FF"},
    lambda t, d: standard_rules(t, 25, (0.5, 0), 90),
    lambda d: 2.718281828 * 2 ** d,
    9)

levy_c = register_fractal(
    "The Levy C Curve",
    "0F",
    {"F": "+F--F+"},
    lambda t, d: standard_rules(t, 45, (0.25, 0.25)),
    lambda d: 2 * 2 ** (d / 2.0),
    16)

hilbert = register_fractal(
    "Hilbert's Space-Filling Curve",
    "X",
    {"X": "+YF-XFX-FY+",
     "Y": "-XF+YFY+FX-"},
    lambda t, d: standard_rules(t),
    lambda d: 2 ** d - 1,
    8)

sierp_hex = register_fractal(
    "Sierpinski's Gasket Hexagonal Variant",
    "F",
    {"F": "G-F-G",
     "G": "F+G+F"},
    lambda t, d: standard_rules(t, (-1) ** d * 60),
    lambda d: 2 ** d,
    8)

koch = register_fractal(
    "Koch Snowflake",
    "0F++F++F",
    {"F": "F-F++F-F"},
    lambda t, d: standard_rules(t, 60, (0.5 * (1 - 3 / (2 * sqrt(3))), 0.25)),
    lambda d: 2 * sqrt(3) / 3 * 3 ** d,
    6)

koch_square = register_fractal(
    "Square Koch Curve",
    "0F-F-F-F",
    {"F": "F+F-F-F+F"},
    lambda t, d: standard_rules(t, 90, (0.25, 0.75)),
    lambda d: 2 * 3 ** d,
    6)

# TODO: Parametrisedregister_fractal
binary_tree = register_fractal(
    "Binary Tree",
    "0++F",
    {"G": "GG",
     "F": "G[+F]-F"},
    lambda t, d: standard_rules(t, 45, (0.5, 0)),
    # A messy, but not intrinsically hugely complicated pair of interlaced
    # geometric progressions
    # TODO: scale with depth, rather than assume infinity. Remember leaves are
    #       weird
    lambda d: 1 + 2 ** (d - 1) * 4 / 3 * (1 + 0.25 * sqrt(2)),
    10)

# TODO: perhaps better done through the OOP interface
def fibo_rules(t):
    """
    A function that uses a closure over a boolean flag to keep track of the
    parity of the index of each symbol, which is needed for the construction of
    the Fibonacci word fractal.

    Mutable object workaround on account of Python 2 not having `nonlocal`s.
    """
    ind_is_odd = [False]
    def F():
        ind_is_odd[0] = not ind_is_odd[0]
        if ind_is_odd[0]:
            return draw(t.forward(1), t.turn_degrees(+90))
        else:
            return draw(t.forward(1), t.turn_degrees(-90))
    def G():
        ind_is_odd[0] = not ind_is_odd[0]
        return draw(t.forward(1))
    return {"F": F, "G": G}

def fibo_dim(n):
    """
    Calculate dimensions of Fibonacci word fractals. See
    fibonacci/investigate.py.
    """
    if n % 3 == 0:
        return (Matrix([ [0, 1], [1, 2] ]) ** (n // 3)
                * Matrix([[1], [3]])).array[0][0]
    elif n % 3 == 2:
        return (Matrix([ [0, 1], [1, 2] ]) ** (n // 3)
                * Matrix([[2], [5]])).array[0][0]
    else:
        return (Matrix([ [0, 1], [1, 2] ]) ** (n // 3)
                * Matrix([[2], [5]])).array[0][0] - 1

fibonacci_word = register_fractal(
    "Fibonacci Word Fractal",
    "0F",
    {"F": "FG",
     "G": "F"},
    lambda t, d: standard_rules(t, 90, additions=fibo_rules(t)),
    fibo_dim,
    23)

crystal = register_fractal(
    "Crystal",
    "F+F+F+F",
    {"F": "FF+F++F+F"},
    lambda t, d: standard_rules(t),
    lambda d: 3 ** d,
    6)

peano = register_fractal(
    "Peano Curve",
    "X",
    {"X": "XFYFX+F+YFXFY-F-XFYFX",
     "Y": "YFXFY-F-XFYFX+F+YFXFY"},
    lambda t, d: standard_rules(t),
    lambda d: 3 ** d - 1,
    5)

krishna_anklets = register_fractal(
    "Krishna Anklets",
    "0-X--X",
    {"X": "XFX--XFX"},
    lambda t, d: standard_rules(t, 45, (0.5, 1)),
    lambda d: sqrt(2) * (2 ** d - 1),
    7)

mango = register_fractal(
    "Mango",
    "0_Y---Y",
    {"X": "F-FF-F--[--X]F-FF-F--F-FF-F--",
     "Y": "f-F+X+F-fY"},
    lambda t, d: standard_rules(t, 60, (0.5, 0.5), additions=
        # black magic
        {"_": lambda: nodraw(t.fjump(-1.5 * d))}),
    lambda d: sqrt(3) * (3 * d - 2),
    22)

board = register_fractal(
    "Board",
    "F+F+F+F",
    {"F": "FF+F+F+F+FF"},
    lambda t, d: standard_rules(t),
    lambda d: 3 ** d,
    5)

square_sierpinski = register_fractal(
    "Square Sierpinski",
    "0_F+XF+F+XF",
    {"X": "XF-F+F-XF+F+XF-F+F-X"},
    lambda t, d: standard_rules(t, 90, (0.5, 0), additions=
        {"_": lambda: nodraw(t.fjump(-0.5))}),
    lambda d: 4 * (2 ** d) - 3,
    6)

# https://jsxgraph.uni-bayreuth.de/wiki/index.php/Penrose_tiling
penrose = register_fractal(
    "Penrose Tiling",
    "0[Y]++[Y]++[Y]++[Y]++[Y]",
    {"X" : "VF++WF----YF[-VF----XF]++",
     "Y" : "+VF--WF[---XF--YF]+",
     "V" : "-XF++YF[+++VF++WF]-",
     "W" : "--VF++++XF[+WF++++YF]--YF",
     "F" : "",
     "+" : "+",
     "-" : "-",
     "[" : "[",
     "]" : "]"},
    lambda t, d: standard_rules(t, 36, (0.5, 0.5), additions=
        {"V": nodraw, "W": nodraw}),
    lambda d: 2.3 * (0.5 * (1 + sqrt(5))) ** d,
    7)

hexagonal_gosper = register_fractal(
    "Hexagonal Gosper",
    "0[FXF]--[FXF]--[FXF]",
    {"X": "X+YF++YF-FX--FXFX-YF+",
     "Y": "-FX+YFYF++YF+FX--FX-Y"},
    lambda t, d: standard_rules(t, 60, (0.5, 0.5)),
    # TODO ???
    lambda d: 1 + 1.5 * 3 ** d,
    4)

quadratic_gosper = register_fractal(
    "Quadratic Gosper",
    "0[YF]-[YF]-[YF]-[YF]",
    {"X": "XFX-YF-YF+FX+FX-YF-YFFX+YF+FXFXYF-FX+YF+FXFX+YF-FXYF-YF-FX+FX+YFYF-",
     "Y": "+FXFX-YF-YF+FX+FXYF+FX-YFYF-FX-YF+FXYFYF-FX-YFFX+FX+YF-YF-FX+FX+YFY",
     },
    lambda t, d: standard_rules(t, 90, (0.5, 0.5)),
    # TODO; this scales wrong
    lambda d: 2 * 5 ** d,
    3)

bourke_triangle = register_fractal(
    "Bourke Triangle",
    "0[G]+[G]+[G]",
    {"F": "F-F+F",
     "G": "F+F+F"},
    lambda t, d: standard_rules(t, 120, (0.5, 0.5)),
    lambda d: 2 * 3 ** (d / 2.0),
    8)

bourke_bush_1 = register_fractal(
    "Bourke's first Bush",
    "0Y",
    {"X": "X[-FFF][+FFF]FX",
     "Y": "YFX[+Y][-Y]"},
    lambda t, d: standard_rules(t, 25.7, (0.5, 0), 90),
    lambda d: 2 * 2 ** d,
    7)

bourke_bush_2 = register_fractal(
    "Bourke's second Bush",
    "0F",
    {"F": "FF+[+F-F-F]-[-F+F+F]"},
    lambda t, d: standard_rules(t, 22.5, (0.5, 0), 90),
    lambda d: 4 * 2 ** d,
    6)

bourke_bush_3 = register_fractal(
    "Bourke's third Bush",
    "0F",
    {"F": "F[+FF][-FF]F[-F][+F]F"},
    lambda t, d: standard_rules(t, 35, (0.5, 0), 90),
    lambda d: 3 ** d,
    5)

saupe_bush = register_fractal(
    "Saupe's Bush",
    "0VZFFF",
    {"V": "[+++W][---W]YV",
     "W": "+X[-W]Z",
     "X": "-W[+X]Z",
     "Y": "YZ",
     "Z": "[-FFF][+FFF]F"},
    lambda t, d: standard_rules(t, 20, (0.5, 0.2), 90, additions=
        {"Z": nodraw, "V": nodraw, "W": nodraw}),
    # TODO: i am truly lost
    lambda d: 2.5 * 3 * d,
    13)

bourke_stick = register_fractal(
    "Bourke Stick",
    "0X",
    {"F": "FF",
     "X": "F[+X]F[-X]+X"},
    lambda t, d: standard_rules(t, 20, (0.5, 0), 90),
    lambda d: 2.3 * 2 ** d,
    9)

bourke_weed = register_fractal(
    "Bourke Weed",
    "0F",
    {"F": "FF-[XY]+[XY]",
     "X": "+FY",
     "Y": "-FX"},
    lambda t, d: standard_rules(t, 22.5, (0.5, 0), 90),
    lambda d: 2.3 * 2 ** d,
    8)

koch_island_1 = register_fractal(
    "Koch Island 1",
    "0F+F+F+F",
    {"F": "F+F-F-FFF+F+F-F"},
    lambda t, d: standard_rules(t, 90, (0.1, 0.57), 15),
    # TODO: total bodge here
    lambda d: 2 * 4 ** d,
    5)

koch_island_2 = register_fractal(
    "Koch Island 2",
    "0F+F+F+F",
    {"F": "F-FF+FF+F+F-F-FF+F+F-F-FF-FF+F"},
    lambda t, d: standard_rules(t, 90, (0.15, 0.37), -25),
    # TODO: this is even worse
    lambda d: 1.2 * 7 ** d,
    3)

koch_island_3 = register_fractal(
    "Koch Island 3",
    "0X+X+X+X+X+X+X+X",
    {"X": "X+YF++YF-FX--FXFX-YF+X",
     "Y": "-FX+YFYF++YF+FX--FX-YF"},
    lambda t, d: standard_rules(t, 45, (0.05, 0.5), -150),
    # TODO: aaaaaaaaaaaaaaaaaaaa
    lambda d: 0.6 * 7 ** d,
    4)

koch_island_4 = register_fractal(
    "Minkowski Island/Sausage",
    "0F+F+F+F",
    {"F": "F+F-F-FF+F+F-F"},
    lambda t, d: standard_rules(t, 90, (0.07, 0.63), -60),
    # TODO y u c k
    lambda d: 0.17 * 7 ** d,
    4)

pentaplexity = register_fractal(
    "Pentaplexity",
    "0F++F++F++F++F",
    {"F": "F++F++F|F-F++F"},
    lambda t, d: standard_rules(t, 36, (0.2, 0)),
    # TODO: figure out actual geometry
    lambda d: 3 ** d,
    4)

bourke_rings = register_fractal(
    "Bourke Rings",
    "0F+F+F+F",
    {"F": "FF+F+F+F+F+F-F"},
    lambda t, d: standard_rules(t, 90, (0.03, 0.52), -140),
    # TODO TODO TODO
    lambda d: 2 * 3 ** d,
    5)

bourke_2 = register_fractal(
    "Bourke 2",
    "0F+F+F+F",
    {"F": "FF+F-F+F+FF"},
    # TODO
    lambda t, d: standard_rules(t, 90, (0.3, 0.3)),
    lambda d: 5 + d + 0.7 * 3 ** d,
    4)

if __name__ == "__main__":
    for i in range(10):
        print("{:2}: {}".format(i, fibo_dim(i)))
    for ind, frac in enumerate(fractal_registry):
        print("{:2}: {}".format(ind, frac))
