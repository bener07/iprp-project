import turtle
import math
import time


def infinity_signal(tur, screen):
    a = 5
    t = 0
    while t <= 2*3.1415926535897932384626433832:
        x = math.sin(t)*a*10
        y = math.sin(2*t)*17
        tur.setposition(x,y)
        screen.update()
        time.sleep(0.016)
        t += 0.1

screen = turtle.Screen()
screen.title("Space Invaders IPRP")
screen.bgcolor("white")
screen.setup(width=500, height=500)
screen.tracer(0)
screen.addshape("enemy.gif")

t = turtle.Turtle(visible=False)
t.shape("enemy.gif")
t.setposition(0, 0)

infinity_signal(t, screen)