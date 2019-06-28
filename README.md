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

![screenshot](https://github.com/goedel-gang/lsystems/blob/master/screenshots/screenshots/00_sierpinskis_gasket.png)
![screenshot](https://github.com/goedel-gang/lsystems/blob/master/screenshots/screenshots/01_the_dragon_curve.png)
![screenshot](https://github.com/goedel-gang/lsystems/blob/master/screenshots/screenshots/02_a_lindenmayer_fern.png)
![screenshot](https://github.com/goedel-gang/lsystems/blob/master/screenshots/screenshots/03_the_levy_c_curve.png)
![screenshot](https://github.com/goedel-gang/lsystems/blob/master/screenshots/screenshots/04_hilberts_spacefilling_curve.png)
![screenshot](https://github.com/goedel-gang/lsystems/blob/master/screenshots/screenshots/05_sierpinskis_gasket_hexagonal_variant.png)
![screenshot](https://github.com/goedel-gang/lsystems/blob/master/screenshots/screenshots/06_koch_snowflake.png)
![screenshot](https://github.com/goedel-gang/lsystems/blob/master/screenshots/screenshots/07_square_koch_curve.png)
![screenshot](https://github.com/goedel-gang/lsystems/blob/master/screenshots/screenshots/08_binary_tree.png)
![screenshot](https://github.com/goedel-gang/lsystems/blob/master/screenshots/screenshots/09_crystal.png)
![screenshot](https://github.com/goedel-gang/lsystems/blob/master/screenshots/screenshots/10_peano_curve.png)
![screenshot](https://github.com/goedel-gang/lsystems/blob/master/screenshots/screenshots/11_krishna_anklets.png)
![screenshot](https://github.com/goedel-gang/lsystems/blob/master/screenshots/screenshots/12_mango.png)
![screenshot](https://github.com/goedel-gang/lsystems/blob/master/screenshots/screenshots/13_board.png)
![screenshot](https://github.com/goedel-gang/lsystems/blob/master/screenshots/screenshots/14_square_sierpinski.png)
![screenshot](https://github.com/goedel-gang/lsystems/blob/master/screenshots/screenshots/15_kolam.png)
![screenshot](https://github.com/goedel-gang/lsystems/blob/master/screenshots/screenshots/16_bourkes_first_bush.png)
![screenshot](https://github.com/goedel-gang/lsystems/blob/master/screenshots/screenshots/17_bourkes_second_bush.png)
![screenshot](https://github.com/goedel-gang/lsystems/blob/master/screenshots/screenshots/18_bourkes_third_bush.png)
![screenshot](https://github.com/goedel-gang/lsystems/blob/master/screenshots/screenshots/19_saupes_bush.png)
![screenshot](https://github.com/goedel-gang/lsystems/blob/master/screenshots/screenshots/20_bourke_stick.png)
![screenshot](https://github.com/goedel-gang/lsystems/blob/master/screenshots/screenshots/21_bourke_weed.png)
![screenshot](https://github.com/goedel-gang/lsystems/blob/master/screenshots/screenshots/22_bourke_triangle.png)
![screenshot](https://github.com/goedel-gang/lsystems/blob/master/screenshots/screenshots/23_koch_island_1.png)
![screenshot](https://github.com/goedel-gang/lsystems/blob/master/screenshots/screenshots/24_koch_island_2.png)
![screenshot](https://github.com/goedel-gang/lsystems/blob/master/screenshots/screenshots/25_koch_island_3.png)
![screenshot](https://github.com/goedel-gang/lsystems/blob/master/screenshots/screenshots/26_koch_island_4.png)
![screenshot](https://github.com/goedel-gang/lsystems/blob/master/screenshots/screenshots/27_pentaplexity.png)
![screenshot](https://github.com/goedel-gang/lsystems/blob/master/screenshots/screenshots/28_bourke_rings.png)
![screenshot](https://github.com/goedel-gang/lsystems/blob/master/screenshots/screenshots/29_bourke_2.png)
![screenshot](https://github.com/goedel-gang/lsystems/blob/master/screenshots/screenshots/30_hexagonal_gosper.png)
![screenshot](https://github.com/goedel-gang/lsystems/blob/master/screenshots/screenshots/31_quadratic_gosper.png)
