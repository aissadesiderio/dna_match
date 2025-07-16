# Importação de bibliotecas
from PPlay.window import *
from PPlay.sprite import *
from PPlay.gameimage import *
from PPlay.mouse import *
import random

# Constantes globais
BASES_DNA = ["A", "T", "C", "G"]
BASES_COMPLETA = ["A", "T", "U", "C", "G"]

# Cria janela
janela = Window(1280, 720)
janela.set_title("DNA MATCH")
janela.set_background_color((0, 34, 53))
fundo = GameImage("fundo.png")
mouse = Mouse()
teclado = janela.get_keyboard()

# Sprites de bases e slots
sprites_bases = {b: Sprite(f"{b}.png") for b in BASES_COMPLETA}
sprites_slot_bases = {b: Sprite(f"{b}_slot.png") for b in BASES_COMPLETA}

# Sprites das fitas e menu
fita_facil = Sprite("fita9.png")
fita_dificil = Sprite("fita12.png")
fita_rna = Sprite("fitaRNA.png")

jogar = Sprite("jogar.png")
nivel = Sprite("nivel.png")
facil = Sprite("facil.png")
dificil = Sprite("dificil.png")
regras = Sprite("regras.png")
sair = Sprite("sair.png")
gamename = GameImage("gamename.png")

# Variáveis de estado
tela = "menu"
modo_jogo = None
clicou_base = False
pontuacao = 0
combo = 0
pontuacoes_aplicadas = False
sprites_animando = []
fitas = []
fita_atual = 0
vel_fita = 100
vel_animacao = 500

# Funções auxiliares
def desenha_menu():
    gamename.set_position(440, 100)
    jogar.set_position((janela.width - jogar.width) / 2, 280)
    nivel.set_position((janela.width - nivel.width) / 2, 340)
    regras.set_position((janela.width - regras.width) / 2, 400)
    sair.set_position((janela.width - sair.width) / 2, 460)
    gamename.draw(); jogar.draw(); nivel.draw(); regras.draw(); sair.draw()

def desenha_nivel():
    facil.set_position((janela.width - facil.width) / 2, 300)
    dificil.set_position((janela.width - dificil.width) / 2, 360)
    facil.draw(); dificil.draw()

def fita_esta_preenchida(fita):
    return all(slot["preenchido"] for slot in fita["slots"])

def inicializa_slots(modo):
    global fitas, fita_atual, pontuacoes_aplicadas
    sprites_animando.clear()
    fita_atual = 0
    fitas = []
    pontuacoes_aplicadas = False
    num_slots = 9 if modo == "fácil" else 12
    altura_fita = fita_facil.height if modo == "fácil" else fita_dificil.height
    y1 = janela.height / 2 - altura_fita - 30
    y2 = y1 + altura_fita + 60

    for i in range(2):
        fita_sprite = Sprite("fita9.png" if modo == "fácil" else "fita12.png")
        fita_sprite.set_position(janela.width, y1 if i == 0 else y2)
        slot_width = fita_sprite.width / num_slots
        slots = []
        for j in range(num_slots):
            slot_x = fita_sprite.x + j * slot_width
            base = random.choice(BASES_DNA if modo == "fácil" else BASES_COMPLETA)
            slots.append({"x": slot_x, "y": fita_sprite.y, "w": slot_width,
                          "base_certa": base, "sprite": None,
                          "preenchido": False, "em_animacao": False})
        fitas.append({"sprite": fita_sprite, "slots": slots, "ativa": i == 0})

    if modo == "difícil":
        y3 = y2 + altura_fita + 60
        fita_sprite = Sprite("fitaRNA.png")
        fita_sprite.set_position(janela.width, y3)
        slot_width = fita_sprite.width / num_slots
        slots = []
        for j in range(num_slots):
            slot_x = fita_sprite.x + j * slot_width
            base = random.choice(BASES_COMPLETA)
            slots.append({"x": slot_x, "y": fita_sprite.y, "w": slot_width,
                          "base_certa": base, "sprite": None,
                          "preenchido": False, "em_animacao": False})
        fitas.append({"sprite": fita_sprite, "slots": slots, "ativa": False})

def calcular_pontuacao():
    global pontuacao, combo, tela, pontuacoes_aplicadas
    pontuacoes_aplicadas = True
    combo = 0
    for i in range(len(fitas[0]["slots"])):
        s1 = fitas[0]["slots"][i]; s2 = fitas[1]["slots"][i]
        s3 = fitas[2]["slots"][i] if modo_jogo == "difícil" and len(fitas) > 2 else None
        b1, b2 = s1["base_certa"], s2.get("base")
        b3 = s3.get("base") if s3 else None
        dna = ((b1 == "A" and b2 == "T") or (b1 == "T" and b2 == "A") or
               (b1 == "C" and b2 == "G") or (b1 == "G" and b2 == "C"))
        rna = True
        if modo_jogo == "difícil" and s3:
            rna = ((b1 == "A" and b3 == "U") or (b1 == "T" and b3 == "A") or
                   (b1 == "C" and b3 == "G") or (b1 == "G" and b3 == "C"))
        if dna and rna:
            pontuacao += 10; combo += 1
            if combo == 3:
                pontuacao += 30; combo = 0
        else:
            pontuacao = max(0, pontuacao - 5); combo = 0
    tela = "fim"

