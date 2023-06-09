from ForGame import *
from math import sin, cos, tan, asin, acos, atan, sinh, cosh, log, pi, e
from pyautogui import prompt

#Missing math functions:
def cotan(x):
    """Return the cotangent of x (measured in radians)."""
    return 1 / tan(x)

def acotan(x):
    """Return the arc cotangent of x (measured in radians)."""
    return pi / 2 - atan(x)

def ln(x):
    """Return the natural logarithm of x."""
    return log(x)

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

#Pictures:
picture = {}
picture['width arrow up'] = Image('width_arrow_up.png')
picture['control info'] = Image('control_info.png')

#Run-flag:
running = True

#Positive vector Oy:
Y_positive_vector_is_up = True

#Current actions:
actions = {'up': False, 'down': False, 'left': False, 'right': False}

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
    def x(self):
        return self.pos[0]

    @x.setter
    def x(self, value: float):
        self.pos = value, self.pos[1]

    @property
    def y(self):
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

def new_function(func: str):
    """Return function from string func.
func - string of function of one var x."""
    def res(x: float):
        """Function with var x."""
        s = func
        return eval(s)
    return res

def draw_axes():
    """Draw axes of plane."""
    pass

def draw_function(func: function, cuts: int = 100):
    """Draw visible part of function on screen.
func - function of one var x,
cuts - splitting of visible segment of function."""
    X, Y = MainCamera.pos
    W, H = MainCamera.size
    xmin = X - W / 2
    xmax = xmin + W
    dx = (xmax - xmin) / cuts
    ps = []
    for i in range(cuts + 1):
        x = xmin + i * dx
        try:
            y = func(x)
        except:
            y = None
        if not type(y) in [int, float]:
            y = None
        ps += [(x, y)]
    for i in range(1, len(ps)):
        if ps[i - 1][1] is None or ps[i][1] is None:
            continue
        figLine(p1 = ps[i - 1],
                p2 = ps[i],
                color = (255, 255, 255))

def draw_integral_rects(func: function, start: float = 0, end: float = 10, cuts: int = 100, sample: float = 0, cl = (0, 255, 0)):
    """Draw rectangles of integral sum.
func - function of one var x,
start - bottom limit of integral,
end - top limit of integral,
cuts - splitting of segment,
sample - x point of segment [0; 1] of calculating."""
    if end < start:
        draw_integral_rects(func, end, start, cuts, sample, (255, 0, 0))
        return
    X, Y = MainCamera.pos
    W, H = MainCamera.size
    xmin = X - W / 2
    xmax = xmin + W
    dx = (end - start) / cuts
    ps = []
    for i in range(cuts):
        x = start + i * dx
        if x < start or x > end:
            continue
        try:
            y = func(x + dx * sample)
        except:
            y = None
        if not type(y) in [int, float]:
            y = None
        ps += [(x, y)]
    for i in range(1, len(ps)):
        x1, y1 = ps[i]
        if y1 is None:
            continue
        x2 = x1 + dx
        y2 = 0
        if x1 > x2:
            x1, x2 = x2, x1
        if y1 > y2:
            y1, y2 = y2, y1
        figRect(pos = (x1, y1),
                size = (x2 - x1, y2 - y1),
                color = cl)

def integral_calculate_rect(func: function, start: float = 0, end: float = 10, cuts: int = 100, sample: float = 0):
    """Return value of integral of function and False if function exactly has a singularity else True.
func - function of one var x,
start - bottom limit of integral,
end - top limit of integral,
cuts - splitting of segment,
sample - x point of segment [0; 1] of calculating."""
    S = 0
    prev_y = None
    flag = True
    if start > end:
        value,flag = integral_calculate_rect(func,end,start,cuts,sample)
        return (-value,flag)
    dx = (end - start) / cuts
    for i in range(cuts):
        x = start + i * dx
        if x < start or x > end:
            continue
        try:
            y = func(x + dx * sample)
            if not type(y) in [int, float]:
                y = None
                flag = False
            else:
                if not prev_y is None and abs(y - prev_y) > maxdy * dx:
                    flag = False
                S = S + dx*y
        except:
            # In case of uncertainty, we output False.  
            # This means that the integral can be calculated incorrectly.
            flag = False
    return S, flag

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
c_info = None
w_arrow = None
f_str = None
f = None
c = None
x1 = None
x2 = None
samp = None
maxdy = None
WHITE = (255,255,255)
GREEN = (0,255,0)
RED = (255,0,0)

def onStart():
    """Start function."""
    global f,f_str, c, x1, x2, samp, c_info
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
    c_info = Sprite(transform.scale(picture['control info'], (512, 128)), (0, 0))
    c_info.rect.topright = (WIDTH, 0)
    w_arrow = Sprite(transform.scale(picture['width arrow up'], (32, 16)), (0, 0))
    w_arrow.rect.midtop = c_info.rect.midbottom

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
                
                if event.key == game.K_DOWN or event.key == game.K_s:
                    actions['down'] = False
                
                if event.key == game.K_LEFT or event.key == game.K_a:
                    actions['left'] = False
                
                if event.key == game.K_RIGHT or event.key == game.K_d:
                    actions['right'] = False

                if event.key == game.K_f:
                    f_str = prompt(text = 'Enter the function:',
                                   title = 'Function',
                                   default = f_str)
                    f = new_function(f_str)
                    result = None

                if event.key == game.K_r:
                    x1 = float(prompt(text = 'Enter start of integral',
                                      title = 'Region',
                                      default = str(x1)))
                    x2 = float(prompt(text = 'Enter end of integral',
                                      title = 'Region',
                                      default = str(x2)))
                    result = None

                if event.key == game.K_m:
                    c = int(prompt(text = 'Enter the spliting:',
                                   title = 'Spliting',
                                   default = str(c)))
                    result = None
                    
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
                    #x1 = ((event.pos[0] * 2 / WIDTH - 1) * MainCamera.size[0] + MainCamera.pos[0]) / 2
                    x1 = MainCamera.x + (event.pos[0] - WIDTH / 2) * MainCamera.size[0] / WIDTH
                    mouse_but[1] = True
                    result = None
                if event.button in [2, 3]:
                    mouse_but[event.button] = True
            #Mouse button up:
            if event.type == game.MOUSEBUTTONUP:
                if event.button in [1, 2, 3]:
                    mouse_but[event.button] = False
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
        for i in all_lines.sprites():
            i.delete()
        for i in all_rects.sprites():
            i.delete()

        #Redraw objects:
        draw_function(func = f,
                      cuts = c)
        draw_integral_rects(func = f,
                            start = x1,
                            end = x2,
                            cuts = c,
                            sample = samp)

        #Integral value:
        if result is None :
            result = integral_calculate_rect(func = f,
                                             start = x1,
                                             end = x2,
                                             cuts = c,
                                             sample = samp)

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
