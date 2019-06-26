"""
Abstract classes and instances to draw L-system fractals.
See [1], and the various other wikipedia pages on fractals.

[1]: https://en.wikipedia.org/wiki/L-system
"""

from collections import namedtuple, Counter
from itertools import chain, starmap

from matrix import Matrix

LSystemFractalTuple = namedtuple(
        "LSystemFractalTuple",
        "name start size_func rules draw_rules iterations")

FRACTAL_REGISTRY = []

class DummyTurtle(object):
    """
    Dummy turtle class, used to probe whether or not certain symbols correspond
    to steps. See the LSystemFractal class.

    Written in the most hacky, lazy way possible
    """
    def __init__(self):
        for i in """forward turn setheading_degrees save_state restore_state
                turn_degrees jump""".split():
            self.__dict__[i] = lambda *args: None

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
        self.generate_transition_matrix()

    def generate_transition_matrix(self):
        """
        Generate the transition matrix for a single rewrite of an L-system. This
        can then be used to calculate the number of steps taken, in logarithmic
        time (in the number of iterations). This is because can use
        exponentiation by squaring on the transition matrix. This is an entirely
        unnecessary optimisation, but it's a fun one to implement.

        It's sometimes possible to actually solve the recurrence to give a
        totally closed form for the number of times each symbol occurs. This
        requires you to diagonalise the matrix though, which is generally messy
        as
        1) It doesn't leave you with integers (or necessarily rationals (or
           necessarily reals))
        2) This isn't solvable by an algorithm for an n by n matrix, as if you
           could solve arbitrary characteristic equations you could solve
           arbitrary polynomials.
        3) It isn't even asymptotically more optimal. In both cases you will
           need to perform exponentiation, although the exponentiation of a
           diagonal matrix obviously has the potential to be a little faster.
        """
        # TODO: probably we could do a little static analysis here in order to
        #       not consider symbols with no impact, although that's a little
        #       graph theoretic.
        self.symbols = list(set(chain(self.start,
                                      *starmap(chain, self.rules.items()))))
        # I don't even know if Python 2 has dictionary comprehensions, and I
        # don't really want to find out
        rule_counter = dict((symbol, Counter(self.rules.get(symbol, symbol)))
                for symbol in self.symbols)
        self.transition_matrix = Matrix(
                [[rule_counter[symbol_to][symbol_from]
                    for symbol_to in self.symbols]
                    for symbol_from in self.symbols])
        t = DummyTurtle()
        initial_counter = Counter(self.start)
        self.initial_vector = Matrix([[initial_counter[symbol]] for symbol in
                self.symbols])
        draw_rules = self.draw_rules(t, 1)
        self.stepping_symbols = set(symbol for symbol in self.symbols if
                draw_rules[symbol]())

    def project_steps(self, iterations):
        """
        Project the number of steps needed for a certain number of iterations.
        In previous iterations, this function was crafted by hand for each
        fractal, but then I had to implement a matrix class to efficiently
        calculate this for the fern function, so I decided to automated the
        whole thing, and take out a point of failure.
        """
        return sum(i[0] for i, sym in
                zip(self.transition_matrix ** iterations * self.initial_vector,
                    self.symbols)
                if sym in self.stepping_symbols)

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
    "0[FX]-[FX]-[FX]-FX",
    lambda d: 2 * 2 ** (d / 2.0),
    {"X": "X+YF+",
     "Y": "-FX-Y"},
    lambda t, d: {"F": lambda: draw(t.forward(1)),
                  "-": lambda: nodraw(t.turn_degrees(+90)),
                  "+": lambda: nodraw(t.turn_degrees(-90)),
                  "0": lambda: nodraw(t.jump(0.5, 0.5),
                                      t.turn_degrees(45 * (d % 2 + 1))),
                  "[": lambda: nodraw(t.save_state()),
                  "]": lambda: nodraw(t.restore_state()),
                  "X": nodraw,
                  "Y": nodraw},
    15)

fern = LSystemFractal(
    "A Lindenmayer Fern",
    "0X",
    # This is basically just noting that it doubles its dimension along each
    # branch, and that it has some limit it approaches at its asymptote, found
    # by trial and error. It would be nice to find this more exactly in terms of
    # trigonometric functions of 25 degrees. (TODO)
    lambda d: 2.718281828 * 2 ** d,
    {"X": "F+[[X]-X]-F[-FX]+X",
     "F": "FF"},
    lambda t, d: {"F": lambda: draw(t.forward(1)),
                  "-": lambda: nodraw(t.turn_degrees(+25)),
                  "+": lambda: nodraw(t.turn_degrees(-25)),
                  "X": nodraw,
                  "[": lambda: nodraw(t.save_state()),
                  "]": lambda: nodraw(t.restore_state()),
                  "0": lambda: nodraw(t.jump(0.5, 0),
                                      t.setheading_degrees(90))},
    8)

levy_c = LSystemFractal(
    "The Levy C Curve",
    "0F",
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
    "0F-F-F-F",
    lambda d: 2 * 3 ** d,
    {"F": "F+F-F-F+F"},
    lambda t, d: {"F": lambda: draw(t.forward(1)),
                  "-": lambda: nodraw(t.turn_degrees(-90)),
                  "+": lambda: nodraw(t.turn_degrees(+90)),
                  "0": lambda: nodraw(t.jump(0.25, 0.75))},
    7)

# TODO: ParametrisedLSystemFractal
binary_tree = LSystemFractal(
    "Binary Tree",
    "_0",
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
