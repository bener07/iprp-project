import turtle
import math
import time
from space_invaders import LARGURA, ALTURA

# =================
# Design Functions
# =================

def drawn_life(ix, iy, l): #"print" dos corações que representam as vidas
    t = turtle.Turtle(visible=True)
    t.penup()
    t.setx(ix + l*40)
    t.sety(iy)
    t.shape("heart.gif")
    return t

def writeOnScreen(text, x, y, color, state, align='center', font=('Arial', 10, "normal"), keep=False): #função que limpa a tela e escreve as frases pedidas quando é chamada
    if state["panelWriter"] != None:
        writer = state["panelWriter"]
    else:
        writer = turtle.Turtle(visible=False)
        state["panelWriter"] = writer
    if not keep:
        writer.clear()
    writer.hideturtle()
    writer.penup()
    writer.goto(x,y)
    writer.color(color)
    writer.write(text, align=align, font=font)

def panel(state): #mostrar o score no canto da tela e pedir á função de desenhar as vidas para o fazer 
    writeOnScreen(
        "Score: "+str(state["score"]),
        -LARGURA/2+10,
        ALTURA/2-50,
        "white",
        state,
        align='left',
        font=('Arial', 30, 'bold')
    )
    for i in range(state["lifes"]):
        state["life_dummies"].append(drawn_life(LARGURA/2-40*state["lifes"], ALTURA/2-20, i))


def atualizar_panel(state): #atualizar a função anterior
    writeOnScreen(
        "Score: "+str(state["score"]),
        -LARGURA/2+10,
        ALTURA/2 - 50,
        "white",
        state,
        align='left',
        font=('Arial', 30, 'bold')
    )
    for life in state["life_dummies"]:
        life.hideturtle()

    for i in range(state["lifes"]):
        state["life_dummies"][i].showturtle()

    state["player"].showturtle()

## Animação do infinito com um enemy

def infinity_signal(tur, screen): #função usada para criar o inimigo que aparece a fazer o simbolo de infinito na tela final
    a = 5
    t = 0
    ix, iy = tur.pos()
    while t <= 2*3.1415926535897932384626433832:
        x = ix + math.sin(t)*a*10
        y = iy + math.sin(2*t)*17
        tur.goto(x,y)
        screen.update()
        time.sleep(0.020)
        t += 0.1
