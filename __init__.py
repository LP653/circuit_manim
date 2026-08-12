import manim as mn
from manim import *
from manim.typing import Vector3D
from manim.typing import Vector3DLike
from manim.typing import Vector2D
from manim.typing import Vector2DLike
import numpy as np

'''

CircuitManim v0.1

Created by github.com/LP653

Based on ManimCE v0.?

GitHub link: ___

Update from journal

'''

class Component(VMobject):
    def __init__(
            self,
            center = ORIGIN,
            radius = 1.0,
            **kwargs
    ) -> None:
        self.center = center

        # TODO: Make calculation to find true radius of item...maybe have that be defined by the child class
        self.radius = radius

        super().__init__(**kwargs)

class Connection(Dot):
    def __init__(self, point=ORIGIN, radius=0.08, **kwargs):
        super().__init__(point, radius, **kwargs)


class Component1(Component):
    def __init__(
            self,
            center: Vector3D = ORIGIN,
            conn: Vector3D = 0.5*UP,
            initial_rot = 0.0,
            **kwargs
    ) -> None:
        self.mcenter = center
        self.conn = Connection(self.mcenter+conn, color=RED)
        
        super().__init__(**kwargs)
    
    def get_conn(self) -> Connection | Vector3D:
        return self.conn

    def get_center(self) -> Connection | Vector3D:
        return self.mcenter
    
    def rotate(self, theta: float, **kwargs):
        self.conn.rotate(theta, about_point=self.get_center())
        super().rotate(theta, **kwargs)
        return self

    def shift(self, *vectors: Vector3DLike, **kwargs):
        self.conn.shift(vectors)
        super().shift(vectors)
        return self
    
    def scale(self, alpha: float, **kwargs):
        self.conn.scale(alpha, about_point=self.get_center())
        super().scale(alpha, about_point=self.get_center(), **kwargs)
        return self

class Ground(Component1):
    def __init__(self, center=ORIGIN, **kwargs):
        self.mcenter = center

        # [RIGHT, UP]
        self.v_line = [
            [0.0, 0.25],
            [0.0, -0.25],
        ]
        self.h_line = [
            [0.0, -0.25],
            [0.28, -0.25],
            [-0.28, -0.25],
            [0.0, -0.25],
        ]

        super().__init__(center=self.mcenter, conn=UP*0.25, **kwargs)

    def generate_points(self):
        self.add_points(self.v_line)
        self.add_points(self.h_line)

    def add_points(self, coords):
        for i in (range(coords.__len__()-1)):
            self.add(Line(
                (coords[i+1][0]+self.mcenter[0])*RIGHT+(coords[i+1][1]+self.mcenter[1])*UP,
                (coords[i][0]+self.mcenter[0])*RIGHT+(coords[i][1]+self.mcenter[1])*UP
            ))

class Power(Component1):
    def __init__(self, center=ORIGIN, **kwargs):
        self.mcenter = center

        super().__init__(center=self.mcenter, conn=0.25*DOWN, **kwargs)

    def generate_points(self):
        self.add(Arrow(
            start = 0.5*DOWN+self.mcenter,
            end = 0.75*UP+self.mcenter,
            tip_style={'fill_opacity': 0.5, 'stroke_width': 0.5},
            max_tip_length_to_length_ratio=0.5,
            max_stroke_width_to_length_ratio=20.0
        ))


