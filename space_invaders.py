import turtle
import random
import time
import os
import sys
from playsound import playsound
import math

# =========================
# Parâmetros / Constantes
# =========================
LARGURA, ALTURA = 700, 600
BORDA_X = (LARGURA // 2) - 20
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

PLAY_SOUND = False

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

def determinateEventExecution(probability):
    return random.random() < probability


# =================
# Design Functions
# =================

def drawn_life(ix, iy, l): #extra
    t = turtle.Turtle(visible=True)
    t.penup()
    t.setx(ix + l*40)
    t.sety(iy)
    t.shape("heart.gif")
    return t

def writeOnScreen(text, x, y, color, align='center', font=('Arial', 10, "normal"), keep=False):
    if STATE["panelWriter"] != None:
        writer = STATE["panelWriter"]
    else:
        writer = turtle.Turtle(visible=False)
        STATE["panelWriter"] = writer
    if not keep:
        writer.clear()
    writer.hideturtle()
    writer.penup()
    writer.goto(x,y)
    writer.color(color)
    writer.write(text, align=align, font=font)

def panel(state): #extra
    writeOnScreen(
        "Score: "+str(state["score"]),
        -LARGURA/2+10,
        ALTURA/2-50,
        "white",
        align='left',
        font=('Arial', 30, 'bold')
    )
    for i in range(state["lifes"]):
        state["life_dummies"].append(drawn_life(LARGURA/2-40*state["lifes"], ALTURA/2-20, i))


def atualizar_panel(state): #extra
    writeOnScreen(
        "Score: "+str(state["score"]),
        -LARGURA/2+10,
        ALTURA/2 - 50,
        "white",
        align='left',
        font=('Arial', 30, 'bold')
    )
    for life in state["life_dummies"]:
        life.hideturtle()

    for i in range(state["lifes"]):
        state["life_dummies"][i].showturtle()

    state["player"].showturtle()

# =========================
# Top Resultados (Highscores)
# =========================
def ler_highscores(filename):
    highscores=[]
    if os.path.exists(filename):
        f = open(filename, 'r')
        linhas = f.readlines()
        f.close()
        for linha in linhas:
            linha=linha.strip("\n")
            username, pontos = linha.split(":")
            highscores.append((username, int(pontos)))
    firstValue = return_value_n(1)
    highscores.sort(key=firstValue, reverse=True) 
    return highscores[:TOP_N] #vai devolver os highscores ordenados até chegar ao numero maximo. (TOP 10)

def return_value_n(n):
    def re(x):
        return x[n]
    return re

def atualizar_highscores(filename, score):
    highscores = ler_highscores(filename)
    if len(highscores)<TOP_N or score>highscores[-1][1]:
        username=input("É CAMELO o teu score foi "+ str(score)+" in chock :O ... \nVá escreve lá o teu nome para ficar registado")
        highscores.append((username,score))
        firstValue = return_value_n(1)
        highscores.sort(key=firstValue, reverse=True) 
        highscores = highscores[:TOP_N]

        f=open(filename,"w")
        for username, score in highscores:
            f.write(username+":"+str(score)+"\n")
        f.close()
        print("tá guardado chefe \n")

    print("\n=== TOP HIGHSCORES ===")
    for i in highscores:
        print(i[0]+":"+str(i[1]))

# =========================
# Guardar / Carregar estado (texto)
# =========================
def guardar_estado_txt(filename, state):
    guardar_jogo={
        "player_pos": state["player"].pos(),
        "enemies_pos": [(*enemy.pos(), state["enemy_moves"][k]) for k, enemy in enumerate(state["enemies"])],
        "enemy_moves": state["enemy_moves"],
        "player_bullets": [b.pos() for b in state["player_bullets"]],
        "enemy_bullets": [b.pos() for b in state["enemy_bullets"]],
        "score": state["score"],
        "frame": state["frame"],
        "lifes": state["lifes"]
    }
    f = open(filename, "w")

    def saveDict(key, strPreFix):
        for values in guardar_jogo[key]:
            guardarDataEmFicheiro(strPreFix, values)

    def guardarDataEmFicheiro(name, savingData):
        f.write(name + ":" + ",".join([str(val) for val in savingData]) + "\n" )

    #player
    guardarDataEmFicheiro("player", guardar_jogo["player_pos"])

    # Inimigos
    saveDict("enemies_pos", "enemy")

    # Balas do jogador
    saveDict("player_bullets", "pbullet")

    # Balas dos inimigos
    saveDict("enemy_bullets", "ebullet")

    # Score e frame
    for dataToSaveFromState in ['score', 'frame', 'lifes']:
        guardarDataEmFicheiro(dataToSaveFromState, (guardar_jogo[dataToSaveFromState],) )

    f.close()
    print("Jogo guardado em " + filename)
    return True

def carregar_estado_txt(filename):
    if not filename or not os.path.exists(filename):
        print(f"Ficheiro {filename} não encontrado. Iniciando novo jogo.")
        return False
    state={
        'score': 0,
        'frame': 0,
        'enemies': [],
        'enemy_moves': [],
        'player_bullets': [],
        'enemy_bullets': [],
        'player_pos': (0, -350)
    }
    f = open(filename, 'r')
    for linha in f:
        linha = linha.strip()
        if not linha or ':' not in linha:
            continue
        
        tipo, dados = linha.split(':', 1)
        
        if tipo == "score":
            state['score'] = int(dados)
        elif tipo == "frame":
            state['frame'] = int(dados)
        elif tipo == "player":
            x, y = dados.split(',')
            state['player_pos'] = (float(x), float(y))
        elif tipo == "enemy":
            x, y, direction = dados.split(',')
            state['enemies'].append((float(x), float(y), int(direction)))
            state["enemy_moves"].append(int(direction))
        elif tipo == "pbullet":
            x, y = dados.split(',')
            state['player_bullets'].append((float(x), float(y)))
        elif tipo == "ebullet":
            x, y = dados.split(',')
            state['enemy_bullets'].append((float(x), float(y)))
    
    f.close()
    print(f"Jogo carregado de {filename}")
    return state

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
    t.shapesize(0.8, 0.09, 1)
    if tipo == "player":
        t.color("yellow") ## Alterar para utilizar com inimigos
    else:
        t.color("red")
    t.showturtle()
    return t

def spawn_inimigos_em_grelha(state, posicoes_existentes, dirs_existentes=None):
    enemies = state["enemies"]
    for enemy_row in range(0, ENEMY_ROWS):
        y_enemy = ENEMY_START_Y - enemy_row*ENEMY_SPACING_Y
        for enemy_col in range(0, ENEMY_COLS):
            x_enemy = ENEMY_START_X + enemy_col*ENEMY_SPACING_X
            enemy = criar_entidade(x_enemy, y_enemy)
            state["enemy_moves"].append(1 if determinateEventExecution(ENEMY_INVERT_CHANCE) else -1)
            enemy.penup()
            enemies.append( enemy )
    # print("[spawn_inimigos_em_grelha] por implementar")
    return

def restaurar_balas(state, lista_pos, tipo):
    for x,y in lista_pos:
        state[tipo+"_bullets"].append(criar_bala(x,y, tipo))

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
# Handlers de teclado
# =========================
def mover_esquerda_handler():
    move_player(-1)
    # print("[mover_esquerda_handler] por implementar")

def mover_direita_handler():
    move_player(1)
    # print("[mover_direita_handler] por implementar")

def disparar_handler():
    # if len(STATE["player_bullets"]) != 0:
    #     return
    player = STATE["player"]
    x,y = player.pos()
    STATE["player_bullets"].append(criar_bala(x,y+10, "player"))
    playsound("./pewpew.mp3", block=False)
    # print("[disparar_handler] por implementar")
    return

def gravar_handler():
    filename=input("nome do ficheiro que vai ficar guardado men ").strip()
    guardar_estado_txt(filename,STATE)
    print("tá gravado cromo")
    return

def infinity_signal(tur, screen):
    a = 5
    t = 0
    ix, iy = tur.pos()
    while t <= 2*3.1415926535897932384626433832:
        x = ix+ math.sin(t)*a*10
        y = iy+math.sin(2*t)*17
        tur.goto(x,y)
        screen.update()
        time.sleep(0.032)
        t += 0.1


def terminar_handler():
    if STATE.get("jogo_terminado", False):
        return #evitar chamar várias vezes o terminar o jogo, deu varios erros não fixes
    
    STATE["jogo_terminado"] = True
    time.sleep(0.06)

    screen = STATE["screen"]
    screen.clear()
    screen.bgcolor("black")

    writeOnScreen("Fim do jogo!", 0, 20, "white", align="center", font=('Arial', 40, "bold"))
    infinity_signal(criar_entidade(0,-17, "enemy"), screen)
    writeOnScreen("Volta ao terminal para receberes novas instruções", 0, -70, "white", align="center", font=('Arial', 14, "bold"), keep=True)

    game_over_dummy = turtle.Turtle(visible=False)
    game_over_dummy.shape('enemy.gif')
    game_over_animation_pos = [[]]
    game_over_dummy

    highscores = ler_highscores(HIGHSCORES_FILE)
    if len(highscores)<TOP_N or STATE["score"]>highscores[-1][1]:
        print("GRANDEEEE +1 para o top10")
        username = input("Escreve o teu nome para ficar registado: ")
        highscores.append((username, STATE["score"]))
        highscores.sort(key=lambda x: x[1], reverse=True)
        highscores = highscores[:TOP_N]

        f = open(HIGHSCORES_FILE, "w")
        for nome, pontos in highscores:
            f.write(nome + ":" + str(pontos) + "\n")
        f.close()
        print("Highscore guardado!")
    
    print("\n=== TOP HIGHSCORES ===")
    highscores_finais = ler_highscores(HIGHSCORES_FILE)
    for i in highscores_finais:
        print(i[0] + ":" + str(i[1]))

    STATE["screen"].bye()
    sys.exit()

def power_up_handler():
    power_up = STATE["power_up"]
    if len(state["player_bullets"]) == 0:
        print("Não tens balas onde aplicar o power up!")
        return
    bullet = STATE["player_bullets"][len(STATE["player_bullets"]) -1] # obter última bala adicionada
    power_up["activated"] = True
    power_up["killing_area_center"] = bullet.pos()
    #print(bullet.pos())
    bx,by = bullet.pos()
    explosao=turtle.Turtle() #criar um novo turtle, tentei usar o outro mas tornava-se muito rapidamente muito complicado
    explosao.hideturtle()
    explosao.speed(0)
    explosao.pu()
    explosao.goto(bx,by-50) # colocamos um raio de 50 em vez de um raio de 70 "como deveria ser" 
                            #para dar a ilusão de que não há injustiças, caso fosse exatamente 
                            #o mesmo tamanho e não acertasse por 2 pixels é muito mais frustrante
                            #do que ver um raio mais pequeno do que ele realmente é
    explosao.color("red","red")
    explosao.pd()
    explosao.begin_fill()
    explosao.circle(50) # já expliquei antes cromo
    explosao.end_fill()
    STATE["screen"].ontimer(explosao.clear, 100) #unica parte mais chata de 0,1 em 0,1 seg vai apagara explosao
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
            state["power_up"]["activated"] = False
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
    moves = state["enemy_moves"]
    for i, enemy in enumerate(state["enemies"]):
        may_i_drift = determinateEventExecution(ENEMY_DRIFT_CHANCE)
        if determinateEventExecution(ENEMY_INVERT_CHANCE):
            moves[i] = -moves[i]
        x, y = enemy.pos()
        new_x = x + ENEMY_DRIFT_STEP*may_i_drift*moves[i]
        new_y = y - ENEMY_FALL_SPEED
        if verifyOutOfBoundariesWidth(new_x+10):
            moves[i] = -moves[i]
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
    for bullet in state["enemy_bullets"]:
        bx, by = bullet.pos()
        x, y = state["player"].pos()
        if ((x-bx)**2 + (y-by)**2) <= COLLISION_RADIUS**2 and not state["hit"]:
            state["player"].hideturtle()
            state["lifes"] -= 1
            bullet.hideturtle()
            state["enemy_bullets"].remove(bullet)
            state["hit"]=True
            return True
            # terminar_handler()
    # print("[verificar_colisoes_player_bullets] por implementar")
    return False

def verificar_colisoes_enemy_bullets(state):
    for bullet in state["player_bullets"]:
        bx, by = bullet.pos()
        radius = COLLISION_RADIUS
        # calcular área de impacto
        if state["power_up"]["activated"]:
                radius = COLLISION_RADIUS*7
                bx, by = state["power_up"]["killing_area_center"]

        def in_impact_area(x,y):
            return (x-bx)**2 + (y-by)**2 <= radius**2

        for k, enemy in enumerate(state["enemies"]):   # enumerate para mais à frente remover a direction do enemy na posição k. 
                                                        # para depois ao guardar as enemy_moves cada valor estar associado ao index correto do enemy correspondente e não haver excessos
            x, y = enemy.pos()
            if in_impact_area(x,y):
                enemy.hideturtle()
                state["enemies"].remove(enemy)
                state["enemy_moves"].remove(state["enemy_moves"][k]) # elimina assim a REFERÊNCIA da direction e não pelo valor
                state["score"] += 50
        # se acertar num enemy então o score altera-se
        if state["lastScore"] != state["score"] and bullet in state["player_bullets"]:
            bullet.hideturtle()
            state["player_bullets"].remove(bullet)
            state["power_up"]["activated"] = False
    return

def inimigo_chegou_ao_fundo(state):
    for enemy in state["enemies"]:
        x,y = enemy.pos()
        if y <= -BORDA_Y + 20:
            return True
    return False

def verificar_colisao_player_com_inimigos(state):
    for enemy in state["enemies"]:
        x,y = enemy.pos()
        px, py = state["player"].pos()
        if ((x-px)**2 + (y-py)**2 <= COLLISION_RADIUS**2):
            print("Colisão inimigo com utilizador")
            return True
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
    for img in ["player.gif", "enemy.gif", "heart.gif"]:
        if not os.path.exists(img):
            print("ERRO: imagem '" + img + "' não encontrada.")
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
        "lifes" : 3,
        "life_dummies": [],
        "power_up": {"killing_area_center": None, "activated": False},
        "score": 0,
        "frame": 0,
        "files": {"highscores": HIGHSCORES_FILE, "save": SAVE_FILE},
        "jogo_terminado": False,
        "lastScore": 0,
        "panelWriter": None,
        "hit": False, # para verificar se o utilizador levou com um balázio
    }

    # Construção inicial
    if loaded:
        # func(var[0], var[1]) = func(*var)         Nota: assumindo que var tem apenas duas entrada na lista
        state["player"] = criar_entidade(*loaded['player_pos'], "player")
        state["score"] = loaded['score']
        state["frame"] = loaded['frame']

        # Recriar inimigos com posições e direções
        for x, y, direction in loaded['enemies']:
            enemy = criar_entidade(x, y, "enemy")
            state["enemies"].append(enemy)
            state["enemy_moves"].append(direction)
        
        # Recriar balas
        restaurar_balas(state, loaded["player_bullets"], "player")
        restaurar_balas(state, loaded["enemy_bullets"], "enemy")

        ## Fazer upload dos moves
        state["enemy_moves"] = loaded["enemy_moves"][:]
        #print(state["enemy_moves"])
    else:
        print("New game!")
        state["player"] = criar_entidade(0, -200, "player") ## inicial: 0, -350
        spawn_inimigos_em_grelha(state, None, None)

    # Variavel global para os keyboard key handlers
    STATE = state

    panel(state)

    # Teclas
    screen.listen()
    screen.onkeypress(mover_esquerda_handler, "a") # original left
    screen.onkeypress(mover_direita_handler, "d") # original right
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
        verificar_colisoes_enemy_bullets(STATE)
        
        if verificar_colisao_player_com_inimigos(STATE):
            print("Colisão direta com inimigo! Game Over")
            atualizar_panel(state)
            terminar_handler()

        if state["lifes"] == 0:
            print("O utilizador perdeu todas as vidas")
            terminar_handler()

        if verificar_colisoes_player_bullets(STATE):
            print("Atingido!")
            state["hit"] = False
            atualizar_panel(state)

        if state["score"] != state["lastScore"]:
            atualizar_panel(state)
            state["lastScore"] = state["score"]

        if inimigo_chegou_ao_fundo(STATE):
            print("Um inimigo chegou ao fundo! Game Over")
            terminar_handler()

        if len(STATE["enemies"]) == 0:
             print("Vitória! Todos os inimigos foram destruídos.")
             terminar_handler()

        STATE["frame"] += 1
        screen.update()
        time.sleep(0.016)