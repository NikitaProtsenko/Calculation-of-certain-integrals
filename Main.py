from ForGame import *
from math import sin, cos, tan, asin, acos, atan, sinh, cosh, log, pi, e
from pyautogui import prompt

#Missing math functions:
def cotan(x: float) -> float:
    """Return the cotangent of x (measured in radians)."""
    return 1 / tan(x)

def acotan(x: float) -> float:
    """Return the arc cotangent of x (measured in radians)."""
    return pi / 2 - atan(x)

def ln(x: float) -> float:
    """Return the natural logarithm of x."""
    return log(x)

def lg(x: float) -> float:
    """Return the decimal logarithm of x."""
    return log(x, 10)

#Math functions abbreviations:
tg = tan
ctg = cotan
actg = acotan
sh = sinh
ch = cosh

#Screen:
FPS = 60
WIDTH, HEIGHT = 1200, 600
screen = newScreen(WIDTH, HEIGHT, 'Integral calculation')

#Type of function:
function = type(round)

#Lines group:
all_lines = newGroup()
#Rectangles group:
all_rects = newGroup()
#Trapeziods group:
all_trapezoids = newGroup()
#Curve trapezoids group:
all_curve_trapezoids = newGroup()

#Pictures:
picture = {}
picture['width arrow up'] = Image('width_arrow_up.png')
picture['control info'] = Image('control_info.png')

#Run-flag:
running = True

#Positive vector Oy:
Y_positive_vector_is_up = True

#Current actions:
actions = {'up': False, 'down': False, 'left': False, 'right': False,
           'tap on width arrow': False}

#Mouse buttons:
mouse_but = {1: False, 2: False, 3: False}

class camera(Sprite):
    """Camera for view.
pos - camera position,
size - camera size,
speed - moving camera speed,
zoom_koef - speed of zoom."""

    def __init__(self, pos: (float, float) = (0, 0), size: (float, float) = (WIDTH, HEIGHT), speed: float = 1, zoom_koef: float = 1.0625):
        Sprite.__init__(self,
                        image = Surface((0, 0), (0, 0, 0)),
                        pos = (0, 0),
                        rect = None)
        self.pos = pos
        self.size = size
        self.speed = speed
        self.zoom_koef = zoom_koef
        all_lines.add(self)

    @property
    def x(self) -> float:
        return self.pos[0]

    @x.setter
    def x(self, value: float):
        self.pos = value, self.pos[1]

    @property
    def y(self) -> float:
        return self.pos[1]

    @y.setter
    def y(self, value: float):
        self.pos = self.pos[0], value

    def update(self):
        """Camera update."""
        pass

    def draw(self):
        """None."""
        return

#Camera of screen:
MainCamera = camera(size = (WIDTH / 100, HEIGHT / 100),
                    speed = 0.05,
                    zoom_koef = 1.125)

class figLine(Sprite):
    """Line.
p1 - start point,
p2 - end point,
color - RGB-color."""
    
    def __init__(self, p1: (float, float), p2: (float, float), color = (0, 0, 0)):
        Sprite.__init__(self,
                        image = Surface((0, 0), (0, 0, 0)),
                        pos = (0, 0),
                        rect = None)
        self.p1 = p1
        self.p2 = p2
        self.color = color
        all_lines.add(self)

    def update(self):
        """Sprite update."""
        self.draw()

    def draw(self):
        """Sprite draw."""
        global screen, MainCamera
        x, y = MainCamera.pos
        dx, dy = [[WIDTH, HEIGHT][i] / MainCamera.size[i] for i in range(2)]
        x1, y1 = self.p1
        x2, y2 = self.p2
        sign = -1 if Y_positive_vector_is_up else 1
        x1 = (x1 - x) * dx + WIDTH / 2
        y1 = sign * (y1 - y) * dy + HEIGHT / 2
        x2 = (x2 - x) * dx + WIDTH / 2
        y2 = sign * (y2 - y) * dy + HEIGHT / 2
        draw.aaline(screen,
                    self.color,
                    (x1, y1),
                    (x2, y2))

