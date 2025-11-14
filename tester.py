#!/bin/python3
import turtle
import time


LARGURA, ALTURA = 600, 600
BORDA_X = (LARGURA // 2) # - 20
BORDA_Y = (ALTURA // 2) - 10

PLAYER_SPEED = 20
PLAYER_BULLET_SPEED = 16

ENEMY_ROWS = 3
ENEMY_COLS = 10
ENEMY_SPACING_X = 60
ENEMY_SPACING_Y = 60
ENEMY_SIZE = 32
ENEMY_START_Y = BORDA_Y - ENEMY_SIZE    # topo visível
ENEMY_START_X = -BORDA_X + ENEMY_SIZE
ENEMY_FALL_SPEED = 0.5
ENEMY_DRIFT_STEP = 2
ENEMY_FIRE_PROB = 0.006
ENEMY_BULLET_SPEED = 8
ENEMY_INVERT_CHANCE = 0.05
ENEMY_DRIFT_CHANCE = 0.5

COLLISION_RADIUS = 10
HIGHSCORES_FILE = "highscores.txt"
SAVE_FILE = "savegame.txt"
TOP_N = 10

STATE = {}


def criar_entidade(x,y):
    t = turtle.Turtle(visible=True)
    t.shape("enemy.gif")
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

def criar_bala(x, y, tipo):
    t = turtle.Turtle(visible=False)
    t.penup()
    t.setpos(x,y)
    t.shape("square")
    t.shapesize(0.8, 0.08, 5)
    t.color("red")
    # print("[criar_bala] por implementar")
    t.penup()
    t.showturtle()
    return t

def spawn_inimigos_em_grelha(state, posicoes_existentes, dirs_existentes=None):
    enemies = state["enemies"]
    for enemy_row in range(0, ENEMY_ROWS):
        enemies.append([])
        print(ENEMY_START_X, ENEMY_START_Y)
        y_enemy = ENEMY_START_Y - enemy_row*ENEMY_SPACING_X
        for enemy_col in range(0, ENEMY_COLS):
            print("doing something")
            x_enemy = ENEMY_START_X + enemy_col*ENEMY_SPACING_Y
            enemies[enemy_row].append( criar_entidade(x_enemy, y_enemy) )
            state["screen"].update()
            time.sleep(0.05)
    # print("[spawn_inimigos_em_grelha] por implementar")
    return

screen = turtle.Screen()
screen.title("Testing Turtle Screen")
screen.bgcolor("white")
screen.tracer(0)
screen.onkeypress(move, "a")

screen.addshape("enemy.gif")

b = criar_bala(0, -100, '')

# STATE["player"] = criar_entidade(-10,-10)
STATE["screen"] = screen
STATE["enemies"] = []
spawn_inimigos_em_grelha(STATE, None)

while True:
    b.sety(b.pos()[1] + 1)
    screen.update()
    time.sleep(0.015)