# Continuação do loop principal e lógica de jogo
from dna_jogo_loop import executar_loop_principal
executar_loop_principal(janela, mouse, teclado, fundo, sprites_bases, sprites_slot_bases,
                        fitas, fita_facil, fita_dificil, fita_rna,
                        BASES_DNA, BASES_COMPLETA,
                        calcular_pontuacao, inicializa_slots, fita_esta_preenchida,
                        desenha_menu, desenha_nivel)

def executar_loop_principal(janela, mouse, teclado, fundo, sprites_bases, sprites_slot_bases,
                            fitas, fita_facil, fita_dificil, fita_rna,
                            BASES_DNA, BASES_COMPLETA,
                            calcular_pontuacao, inicializa_slots, fita_esta_preenchida,
                            desenha_menu, desenha_nivel):

    global tela, modo_jogo, pontuacao, clicou_base, sprites_animando, fita_atual, pontuacoes_aplicadas

    while True:
        fundo.draw()

        if tela == "menu":
            desenha_menu()

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
            desenha_nivel()

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

            if teclado.key_pressed("ESC"):
                tela = "menu"
                modo_jogo = None

        elif tela == "jogo":
            for idx, fita in enumerate(fitas):
                if not fita["ativa"]:
                    continue

                sprite = fita["sprite"]
                if sprite.x > 0:
                    deslocamento = 100 * janela.delta_time()
                    sprite.x -= deslocamento
                    for slot in fita["slots"]:
                        slot["x"] -= deslocamento

                sprite.draw()
                for slot in fita["slots"]:
                    if slot["sprite"]:
                        slot["sprite"].x = slot["x"] + slot["w"] / 2 - slot["sprite"].width / 2
                        slot["sprite"].y = slot["y"] + sprite.height / 2 - slot["sprite"].height / 2
                        slot["sprite"].draw()

            # Desenha bases clicáveis
            bases_ativas = BASES_DNA if modo_jogo == "fácil" else BASES_COMPLETA
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
                            if not slot["preenchido"] and not slot["em_animacao"] and slot["x"] + slot["w"] / 2 < janela.width:
                                destino_x = slot["x"] + slot["w"] / 2 - sprites_slot_bases[base].width / 2
                                destino_y = slot["y"] + fitas[fita_atual]["sprite"].height / 2 - sprites_slot_bases[base].height / 2
                                sprite = sprites_slot_bases[base].clone()
                                sprite.base_letra = base
                                sprite.set_position(sprite_base.x, sprite_base.y)
                                slot["em_animacao"] = True
                                sprites_animando.append({"sprite": sprite, "destino": (destino_x, destino_y), "slot": slot})
                                break
                else:
                    if not mouse.is_button_pressed(1):
                        clicou_base = False

                pos_x += sprite_base.width + 20

            # Atualiza animações
            for anim in sprites_animando[:]:
                sprite = anim["sprite"]
                dest_x, dest_y = anim["destino"]
                dx = dest_x - sprite.x
                dy = dest_y - sprite.y
                distancia = (dx ** 2 + dy ** 2) ** 0.5
                velocidade = 500 * janela.delta_time()

                if distancia < velocidade:
                    slot = anim["slot"]
                    sprite.x = slot["x"] + slot["w"] / 2 - sprite.width / 2
                    sprite.y = slot["y"] + fitas[fita_atual]["sprite"].height / 2 - sprite.height / 2
                    if not slot["preenchido"]:
                        slot["sprite"] = sprite
                        slot["preenchido"] = True
                        slot["base"] = sprite.base_letra
                        slot["em_animacao"] = False
                    sprites_animando.remove(anim)
                else:
                    sprite.x += velocidade * dx / distancia
                    sprite.y += velocidade * dy / distancia
                    sprite.draw()

            # Verifica transição entre fitas
            if fita_esta_preenchida(fitas[fita_atual]):
                if fita_atual + 1 < len(fitas):
                    fita_atual += 1
                    fitas[fita_atual]["ativa"] = True
                else:
                    calcular_pontuacao()

            janela.draw_text(f"Pontos: {pontuacao}", janela.width - 200, 20, size=25, color=(0, 255, 255), bold=True)

            if teclado.key_pressed("ESC"):
                tela = "menu"
                modo_jogo = None

        elif tela == "fim":
            fundo.draw()
            janela.draw_text("FIM DE JOGO", janela.width / 2 - 100, 150, size=40, color=(0,255,255), bold=True)
            janela.draw_text(f"Sua Pontuação: {pontuacao}", janela.width / 2 - 120, 220, size=40, color=(0,255,255), bold=True)
            if teclado.key_pressed("ESC") or teclado.key_pressed("RETURN"):
                tela = "menu"
                modo_jogo = None

        janela.update()