class figRect(Sprite):
    """Rect.
pos - position of min point of axes,
size - sizes of rectangle (width, height),
color - RGB-color of rectangle."""

    def __init__(self, pos: (float, float), size: (float, float), color = (0, 0, 0)):
        Sprite.__init__(self,
                        image = Surface((0, 0), (0, 0, 0)),
                        pos = (0, 0),
                        rect = None)
        self.pos = pos
        self.size = size
        self.color = color
        all_rects.add(self)

    def update(self):
        """Sprite update."""
        self.draw()

    def draw(self):
        """Sprite draw."""
        global screen, MainCamera
        x, y = MainCamera.pos
        dx, dy = [[WIDTH, HEIGHT][i] / MainCamera.size[i] for i in range(2)]
        x1, y1 = self.pos
        x2, y2 = self.size
        x2 += x1
        y2 += y1
        sign = -1 if Y_positive_vector_is_up else 1
        x1 = (x1 - x) * dx + WIDTH / 2
        y1 = sign * (y1 - y) * dy + HEIGHT / 2
        x2 = (x2 - x) * dx + WIDTH / 2
        y2 = sign * (y2 - y) * dy + HEIGHT / 2
        if x1 > x2:
            x1, x2 = x2, x1
        if y1 > y2:
            y1, y2 = y2, y1
        draw.rect(screen,
                  self.color,
                  gameRect(x1, y1, x2 - x1, y2 - y1),
                  width = 1)

class figTrapezoid(Sprite):
    """Trapeze on the side.
pos - position of min point of axes,
width - height of trapezoid,
leftBase - left base of trapezoid,
rightBase - right base of trapezoid,
color - RGB-color of rectangle."""

    def __init__(self, pos: (float, float), width : float, leftBase : float, rightBase : float, color = (0, 0, 0)):
        Sprite.__init__(self,
                        image = Surface((0, 0), (0, 0, 0)),
                        pos = (0, 0),
                        rect = None)
        self.pos = pos
        self.width = width
        self.leftBase = leftBase
        self.rightBase = rightBase
        self.color = color
        all_trapezoids.add(self)

    def update(self):
        """Sprite update."""
        self.draw()

    def draw(self):
        """Sprite draw."""
        global screen, MainCamera
        x, y = MainCamera.pos
        dx, dy = [[WIDTH, HEIGHT][i] / MainCamera.size[i] for i in range(2)]
        x1, y1 = self.pos
        x2 = self.width 
        yl = self.leftBase
        yr = self.rightBase
        x2 += x1
        yl += y1
        yr += y1
        sign = -1 if Y_positive_vector_is_up else 1
        x1 = (x1 - x) * dx + WIDTH / 2
        y1 = sign * (y1 - y) * dy + HEIGHT / 2
        x2 = (x2 - x) * dx + WIDTH / 2
        yl = sign * (yl - y) * dy + HEIGHT / 2
        yr = sign * (yr - y) * dy + HEIGHT / 2
        if x1 > x2:
            x1, x2 = x2, x1
        draw.polygon(screen,
                     self.color,
                     [(x1, y1), (x2, y1), (x2, yr), (x1, yl)],
                     width = 1)

class figCurveTrapezoid(Sprite):
    """Trapeze on the straight side.
p1, p2, p3 - points of curve side of trapezoid,
color - RGB-color of rectangle."""

    def __init__(self, p1: (float, float), p2 : (float,float), p3 : (float,float), cuts = 10, color = (0, 0, 0)):
        Sprite.__init__(self,
                        image = Surface((0, 0), (0, 0, 0)),
                        pos = (0, 0),
                        rect = None)
        self.p1, self.p2, self.p3 = sorted([p1, p2, p3], key = lambda p: p[0])

        self.function = figCurveTrapezoid.parabola(self.p1, self.p2, self.p3)
        self.color = color
        dx = (self.p3[0] - self.p1[0]) / cuts
        ps = list(map(lambda i : ((px := p1[0] + dx * i), self.function(px)) ,
                      range(cuts + 1) ))
        list(map(lambda i : figLine(ps[i], ps[i + 1], self.color),
                 range(cuts)))
        all_curve_trapezoids.add(self)

    def parabola(p1: (float, float), p2: (float, float), p3: (float, float)) -> function:
        """Return parabola of 3 points."""
        x1, y1 = p1
        x2, y2 = p2
        x3, y3 = p3
        
        dy2y1 = y2 - y1
        x1x2 = x1 * x2
        x2y1 = x2 * y1
        x1y2 = x1 * y2
        sx1x2 = x1 + x2
        dx2x1 = x2 - x1
        dx2y1_x1y2 = x2y1 - x1y2
        try:
            a = (y3 - ((x3 * dy2y1 + dx2y1_x1y2) / (x2 - x1))) / (x3 * (x3 - sx1x2) + x1x2)
            b = dy2y1 / dx2x1 - a * sx1x2
            c = dx2y1_x1y2 / dx2x1 + a * x1x2
            return new_function(f'{a}*x*x + {b}*x + {c}')
        except:
            return lambda x: 0

    def update(self):
        """Sprite update."""
        self.draw()

    def draw(self):
        """Sprite draw."""
        global screen, MainCamera
        x, y = MainCamera.pos
        dx, dy = [[WIDTH, HEIGHT][i] / MainCamera.size[i] for i in range(2)]
        x1, yl = self.p1
        y1 = 0
        x2, yr = self.p3
        sign = -1 if Y_positive_vector_is_up else 1
        x1 = (x1 - x) * dx + WIDTH / 2
        y1 = sign * (y1 - y) * dy + HEIGHT / 2
        x2 = (x2 - x) * dx + WIDTH / 2
        yl = sign * (yl - y) * dy + HEIGHT / 2
        yr = sign * (yr - y) * dy + HEIGHT / 2
        if x1 > x2:
            x1, x2 = x2, x1
        draw.lines(screen,
                   self.color,
                   False,
                   [(x1, yl), (x1, y1), (x2, y1), (x2, yr)],
                   width = 1)

