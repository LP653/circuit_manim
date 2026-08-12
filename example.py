from circuit_manim import *

class example_video(Scene):
    def construct(self):
        circ = Circuit()
        
        op = Opamp(color=YELLOW)
        feedback_resistor = Resistor(center=UP*2+LEFT*2, color=YELLOW).rotate(PI)

        ground = Ground(center=RIGHT*2+DOWN*2, color=YELLOW)

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
