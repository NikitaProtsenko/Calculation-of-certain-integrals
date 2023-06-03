from math import *
import pygame 
pygame.init() # запустить pygame
screen = pygame.display.set_mode((500,500)) # создать окно 500x500
pygame.display.set_caption("func_graph") # название окна
all_sprites=pygame.sprite.Group() # группа спрайтов  
clock = pygame.time.Clock() 
running = True
fps=60
class Line(pygame.sprite.Sprite):
    def __init__(self,pos,x,y):
        pygame.sprite.Sprite.__init__(self)
        if pos=="x": # ось абсцисс
            self.image=pygame.Surface((3,400)) # линия 3x400
            self.image.fill((0,0,0)) # закрасить черным цветом
            self.rect = self.image.get_rect()
            self.rect.centerx = x # центр по x
            self.rect.centery = y # центр по y
        elif pos=="y": # ось ординат 
            self.image=pygame.Surface((400,3)) # линия 3x400
            self.image.fill((0,0,0)) # закрасить черным цветом
            self.rect = self.image.get_rect()
            self.rect.centerx = x # центр по x
            self.rect.centery = y # центр по y
class Dot(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.surface.Surface((5,5)) # точка 5x5
        self.image.fill((0,0,0)) # закрасить черным цветом
        self.rect=self.image.get_rect()
        self.rect.centerx=x # центр по x
        self.rect.centery=y # центр по y
def Calc(func):
    i=-10 # начальное значение аргумента
    while i<=10: # пока аргумент меньше 10
        mass="" # темп-строка
        for j in func: # для каждого символа в строке func(наша функция)
            if j == "x": # если символ = x, то добавляем i в темп-строку
                mass+=str(i)
            else: # если нет, то добавить исходный символ
                mass+=j
            i+=0.0001 # увеличить аргумент на 0.0001
        try:
          res1=eval(mass) # посчитать функцию и получить результат
        except:
          res1=10000 # если функцию нельзя посчитать, то результат число вне координат(знаю, костыль)
        dot=Dot(250+i*10,250-res1*10) # dot - точка с координатой(0+x,0+y), так как это дисплей, то вектор "y" направлен вниз
        all_sprites.add(dot) # добавить точку в группу спрайтов
func = str(input("y = ")) # ввод данных 
calc = Calc(func) # вызвать функцию Calc от func

line = Line("y",250,250) # добавить ось ординат
all_sprites.add(line)
line1 = Line("x",250,250) # добавить ось абсцисс
all_sprites.add(line1)

while running: # основной цикл
    clock.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # если закрыл окно - завершить программу
            running = False
    screen.fill((255,255,255)) # залить поле белым цветом
    all_sprites.draw(screen) # нарисовать все спрайты(т.е. наши точки)
    pygame.display.flip()
pygame.quit()