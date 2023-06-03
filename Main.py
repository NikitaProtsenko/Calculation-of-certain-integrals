from math import *
import pygame
from ForGame import *

screen = NewScreen(WIDTH, HEIGHT, 'Integral calculation')
running = True
fps=60

class Line(pygame.sprite.Sprite):
    def __init__(self,pos,x,y):
        pygame.sprite.Sprite.__init__(self)
        if pos=="x": # Ã®Ã±Ã¼ Ã Ã¡Ã±Ã¶Ã¨Ã±Ã±
            self.image=pygame.Surface((3,400)) # Ã«Ã¨Ã­Ã¨Ã¿ 3x400
            self.image.fill((0,0,0)) # Ã§Ã ÃªÃ°Ã Ã±Ã¨Ã²Ã¼ Ã·Ã¥Ã°Ã­Ã»Ã¬ Ã¶Ã¢Ã¥Ã²Ã®Ã¬
            self.rect = self.image.get_rect()
            self.rect.centerx = x # Ã¶Ã¥Ã­Ã²Ã° Ã¯Ã® x
            self.rect.centery = y # Ã¶Ã¥Ã­Ã²Ã° Ã¯Ã® y
        elif pos=="y": # Ã®Ã±Ã¼ Ã®Ã°Ã¤Ã¨Ã­Ã Ã² 
            self.image=pygame.Surface((400,3)) # Ã«Ã¨Ã­Ã¨Ã¿ 3x400
            self.image.fill((0,0,0)) # Ã§Ã ÃªÃ°Ã Ã±Ã¨Ã²Ã¼ Ã·Ã¥Ã°Ã­Ã»Ã¬ Ã¶Ã¢Ã¥Ã²Ã®Ã¬
        if pos=="x": # îñü àáñöèññ
            self.image=pygame.Surface((1,400)) # ëèíèÿ 3x400
            self.image.fill((0,0,0)) # çàêðàñèòü ÷åðíûì öâåòîì
            self.rect = self.image.get_rect()
            self.rect.centerx = x # öåíòð ïî x
            self.rect.centery = y # öåíòð ïî y
        elif pos=="y": # îñü îðäèíàò 
            self.image=pygame.Surface((400,1)) # ëèíèÿ 3x400
            self.image.fill((0,0,0)) # çàêðàñèòü ÷åðíûì öâåòîì
            self.rect = self.image.get_rect()
            self.rect.centerx = x # Ã¶Ã¥Ã­Ã²Ã° Ã¯Ã® x
            self.rect.centery = y # Ã¶Ã¥Ã­Ã²Ã° Ã¯Ã® y