# A component mobject with 2 connection points
class Component2(Component):
    def __init__(
            self,
            center= ORIGIN,
            conn_a: Vector3D = 1.0*UP,
            conn_b: Vector3D = 1.0*DOWN,
            initial_rot=0.0, # TODO: Make ability to instantiate resistor with initial rotation
            radius=1.0,
            **kwargs
    ) -> None:
        # TODO: Maybe make a *connections array for components to be added to for the child component classes
        self.mcenter = center

        self.conn_a = Connection(self.mcenter+radius*conn_a, color = RED)
        self.conn_b = Connection(self.mcenter+radius*conn_b, color = BLUE)

        super().__init__(**kwargs)

    def get_conn_a(self) -> Connection | Vector3D:
        return self.conn_a
    def get_conn_b(self) -> Connection | Vector3D:
        return self.conn_b 
    def get_center(self) -> Vector3D:
        return self.mcenter
    def set_conn_a(self, val: Connection | Vector3D):
        self.conn_a = val
        return self
    def set_conn_b(self, val: Connection | Vector3D):
        self.conn_b = val
        return self
    
    def scale(self, alpha: float, **kwargs):
        self.conn_a.scale(alpha, about_point=self.get_center())
        self.conn_b.scale(alpha, about_point=self.get_center())
        super().scale(alpha, about_point=self.get_center(), **kwargs)
        return self

    def rotate(self, theta: float, **kwargs):
        self.conn_a.rotate(theta, about_point=self.get_center())
        self.conn_b.rotate(theta, about_point=self.get_center())
        
        super().rotate(theta, **kwargs)
        return self
    
    def shift(self, *vectors: Vector3DLike, **kwargs):
        # TODO: Make shiftDemo function
        self.conn_a.shift(vectors)
        self.conn_b.shift(vectors)
        super().shift(vectors)
        return self

class Resistor(Component2):
    def __init__(self, center=ORIGIN, initial_rot=0.0, radius=1.0, **kwargs) -> None:
        # [RIGHT coord, UP coord]
        self.mcenter = center

        self.coords: list[Vector2D] = [
            [0.0, 1.0],
            [0.0, 0.6236559139784945],
            [0.15053763440860216, 0.4946236559139785],
            [-0.15053763440860216, 0.25806451612903225],
            [0.15053763440860216, 0.02150537634408602],
            [-0.15053763440860216, -0.1935483870967742],
            [0.15053763440860216, -0.4408602150537634],
            [0.0, -0.5698924731182796],
            [0.0, -1.0]
        ]

        super().__init__(conn_a=1.0*UP, conn_b=1.0*DOWN, center = self.mcenter, **kwargs)

    def generate_points(self):
        self.start_new_path(self.center)
        self.set_points_as_corners(self.get_coords())

    def get_coords(self):
        return [coord[1]*UP + coord[0]*RIGHT + self.mcenter for coord in self.coords]

class Capacitor(Component2):
    def __init__(self, center=ORIGIN, **kwargs):
        self.mcenter = center

        # [RIGHT, UP]
        # Coordinates of top lines
        self.top_coords = [
            [0.0, 1.0],
            [0.0, 0.085],
            [0.2, 0.085],
            [-0.2, 0.085]
        ]

        # Bottom vertical line
        self.bottom_coords = [
            [0.0, 0.0],
            [0.0, -1.0]
        ]

        super().__init__(conn_a=1.0*UP, conn_b=1.0*DOWN, center = self.mcenter, **kwargs)
    
    def generate_points(self):
        # Top section
        self.add(
            Line(
                self.top_coords[1][0]*RIGHT+self.top_coords[1][1]*UP+self.mcenter,
                self.top_coords[0][0]*RIGHT+self.top_coords[0][1]*UP+self.mcenter
            ),
            Line(
                
                self.top_coords[3][0]*RIGHT+self.top_coords[3][1]*UP+self.mcenter,
                self.top_coords[2][0]*RIGHT+self.top_coords[2][1]*UP+self.mcenter
            )
        )

        # Bottom Arc
        ang_cen = PI*0.5
        ang = PI*0.5
        self.add(
            Arc(0.25, ang_cen, -0.5*ang, arc_center=DOWN*0.2325+self.mcenter),
            Arc(0.25, ang_cen, ang*0.5, arc_center=DOWN*0.2325+self.mcenter)
        )
        
        # Bottom Vertical Line
        self.add(Line(
            self.bottom_coords[0][0]*RIGHT+self.bottom_coords[0][1]*UP+self.mcenter,
            self.bottom_coords[1][0]*RIGHT+self.bottom_coords[1][1]*UP+self.mcenter
        ))

