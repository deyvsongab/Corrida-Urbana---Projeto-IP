import pygame, pygame_menu, sys
from pygame_menu import themes
from pathlib import Path
import os

def jogo():
    os.system('cmd /k "python3 main.py"')

def creditos():
    menu._open(creditos)

def idiomas():
    menu._open(idiomas)

pygame.init()

info = pygame.display.Info()
tela_largura,tela_altura = info.current_w,info.current_h

tela = pygame.display.set_mode((tela_largura, tela_altura), pygame.FULLSCREEN)

menu = pygame_menu.Menu('Jogo de IP 2024.1', tela_largura, tela_altura, theme=themes.THEME_BLUE)
menu.add.button('Iniciar', jogo)
menu.add.button('Idioma', idiomas)
menu.add.button('Créditos', creditos)
menu.add.button('Sair', pygame_menu.events.EXIT)

creditos = pygame_menu.Menu('Créditos', tela_largura, tela_altura, theme=themes.THEME_BLUE)
creditos.add.label("Esse jogo foi feito para a cadeira Introdução a Programação no semestre 2024.1\nParticipantes da equipe:\nAntônio Henrique\nCaio Leitão\nDeyvson Gabriel\nMaria Gabriela\nMiriam Gonzaga")

idiomas = pygame_menu.Menu('Idiomas', tela_largura, tela_altura, theme=themes.THEME_BLUE)
idiomas.add.label('Selecione seu idioma:')
idiomas.add.button('Portugues')

menu.mainloop(tela)
