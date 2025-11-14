import json
import os

# =========================
# Utilidades
# =========================

def armazenar_dict(filename, data: dict):
    if not isinstance(data, dict):
        raise ValueError("Impossível adicionar tipo diferente de dict!")
    data = str(data)
    data = data.replace("}", "\n}").replace("{", "{\n")
    with open(filename, "w") as file:
        file.write(data)

def lerJson(filename):
    if filename not in os.listdir():
        return False
    with open(filename, "r") as file:
        content = file.read()
    return eval(content)