class Switch2(Component2):
    def __init__(self, center=ORIGIN, **kwargs):
        self.mcenter = center

        # [RIGHT, UP] 0.35
        # Coordinates of top lines
        self.left_coords = [
            [-1.0, 0.0],
            [-0.4286, 0.0],
            [0.4286, 0.2714]
        ]
        self.right_coords = [
            [0.2857, 0.0],
            [1.0, 0.0]
        ]
        self.top_connection = [
            [0.0, 0.1357],
            [0.0, 0.2857]
        ]
        self.top_squiggle = [
            [0.0, 0.4],
            [0.0, 0.4857],
            [-0.1571, 0.5857],
            [0.0, 0.6857],
            [0.0, 0.8286],
        ]
        self.top_lines = [
            [0.0, 0.9143],
            [0.0, 1.314],
            [-0.4143, 1.314],
            [0.3857, 1.314],
            [0.3857, 1.0],
            [0.3857, 1.643],
        ]

        super().__init__(conn_a=LEFT*1.0, conn_b=RIGHT*1.0, center=self.mcenter, **kwargs)
    
    def generate_points(self):
        self.add_points(self.left_coords)
        self.add_points(self.right_coords)
        self.add_points(self.top_connection)
        self.add_points(self.top_squiggle)
        self.add_points(self.top_lines)

    def rotate(self, theta, **kwargs):
        super().rotate(theta, about_point=self.get_center(), **kwargs)
        
    
    def add_points(self, coords):
        for i in (range(coords.__len__()-1)):
            self.add(Line(
                coords[i+1][0]*RIGHT+coords[i+1][1]*UP+self.mcenter,
                coords[i][0]*RIGHT+coords[i][1]*UP+self.mcenter
            ))

class LED(Component2):
    def __init__(self, center=ORIGIN, **kwargs):

        self.mcenter = center

        # [RIGHT, UP]
        self.main_line = [
            [0.0, 1.0],
            [0.0, -1.0]
        ]

        a = np.sqrt(3)/5
        self.triangle = [
            [-a, 0.4], # top left
            [a, 0.4], # top right
            [0, -0.2], # bottom
            [-a, 0.4] # top left
        ]

        self.diode_line  = [
            [0.4, -0.16],
            [-0.4, -0.16]
        ]

        self.arr1 = [
            [-0.5, 0.56/9],
            [-0.96, -101/225],
            [-0.61, -2.78/9],
            [-0.865, -0.845/9],
            [-0.94, -101/225],
        ]
        # y = 1.2x+0.14
        # (-0.175+0.1*a, -0.05+a/9)

        self.arr2 = [
            [-0.5, 104/225],
            [-0.96, -11/225],
            [-0.61, 41/450],
            [-0.865, 551/1800],
            [-0.96, -2/45],
        ]

        super().__init__(conn_a=UP*1.0, conn_b=DOWN*1.0, center=self.mcenter, **kwargs)

    def generate_points(self):
        self.add_points(self.main_line)
        self.add_points(self.triangle)
        self.add_points(self.diode_line)
        self.add_points(self.arr1)
        self.add_points(self.arr2)

    def rotate(self, theta: float, **kwargs):
        super().rotate(theta, about_point=self.get_center(), **kwargs)
        return self

    def add_points(self, coords):
        for i in (range(coords.__len__()-1)):
            self.add(Line(
                coords[i+1][0]*RIGHT+coords[i+1][1]*UP+self.mcenter,
                coords[i][0]*RIGHT+coords[i][1]*UP+self.mcenter
            ))

