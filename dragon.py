from hilbert import gen_l, directions

class DrgA:
    F = 0
    L = 1
    R = 2
    X = 3
    Y = 4

RULES = {DrgA.X: [DrgA.X,
                  DrgA.R,
                  DrgA.Y,
                  DrgA.F,
                  DrgA.R],
         DrgA.Y: [DrgA.L,
                  DrgA.F,
                  DrgA.X,
                  DrgA.L,
                  DrgA.Y]}

def draw_drg(depth=10, width=1000, x=0.5, y=0.5, direction=0):
    tlines = 0
    exlines = float(1 << (depth - 1))
    twidth = sqrt(1 << depth) * 2
    x *= twidth
    y *= twidth
    strokeWeight(float(width) / twidth / 5.0)
    for action in gen_l(depth, pattern=[DrgA.F, DrgA.X], rules=RULES):
        if action == DrgA.F:
            tlines += 1
            stroke(tlines * 255 / exlines, 255, 255)
            cx, cy = directions[direction % 4]
            nx = x + cx
            ny = y + cy
            line(x * width / twidth, y * width / twidth, nx * width / twidth, ny * width / twidth)
            x, y = nx, ny
            yield
        elif action == DrgA.L:
            direction += 1
        elif action == DrgA.R:
            direction -= 1
    print("done")