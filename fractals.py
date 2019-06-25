"""
Abstract classes and instances to draw L-system fractals.
See [1], and the various other wikipedia pages on fractals.

[1]: https://en.wikipedia.org/wiki/L-system
"""

from collections import namedtuple
from itertools import chain

from matrix import Matrix

LSystemFractalTuple = namedtuple(
        "LSystemFractalTuple",
        "name start steps_func size_func rules draw_rules iterations")

FRACTAL_REGISTRY = []

class LSystemFractal(LSystemFractalTuple):
    """
    Class representing an L-system fractal. This is a thin wrapper around the
    namedtuple that stores the fields, but additionally, this automatically
    registers any new fractals in the FRACTAL_REGISTRY. Fractals should expect
    to be drawn in a square box with side length 1 and one corner at (0, 0).
    The initial drawing state will be a turtle at (0, 0) facing in the direction
    of the x-axis. This can be modified by prefixing the initial string with a
    dummy "0" symbol, and using that symbol to perform setup. To execute
    multiple lines of setup in a single line, you can use a tuple.
    The turtle's forward() method should be scaled so that if you use forward(1)
    for each accounted drawing step, it will fit in the square. The setpos() and
    jump() methods take inputs in [0, 1]^2 though.
    Properties:
    start:      initial string
    size_func:  A function taking an integer (the number of iterations) and
                returning the expected largest dimension of the fractal (height
                or width), given in unit drawing steps.
    steps_func: A function taking an integer (the number of iterations) and
                returning the expected number of steps to take. This is needed
                for colouring.
    rules:      The rules for rewriting at each iteration, as a mapping object.
    draw_rules: The action to take when drawing for each symbol of the alphabet,
                as a mapping again, this time mapping to nullary functions. This
                is a function of a turtle-like object, the depth of the fractal,
                and the width of the square it should be drawn in, so the
                fractal can make adjustments for itself and access drawing
                methods. If a rule returns a truthy value when called, that is
                taken to mean that it has constituted a step.
    iterations: The default number of iterations to perform.
    """
    def __init__(self, *args, **kwargs):
        FRACTAL_REGISTRY.append(self)
        super(LSystemFractalTuple, self).__init__(*args, **kwargs)

def substitute(sequence, rules):
    """
    Lazy generator that replaces a set of symbols in its iterable input as
    instructed. Very flexible/abstract - works so long as you have a correctly
    behaving lookup of "rules" for any symbols, which understand indexing, "in",
    "not in" and map to iterables of other symbols.
    """
    for symbol in sequence:
        if symbol not in rules:
            yield symbol
        else:
            for sym in rules[symbol]:
                yield sym

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

sierpinski = LSystemFractal(
    "Sierpinski's Gasket",
    "F-G-G",
    lambda d: 3 ** d * 3,
    lambda d: 2 ** d,
    {"F": "F-G+F+G-F",
     "G": "GG"},
    lambda t, d: {"F": lambda: draw(t.forward(1)),
                  "G": lambda: draw(t.forward(1)),
                  "-": lambda: nodraw(t.turn_degrees(+120)),
                  "+": lambda: nodraw(t.turn_degrees(-120))},
    10)

dragon = LSystemFractal(
    "The Dragon Curve",
    "0FX",
    lambda d: 2 ** d,
    # TODO: basically no idea about dragon dimensions, this is all guesswork.
    lambda d: 2 * 2 ** (d / 2.0),
    {"X": "X+YF+",
     "Y": "-FX-Y"},
    lambda t, d: {"F": lambda: draw(t.forward(1)),
                  "-": lambda: nodraw(t.turn_degrees(+90)),
                  "+": lambda: nodraw(t.turn_degrees(-90)),
                  "0": lambda: nodraw(t.turn_degrees(45 + 45 * d),
                                      t.jump(0.35, 0.25)),
                  "X": nodraw,
                  "Y": nodraw},
    16)

def fern_steps(depth):
    r"""
    Helper function to calculate the number of steps for a Lindenmayer fern.
    This should be logarithmic in the number of iterations, as it uses
    exponentiation by squaring on the transition matrix. This is an entirely
    unnecessary optimisation, but it's a fun one to implement.

    Letting the state after `n` iterations be encoded in some matrix
          / F_n \ <- number of 'F's in the string at the `n`th iteration
    M_n = |     |
          \ X_n / <- number of 'X's "
    so then
          / 0 \
    M_0 = |   |
          \ 1 /
    and the transition to M_{n + 1} is encoded by
    M_{n + 1} = T M_n, where
        / 3  2 \
    T = |      |
        \ 0  4 /
    So then
    M_n = T ^ n M_0, and we can extract the value of F_n.

    It's probably possible to actually solve this recurrence to give a totally
    closed form for F_n, but
    1) I'm not clever enough
    2) This would still involve powers, so would not be asymptotically more
       efficient
    TODO: this is fairly doable. Just diagonalise T, basically. Not sure if
          better done by hand or by program..

    Of course this whole function could be inlined but then I would have to
    sacrifice this beautiful docstring.
    """
    return (Matrix([[3, 2], [0, 4]]) ** depth * Matrix([[0], [1]])).array[0][0]

