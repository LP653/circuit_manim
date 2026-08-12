# Circuit Manim

## Outline

* [Intro](#introduction-and-opening-remarks)
* [Using this Library](#using-this-library)
* [Component specifications](#component-specifications)
* [Conclusions](#conclusions-and-work-to-do)

## Introduction and Opening Remarks

This is essentially extension of ManimCE for electronics circuits, including various components, limited auto-wiring, and plenty of animation possibilities.

You can see an example of how to use `circuit_manim` in the [`example.py`](./example.py) file. The next section will go over it.

Currently, you must download this repository to a folder (I called mine `circuit_manim`); then the library can be imported from a new python file within `circuit_manim`'s parent directory. And you would run it in any way a manim python file can be rendered (i.e. command line, [manimSV extension](https://marketplace.visualstudio.com/items?itemName=Rickaym.manim-sideview), etc.)

```
├── example.py
└── circuit_manim
    └── __init__.py
```

__**Please note**__:

This library was created with Manim v0.20.1, I suspect Manim v0.21.0 should still work with it but I have yet to test it.

## Using this Library

You'll start by intantiating a [`Circuit`]() mobject: `circ = Circuit()`

Each circuit component is derived from the parent [`Component`]() class. You can then assign instantiated components to variables:

```
op = Opamp(color=YELLOW)
feedback_resistor = Resistor(center=UP*2+LEFT*2, color=YELLOW).rotate(PI)
ground = Ground(center=RIGHT*2+DOWN*2, color=YELLOW)
```

Each component can be connected using the [`Wire`]() class. The `Wire`s connect to the `Component`s via [`Connections`](). You can connect components via `Wire` variables:

```
wire1 = Wire(
            op.get_conn_a().get_center(),
            feedback_resistor.get_conn_a().get_center(),
            color=YELLOW
        )
wire2 = Wire(
            op.get_conn_c().get_center(),
            feedback_resistor.get_conn_b().get_center(),
            color=YELLOW
        )
wire3 = Wire(
            op.get_conn_b().get_center(),
            ground.get_conn().get_center(),
            color=YELLOW
        )
```

Then each `Component` and `Wire` is added to the `Circuit` and you can do what you want to the `Circuit` as a whole or individual `Component`s:

```
circ.add(
    op,
    feedback_resistor,
    ground,
    wire1,
    wire2,
    wire3
)

self.play(Create(circ))
self.wait()

self.play(circ.animate.set_color(RED_B))

self.play(circ.animate.shift(RIGHT))
self.play(circ.animate.shift(LEFT))

self.play(circ.animate.set_color(YELLOW))
self.wait()

self.play(Uncreate(circ))
```

![Example Circuit Video](./media/video/example_video.gif)

## Component specifications

Each `Component` has at least one `Connection`; `Component`s into categories depending on the number of `Connection`s:

* `Component1`: A component with only one connection
    * Ground Connection
    * Power Connection
* `Component2`: A component with two connections
    * Resistor
    * Capacitor
    * 2-Way Switch
    * LED
    * Voltage Source
    * Current Source
    * Battery
* `Component3`: A component with three connections
    * Opamp
    * Potentiometer
    * 3-Way Switch

You can go into a deeper dive into how you can use these components in the [`circuit_manim_journal.ipynb`](./circuit_manim_journal.ipynb) file.

## Conclusions and Further Work

Originally, I was creating a video using Manim animation to construct a circuit, but it quickly ballooned and was difficult to keep track of different components and which ones were copies. I realized I needed a library to source my components from.

There is a long list of tasks that need done for this library to be very versatile. I am working on them but I wanted to share my progress thus far. This is my first attempt to create a Python library so any advice or suggestions are welcome.

* Components
    * Make initial rotation work; currently must be rotated post-instantiation
    * Use bezier curves to draw components rather than Lines and Arcs, will make it far more efficient
* Wires
    * Add updaters so the wires always keep at their connections, even when they move
        * This makes animating components and their wires far easier than it currently is
    * Create alpha or "duty cycle" variable for wire
        * This would mean that if there is a bend in the wire, we could assign where the bend is proportionally
    * Make wire "sense" if it intersects a component and go around
        * I have heard of the PIP (Point-In-Polygon) algorithm, that should apply here
* Circuits
    * Create circuit `Inputs` and `Outputs` so `Circuit`s can be chained together.