# Importação das bibliotecas da PPlay e outras
from PPlay.window import *
from PPlay.sprite import *
from PPlay.gameimage import *
from PPlay.mouse import *
import random

# Cria a janela do jogo
janela = Window(1280, 720)
janela.set_title("DNA MATCH")
janela.set_background_color((0, 34, 53))  # Cor de fundo azul escuro
fundo = GameImage("fundo.png")
mouse = Mouse()
teclado = janela.get_keyboard()

# Imagens das bases de DNA
sprites_bases = {
    "A": Sprite("A.png"),
    "T": Sprite("T.png"),
    "C": Sprite("C.png"),
    "G": Sprite("G.png"),
    "U": Sprite("U.png")
}

# Imagens das bases colocadas nos slots
sprites_slot_bases = {
    "A": Sprite("A_slot.png"),
    "T": Sprite("T_slot.png"),
    "C": Sprite("C_slot.png"),
    "G": Sprite("G_slot.png"),
    "U": Sprite("U_slot.png")
}

# Imagens das fitas
fita_facil = Sprite("fita9.png")
fita_dificil = Sprite("fita12.png")

# Imagens do menu
jogar = Sprite("jogar.png")
nivel = Sprite("nivel.png")
facil = Sprite("facil.png")
dificil = Sprite("dificil.png")
regras = Sprite("regras.png")
sair = Sprite("sair.png")
gamename = GameImage("gamename.png")

# Variáveis que controlam o estado do jogo
tela = "menu"
modo_jogo = None
clicou_base = False

pontuacao = 0
combo = 0
pontuacoes_aplicadas = False
sprites_animando = []
fitas = []
fita_atual = 0

# Velocidades da fita e da animação
vel_fita = 100
vel_animacao = 500

# Função que prepara as fitas com os slots

def inicializa_slots(modo):
    global fitas, fita_atual, pontuacoes_aplicadas
    sprites_animando.clear()
    fita_atual = 0
    fitas = []
    pontuacoes_aplicadas = False

    num_slots = 9 if modo == "fácil" else 12
    y1 = janela.height / 2 - fita_facil.height / 2 - 30
    y2 = y1 + fita_facil.height + 60

    for i in range(2):
        fita_sprite = Sprite("fita9.png" if modo == "fácil" else "fita12.png")
        fita_sprite.set_position(janela.width, y1 if i == 0 else y2)
        slot_width = fita_sprite.width / num_slots

        slots = []
        for j in range(num_slots):
            slot_x = fita_sprite.x + j * slot_width
            base = random.choice(["A", "T", "C", "G"] if modo == "fácil" else ["A", "U", "C", "G"])
            slots.append({
                "x": slot_x,
                "y": fita_sprite.y,
                "w": slot_width,
                "base_certa": base,
                "sprite": None,
                "preenchido": False
            })

        fitas.append({"sprite": fita_sprite, "slots": slots, "ativa": i == 0})