fern = LSystemFractal(
    "A Lindenmayer Fern",
    "0X",
    fern_steps,
    # TODO: better approach to this
    lambda d: 0.1 * 3 ** d,
    {"X": "F+[[X]-X]-F[-FX]+X",
     "F": "FF"},
    lambda t, d: {"F": lambda: draw(t.forward(1)),
                  "-": lambda: nodraw(t.turn_degrees(+25)),
                  "+": lambda: nodraw(t.turn_degrees(-25)),
                  "X": nodraw,
                  "[": t.save_state,
                  "]": t.restore_state,
                  "0": lambda: nodraw(t.jump(0.5, 0),
                                      t.setheading_degrees(90))},
    8)

levy_c = LSystemFractal(
    "The Levy C Curve",
    "0F",
    lambda d: 2 ** d,
    lambda d: 2 * 2 ** (d / 2.0),
    {"F": "+F--F+"},
    lambda t, d: {"F": lambda: draw(t.forward(1)),
                  "-": lambda: nodraw(t.turn_degrees(-45)),
                  "+": lambda: nodraw(t.turn_degrees(+45)),
                  "0": lambda: nodraw(t.jump(0.25, 0.25))},
    18)

hilbert = LSystemFractal(
    "Hilbert's Space-Filling Curve",
    "A",
    lambda d: 4 ** d,
    lambda d: 2 ** d,
    {"A": "-BF+AFA+FB-",
     "B": "+AF-BFB-FA+"},
    lambda t, d: {"F": lambda: draw(t.forward(1)),
                  "A": nodraw,
                  "B": nodraw,
                  "-": lambda: nodraw(t.turn_degrees(+90)),
                  "+": lambda: nodraw(t.turn_degrees(-90))},
    8)

sierp_hex = LSystemFractal(
    "Sierpinski's Gasket Hexagonal Variant",
    "A",
    lambda d: 3 ** d,
    lambda d: 2 ** d,
    {"A": "B-A-B",
     "B": "A+B+A"},
    lambda t, d: {"A": lambda: draw(t.forward(1)),
                  "B": lambda: draw(t.forward(1)),
                  "-": lambda: nodraw(t.turn_degrees(-60 * (-1) ** d)),
                  "+": lambda: nodraw(t.turn_degrees(60 * (-1) ** d))},
    8)

koch = LSystemFractal(
    "Koch Snowflake",
    "0F--F--F",
    lambda d: 3 * 4 ** d,
    lambda d: 2 * sqrt(3) / 3 * 3 ** d,
    {"F": "F+F--F+F"},
    lambda t, d: {"F": lambda: draw(t.forward(1)),
                  "-": lambda: nodraw(t.turn_degrees(60)),
                  "+": lambda: nodraw(t.turn_degrees(-60)),
                  "0": lambda: nodraw(
                      t.jump(0.5 * (1 - 3 / (2 * sqrt(3))), 0.25))},
    8)

koch_square = LSystemFractal(
    "Square Koch Curve",
    "0F--F",
    lambda d: 2 * 5 ** d,
    lambda d: 3 ** d,
    {"F": "F+F-F-F+F"},
    lambda t, d: {"F": lambda: draw(t.forward(1)),
                  "-": lambda: nodraw(t.turn_degrees(-90)),
                  "+": lambda: nodraw(t.turn_degrees(+90)),
                  "0": lambda: nodraw(t.jump(0, 0.5))},
    7)

# TODO: ParametrisedLSystemFractal
binary_tree = LSystemFractal(
    "Binary Tree",
    "_0",
    # see the Lindenmayer fern's documentation
    lambda d: sum(chain(*(Matrix([[2, 0], [1, 2]]) ** d
                        * Matrix([[1], [0]])).array)),
    # A messy, but not intrinsically hugely complicated pair of interlaced
    # geometric progressions
    # TODO: scale with depth, rather than assume infinity. Remember leaves are
    #       weird
    lambda d: 2 ** (d - 1) * 4 / 3 * (1 + 0.25 * sqrt(2)),
    {"1": "11",
     "0": "1[0]0"},
    lambda t, d: {"0": lambda: draw(t.forward(1)),
                  "1": lambda: draw(t.forward(1)),
                  "[": lambda: nodraw(t.save_state(),
                                      t.turn_degrees(45)),
                  "]": lambda: nodraw(t.restore_state(),
                                      t.turn_degrees(-45)),
                  "_": lambda: nodraw(t.jump(0.5, 0),
                                      t.setheading_degrees(90))},
    10)