class VoltageSource(Component2):
    def __init__(self, center = ORIGIN, **kwargs):
        self.mcenter = center

        # Plus
        self.v_plus_coords = [
            [0.0, 0.375],
            [0.0, 0.125]
        ]
        self.h_plus_coords = [
            [-0.125, 0.25],
            [0.125, 0.25]
        ]

        # Minus
        self.minus_coords = [
            [0.125, -0.25],
            [-0.125, -0.25]
        ]

        # Connections
        self.top_connection_coords = [
            [0.0, 0.5],
            [0.0, 1.0]
        ]
        self.bottom_connection_coords = [
            [0.0, -0.5],
            [0.0, -1.0]
        ]

        super().__init__(conn_a=1.0*UP, conn_b=1.0*DOWN, center=self.mcenter, **kwargs)
    
    def generate_points(self):
        self.add_points(self.top_connection_coords)
        self.add(Circle(radius=0.5).shift(self.mcenter))
        self.add_points(self.v_plus_coords)
        self.add_points(self.h_plus_coords)
        self.add_points(self.minus_coords)
        self.add_points(self.bottom_connection_coords)

    def add_points(self, *coords_list):
        for coords in coords_list:
            for i in (range(coords.__len__()-1)):
                self.add(Line(
                    coords[i+1][0]*RIGHT+coords[i+1][1]*UP+self.mcenter,
                    coords[i][0]*RIGHT+coords[i][1]*UP+self.mcenter
                ))

class CurrentSource(Component2):
    def __init__(self, center = ORIGIN, **kwargs):
        self.mcenter = center

        self.arrow_coords = [
            [0.0, -0.45],
            [0.0, 0.45]
        ]

        # Connections
        self.top_connection_coords = [
            [0.0, 0.5],
            [0.0, 1.0]
        ]
        self.bottom_connection_coords = [
            [0.0, -0.5],
            [0.0, -1.0]
        ]

        super().__init__(conn_a=1.0*UP, conn_b=1.0*DOWN, center=self.mcenter, **kwargs)
    
    def generate_points(self):
        self.add_points(self.top_connection_coords)
        self.add(Circle(radius=0.5).shift(self.mcenter))
        self.add(Arrow(
            self.arrow_coords[0][0]*RIGHT + self.arrow_coords[0][1]*UP + self.mcenter,
            self.arrow_coords[1][0]*RIGHT + self.arrow_coords[1][1]*UP + self.mcenter,
            tip_style={'fill_opacity': 0.5, 'stroke_width': 0.5},
            max_tip_length_to_length_ratio=0.5,
            max_stroke_width_to_length_ratio=20.0
        ))
        self.add_points(self.bottom_connection_coords)

    def add_points(self, coords):
        for i in (range(coords.__len__()-1)):
            self.add(Line(
                coords[i+1][0]*RIGHT+coords[i+1][1]*UP+self.mcenter,
                coords[i][0]*RIGHT+coords[i][1]*UP+self.mcenter
            ))

class Battery(Component2):
    def __init__(self, center = ORIGIN, **kwargs):
        self.mcenter = center

        self.top_connection = [
            [0.0, 1.0],
            [0.0, 0.2]
        ]
        self.top_big_line = [
            [0.35, 0.2],
            [-0.35, 0.2],
        ]
        self.top_small_line = [
            [0.2, 0.075],
            [-0.2, 0.075],
        ]
        self.bottom_big_line = [
            [0.35, -0.075],
            [-0.35, -0.075],
        ]
        self.bottom_small_line = [
            [0.2, -0.2],
            [-0.2, -0.2],
        ]
        self.bottom_connection = [
            [0.0, -0.2],
            [0.0, -1.0]
        ]

        super().__init__(self.mcenter, **kwargs)
    
    def generate_points(self):
        self.add_points(self.top_connection)
        self.add_points(self.top_big_line)
        self.add_points(self.top_small_line)
        self.add_points(self.bottom_big_line)
        self.add_points(self.bottom_small_line)
        self.add_points(self.bottom_connection)

    def add_points(self, coords):
        for i in (range(coords.__len__()-1)):
            self.add(Line(
                coords[i+1][0]*RIGHT+coords[i+1][1]*UP+self.mcenter,
                coords[i][0]*RIGHT+coords[i][1]*UP+self.mcenter
            ))


