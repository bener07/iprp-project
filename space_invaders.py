#!/bin/python3
import turtle
import random
import time
import os
import sys

from extras import *

# =========================
# Parâmetros / Constantes
# =========================
LARGURA, ALTURA = 700, 600
BORDA_X = (LARGURA // 2) - 20
BORDA_Y = (ALTURA // 2) - 10

PLAYER_SPEED = 20
PLAYER_BULLET_SPEED = 16

ENEMY_ROWS = 2
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

STATE = None  # usado apenas para callbacks do teclado

# ==================
# boolean functions
# ==================

def verifyOutOfBoundariesWidth(x):
    if x <= -BORDA_X+20 or x >= BORDA_X-20:
        return True
    return False

def verifyOutOfBoundariesHeight(y):
    if y <= -BORDA_Y or y >= BORDA_Y:
        return True
    return False



# =========================
# Top Resultados (Highscores)
# =========================
def ler_highscores(filename):
    # print("[ler_highscores] implementado com json, devolve dict")
    return lerJson(filename)

def atualizar_highscores(filename, score):
    armazenar_dict(filename, score)
    # print("[atualizar_highscores] implementado com json, devolve None")

# =========================
# Guardar / Carregar estado (texto)
# =========================
def guardar_estado_txt(filename, state):
    armazenar_dict(filename, state)
    # print("[guardar_estado_txt] implementado com json, devolve None")

def carregar_estado_txt(filename):
    # print("[carregar_estado_txt] implementado com json, devolve dict ou False, caso não encontre")
    return lerJson(filename) # carregar outro jogo já guardado

    

# =========================
# Criação de entidades (jogador, inimigo e balas)
# =========================
def criar_entidade(x,y, tipo="enemy"):
    t = turtle.Turtle(visible=True)
    if tipo == "player":
        t.shape("player.gif")
    else:
        t.shape("enemy.gif")
    t.penup()
    t.setposition(x,y)
    # print("[criar_entidade] por implementar")
    return t 

def criar_bala(x, y, tipo):
    t = turtle.Turtle(visible=False)
    t.penup()
    t.setpos(x,y)
    t.shape("square")
    t.shapesize(0.8, 0.08, 5)
    if tipo == "player":
        t.color("yellow") ## Alterar para utilizar com inimigos
    else:
        t.color("red")
    t.showturtle()
    return t

def spawn_inimigos_em_grelha(state, posicoes_existentes, dirs_existentes=None):
    enemies = state["enemies"]
    for enemy_row in range(0, ENEMY_ROWS):
        print(ENEMY_START_X, ENEMY_START_Y)
        y_enemy = ENEMY_START_Y - enemy_row*ENEMY_SPACING_Y
        for enemy_col in range(0, ENEMY_COLS):
            x_enemy = ENEMY_START_X + enemy_col*ENEMY_SPACING_X
            enemy = criar_entidade(x_enemy, y_enemy)
            enemy.penup()
            enemies.append( enemy )
    # print("[spawn_inimigos_em_grelha] por implementar")
    return

def restaurar_balas(state, lista_pos, tipo):
    # print("[restaurar_balas] por implementar")
    return

# =========================
# Movimento de utilizador
# =========================
def move_player(direction):
    player = STATE["player"]
    x,y = player.pos()
    new_x = x + direction*PLAYER_SPEED
    if verifyOutOfBoundariesWidth(new_x):
        return
    player.setx(new_x)

# =========================
# Handlers de tecl
# =========================
def mover_esquerda_handler():
    move_player(-1)
    # print("[mover_esquerda_handler] por implementar")

def mover_direita_handler():
    move_player(1)
    # print("[mover_direita_handler] por implementar")

def disparar_handler():
    player = STATE["player"]
    x,y = player.pos()
    STATE["player_bullets"].append(criar_bala(x,y+10, "player"))
    # print("[disparar_handler] por implementar")
    return

def gravar_handler():
    # print("[gravar_handler] por implementar")
    return

def terminar_handler():
    # print("[terminar_handler] por implementar")
    return

def power_up_handler():
    # power up por implementar
    return

# =========================
# Atualizações e colisões
# =========================
def atualizar_balas_player(state):
    for bl in state["player_bullets"]:
        x, y = bl.pos()
        if y > BORDA_Y + 20:
            bl.hideturtle()
            state["player_bullets"].remove(bl)
        bl.setpos(x, y + PLAYER_BULLET_SPEED)
    # print("[atualizar_balas_player] por implementar")
    return

def atualizar_balas_inimigos(state):
    for ebl in state["enemy_bullets"]:
        x, y = ebl.pos()
        if y < -BORDA_Y + 20:
            ebl.hideturtle()
            state["enemy_bullets"].remove(ebl)
        ebl.setpos(x, y - ENEMY_BULLET_SPEED)
    # print("[atualizar_balas_inimigos] por implementar")
    return

def atualizar_inimigos(state):
    may_i_drift = determinateEventExecution(ENEMY_DRIFT_CHANCE)
    invert = state["enemy_invert"]
    for enemy in state["enemies"]:
        x, y = enemy.pos()
        new_x = x #+ ENEMY_DRIFT_STEP*may_i_drift*invert
        new_y = y #- ENEMY_FALL_SPEED
        if verifyOutOfBoundariesWidth(new_x+10):
            state["enemy_invert"] = -invert
        enemy.setx(new_x)
        enemy.sety(new_y)
    # print("[atualizar_inimigos] por implementar")
    return

def inimigos_disparam(state):
    for enemy in state["enemies"]:
        x, y = enemy.pos()
        if determinateEventExecution(ENEMY_FIRE_PROB):
            state["enemy_bullets"].append(criar_bala(x,y-10, "enemy"))
    # print("[inimigos_disparam] por implementar")
    return

def verificar_colisoes_player_bullets(state):
    # print("[verificar_colisoes_player_bullets] por implementar")
    return

def verificar_colisoes_enemy_bullets(state):
    for bullet in state["player_bullets"]:
        bx, by = bullet.pos()
        for enemy in state["enemies"]:
            x, y = enemy.pos()
            print(x,y)
            if ((x-bx)**2 + (y - by)**2 <= COLLISION_RADIUS and by >= y) and bullet in state["player_bullets"]:
                print("Atingido")
                enemy.hideturtle()
                bullet.hideturtle()
                state["player_bullets"].remove(bullet)
                state["enemies"].remove(enemy)
    # print("[verificar_colisoes_enemy_bullets] por implementar")
    return

def inimigo_chegou_ao_fundo(state):
    # print("[inimigo_chegou_ao_fundo] por implementar")
    return

def verificar_colisao_player_com_inimigos(state):
    # print("[verificar_colisao_player_com_inimigos] por implementar")
    return

# =========================
# Execução principal
# =========================
if __name__ == "__main__":
    # Pergunta inicial
    filename = input("Carregar jogo? Se sim, escreva nome do ficheiro, se não carregue Return: ").strip()
    loaded = carregar_estado_txt(filename)

    # Ecrã
    screen = turtle.Screen()
    screen.title("Space Invaders IPRP")
    screen.bgcolor("black")
    screen.setup(width=LARGURA, height=ALTURA)
    screen.tracer(0)

    # Imagens obrigatórias
    for img in ["player.gif", "enemy.gif"]:
        if not os.path.exists(img):
            # print("ERRO: imagem '" + img + "' não encontrada.")
            sys.exit(1)
        screen.addshape(img)

    # Estado base
    state = {
        "screen": screen,
        "player": None,
        "enemies": [],
        "enemy_invert": 1,
        "enemy_moves": [],
        "player_bullets": [],
        "enemy_bullets": [],
        "score": 0,
        "frame": 0,
        "files": {"highscores": HIGHSCORES_FILE, "save": SAVE_FILE}
    }

    # Construção inicial
    if isinstance(loaded, dict):
        # print("recebeu-se dicionário")
        sys.exit(0)
    else:
        # print("New game!")
        state["player"] = criar_entidade(0, -200, "player") ## inicial: 0, -350
        spawn_inimigos_em_grelha(state, None, None)

    # Variavel global para os keyboard key handlers
    STATE = state

    # Teclas
    screen.listen()
    screen.onkeypress(mover_esquerda_handler, "a")
    screen.onkeypress(mover_direita_handler, "d")
    screen.onkeypress(disparar_handler, "space")
    screen.onkeypress(gravar_handler, "g")
    screen.onkeypress(terminar_handler, "Escape")
    screen.onkeypress(power_up_handler, "p")

    # Loop principal
    while True:
        atualizar_balas_player(STATE)
        atualizar_inimigos(STATE)
        inimigos_disparam(STATE)
        atualizar_balas_inimigos(STATE)
        verificar_colisoes_player_bullets(STATE)
        
        if verificar_colisao_player_com_inimigos(STATE):
            # print("Colisão direta com inimigo! Game Over")
            terminar_handler()
        
        if verificar_colisoes_enemy_bullets(STATE):
            # print("Atingido por inimigo! Game Over")
            terminar_handler()

        if inimigo_chegou_ao_fundo(STATE):
            # print("Um inimigo chegou ao fundo! Game Over")
            terminar_handler()

        # if len(STATE["enemies"]) == 0:
        #     # print("Vitória! Todos os inimigos foram destruídos.")
        #     terminar_handler()

        STATE["frame"] += 1
        screen.update()
        time.sleep(0.016)