class Dot(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.surface.Surface((5,5)) # Ã²Ã®Ã·ÃªÃ  5x5
        self.image.fill((0,0,0)) # Ã§Ã ÃªÃ°Ã Ã±Ã¨Ã²Ã¼ Ã·Ã¥Ã°Ã­Ã»Ã¬ Ã¶Ã¢Ã¥Ã²Ã®Ã¬
        self.image=pygame.surface.Surface((1,1)) # òî÷êà 5x5
        self.image.fill((0,0,0)) # çàêðàñèòü ÷åðíûì öâåòîì
        self.rect=self.image.get_rect()
        self.rect.centerx=x # Ã¶Ã¥Ã­Ã²Ã° Ã¯Ã® x
        self.rect.centery=y # Ã¶Ã¥Ã­Ã²Ã° Ã¯Ã® y
def Calc(func):
    i=-10 # Ã­Ã Ã·Ã Ã«Ã¼Ã­Ã®Ã¥ Ã§Ã­Ã Ã·Ã¥Ã­Ã¨Ã¥ Ã Ã°Ã£Ã³Ã¬Ã¥Ã­Ã²Ã 
    while i<=10: # Ã¯Ã®ÃªÃ  Ã Ã°Ã£Ã³Ã¬Ã¥Ã­Ã² Ã¬Ã¥Ã­Ã¼Ã¸Ã¥ 10
        mass="" # Ã²Ã¥Ã¬Ã¯-Ã±Ã²Ã°Ã®ÃªÃ 
        for j in func: # Ã¤Ã«Ã¿ ÃªÃ Ã¦Ã¤Ã®Ã£Ã® Ã±Ã¨Ã¬Ã¢Ã®Ã«Ã  Ã¢ Ã±Ã²Ã°Ã®ÃªÃ¥ func(Ã­Ã Ã¸Ã  Ã´Ã³Ã­ÃªÃ¶Ã¨Ã¿)
            if j == "x": # Ã¥Ã±Ã«Ã¨ Ã±Ã¨Ã¬Ã¢Ã®Ã« = x, Ã²Ã® Ã¤Ã®Ã¡Ã Ã¢Ã«Ã¿Ã¥Ã¬ i Ã¢ Ã²Ã¥Ã¬Ã¯-Ã±Ã²Ã°Ã®ÃªÃ³
                mass+=str(i)
            else: # Ã¥Ã±Ã«Ã¨ Ã­Ã¥Ã², Ã²Ã® Ã¤Ã®Ã¡Ã Ã¢Ã¨Ã²Ã¼ Ã¨Ã±ÃµÃ®Ã¤Ã­Ã»Ã© Ã±Ã¨Ã¬Ã¢Ã®Ã«
                mass+=j
            i+=0.0001 # Ã³Ã¢Ã¥Ã«Ã¨Ã·Ã¨Ã²Ã¼ Ã Ã°Ã£Ã³Ã¬Ã¥Ã­Ã² Ã­Ã  0.0001
        try:
          res1=eval(mass) # Ã¯Ã®Ã±Ã·Ã¨Ã²Ã Ã²Ã¼ Ã´Ã³Ã­ÃªÃ¶Ã¨Ã¾ Ã¨ Ã¯Ã®Ã«Ã³Ã·Ã¨Ã²Ã¼ Ã°Ã¥Ã§Ã³Ã«Ã¼Ã²Ã Ã²
        except:
          res1=10000 # Ã¥Ã±Ã«Ã¨ Ã´Ã³Ã­ÃªÃ¶Ã¨Ã¾ Ã­Ã¥Ã«Ã¼Ã§Ã¿ Ã¯Ã®Ã±Ã·Ã¨Ã²Ã Ã²Ã¼, Ã²Ã® Ã°Ã¥Ã§Ã³Ã«Ã¼Ã²Ã Ã² Ã·Ã¨Ã±Ã«Ã® Ã¢Ã­Ã¥ ÃªÃ®Ã®Ã°Ã¤Ã¨Ã­Ã Ã²(Ã§Ã­Ã Ã¾, ÃªÃ®Ã±Ã²Ã»Ã«Ã¼)
        dot=Dot(250+i*10,250-res1*10) # dot - Ã²Ã®Ã·ÃªÃ  Ã± ÃªÃ®Ã®Ã°Ã¤Ã¨Ã­Ã Ã²Ã®Ã©(0+x,0+y), Ã²Ã Ãª ÃªÃ Ãª Ã½Ã²Ã® Ã¤Ã¨Ã±Ã¯Ã«Ã¥Ã©, Ã²Ã® Ã¢Ã¥ÃªÃ²Ã®Ã° "y" Ã­Ã Ã¯Ã°Ã Ã¢Ã«Ã¥Ã­ Ã¢Ã­Ã¨Ã§
        all_sprites.add(dot) # Ã¤Ã®Ã¡Ã Ã¢Ã¨Ã²Ã¼ Ã²Ã®Ã·ÃªÃ³ Ã¢ Ã£Ã°Ã³Ã¯Ã¯Ã³ Ã±Ã¯Ã°Ã Ã©Ã²Ã®Ã¢
func = str(input("y = ")) # Ã¢Ã¢Ã®Ã¤ Ã¤Ã Ã­Ã­Ã»Ãµ 
calc = Calc(func) # Ã¢Ã»Ã§Ã¢Ã Ã²Ã¼ Ã´Ã³Ã­ÃªÃ¶Ã¨Ã¾ Calc Ã®Ã² func

line = Line("y",250,250) # Ã¤Ã®Ã¡Ã Ã¢Ã¨Ã²Ã¼ Ã®Ã±Ã¼ Ã®Ã°Ã¤Ã¨Ã­Ã Ã²
all_sprites.add(line)
line1 = Line("x",250,250) # Ã¤Ã®Ã¡Ã Ã¢Ã¨Ã²Ã¼ Ã®Ã±Ã¼ Ã Ã¡Ã±Ã¶Ã¨Ã±Ã±
all_sprites.add(line1)

while running: # Ã®Ã±Ã­Ã®Ã¢Ã­Ã®Ã© Ã¶Ã¨ÃªÃ«
    clock.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # Ã¥Ã±Ã«Ã¨ Ã§Ã ÃªÃ°Ã»Ã« Ã®ÃªÃ­Ã® - Ã§Ã Ã¢Ã¥Ã°Ã¸Ã¨Ã²Ã¼ Ã¯Ã°Ã®Ã£Ã°Ã Ã¬Ã¬Ã³
            running = False
    screen.fill((255,255,255)) # Ã§Ã Ã«Ã¨Ã²Ã¼ Ã¯Ã®Ã«Ã¥ Ã¡Ã¥Ã«Ã»Ã¬ Ã¶Ã¢Ã¥Ã²Ã®Ã¬
    all_sprites.draw(screen) # Ã­Ã Ã°Ã¨Ã±Ã®Ã¢Ã Ã²Ã¼ Ã¢Ã±Ã¥ Ã±Ã¯Ã°Ã Ã©Ã²Ã»(Ã².Ã¥. Ã­Ã Ã¸Ã¨ Ã²Ã®Ã·ÃªÃ¨)
    pygame.display.flip()
pygame.quit()