class Component3(Component):
    def __init__(
            self,
            center= ORIGIN,
            conn_a: Vector3D = 1.0*UP, # TODO: Get proper default connections
            conn_b: Vector3D = 1.0*DOWN,
            conn_c: Vector3D = 1.0*RIGHT,
            initial_rot=0.0, # TODO: Make ability to instantiate resistor with initial rotation
            radius=1.0,
            **kwargs
    ) -> None:
        # TODO: Maybe make a *connections array for components to be added to for the child component classes
        self.mcenter = center

        self.conn_a = Connection(self.mcenter+radius*conn_a, color = RED)
        self.conn_b = Connection(self.mcenter+radius*conn_b, color = BLUE)
        self.conn_c = Connection(self.mcenter+radius*conn_c, color = GREEN)

        super().__init__(**kwargs)

    def get_conn_a(self) -> Connection | Vector3D:
        return self.conn_a
    def get_conn_b(self) -> Connection | Vector3D:
        return self.conn_b 
    def get_center(self) -> Vector3D:
        return self.self.mcenter
    def set_conn_a(self, val: Connection | Vector3D):
        self.conn_a = val
        return self
    def set_conn_b(self, val: Connection | Vector3D):
        self.conn_b = val
        return self
    def get_conn_c(self) -> Connection | Vector3D:
        return self.conn_c
    def set_conn_c(self, val: Connection | Vector3D):
        self.conn_c = val
        return self
    
    def scale(self, alpha: float, **kwargs):
        self.conn_a.scale(alpha, about_point=self.get_center())
        self.conn_b.scale(alpha, about_point=self.get_center())
        self.conn_c.scale(alpha, about_point=self.get_center())
        
        super().scale(alpha, about_point=self.get_center(), **kwargs)
        return self

    def rotate(self, theta: float, **kwargs):
        self.conn_a.rotate(theta, about_point=self.get_center())
        self.conn_b.rotate(theta, about_point=self.get_center())
        self.conn_c.rotate(theta, about_point=self.get_center())
        
        super().rotate(theta, **kwargs)
        return self
    
    def shift(self, *vectors: Vector3DLike, **kwargs):
        # TODO: Make shiftDemo function
        self.conn_a.shift(vectors)
        self.conn_b.shift(vectors)
        self.conn_c.shift(vectors)
        super().shift(vectors)
        return self

