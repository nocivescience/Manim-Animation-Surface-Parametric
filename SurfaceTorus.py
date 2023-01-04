from manim import *
class TorusScene(ThreeDScene):
    CONFIG={
        'axes_config':{
            'x_range':[-5,5],
            'y_range':[-5,5],
            'z_range':[-5,5],
        },
        'torus_config':{
            'u_range':[-4,4],
            'v_range':[-4,4],
            'resolution':32,
        }
    }
    def construct(self):
        axes=ThreeDAxes(
            **self.CONFIG['axes_config']
        )
        self.set_camera_orientation(phi=80*DEGREES,theta=50*DEGREES)
        self.begin_ambient_camera_rotation()
        def torus(u,v):
            return np.array([
                (2.76+1.2*np.cos(u))*np.cos(v),
                (2.76+1.2*np.cos(u))*np.sin(v),
                1.2*np.sin(u)   
            ])
        def cono(u,v):
            return np.array([
                np.cos(v),
                np.sin(v)*np.cos(v),
                u
            ])
        def sphere(u,v):
            return np.array([
                np.cos(u)*np.cos(v),
                np.cos(u)*np.sin(v),
                np.sin(u)
            ])
        def superficie(u,v):
            return np.array([
                u,
                v,
                0.5*(np.sin(u)+np.cos(v))-0.025*(u**2+v**2)
            ])
        surface=Surface(
            lambda u,v: torus(u,v), **self.CONFIG['torus_config']
        )
        surface2=Surface(
            lambda u,v: cono(u,v),**self.CONFIG['torus_config']
        )
        surface3=Surface(
            lambda u, v: sphere(u,v), **self.CONFIG['torus_config']
        )
        surface4=Surface(
            lambda u,v: superficie(u,v), **self.CONFIG['torus_config']
        )
        self.play(Create(axes))
        surfaces=VGroup(surface,surface2,surface3,surface4)
        prime_surface=surfaces[0].copy()
        self.play(Create(prime_surface))
        for i in range(len(surfaces)):
            if i==0:
                self.remove(prime_surface)
            self.play(Transform(surfaces[0],surfaces[i]))
        self.wait()
        circle=Circle(radius=.25)
        point=VectorizedPoint(np.array([-2,2,2]))
        circle.add_updater(lambda t: t.move_to(point))
        surface_circle=always_redraw(
            lambda: circle.copy().apply_function(
                lambda p: superficie(*p[:2])
            )
        )
        line=always_redraw(
            lambda: Line(point.get_location(), superficie(*point.get_location()[:2]))
        )
        self.play(Create(circle),Create(line),Create(surface_circle))
        for vect in [2*LEFT,3*RIGHT,2*DOWN,UP,2*LEFT,RIGHT*1.4,3*UP,3*DOWN,4*UP,4*DOWN,2*UP,2*DOWN,ORIGIN]:
            self.play(
                point.animate.move_to(vect), run_time=3
            )
        self.wait()