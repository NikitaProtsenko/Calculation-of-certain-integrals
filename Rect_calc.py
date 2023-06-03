from cmath import rect
import math

from turtle import Screen
from ForGame import *
def calc_function(func : str, x:float):
    s = func.replace("x",str(x))
    return eval(s,{'__builitins__':None},{'math':math})

def Rect_integral(screen,pos:(int,int),a: float,b: float,func:str, section : int):
    dx = (b-a)/section
    result = 0
    for i in range(section):
        x = dx*i+a
        function_calc = calc_function(func,x)
        draw.rect(screen,(0,0,0),(x+pos[0],pos[0],x+pos[0]+dx,pos[1]-function_calc))
        result += function_calc*dx
    return result


