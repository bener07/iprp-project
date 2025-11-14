#!/bin/python3
import turtle
import time


STATE = {}


def criar_entidade(x,y):
    t = turtle.Turtle(visible=True)
    t.shape("player.gif")
    t.setposition(x,y)
    t.showturtle()
    return t

def move():
    print("Clicado")
    player = STATE["player"]
    print(player.getpos())
    exit()
    new_x = player.x + direction*10
    player.goto(new_x, y)



screen = turtle.Screen()
screen.title("Testing Turtle Screen")
screen.bgcolor("white")
screen.tracer(0)
screen.onkeypress(move, "a")

screen.addshape("player.gif")

STATE["player"] = criar_entidade(0,0)
STATE["screen"] = screen
while True:
    screen.update()
    time.sleep(0.001)