class Opamp(Component3):
    def __init__(self, center=ORIGIN, **kwargs):
        self.mcenter = center
        self.right = RIGHT*0.6589

        # Because I originally constructed this differently than all the other components, it may need reformatted to be constructed consistently with other components

        self.triangle_points = self.get_triangle_points(ORIGIN, self.right)
        
        # TODO: Maybe figure out if these should be Connections or Vector3Ds...we should just be consistent
        self.conn_a = LEFT*1.0+UP*0.3372 # Positive Connection
        self.conn_b = LEFT*1.0+DOWN*0.3372 # Negative Connection
        self.conn_c = RIGHT*1.0 # Output Connection

        self.sym_size = 0.07558
        self.pos_sym_pos = LEFT*0.4864+UP*0.3488
        self.neg_sym_pos = LEFT*0.4864+DOWN*0.3488

        self.pos_tri = RIGHT*self.triangle_points[1] + UP*self.pos_sym_pos # Point where positive connection connects to the triangle
        self.neg_tri = RIGHT*self.triangle_points[1] + UP*self.neg_sym_pos
        self.out_tri = RIGHT*0.6202

        # Negative symbol
        self.neg_sym = [self.sym_size*LEFT+self.neg_sym_pos, self.sym_size*RIGHT+self.neg_sym_pos]
        # Positive symbol requires 2 shapes
        self.h_pos_sym = [self.sym_size*LEFT+self.pos_sym_pos,self.sym_size*RIGHT+self.pos_sym_pos]
        self.v_pos_sym = [self.sym_size*UP+self.pos_sym_pos,self.sym_size*DOWN+self.pos_sym_pos]

        # Positive connection
        self.pos_conn = [self.conn_a, self.pos_tri*RIGHT+self.conn_a*UP]
        # Negative connection
        self.neg_conn = [self.conn_b, self.neg_tri*RIGHT+self.conn_b*UP]
        # Output connection
        self.out_conn = [self.out_tri, self.conn_c]

        super().__init__(conn_a=self.conn_a, conn_b=self.conn_b, conn_c=self.conn_c, center=self.mcenter, **kwargs)

    def generate_points(self):
        self.add_points(
            self.triangle_points,

            self.neg_sym,

            self.h_pos_sym,
            self.v_pos_sym,
            
            self.neg_conn,
            self.pos_conn,
            self.out_conn
        )
    
    def add_points(self, *coords_list):
        for coords in coords_list:
            for i in (range(coords.__len__()-1)):
                self.add(Line(
                    coords[i+1][0]*RIGHT+coords[i+1][1]*UP+self.mcenter,
                    coords[i][0]*RIGHT+coords[i][1]*UP+self.mcenter
                ))

    def get_norm(self, vect):
        return sum((x**2 for x in vect))**0.5
    
    def get_triangle_points(self, pc, pr):
        L = self.get_norm(pr - pc)
        h_stretch = 1.0875
        v_stretch = 0.55
        p1 = UP*(pc + L*np.sin((2-v_stretch)*PI/3)) + RIGHT*(pc + L*np.cos((2+h_stretch)*PI/3))
        p2 = UP*(pc + L*np.sin((4+v_stretch)*PI/3)) + RIGHT*(pc + L*np.cos((4-h_stretch)*PI/3))
        return [pr, p1, p2, pr]

class Potentiometer(Component3):
    def __init__(self, center=ORIGIN, **kwargs):
        self.mcenter = center

        # [RIGHT, UP]
        # Maybe find way to create a Resistor with 5 humps, then create an Arrow
        self.res_coords = [
            [0.0, 1.0], 
            [0.0, 0.5333333333333334], 
            [-0.10980392156862746, 0.4313725490196079], 
            [0.10980392156862746, 0.2901960784313726], 
            [-0.10980392156862746, 0.14901960784313728], 
            [0.10980392156862746, 0.0], 
            [-0.10980392156862746, -0.14901960784313728], 
            [0.10980392156862746, -0.2901960784313726], 
            [-0.10980392156862746, -0.4313725490196079], 
            [0.0, -0.5333333333333334], 
            [0.0, -1.0]
        ]

        self.arrow1_coords = [
            [0.225, -0.165],
            [0.10980392156862746, 0.0],
            [0.225, 0.165],
            [0.225, 0.0],
            [0.525, 0.0],
            [0.225, 0.0],
            [0.225, -0.165]
        ]

        self.arrow2_coords = [
            [0.325, -0.375],
            [0.25, -0.24],
            [0.175, -0.375],
            [0.25, -0.375],
            [0.25, -0.51],
            [0.25, -0.375],
            [0.325, -0.375]
        ]

        super().__init__(conn_a = UP*1.0, conn_b = DOWN*1.0, conn_c = RIGHT*0.525, center=self.mcenter, **kwargs)
    
    def generate_points(self):
        # Resistor section
        self.add_points(self.res_coords)
        # 1st Arrow section
        self.add_points(self.arrow1_coords)
        # 2nd Arrow section
        self.add_points(self.arrow2_coords)
    
    def add_points(self, coords):
        for i in (range(coords.__len__()-1)):
            self.add(Line(
                coords[i+1][0]*RIGHT+coords[i+1][1]*UP+self.mcenter,
                coords[i][0]*RIGHT+coords[i][1]*UP+self.mcenter
            ))

