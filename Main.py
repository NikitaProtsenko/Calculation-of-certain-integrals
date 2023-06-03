from math import *
from Rect_calc import *
import pygame
from ForGame import *
WIDTH = 600
HEIGHT = 600
screen = newScreen(WIDTH, HEIGHT, 'Integral calculation')
running = True
fps=60

class Line(Sprite):
    def __init__(self,pos,x,y):
        pygame.sprite.Sprite.__init__(self)
        if pos=="x": 
            self.image=pygame.Surface((1,400))
            self.image.fill((0,0,0)) 
            self.rect = self.image.get_rect()
            self.rect.centerx = x 
            self.rect.centery = y 
        elif pos=="y": 
            self.image=pygame.Surface((400,1)) # Ã«Ã¨Ã­Ã¨Ã¿ 3x400
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
pos = (200,200)
line = Line("y",pos[0],pos[1]) # Ã¤Ã®Ã¡Ã Ã¢Ã¨Ã²Ã¼ Ã®Ã±Ã¼ Ã®Ã°Ã¤Ã¨Ã­Ã Ã²
all_sprites.add(line)
line1 = Line("x",pos[0],pos[1]) # Ã¤Ã®Ã¡Ã Ã¢Ã¨Ã²Ã¼ Ã®Ã±Ã¼ Ã Ã¡Ã±Ã¶Ã¨Ã±Ã±
all_sprites.add(line1)
while running: # Ã®Ã±Ã­Ã®Ã¢Ã­Ã®Ã© Ã¶Ã¨ÃªÃ«
    clock.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # Ã¥Ã±Ã«Ã¨ Ã§Ã ÃªÃ°Ã»Ã« Ã®ÃªÃ­Ã® - Ã§Ã Ã¢Ã¥Ã°Ã¸Ã¨Ã²Ã¼ Ã¯Ã°Ã®Ã£Ã°Ã Ã¬Ã¬Ã³
            running = False
    

    screen.fill((255,255,255)) 
    Rect_integral(screen,pos,all_sprites,1,6,"x**2",50)# Ã§Ã Ã«Ã¨Ã²Ã¼ Ã¯Ã®Ã«Ã¥ Ã¡Ã¥Ã«Ã»Ã¬ Ã¶Ã¢Ã¥Ã²Ã®Ã¬
    all_sprites.draw(screen) # Ã­Ã Ã°Ã¨Ã±Ã®Ã¢Ã Ã²Ã¼ Ã¢Ã±Ã¥ Ã±Ã¯Ã°Ã Ã©Ã²Ã»(Ã².Ã¥. Ã­Ã Ã¸Ã¨ Ã²Ã®Ã·ÃªÃ¨)
    pygame.display.flip()
pygame.quit()
