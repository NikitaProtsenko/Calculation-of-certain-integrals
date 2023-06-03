from math import *
import pygame 
pygame.init() # ��������� pygame
screen = pygame.display.set_mode((500,500)) # ������� ���� 500x500
pygame.display.set_caption("func_graph") # �������� ����
all_sprites=pygame.sprite.Group() # ������ ��������  
clock = pygame.time.Clock() 
running = True
fps=60
class Line(pygame.sprite.Sprite):
    def __init__(self,pos,x,y):
        pygame.sprite.Sprite.__init__(self)
        if pos=="x": # ��� �������
            self.image=pygame.Surface((3,400)) # ����� 3x400
            self.image.fill((0,0,0)) # ��������� ������ ������
            self.rect = self.image.get_rect()
            self.rect.centerx = x # ����� �� x
            self.rect.centery = y # ����� �� y
        elif pos=="y": # ��� ������� 
            self.image=pygame.Surface((400,3)) # ����� 3x400
            self.image.fill((0,0,0)) # ��������� ������ ������
            self.rect = self.image.get_rect()
            self.rect.centerx = x # ����� �� x
            self.rect.centery = y # ����� �� y
class Dot(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.surface.Surface((5,5)) # ����� 5x5
        self.image.fill((0,0,0)) # ��������� ������ ������
        self.rect=self.image.get_rect()
        self.rect.centerx=x # ����� �� x
        self.rect.centery=y # ����� �� y
def Calc(func):
    i=-10 # ��������� �������� ���������
    while i<=10: # ���� �������� ������ 10
        mass="" # ����-������
        for j in func: # ��� ������� ������� � ������ func(���� �������)
            if j == "x": # ���� ������ = x, �� ��������� i � ����-������
                mass+=str(i)
            else: # ���� ���, �� �������� �������� ������
                mass+=j
            i+=0.0001 # ��������� �������� �� 0.0001
        try:
          res1=eval(mass) # ��������� ������� � �������� ���������
        except:
          res1=10000 # ���� ������� ������ ���������, �� ��������� ����� ��� ���������(����, �������)
        dot=Dot(250+i*10,250-res1*10) # dot - ����� � �����������(0+x,0+y), ��� ��� ��� �������, �� ������ "y" ��������� ����
        all_sprites.add(dot) # �������� ����� � ������ ��������
func = str(input("y = ")) # ���� ������ 
calc = Calc(func) # ������� ������� Calc �� func

line = Line("y",250,250) # �������� ��� �������
all_sprites.add(line)
line1 = Line("x",250,250) # �������� ��� �������
all_sprites.add(line1)

while running: # �������� ����
    clock.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # ���� ������ ���� - ��������� ���������
            running = False
    screen.fill((255,255,255)) # ������ ���� ����� ������
    all_sprites.draw(screen) # ���������� ��� �������(�.�. ���� �����)
    pygame.display.flip()
pygame.quit()