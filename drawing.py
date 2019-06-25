"""
The drawing layer of abstraction
"""

from math import sin, cos, pi

from fractals import substitute

class ProcessingTurtle:
    """
    A little turtle class to execute the actual drawing of an L-system. Mostly
    pretty self-explanatory. No error checking done.
    """
    def __init__(self, graphics, x=0, y=0, heading=0, pendown=True):
        self.graphics = graphics
        self.x = x
        self.y = y
        self.heading = heading
        self._pendown = True
        self.times_moved = 0
        self.state_stack = []

    def setpos(self, nx, ny):
        if self._pendown:
            self.graphics.line(self.x, self.y, nx, ny)
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

def draw_fractal(graphics, fractal, w):
    """
    Draw an LSystemFractal, by repeatedly applying its own rewrite rules, in a
    stack of lazy generators, and then using its drawing rules.
    """
    t = ProcessingTurtle(graphics, 0, 0, 0)
    graphics.background(0)
    path = fractal.start
    expected_steps = fractal.size_func(fractal.iterations)
    draw_rules = fractal.draw_rules(t, fractal.iterations, w)
    for _ in xrange(fractal.iterations):
        path = substitute(path, fractal.rules)
    for symbol in path:
        graphics.stroke(255.0 * t.times_moved / expected_steps, 255, 255)
        draw_rules[symbol]()
        yield
