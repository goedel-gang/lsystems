"""
The drawing layer of abstraction

It uses layered lazy generators so it is very memory-efficient - effectively
using only a call-stack of the size of the number of iterations.
"""

from math import sin, cos, pi, radians

from fractals import substitute

class ProcessingTurtle(object):
    """
    A little turtle class to execute the actual drawing of an L-system. Mostly
    pretty self-explanatory. No error checking done.

    This is a slightly unconventional kind of turtle - see the documentation for
    LSystemFractal.
    """
    def __init__(self, graphics, x=0, y=0, heading=0, pendown=True,
            input_scale=1.0, output_scale=1.0):
        self.graphics = graphics
        self.x = x
        self.y = y
        self.heading = heading
        self._pendown = pendown
        self.input_scale = input_scale
        self.output_scale = output_scale
        self.times_moved = 0
        self.state_stack = []

    def output_rescale(self, scale):
        """
        Set the scale factor for drawing graphics. This has to be handled by the
        turtle, rather than by using pushMatrix() and friends, because we only
        want to mess with coordinates, not stroke widths and such.
        """
        self.output_scale *= scale

    def input_rescale(self, scale):
        """
        Set the scale factor for input. This is separate from the output because
        the fractals are all agnostic to width.
        """
        self.input_scale *= scale

    def setpos(self, nx, ny):
        if self._pendown:
            self.graphics.line(self.x * self.output_scale,
                               self.y * self.output_scale,
                               nx * self.output_scale,
                               ny * self.output_scale)
        self.jump(nx, ny)

    def jump(self, nx, ny):
        self.x = nx
        self.y = ny

    def setheading_degrees(self, heading):
        self.heading = radians(heading)

    def forward(self, steps):
        self.setpos(self.x + 1.0 * steps / self.input_scale * cos(self.heading),
                    self.y + 1.0 * steps / self.input_scale * sin(self.heading))
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

def draw_fractal(graphics, fractal, w, depth):
    """
    Draw an LSystemFractal, by repeatedly applying its own rewrite rules, in a
    stack of lazy generators, and then using its drawing rules.
    """
    t = ProcessingTurtle(graphics)
    path = fractal.start
    expected_steps = fractal.steps_func(depth)
    draw_rules = fractal.draw_rules(t, depth)
    t.input_rescale(fractal.size_func(depth))
    t.output_rescale(w)
    for _ in xrange(depth):
        path = substitute(path, fractal.rules)
    for symbol in path:
        graphics.stroke(255.0 * t.times_moved / expected_steps, 255, 255)
        if draw_rules[symbol]():
            yield
