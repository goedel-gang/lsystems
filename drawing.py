"""
The drawing layer of abstraction for Processing.
"""

from math import sin, cos, pi, radians

class ProcessingTurtle(object):
    """
    A little turtle class to execute the actual drawing of an L-system. Mostly
    pretty self-explanatory. No error checking done.

    This is a slightly unconventional kind of turtle - see the documentation for
    LSystemFractal.
    """
    def __init__(self, graphics):
        self.graphics = graphics
        self.x = 0
        self.y = 0
        self.heading = 0
        self._pendown = True
        self.input_scale = 1.0
        self.output_scale = 1.0
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
            self.times_moved += 1
        self.jump(nx, ny)

    def jump(self, nx, ny):
        self.x = nx
        self.y = ny

    def setheading_degrees(self, heading):
        self.heading = radians(heading)

    def forward(self, steps):
        self.setpos(self.x + 1.0 * steps / self.input_scale * cos(self.heading),
                    self.y + 1.0 * steps / self.input_scale * sin(self.heading))

    def fjump(self, steps):
        self.jump(self.x + 1.0 * steps / self.input_scale * cos(self.heading),
                  self.y + 1.0 * steps / self.input_scale * sin(self.heading))

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

    def sethue(self, h):
        self.graphics.stroke(h, 255, 255)
