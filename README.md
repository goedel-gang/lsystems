# lsystems

A general approach to L-systems in Python processing, using layered generators,
with a couple implemented. Due to the use of generators they also generate
gradually, giving a nice "drawing" effect, rather than blocking for several
frames. Basically the beauty of it is that having written all the "library"
code, I can define fractals as simply as

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

As you can see, it's currently also very easy to read.

Even though I say so myself, the colouring effects are really cool. Not only are
they all rainbow coloured, but the rainbow is extrapolated from the reproduction
rules of each L-system automatically. Basically, when you're only interested in
symbol count, you can use a linear transition matrix and exponentiation by
squaring to calculate the count of each symbol at the `n`th iteration in
`log(n)` time. This is a totally unnecessary but nevertheless awesome
optimisation to be able to make.

The version used to generate [this video](https://youtu.be/kf3hgNMjzX4) is at
the [video tag](https://github.com/goedel-gang/lsystems/tree/video).

Here are some screenshots:

![screenshot](https://github.com/goedel-gang/lsystems/blob/master/screenshots/sierpinski.png)
![screenshot](https://github.com/goedel-gang/lsystems/blob/master/screenshots/dragon.png)
![screenshot](https://github.com/goedel-gang/lsystems/blob/master/screenshots/fern.png)
![screenshot](https://github.com/goedel-gang/lsystems/blob/master/screenshots/levyC.png)
![screenshot](https://github.com/goedel-gang/lsystems/blob/master/screenshots/hilbert.png)
![screenshot](https://github.com/goedel-gang/lsystems/blob/master/screenshots/sierp_hex.png)
![screenshot](https://github.com/goedel-gang/lsystems/blob/master/screenshots/koch_snowflake.png)
![screenshot](https://github.com/goedel-gang/lsystems/blob/master/screenshots/koch_square.png)
![screenshot](https://github.com/goedel-gang/lsystems/blob/master/screenshots/binary_tree.png)
