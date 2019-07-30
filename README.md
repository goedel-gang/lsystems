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
    {"F": "F+G-F-G+F",
     "G": "GG"},
    lambda t, d: standard_rules(t, 120),
    lambda d: 2 ** d,
    9)
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

![screenshot](https://github.com/goedel-gang/lsystems/blob/master/screenshots/00_sierpinskis_gasket.png)
![screenshot](https://github.com/goedel-gang/lsystems/blob/master/screenshots/01_the_dragon_curve.png)
![screenshot](https://github.com/goedel-gang/lsystems/blob/master/screenshots/02_a_lindenmayer_fern.png)
![screenshot](https://github.com/goedel-gang/lsystems/blob/master/screenshots/03_the_levy_c_curve.png)
![screenshot](https://github.com/goedel-gang/lsystems/blob/master/screenshots/04_hilberts_spacefilling_curve.png)
![screenshot](https://github.com/goedel-gang/lsystems/blob/master/screenshots/05_sierpinskis_gasket_hexagonal_variant.png)
![screenshot](https://github.com/goedel-gang/lsystems/blob/master/screenshots/06_koch_snowflake.png)
![screenshot](https://github.com/goedel-gang/lsystems/blob/master/screenshots/07_square_koch_curve.png)
![screenshot](https://github.com/goedel-gang/lsystems/blob/master/screenshots/08_binary_tree.png)
![screenshot](https://github.com/goedel-gang/lsystems/blob/master/screenshots/09_fibonacci_word_fractal.png)
![screenshot](https://github.com/goedel-gang/lsystems/blob/master/screenshots/10_crystal.png)
![screenshot](https://github.com/goedel-gang/lsystems/blob/master/screenshots/11_peano_curve.png)
![screenshot](https://github.com/goedel-gang/lsystems/blob/master/screenshots/12_cantor_set.png)
![screenshot](https://github.com/goedel-gang/lsystems/blob/master/screenshots/13_sierpinski_star.png)
![screenshot](https://github.com/goedel-gang/lsystems/blob/master/screenshots/14_sierpinskis_carpet.png)
![screenshot](https://github.com/goedel-gang/lsystems/blob/master/screenshots/15_krishna_anklets.png)
![screenshot](https://github.com/goedel-gang/lsystems/blob/master/screenshots/16_mango.png)
![screenshot](https://github.com/goedel-gang/lsystems/blob/master/screenshots/17_board.png)
![screenshot](https://github.com/goedel-gang/lsystems/blob/master/screenshots/18_square_sierpinski.png)
![screenshot](https://github.com/goedel-gang/lsystems/blob/master/screenshots/19_penrose_tiling.png)
![screenshot](https://github.com/goedel-gang/lsystems/blob/master/screenshots/20_hexagonal_gosper.png)
![screenshot](https://github.com/goedel-gang/lsystems/blob/master/screenshots/21_quadratic_gosper.png)
![screenshot](https://github.com/goedel-gang/lsystems/blob/master/screenshots/22_bourke_triangle.png)
![screenshot](https://github.com/goedel-gang/lsystems/blob/master/screenshots/23_bourkes_first_bush.png)
![screenshot](https://github.com/goedel-gang/lsystems/blob/master/screenshots/24_bourkes_second_bush.png)
![screenshot](https://github.com/goedel-gang/lsystems/blob/master/screenshots/25_bourkes_third_bush.png)
![screenshot](https://github.com/goedel-gang/lsystems/blob/master/screenshots/26_saupes_bush.png)
![screenshot](https://github.com/goedel-gang/lsystems/blob/master/screenshots/27_bourke_stick.png)
![screenshot](https://github.com/goedel-gang/lsystems/blob/master/screenshots/28_bourke_weed.png)
![screenshot](https://github.com/goedel-gang/lsystems/blob/master/screenshots/29_koch_island_1.png)
![screenshot](https://github.com/goedel-gang/lsystems/blob/master/screenshots/30_koch_island_2.png)
![screenshot](https://github.com/goedel-gang/lsystems/blob/master/screenshots/31_koch_island_3.png)
![screenshot](https://github.com/goedel-gang/lsystems/blob/master/screenshots/32_minkowski_islandsausage.png)
![screenshot](https://github.com/goedel-gang/lsystems/blob/master/screenshots/33_pentaplexity.png)
![screenshot](https://github.com/goedel-gang/lsystems/blob/master/screenshots/34_bourke_rings.png)
![screenshot](https://github.com/goedel-gang/lsystems/blob/master/screenshots/35_bourke_2.png)