class Switch3(Component3):
    def __init__(self, center=ORIGIN, **kwargs):
        self.mcenter = center

        # [RIGHT, UP]
        self.left_bottom_coords = [
            [-0.5143, -0.2429],
            [-0.5143, -0.5714],
            [-1.071, -0.5714]
        ]

        self.left_top_coords = [
            [-0.5143, 0.2857],
            [-0.5143, 0.5071],
            [-1.071, 0.5071]
        ]

        self.right_coords = [
            [1.0, 0.0],
            [0.4286, 0.0],
            [-0.9214, -0.4571]
        ]

        self.bottom_connection = [
            [0.0, -0.1429],
            [0.0, -0.2857]
        ]

        self.bottom_squiggle = [
            [0.0, -0.3714],
            [0.0, -0.4857],
            [0.1571, -0.5714],
            [0.0, -0.65],
            [0.0, -0.8143]
        ]

        self.bottom_lines = [
            [0.0, -0.9714],
            [0.0, -1.307],
            [0.4214, -1.307],
            [-0.4214, -1.307]
        ]

        super().__init__(
            conn_a=self.left_bottom_coords[2][0]*RIGHT + self.left_bottom_coords[2][1]*UP,
            conn_b=self.left_top_coords[2][0]*RIGHT+self.left_top_coords[2][1]*UP,
            conn_c=self.right_coords[0][0]*RIGHT+self.right_coords[0][1]*UP,
            center=self.mcenter,
            **kwargs
        )

    def generate_points(self):
        self.add_points(
            self.right_coords,
            self.left_bottom_coords,
            self.left_top_coords,
            self.bottom_connection,
            self.bottom_squiggle,
            self.bottom_lines
        )
    
    def add_points(self, *coords_list):
        for coords in coords_list:
            for i in (range(coords.__len__()-1)):
                self.add(Line(
                    coords[i+1][0]*RIGHT+coords[i+1][1]*UP+self.mcenter,
                    coords[i][0]*RIGHT+coords[i][1]*UP+self.mcenter
                ))


class Wire(VGroup):
    def __init__(
        self,
        conn_a: Connection,
        conn_b: Connection,
        **kwargs
    ):
        super().__init__()

        # TODO: Possibly assign updaters according to the centers of conn_a and conn_b
        
        # Check if one or multiple lines necessary...
        # just check X/Y coords for now, should use PIP algorithm to avoid other circuit mobjects?

        right_val = (conn_a*RIGHT - conn_b*RIGHT)[0]
        up_val = (conn_a*UP - conn_b*UP)[1]

        right_check = abs(right_val) < 0.05
        up_check = abs(up_val) < 0.05
        
        # Use only one Line with both connections as endpoints IF either the X OR Y coords are the same
        if (right_check or up_check):
            self.add(Line(conn_a, conn_b, **kwargs))

        # TODO: Figure out prioritization of right and up coordinates, which one goes first...
        #       likely will have to consider "clockwise" or "counterclockwise" wire arrangement, if that makes sense 
        #       currently, the ground wire is messed up
        #
        #       For now, the a and b connections can be switched if it looks bad

        # Different X and Y coord requires 2 Lines
        # go to conn_b's x coord first
        elif right_val < 0 or up_val < 0:
            self.add(Line(conn_a, conn_b*UP+conn_a*RIGHT, **kwargs))
            self.add(Line(conn_b*UP+conn_a*RIGHT, conn_b, **kwargs))

        # go to conn_b's y coord first
        else:
            self.add(Line(conn_a, conn_b*RIGHT+conn_a*UP, **kwargs))
            self.add(Line(conn_b*RIGHT+conn_a*UP, conn_b, **kwargs))


class Circuit(VGroup):
    def __init__(
        self,
        *components,
        **kwargs
    ):
        super().__init__()
        self.add(*components)