# Loop principal do jogo
while True:
    fundo.draw()

    if tela == "menu":
        gamename.set_position(440, 100)
        jogar.set_position((janela.width - jogar.width) / 2, 280)
        nivel.set_position((janela.width - nivel.width) / 2, 340)
        regras.set_position((janela.width - regras.width) / 2, 400)
        sair.set_position((janela.width - sair.width) / 2, 460)

        gamename.draw()
        jogar.draw()
        nivel.draw()
        regras.draw()
        sair.draw()

        if mouse.is_over_object(jogar) and mouse.is_button_pressed(1):
            if modo_jogo is None:
                tela = "nivel"
            else:
                inicializa_slots(modo_jogo)
                tela = "jogo"

        if mouse.is_over_object(nivel) and mouse.is_button_pressed(1):
            tela = "nivel"
            modo_jogo = None

        if mouse.is_over_object(sair) and mouse.is_button_pressed(1):
            janela.close()

    elif tela == "nivel":
        facil.set_position((janela.width - facil.width) / 2, 300)
        dificil.set_position((janela.width - dificil.width) / 2, 360)
        facil.draw()
        dificil.draw()

        if mouse.is_over_object(facil) and mouse.is_button_pressed(1):
            modo_jogo = "fácil"
            pontuacao = 0
            inicializa_slots(modo_jogo)
            tela = "jogo"

        if mouse.is_over_object(dificil) and mouse.is_button_pressed(1):
            modo_jogo = "difícil"
            pontuacao = 0
            inicializa_slots(modo_jogo)
            tela = "jogo"

    elif tela == "jogo":
        for idx in range(len(fitas)):
            fita = fitas[idx]
            if not fita["ativa"]:
                continue

            sprite = fita["sprite"]

            # Verifica se todos os slots da fita estão preenchidos
            todos_preenchidos = True
            for slot in fita["slots"]:
                if not slot["preenchido"]:
                    todos_preenchidos = False
                    break

            if not todos_preenchidos:
                sprite.x -= vel_fita * janela.delta_time()
            sprite.draw()

            for slot in fita["slots"]:
                # Verifica novamente se todos os slots estão preenchidos antes de mover
                todos_preenchidos = True
                for s in fita["slots"]:
                    if not s["preenchido"]:
                        todos_preenchidos = False
                        break

                if not todos_preenchidos:
                    slot["x"] -= vel_fita * janela.delta_time()

                if slot["sprite"]:
                    slot["sprite"].x = slot["x"] + slot["w"] / 2 - slot["sprite"].width / 2
                    slot["sprite"].y = slot["y"] + sprite.height / 2 - slot["sprite"].height / 2
                    slot["sprite"].draw()

        # As bases desenhadas para o jogador clicar
        bases_ativas = ["A", "T", "C", "G"] if modo_jogo == "fácil" else ["A", "U", "C", "G"]
        total_largura = len(bases_ativas) * (sprites_bases[bases_ativas[0]].width + 20) - 20
        pos_x = (janela.width - total_largura) / 2

        for base in bases_ativas:
            sprite_base = sprites_bases[base]
            sprite_base.set_position(pos_x, 600)
            sprite_base.draw()

            if mouse.is_over_object(sprite_base):
                if mouse.is_button_pressed(1) and not clicou_base:
                    clicou_base = True
                    for slot in fitas[fita_atual]["slots"]:
                        if not slot["preenchido"]:
                            destino_x = slot["x"] + slot["w"] / 2 - sprites_slot_bases[base].width / 2
                            destino_y = slot["y"] + fitas[fita_atual]["sprite"].height / 2 - sprites_slot_bases[base].height / 2
                            sprite = Sprite(f"{base}_slot.png")
                            sprite.set_position(sprite_base.x, sprite_base.y)
                            sprites_animando.append({
                                "sprite": sprite,
                                "destino": (destino_x, destino_y),
                                "slot": slot
                            })
                            break
            else:
                if not mouse.is_button_pressed(1):
                    clicou_base = False

            pos_x += sprite_base.width + 20

        for anim in sprites_animando[:]:
            sprite = anim["sprite"]
            dest_x, dest_y = anim["destino"]
            dx = dest_x - sprite.x
            dy = dest_y - sprite.y
            distancia = (dx ** 2 + dy ** 2) ** 0.5
            velocidade = vel_animacao * janela.delta_time()

            if distancia < velocidade:
                slot = anim["slot"]
                sprite.x = slot["x"] + slot["w"] / 2 - sprite.width / 2
                sprite.y = slot["y"] + fita_facil.height / 2 - sprite.height / 2
                slot["sprite"] = sprite
                slot["preenchido"] = True
                slot["base"] = base
                sprites_animando.remove(anim)
            else:
                sprite.x += velocidade * dx / distancia
                sprite.y += velocidade * dy / distancia
                sprite.draw()

        # Verifica se todos os slots da primeira fita estão preenchidos
        todos_preenchidos_fita0 = True
        for slot in fitas[0]["slots"]:
            if not slot["preenchido"]:
                todos_preenchidos_fita0 = False
                break

        if fita_atual == 0 and todos_preenchidos_fita0:
            fita_atual = 1
            fitas[1]["ativa"] = True

        if modo_jogo == "fácil" and not pontuacoes_aplicadas:
            # Verifica se todos os slots da segunda fita estão preenchidos
            todos_preenchidos = True
            for slot in fitas[1]["slots"]:
                if not slot["preenchido"]:
                    todos_preenchidos = False
                    break

            if todos_preenchidos:
                pontuacoes_aplicadas = True
                combo = 0
                for i in range(len(fitas[0]["slots"])):
                    slot1 = fitas[0]["slots"][i]
                    slot2 = fitas[1]["slots"][i]

                    base1 = slot1["base_certa"]
                    base2 = slot2["base"]

                    corretas = (
                        (base1 == "A" and base2 == "T") or
                        (base1 == "T" and base2 == "A") or
                        (base1 == "C" and base2 == "G") or
                        (base1 == "G" and base2 == "C")
                    )

                    if corretas:
                        pontuacao += 10
                        combo += 1
                        if combo == 3:
                            pontuacao += 30
                            combo = 0
                    else:
                        pontuacao -= 5
                        combo = 0

                tela = "fim"

        janela.draw_text(f"Pontos: {pontuacao}", janela.width - 200, 20, size=25, color=(0, 255, 255), bold=True)

        if teclado.key_pressed("ESC"):
            tela = "menu"
            modo_jogo = None

    elif tela == "fim":
        fundo.draw()
        janela.draw_text("FIM DE JOGO", janela.width / 2 - 100, 150, size=40, color=(0,255,255), bold=True)
        janela.draw_text(f"Sua Pontuação: {pontuacao}", janela.width / 2 - 120, 220, size=40, color=(0,255,255), bold=True)

        if teclado.key_pressed("RETURN"):
            modo_jogo = None
            tela = "menu"

    janela.update()
