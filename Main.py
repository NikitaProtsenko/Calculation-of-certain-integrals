from math import *
import pygame
from ForGame import *

screen = NewScreen(WIDTH, HEIGHT, 'Integral calculation')
running = True
fps=60

class Line(pygame.sprite.Sprite):
    def __init__(self,pos,x,y):
        pygame.sprite.Sprite.__init__(self)
        if pos=="x": # îñü àáñöèññ
            self.image=pygame.Surface((3,400)) # ëèíèÿ 3x400
            self.image.fill((0,0,0)) # çàêðàñèòü ÷åðíûì öâåòîì
            self.rect = self.image.get_rect()
            self.rect.centerx = x # öåíòð ïî x
            self.rect.centery = y # öåíòð ïî y
        elif pos=="y": # îñü îðäèíàò 
            self.image=pygame.Surface((400,3)) # ëèíèÿ 3x400
            self.image.fill((0,0,0)) # çàêðàñèòü ÷åðíûì öâåòîì
            self.rect = self.image.get_rect()
            self.rect.centerx = x # öåíòð ïî x
            self.rect.centery = y # öåíòð ïî y
class Dot(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.surface.Surface((5,5)) # òî÷êà 5x5
        self.image.fill((0,0,0)) # çàêðàñèòü ÷åðíûì öâåòîì
        self.rect=self.image.get_rect()
        self.rect.centerx=x # öåíòð ïî x
        self.rect.centery=y # öåíòð ïî y
def Calc(func):
    i=-10 # íà÷àëüíîå çíà÷åíèå àðãóìåíòà
    while i<=10: # ïîêà àðãóìåíò ìåíüøå 10
        mass="" # òåìï-ñòðîêà
        for j in func: # äëÿ êàæäîãî ñèìâîëà â ñòðîêå func(íàøà ôóíêöèÿ)
            if j == "x": # åñëè ñèìâîë = x, òî äîáàâëÿåì i â òåìï-ñòðîêó
                mass+=str(i)
            else: # åñëè íåò, òî äîáàâèòü èñõîäíûé ñèìâîë
                mass+=j
            i+=0.0001 # óâåëè÷èòü àðãóìåíò íà 0.0001
        try:
          res1=eval(mass) # ïîñ÷èòàòü ôóíêöèþ è ïîëó÷èòü ðåçóëüòàò
        except:
          res1=10000 # åñëè ôóíêöèþ íåëüçÿ ïîñ÷èòàòü, òî ðåçóëüòàò ÷èñëî âíå êîîðäèíàò(çíàþ, êîñòûëü)
        dot=Dot(250+i*10,250-res1*10) # dot - òî÷êà ñ êîîðäèíàòîé(0+x,0+y), òàê êàê ýòî äèñïëåé, òî âåêòîð "y" íàïðàâëåí âíèç
        all_sprites.add(dot) # äîáàâèòü òî÷êó â ãðóïïó ñïðàéòîâ
func = str(input("y = ")) # ââîä äàííûõ 
calc = Calc(func) # âûçâàòü ôóíêöèþ Calc îò func

line = Line("y",250,250) # äîáàâèòü îñü îðäèíàò
all_sprites.add(line)
line1 = Line("x",250,250) # äîáàâèòü îñü àáñöèññ
all_sprites.add(line1)

while running: # îñíîâíîé öèêë
    clock.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # åñëè çàêðûë îêíî - çàâåðøèòü ïðîãðàììó
            running = False
    screen.fill((255,255,255)) # çàëèòü ïîëå áåëûì öâåòîì
    all_sprites.draw(screen) # íàðèñîâàòü âñå ñïðàéòû(ò.å. íàøè òî÷êè)
    pygame.display.flip()
pygame.quit()