def function_point(func: function, x: float) -> (float, float):
    """Return point of function in x.
func - string of function of one var x,
x - point value."""
    try:
        y = func(x)
    except:
        y = None
    if not type(y) in [int, float]:
        y = None
    return x, y

def new_function(func: str) -> function:
    """Return function from string func.
func - string of function of one var x."""
    def res(x: float):
        """Function with var x."""
        s = func.replace('^', '**')
        return eval(s)
    return res

def draw_axes():
    """Draw axes of plane."""
    X, Y = MainCamera.pos
    W, H = MainCamera.size
    xmin = X - W / 2
    xmax = xmin + W
    ymin = Y - H / 2
    ymax = ymin + H
    size = W / 200
    if ymin < 0 and ymax > 0:
        figLine(p1 = (xmin, 0),
                p2 = (xmax, 0),
                color = (0, 0, 255))
    if xmin < 0 and xmax > 0:
        figLine(p1 = (0, ymin),
                p2 = (0, ymax),
                color = (0, 0, 255))
    d = int(lg(W))
    small = 10 ** (d - 1)
    big = small * 10
    left_ruler = small * int(xmin // small)
    if xmin > 0:
        left_ruler += small
    bottom_ruler = small * int(ymin // small)
    if ymin > 0:
        bottom_ruler += small
    ruler_count_Ox = int((xmax - left_ruler) // small)
    ruler_count_Oy = int((ymax - bottom_ruler) // small)
    ruler_Ox = list(map(lambda i: left_ruler + i * small,
                    range(ruler_count_Ox)))
    ruler_Oy = list(map(lambda i: bottom_ruler + i * small,
                    range(ruler_count_Oy)))
    list(map(lambda i: (figLine(p1 = (i, -size * 2),
                               p2 = (i, size * 2),
                               color = (0, 255, 255)) if (i % big) < small * 2 / 3 else
                        figLine(p1 = (i, -size),
                                p2 = (i, size),
                                color = (0, 0, 255))),
             ruler_Ox))
    list(map(lambda i: (figLine(p1 = (-size * 2, i),
                               p2 = (size * 2, i),
                               color = (0, 255, 255)) if (i % big) < small * 2 / 3 else
                        figLine(p1 = (-size, i),
                                p2 = (size, i),
                                color = (0, 0, 255))),
             ruler_Oy))

def draw_function(func: function, cuts: int = 100):
    """Draw visible part of function on screen.
func - function of one var x,
cuts - splitting of visible segment of function."""
    X, Y = MainCamera.pos
    W, H = MainCamera.size
    xmin = X - W / 2
    xmax = xmin + W
    ymin = Y - H / 2
    ymax = ymin + H
    dx = (xmax - xmin) / cuts
    ps = list(map(lambda i: function_point(func = func,
                                           x = xmin + i * dx),
                  range(cuts + 1)))
    ps = list(map(lambda p: p if p[1] is None or p[1] >= ymin and p[1] <= ymax else (p[0], None),
                  ps))
    #Be sure to convert to list to craete figLines:
    list(map(lambda i: figLine(p1 = ps[i - 1],
                               p2 = ps[i],
                               color = (255, 255, 255)) if not (ps[i - 1][1] is None or ps[i][1] is None) else None,
             range(1, len(ps))))

def draw_integral_rects(func: function, start: float = 0, end: float = 10, cuts: int = 100, sample: float = 0, cl = (0, 255, 0)):
    """Draw rectangles of integral sum.
func - function of one var x,
start - bottom limit of integral,
end - top limit of integral,
cuts - splitting of segment,
sample - x point of segment [0; 1] of calculating,
cl - color of integral figures."""
    if end < start:
        draw_integral_rects(func, end, start, cuts, sample, (255, 0, 0))
        return
    X, Y = MainCamera.pos
    W, H = MainCamera.size
    xmin = X - W / 2
    xmax = xmin + W
    dx = (end - start) / cuts
    start += (int((xmin - start) // dx) * dx) if start < xmin else 0
    end += (int((xmax - end) // dx) * dx) if end > xmax else 0
    if end <= start:
        return
    cuts = int((end - start) // dx) + 1
    ps = list(map(lambda i: function_point(func, start + (i + sample) * dx),
                  range(cuts)))
    list(map(lambda i: ((px := ps[i][0] - dx * sample), figRect(pos = (px, ps[i][1]) if ps[i][1] < 0 else (px, 0),
                                                                size = (dx, abs(ps[i][1])),
                                                                color = cl)) if not ps[i][1] is None else None,
             range(len(ps))))

def calculate_rect(func: function, x: float, dx: float, right: [bool] = [True]) -> float:
    """Return square area with width dx and height func(x).
func - function of one var x,
x - point value,
dx - square width,
right - stay [True] if calculate done else [False]."""
    x, y = function_point(func, x)
    s = 0
    if y is None:
        right[0] = False
    else:
        s = y * dx
    return s

def integral_calculate_rect(func: function, start: float = 0, end: float = 10, cuts: int = 100, sample: float = 0) -> (float, bool):
    """Return value of integral of function and False if function exactly has a singularity else True.
func - function of one var x,
start - bottom limit of integral,
end - top limit of integral,
cuts - splitting of segment,
sample - x point of segment [0; 1] of calculating."""
    if start > end:
        value, flag = integral_calculate_rect(func = func,
                                              start = end,
                                              end = start,
                                              cuts = cuts,
                                              sample = sample)
        return -value, flag
    S = 0
    flag = [True]
    dx = (end - start) / cuts
    S = sum(map(lambda i: calculate_rect(func = func,
                                         x = start + (i + sample) * dx,
                                         dx = dx,
                                         right = flag),
                range(cuts)))
    return S, flag[0]


def draw_integral_trapezoid(func: function, start: float = 0, end: float = 10, cuts: int = 100, cl = (0, 255, 0)):
    """Draw rectangles of integral sum.
func - function of one var x,
start - bottom limit of integral,
end - top limit of integral,
cuts - splitting of segment,
cl - color of integral figures."""
    if end < start:
        draw_integral_trapezoid(func, end, start, cuts, (255, 0, 0))
        return
    X, Y = MainCamera.pos
    W, H = MainCamera.size
    xmin = X - W / 2
    xmax = xmin + W
    dx = (end - start) / cuts
    start += (int((xmin - start) // dx) * dx) if start < xmin else 0
    end += (int((xmax - end) // dx) * dx) if end > xmax else 0
    if end <= start:
        return
    cuts = int((end - start) // dx) + 1
    ps = list(map(lambda i: function_point(func, start + i * dx),
                  range(cuts)))
    list(map(lambda i: figTrapezoid(pos = (ps[i][0], 0),
                               width = dx,
                               leftBase = ps[i][1],
                               rightBase = ps[i + 1][1],
                               color = cl) if not ps[i][1] is None else None,
             range(len(ps) - 1)))

def calculate_trapezoid(func: function, x: float, dx: float, right: [bool] = [True]) -> float:
    """Return square area with width dx and height func(x).
func - function of one var x,
x - point value,
dx - trapezoid height,
right - stay [True] if calculate done else [False]."""
    x, y1 = function_point(func, x)
    y2 = func(x + dx)
    s = 0
    if (y1 is None) or (y2 is None):
        right[0] = False
    else:
        s = ((y1 + y2) / 2) * dx
    return s

def integral_calculate_trapezoid(func: function, start: float = 0, end: float = 10, cuts: int = 100) -> (float, bool):
    """Return value of integral of function and False if function exactly has a singularity else True.
func - function of one var x,
start - bottom limit of integral,
end - top limit of integral,
cuts - splitting of segment."""
    if start > end:
        value, flag = integral_calculate_trapezoid (func = func,
                                              start = end,
                                              end = start,
                                              cuts = cuts)
        return -value, flag
    S = 0
    flag = [True]
    dx = (end - start) / cuts
    S = sum(map(lambda i: calculate_trapezoid(func = func,
                                         x = start + i * dx,
                                         dx = dx,
                                         right = flag),
                range(cuts)))
    return S, flag[0]

def draw_integral_curve_trapezoid(func: function, start: float = 0, end: float = 10, cuts: int = 100, sample: float = 0.5, cl = (0, 255, 0)):
    """Draw rectangles of integral sum.
func - function of one var x,
start - bottom limit of integral,
end - top limit of integral,
cuts - splitting of segment,
sample - x point of segment [0; 1] of calculating,
cl - color of integral figures."""
    if end < start:
        draw_integral_curve_trapezoid(func, end, start, cuts, sample, (255, 0, 0))
        return
    X, Y = MainCamera.pos
    W, H = MainCamera.size
    xmin = X - W / 2
    xmax = xmin + W
    cuts2 = int(cuts ** 0.5)
    dx = (end - start) / cuts2
    start += (int((xmin - start) // dx) * dx) if start < xmin else 0
    end += (int((xmax - end) // dx) * dx) if end > xmax else 0
    if end <= start:
        return
    cuts = int((end - start) // dx) + 1
    ps = list(map(lambda i: function_point(func, start + i * dx),
                  range(cuts)))
    list(map(lambda i: figCurveTrapezoid(p1 = ps[i], 
                                         p2 = ((px := ps[i][0] + sample * dx), func(px)),
                                         p3 = ps[i + 1],
                                         cuts = cuts2,
                                         color = cl) if not ps[i][1] is None else None,
             range(len(ps) - 1)))

def calculate_curve_trapezoid(func: function, x: float, dx: float, right: [bool] = [True]) -> float:
    """Return square area with width dx and height func(x).
func - function of one var x,
x - point value,
dx - trapezoid height,
right - stay [True] if calculate done else [False]."""
    a = x
    b = x + dx
    y1 = func(a)
    y2 = func(b)
    y3 = func((a + b) / 2)
    s = 0
    if (y1 is None) or (y2 is None) or (y3 is None):
        right[0] = False
    else:
        s = ((b - a) / 6) * (y1 + 4 * y3 + y2)
    return s

def integral_calculate_curve_trapezoid(func: function, start: float = 0, end: float = 10, cuts: int = 100, sample: float = 0.5) -> (float, bool):
    """Return value of integral of function and False if function exactly has a singularity else True.
func - function of one var x,
start - bottom limit of integral,
end - top limit of integral,
cuts - splitting of segment."""
    if start > end:
        value, flag = integral_calculate_curve_trapezoid (func = func,
                                                          start = end,
                                                          end = start,
                                                          cuts = cuts,
                                                          sample = sample)
        return -value, flag
    S = 0
    flag = [True]
    cuts = int(cuts ** 0.5)
    dx = (end - start) / cuts
    S = sum(map(lambda i: calculate_curve_trapezoid(func = figCurveTrapezoid.parabola(p1 = ((px := (x0 := start + i * dx)), func(px)),
                                                                                      p2 = ((px := x0 + sample * dx), func(px)),
                                                                                      p3 = ((px := x0 + dx, func(px)))),
                                                    x = x0,
                                                    dx = dx,
                                                    right = flag),
                range(cuts)))
    return S, flag[0]

def draw_text(surf: game.Surface, text: str, size: int, x: int, y: int, color: (int, int, int)):
    """Draw text on surface surf.
surf - surface for drawning,
text - text for drawning,
size - font size,
x, y - position of drawning,
color - RGB-color."""
    font = game.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    surf.blit(text_surface, text_rect)
    
#Globals for onStart function:
c_info_pic = None
c_info = None
w_arrow_pic = None
w_arrow = None
info_show = None
f_str = None
f = None
c = None
x1 = None
x2 = None
samp = None
maxdy = None
show_function = None
show_integral = None
int_mode = None
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

def onStart():
    """Start function."""
    global f_str, f, c, x1, x2, samp, show_function, show_integral, int_mode, c_info_pic, c_info, w_arrow_pic, w_arrow, info_show
    f_str = prompt(text = 'Enter the function:',
                   title = 'Function',
                   default='sin(x)')
    f = new_function(f_str)
    c = 100
    x1 = float(prompt(text = 'Enter x1',
                      title = 'x1',
                      default = '0'))
    x2 = float(prompt(text = 'Enter x2',
                      title = 'x2',
                      default = '10'))
    maxdy = 1000
    samp = 0.5
    show_function = True
    show_integral = True
    int_mode = 2
    w, h = picture['control info'].get_size()
    c_info_pic = transform.scale(picture['control info'], (w * 2, h * 2))
    c_info = Sprite(c_info_pic, (0, 0))
    c_info.rect.topright = (WIDTH, 0)
    w, h = picture['width arrow up'].get_size()
    w_arrow_pic = transform.scale(picture['width arrow up'], (w * 2, h * 2))
    w_arrow = Sprite(w_arrow_pic, (0, 0))
    w_arrow.rect.midtop = c_info.rect.midbottom
    info_show = True

if __name__ == '__main__':
    onStart()
    result = None
    while running:
        clock.tick(FPS)
        for event in gameEvents():
            #Program exit:
            if event.type == game.QUIT:
                running = False
            #Keyboard key down:
            if event.type == game.KEYDOWN:
                if event.key == game.K_UP or event.key == game.K_w:
                    actions['up'] = True
                
                if event.key == game.K_DOWN or event.key == game.K_s:
                    actions['down'] = True
                
                if event.key == game.K_LEFT or event.key == game.K_a:
                    actions['left'] = True
                
                if event.key == game.K_RIGHT or event.key == game.K_d:
                    actions['right'] = True
            #Keyboard key up:
            if event.type == game.KEYUP:
                if event.key == game.K_UP or event.key == game.K_w:
                    actions['up'] = False
                
                elif event.key == game.K_DOWN or event.key == game.K_s:
                    actions['down'] = False
                
                elif event.key == game.K_LEFT or event.key == game.K_a:
                    actions['left'] = False
                
                elif event.key == game.K_RIGHT or event.key == game.K_d:
                    actions['right'] = False

                elif event.key == game.K_f:
                    f_str = prompt(text = 'Enter the function:',
                                   title = 'Function',
                                   default = f_str)
                    f = new_function(f_str)
                    result = None

                elif event.key == game.K_r:
                    x1 = eval(prompt(text = 'Enter start of integral',
                                     title = 'Region',
                                     default = str(x1)))
                    x2 = eval(prompt(text = 'Enter end of integral',
                                     title = 'Region',
                                     default = str(x2)))
                    result = None

                elif event.key == game.K_m:
                    c = int(prompt(text = 'Enter the spliting:',
                                   title = 'Spliting',
                                   default = str(c)))
                    result = None
                
                elif event.key == game.K_z:
                    show_function = not show_function
                
                elif event.key == game.K_x:
                    show_integral = not show_integral

                elif event.key == game.K_i:
                    if info_show:
                        c_info.rect.bottom = 0
                        w_arrow.rect.top = 0
                        w_arrow.img(transform.flip(w_arrow_pic, False, True))
                    else:
                        c_info.rect.top = 0
                        w_arrow.rect.top = c_info.rect.bottom
                        w_arrow.img(w_arrow_pic)
                    info_show = not info_show

                elif event.key in [game.K_KP_1, game.K_KP1, game.K_1]:
                    int_mode = 1

                elif event.key in [game.K_KP_2, game.K_KP2, game.K_2]:
                    int_mode = 2

                elif event.key in [game.K_KP_3, game.K_KP3, game.K_3]:
                    int_mode = 3
            #Mouse wheel:
            if event.type == game.MOUSEWHEEL:
                if event.y == 1:
                    MainCamera.size = tuple(MainCamera.size[i] / MainCamera.zoom_koef for i in range(2))
                    MainCamera.speed /= MainCamera.zoom_koef

                if event.y == -1:
                    MainCamera.size = tuple(MainCamera.size[i] * MainCamera.zoom_koef for i in range(2))
                    MainCamera.speed *= MainCamera.zoom_koef
            #Mouse button down:
            if event.type == game.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if (event.pos[0] > w_arrow.rect.left and event.pos[0] < w_arrow.rect.right and
                        event.pos[1] > w_arrow.rect.top and event.pos[1] < w_arrow.rect.bottom):
                        actions['tap on width arrow'] = True
                    else:
                        x1 = MainCamera.x + (event.pos[0] - WIDTH / 2) * MainCamera.size[0] / WIDTH
                        mouse_but[1] = True
                        result = None
                if event.button in [2, 3]:
                    mouse_but[event.button] = True
            #Mouse button up:
            if event.type == game.MOUSEBUTTONUP:
                if event.button == 1:
                    if (event.pos[0] > w_arrow.rect.left and event.pos[0] < w_arrow.rect.right and
                        event.pos[1] > w_arrow.rect.top and event.pos[1] < w_arrow.rect.bottom and
                        actions['tap on width arrow']):
                        if info_show:
                            c_info.rect.bottom = 0
                            w_arrow.rect.top = 0
                            w_arrow.img(transform.flip(w_arrow_pic, False, True))
                        else:
                            c_info.rect.top = 0
                            w_arrow.rect.top = c_info.rect.bottom
                            w_arrow.img(w_arrow_pic)
                        info_show = not info_show
                if event.button in [1, 2, 3]:
                    mouse_but[event.button] = False
                actions['tap on width arrow'] = False
            #Mouse moution:
            if event.type == game.MOUSEMOTION:
                if mouse_but[3]:
                    k = MainCamera.size[0] / WIDTH
                    x, y = event.rel
                    x *= -k
                    y *= k
                    MainCamera.x += x
                    MainCamera.y += y

        #Sign of vector Oy:
        sign = -1 if Y_positive_vector_is_up else 1
        #Control of camera:
        if actions['up']:
            MainCamera.y -= MainCamera.speed * sign
        if actions['down']:
            MainCamera.y += MainCamera.speed * sign
        if actions['left']:
            MainCamera.x -= MainCamera.speed
        if actions['right']:
            MainCamera.x += MainCamera.speed

        #Select integral region:
        if mouse_but[1]:
            #x2 = ((getMousePos()[0] * 2 / WIDTH - 1) * MainCamera.size[0] + MainCamera.pos[0]) / 2
            x2 = MainCamera.x + (getMousePos()[0] - WIDTH / 2) * MainCamera.size[0] / WIDTH
            result = None

        #For redraw:
        list(map(lambda i: i.delete(),
                 all_lines.sprites() +
                 all_rects.sprites() +
                 all_trapezoids.sprites() +
                 all_curve_trapezoids.sprites()))

        #Redraw objects:
        if show_function:
            draw_function(func = f,
                          cuts = c)
        if show_integral:
            if int_mode == 1:
                draw_integral_rects(func = f,
                                    start = x1,
                                    end = x2,
                                    cuts = c,
                                    sample = samp)
            elif int_mode == 2:
                draw_integral_trapezoid(func = f,
                                        start = x1,
                                        end = x2,
                                        cuts = c)
            elif int_mode == 3:
                draw_integral_curve_trapezoid(func = f,
                                        start = x1,
                                        end = x2,
                                        cuts = c)

        draw_axes()

        #Integral value:
        if result is None :
            if int_mode == 1:
                result = integral_calculate_rect(func = f,
                                                 start = x1,
                                                 end = x2,
                                                 cuts = c,
                                                 sample = samp)
            elif int_mode == 2:
                result = integral_calculate_trapezoid(func = f,
                                                      start = x1,
                                                      end = x2,
                                                      cuts = c)
            elif int_mode == 3:
                result = integral_calculate_curve_trapezoid(func = f,
                                                            start = x1,
                                                            end = x2,
                                                            cuts = c)

        #Draw all:
        AllUpdate(screen, all_sprites, (0, 0, 0), flip = False)
        t = 'F(x) = ' + f_str
        draw_text(surf = screen,
                  text = t,
                  size = 20,
                  x = 10,
                  y = 20,
                  color = WHITE)
        t = 'RESULT : ' + str(result[0])
        draw_text(surf = screen,
                  text = t,
                  size = 20,
                  x = 10,
                  y = 40,
                  color = GREEN if result[1] else RED)
        game.display.flip()
    game.quit()
