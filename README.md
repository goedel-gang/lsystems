# lsystems

A general approach to L-systems in Python processing, using layered generators,
with a couple implemented. Due to the use of generators they also generate
gradually, giving a nice "drawing" effect, rather than blocking for several
frames. Basically the beauty of it is that having written all the "library"
code, I can define fractals as simply as

```Python
sierpinski = LSystemFractal(
    "Sierpinski's Gasket",
    "F+G+G",
    lambda d: 2 ** d,
    {"F": "F+G-F-G+F",
     "G": "GG"},
    lambda t, d: standard_rules(t, d, 120),
    10)
```

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

![screenshot](https://github.com/goedel-gang/lsystems/blob/master/screenshots/sierpinskis_gasket.png)
![screenshot](https://github.com/goedel-gang/lsystems/blob/master/screenshots/the_dragon_curve.png)
![screenshot](https://github.com/goedel-gang/lsystems/blob/master/screenshots/a_lindenmayer_fern.png)
![screenshot](https://github.com/goedel-gang/lsystems/blob/master/screenshots/the_levy_c_curve.png)
![screenshot](https://github.com/goedel-gang/lsystems/blob/master/screenshots/hilberts_spacefilling_curve.png)
![screenshot](https://github.com/goedel-gang/lsystems/blob/master/screenshots/sierpinskis_gasket_hexagonal_variant.png)
![screenshot](https://github.com/goedel-gang/lsystems/blob/master/screenshots/koch_snowflake.png)
![screenshot](https://github.com/goedel-gang/lsystems/blob/master/screenshots/square_koch_curve.png)
![screenshot](https://github.com/goedel-gang/lsystems/blob/master/screenshots/binary_tree.png)
