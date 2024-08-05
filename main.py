import pygame
from pygame.locals import *
from sys import exit
from random import randint
import os

pygame.init()

class Game():
    def __init__(self):
        self.info = pygame.display.Info()
        self.tela_largura, self.tela_altura = self.info.current_w, self.info.current_h
        self.diretorio_principal = os.path.dirname(__file__)
        self.diretorio_imagens = os.path.join(self.diretorio_principal, 'imagens')
        self.sprites_inimigo = pygame.image.load(os.path.join(self.diretorio_imagens, 'inimigo_frame.png'))
        self.sprites_pessoa = pygame.image.load(os.path.join(self.diretorio_imagens, 'pessoa_frames.png'))
        self.sprites_onibus = pygame.image.load(os.path.join(self.diretorio_imagens, 'frames_onibus.png'))
        self.sprites_buraco = pygame.image.load(os.path.join(self.diretorio_imagens, 'buraco.png'))
        self.sprites_ferramenta = pygame.image.load(os.path.join(self.diretorio_imagens, 'ferramenta.png')) 
        self.sprites_estrela = pygame.image.load(os.path.join(self.diretorio_imagens, 'estrela.png')) 
        self.sprites_contadorpxt = pygame.image.load(os.path.join(self.diretorio_imagens, 'contador_pxt.png')) 
        self.eixo_x = int(self.tela_largura/2)
        self.eixo_y = int(self.tela_altura/2)
        self.cir_x = randint(self.tela_largura//30+40, self.tela_largura-(self.tela_largura//30)-40)
        self.cir_y = randint(self.tela_altura//20+40, self.tela_altura-(self.tela_altura//20)-40)
        self.tri_x = 200000
        self.tri_y = 200000
        self.ferramenta_x = 200000
        self.ferramenta_y = 200000
        self.buraco_x1 = randint(self.tela_largura//30+40, self.tela_largura-(self.tela_largura//30)-40)
        self.buraco_y1 = randint(self.tela_altura//20+40, self.tela_altura-(self.tela_altura//20)-40)
        self.buraco_x2 = randint(self.tela_largura//30+40, self.tela_largura-(self.tela_largura//30)-40)
        self.buraco_y2 = randint(self.tela_altura//20+40, self.tela_altura-(self.tela_altura//20)-40)
        self.buraco_x3 = randint(self.tela_largura//30+40, self.tela_largura-(self.tela_largura//30)-40)
        self.buraco_y3 = randint(self.tela_altura//20+40, self.tela_altura-(self.tela_altura//20)-40)
        self.todas_sprites = pygame.sprite.Group()
        self.index_lista = 0
        self.inimigo = Inimigo(self.tri_x, self.tri_y, self.sprites_inimigo, self.index_lista)
        self.pessoa = Pessoa(self.cir_x, self.cir_y, self.sprites_pessoa, self.index_lista)
        self.buraco1 = Buraco1(self.buraco_x1, self.buraco_y1, self.sprites_buraco)
        self.buraco2 = Buraco2(self.buraco_x2, self.buraco_y2, self.sprites_buraco)
        self.buraco3 = Buraco3(self.buraco_x3, self.buraco_y3, self.sprites_buraco)
        self.ferramenta = Ferramenta(self.ferramenta_x, self.ferramenta_y, self.sprites_ferramenta)
        self.todas_sprites.add(self.inimigo)
        self.todas_sprites.add(self.pessoa)
        self.todas_sprites.add(self.buraco1)
        self.todas_sprites.add(self.buraco2)
        self.todas_sprites.add(self.buraco3)
        self.todas_sprites.add(self.ferramenta)
        self.variaveis()
        self.inicio()
        self.jogo()

    def tela(self):
        self.branco = (255,255,255)
        self.cinza = (70,70,70)
        self.marrom = (92,46,36)
        self.amarelo = (245,216,96)
        self.screen = pygame.display.set_mode((self.tela_largura, self.tela_altura), pygame.FULLSCREEN)
        self.coli_up = pygame.draw.rect(self.screen, (139,195,74), (0,0, self.tela_largura, self.tela_altura//20+6))
        self.coli_down = pygame.draw.rect(self.screen, (139,195,74), (0,self.tela_altura-(self.tela_altura//20)-6, self.tela_largura, self.tela_altura))
        self.coli_left = pygame.draw.rect(self.screen, (139,195,74), (0,0, self.tela_largura/30+6, self.tela_altura))
        self.coli_right = pygame.draw.rect(self.screen, (139,195,74), (self.tela_largura - (self.tela_largura/30),0, self.tela_largura, self.tela_altura))
        pygame.display.set_caption('TI CDU')
        self.relogio = pygame.time.Clock()

    def desenha_estrelas(self, estrelas):
        self.distancia = self.tela_largura-250
        for i in range(estrelas):
            self.grupo_star = pygame.sprite.Group()
            self.grupo_star.add(Estrela(self.distancia, (self.tela_altura//20)//2, self.sprites_estrela))
            self.grupo_star.draw(self.screen)
            self.distancia += 50


    def texto(self):
        self.fonte = pygame.font.SysFont('arial', 40, True, True)
        self.fonte2 = pygame.font.SysFont('arial', 50, True, True)
        self.mensagem_mapa1 = 'Colete o máximo de passageiros e desvie dos trombadinhas!'
        self.mensagem_morte = 'Você perdeu! Parabéns pela sua façanha, pressione R para tentar novamente!'
        self.form_mp1 = self.fonte2.render(self.mensagem_mapa1, True, (0,0,0))
        self.cent_mp1 = self.form_mp1.get_rect()
        self.form_morte = self.fonte2.render(self.mensagem_morte, True, (0,0,0))
        self.cent_morte = self.form_morte.get_rect()
        self.mensagem = f'Pontuação: {self.pontuacao}/25'
        self.quantidade_pxt = f'{self.numero_pessoas}            {self.numero_trombadinhas}'
        self.texto_formatado = self.fonte.render(self.mensagem, True, (0,0,0))
        self.pxt_formatado = self.fonte.render(self.quantidade_pxt, True, (0,0,0))
    
    def variaveis(self):
        self.pontuacao = 0
        self.numero_s = 0
        self.numero_pessoas = 0
        self.numero_trombadinhas = 0
        self.velocidade = 40
        self.velocidade_inimigo = 5
        self.estrelas = 5
        self.conta_tempo = 0
        self.dobro_tempo = 0
        self.comecou = False
        self.pegou = True
    
    def inicio(self):
        self.tela()
        self.texto()
        while self.comecou == False:
            self.screen.fill((255,255,255))
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        exit()
                    else:
                        self.comecou = True
            self.cent_mp1.center = (self.tela_largura//2, self.tela_altura//2)
            self.screen.blit(self.form_mp1, self.cent_mp1)
            pygame.display.flip()

    def hitbox(self):
        if self.numero_s == 0: #direita
            self.frente = pygame.draw.rect(self.screen, self.branco, (self.eixo_x+40, self.eixo_y, 40, 40))
            self.direita = pygame.draw.rect(self.screen, self.branco, (self.eixo_x, self.eixo_y+40, 40, 40))
            self.esquerda = pygame.draw.rect(self.screen, self.branco, (self.eixo_x, self.eixo_y-40, 40, 40))
        if self.numero_s == 1: #esquerda
            self.frente = pygame.draw.rect(self.screen, self.branco, (self.eixo_x-40, self.eixo_y, 40, 40))
            self.direita = pygame.draw.rect(self.screen, self.branco, (self.eixo_x, self.eixo_y-40, 40, 40))
            self.esquerda = pygame.draw.rect(self.screen, self.branco, (self.eixo_x, self.eixo_y+40, 40, 40))
        if self.numero_s == 2: #cima
            self.frente = pygame.draw.rect(self.screen, self.branco, (self.eixo_x, self.eixo_y-40, 40, 40))
            self.direita = pygame.draw.rect(self.screen, self.branco, (self.eixo_x+40, self.eixo_y, 40, 40))
            self.esquerda = pygame.draw.rect(self.screen, self.branco, (self.eixo_x-40, self.eixo_y, 40, 40))
        if self.numero_s == 3: #baixo
            self.frente = pygame.draw.rect(self.screen, self.branco, (self.eixo_x, self.eixo_y+40, 40, 40))
            self.direita = pygame.draw.rect(self.screen, self.branco, (self.eixo_x-40, self.eixo_y, 40, 40))
            self.esquerda = pygame.draw.rect(self.screen, self.branco, (self.eixo_x+40, self.eixo_y, 40, 40))

    def limite_mapa(self):
        self.screen.fill(self.cinza)
        self.coli_up = pygame.draw.rect(self.screen, (139,195,74), (0,0, self.tela_largura, self.tela_altura//20+6))
        self.coli_down = pygame.draw.rect(self.screen, (139,195,74), (0,self.tela_altura-(self.tela_altura//20)-6, self.tela_largura, self.tela_altura))
        self.coli_left = pygame.draw.rect(self.screen, (139,195,74), (0,0, self.tela_largura/30+16, self.tela_altura))
        self.coli_right = pygame.draw.rect(self.screen, (139,195,74), (self.tela_largura - (self.tela_largura/30)-16,0, self.tela_largura, self.tela_altura))

    def jogo(self):
        while self.comecou == True:
            self.relogio.tick(10)
            self.hitbox()
            self.formas()
            self.ferramentas()
            self.tela()
            self.limite_mapa()
            self.desenha_estrelas(self.estrelas)
            self.texto()
            self.eventos()
            self.movimentacao()
            self.checa_colisoes()
            self.pontua()
            self.update()


    def eventos(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    exit()
    def movimentacao(self):
        if pygame.key.get_pressed()[K_LEFT] and self.frente.colliderect(self.coli_left) == False:
            if self.direita.colliderect(self.coli_left) == False and self.esquerda.colliderect(self.coli_left) == False:
                self.eixo_x -= 40
                self.numero_s = 1
        elif pygame.key.get_pressed()[K_RIGHT] and self.frente.colliderect(self.coli_right) == False:
            if self.direita.colliderect(self.coli_right) == False and self.esquerda.colliderect(self.coli_right) == False:
                self.eixo_x += 40
                self.numero_s = 0      
        elif pygame.key.get_pressed()[K_UP] and self.frente.colliderect(self.coli_up) == False:
            if self.direita.colliderect(self.coli_up) == False and self.esquerda.colliderect(self.coli_up) == False:
                self.eixo_y -= 40
                self.numero_s = 2
        elif pygame.key.get_pressed()[K_DOWN] and self.frente.colliderect(self.coli_down) == False:
            if self.direita.colliderect(self.coli_down) == False and self.esquerda.colliderect(self.coli_down) == False:
                self.eixo_y += 40
                self.numero_s = 3

    def formas(self):
        self.p_buraco = pygame.draw.circle(self.screen, self.marrom, (self.buraco_x1,self.buraco_y1), 40, width=0)
        self.s_buraco = pygame.draw.circle(self.screen, self.marrom, (self.buraco_x2,self.buraco_y2), 40, width=0)
        self.t_buraco = pygame.draw.circle(self.screen, self.marrom, (self.buraco_x3,self.buraco_y3), 40, width=0)
        self.onibus = pygame.draw.rect(self.screen, (0,0,255), (self.eixo_x,self.eixo_y, 40, 40))
        self.pessoa = pygame.draw.circle(self.screen, (0,255,0), (self.cir_x,self.cir_y), 20, width=0)
        self.trombadinha = pygame.draw.polygon(self.screen, (255,0,0), [[self.tri_x,self.tri_y], [self.tri_x+25,self.tri_y+40], [self.tri_x-25,self.tri_y+40]])
        if self.numero_s == 0:
            pygame.draw.rect(self.screen, (0,0,255), (self.eixo_x-40, self.eixo_y, 40, 40))
        if self.numero_s == 1:
            pygame.draw.rect(self.screen, (0,0,255), (self.eixo_x+40, self.eixo_y, 40, 40))
        if self.numero_s == 2:
            pygame.draw.rect(self.screen, (0,0,255), (self.eixo_x, self.eixo_y+40, 40, 40))
        if self.numero_s == 3:
            pygame.draw.rect(self.screen, (0,0,255), (self.eixo_x, self.eixo_y-40, 40, 40))

    def ferramentas(self):
        if self.pegou == True:
            if self.conta_tempo % 50 == 0 and self.conta_tempo != 0:
                if self.estrelas < 5:
                    self.pegou = False
                    self.ferramenta_x = randint(self.tela_largura//30+40, self.tela_largura-(self.tela_largura//30)-40)
                    self.ferramenta_y = randint(self.tela_altura//20+40, self.tela_altura-(self.tela_altura//20)-40)
        self.ferramenta = pygame.draw.rect(self.screen, self.amarelo, (self.ferramenta_x, self.ferramenta_y, 40, 40))

    def checa_colisoes(self):
        if self.onibus.colliderect(self.pessoa):
            self.cir_x = randint(self.tela_largura//30+40, self.tela_largura-(self.tela_largura//30)-40)
            self.cir_y = randint(self.tela_altura//20+40, self.tela_altura-(self.tela_altura//20)-40)
            if self.pontuacao == 0:
                self.tri_x = randint(self.tela_largura//30+40, self.tela_largura-(self.tela_largura//30)-40)
                self.tri_y = randint(self.tela_altura//20+40, self.tela_altura-(self.tela_altura//20)-40)
            self.pontuacao += 1
            self.numero_pessoas += 1
        if self.onibus.colliderect(self.trombadinha):
            self.tri_x = randint(self.tela_largura//30+40, self.tela_largura-(self.tela_largura//30)-40)
            self.tri_y = randint(self.tela_altura//20+40, self.tela_altura-(self.tela_altura//20)-40)
            self.pontuacao -= 1
            if self.pontuacao <= 0:
                self.tri_x = 200000
                self.tri_y = 200000
                self.pontuacao = 0
            self.numero_trombadinhas += 1
        if self.onibus.colliderect(self.p_buraco):
            self.buraco_x1 = randint(self.tela_largura//30+40, self.tela_largura-(self.tela_largura//30)-40)
            self.buraco_y1 = randint(self.tela_altura//20+40, self.tela_altura-(self.tela_altura//20)-40)
            if self.estrelas == 5:
                self.pegou == True
            self.estrelas -= 1
        if self.onibus.colliderect(self.s_buraco):
            self.buraco_x2 = randint(self.tela_largura//30+40, self.tela_largura-(self.tela_largura//30)-40)
            self.buraco_y2 = randint(self.tela_altura//20+40, self.tela_altura-(self.tela_altura//20)-40)
            if self.estrelas == 5:
                self.pegou == True
            self.estrelas -= 1
        if self.onibus.colliderect(self.t_buraco):
            self.buraco_x3 = randint(self.tela_largura//30+40, self.tela_largura-(self.tela_largura//30)-40)
            self.buraco_y3 = randint(self.tela_altura//20+40, self.tela_altura-(self.tela_altura//20)-40)
            if self.estrelas == 5:
                self.pegou == True
            self.estrelas -= 1
        if self.onibus.colliderect(self.ferramenta):
            self.ferramenta_x = 200000
            self.ferramenta_y = 200000
            self.estrelas += 1
            self.pegou = True

    def pontua(self):
        if self.pontuacao < 5:
            self.velocidade_inimigo = 5
        elif self.pontuacao < 10:
            self.velocidade_inimigo = 10
        elif self.pontuacao < 15:
            self.velocidade_inimigo = 15
        elif self.pontuacao < 20:
            self.velocidade_inimigo = 20
        elif self.pontuacao == 20:
            self.velocidade_inimigo = 21
        elif self.pontuacao == 21:
            self.velocidade_inimigo = 22
        elif self.pontuacao == 22:
            self.velocidade_inimigo = 23
        elif self.pontuacao == 23:
            self.velocidade_inimigo = 25
        elif self.pontuacao == 24:
            self.velocidade_inimigo = 30
        
        if self.pontuacao == 25:
            self.ganhou = True
            if self.numero_trombadinhas > 0:
                self.mensagem_fim_mapa1 = 'Parabéns! Você passou do primeiro teste, mas ainda precisa melhorar.'
            else:
                self.mensagem_fim_mapa1 = 'Parabéns! Você concluiu o nível sem pegar trombadinhas.'
            self.mensagem_pontuacao_mapa1 = f'Você coletou {self.numero_pessoas} pessoas e {self.numero_trombadinhas} trombadinhas!'
            self.form_fim_mp1 = self.fonte2.render(self.mensagem_fim_mapa1, True, (0,0,0))
            self.form_pontuacao_mp1 = self.fonte2.render(self.mensagem_pontuacao_mapa1, True, (0,0,0))
            self.cent_fim_mp1 = self.form_fim_mp1.get_rect()
            self.cent_pontuacao_mp1 = self.form_pontuacao_mp1.get_rect()
            while self.ganhou == True:
                self.screen.fill(self.branco)
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        exit()
                    if event.type == KEYDOWN:
                        if event.key == K_ESCAPE:
                            pygame.quit()
                            exit()
                self.cent_fim_mp1.center = (self.tela_largura//2, self.tela_altura//2)
                self.cent_pontuacao_mp1.center = (self.tela_largura//2, self.tela_altura//2)
                cent_pontuacao_final = (self.cent_pontuacao_mp1[0], self.cent_pontuacao_mp1[1]+self.cent_pontuacao_mp1[3], self.cent_pontuacao_mp1[2], self.cent_pontuacao_mp1[3])
                self.screen.blit(self.form_fim_mp1, self.cent_fim_mp1)
                self.screen.blit(self.form_pontuacao_mp1, cent_pontuacao_final)
                pygame.display.flip()
        if self.estrelas <= 0:
            self.comecou = False
            self.perde()

    def update(self):
        if self.conta_tempo % 2 == 0:
            self.index_lista_inimigo = 1
        else:
            self.index_lista_inimigo = 0
        if int(self.dobro_tempo) % 2 == 0:
            self.index_lista_pessoa = 1
        else:
            self.index_lista_pessoa = 0
        self.tri_x = seguirx(self.eixo_x, self.tri_x, self.velocidade_inimigo)
        self.tri_y = seguiry(self.eixo_y, self.tri_y, self.velocidade_inimigo)
        self.conta_tempo += 1
        self.dobro_tempo += 0.25
        self.screen.blit(self.texto_formatado, (5,10))
        self.screen.blit(self.pxt_formatado, (450, 10))
        self.todas_sprites.draw(self.screen)
        self.todas_sprites.update()
        self.todas_sprites = pygame.sprite.Group()
        self.inimigo = Inimigo(self.tri_x, self.tri_y, self.sprites_inimigo, self.index_lista_inimigo)
        self.pessoa = Pessoa(self.cir_x, self.cir_y, self.sprites_pessoa, self.index_lista_pessoa)
        self.onibus = Onibus(self.eixo_x, self.eixo_y, self.sprites_onibus, self.numero_s)
        self.buraco1 = Buraco1(self.buraco_x1, self.buraco_y1, self.sprites_buraco)
        self.buraco2 = Buraco2(self.buraco_x2, self.buraco_y2, self.sprites_buraco)
        self.buraco3 = Buraco3(self.buraco_x3, self.buraco_y3, self.sprites_buraco)
        self.ferramenta = Ferramenta(self.ferramenta_x, self.ferramenta_y, self.sprites_ferramenta)
        self.conta_pxt = Contapxt(self.sprites_contadorpxt)
        self.todas_sprites.add(self.conta_pxt)
        self.todas_sprites.add(self.buraco1)
        self.todas_sprites.add(self.buraco2)
        self.todas_sprites.add(self.buraco3)
        self.todas_sprites.add(self.ferramenta)
        self.todas_sprites.add(self.inimigo)
        self.todas_sprites.add(self.pessoa)
        self.todas_sprites.add(self.onibus)
        pygame.display.flip()

    def perde(self):
        self.perdeu = True
        while self.perdeu == True:
            self.screen.fill(self.branco)
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        exit()
                    if event.key == K_r:
                        Game()
            self.cent_morte.center = (self.tela_largura//2, self.tela_altura//2)
            self.screen.blit(self.form_morte, self.cent_morte)
            pygame.display.flip()

class Inimigo(pygame.sprite.Sprite):
    def __init__(self, tri_x, tri_y, sprites_inimigo, index_lista):
        pygame.sprite.Sprite.__init__(self)
        self.imagens_inimigo = []
        for i in range(2):
            self.img_inimigo = sprites_inimigo.subsurface((i*32,0),(32,32))
            self.img_inimigo = pygame.transform.scale(self.img_inimigo,(32*2,32*2))
            self.imagens_inimigo.append(self.img_inimigo)
        self.image = self.imagens_inimigo[index_lista]
        self.rect = self.image.get_rect()
        self.rect.center = (tri_x, tri_y+15)

class Pessoa(pygame.sprite.Sprite):
    def __init__(self, cir_x, cir_y, sprites_pessoa, index_lista):
        pygame.sprite.Sprite.__init__(self)
        self.imagens_pessoa = []
        for i in range(2):
            self.img_pessoa = sprites_pessoa.subsurface((i*32,0),(32,32))
            self.img_pessoa = pygame.transform.scale(self.img_pessoa,(32*2,32*2)) 
            self.imagens_pessoa.append(self.img_pessoa)
        self.image = self.imagens_pessoa[index_lista]
        self.rect = self.image.get_rect()
        self.rect.center = (cir_x, cir_y)

class Onibus(pygame.sprite.Sprite):
    def __init__(self, eixo_x, eixo_y, sprites_onibus, numero_s):
        pygame.sprite.Sprite.__init__(self)
        self.imagens_onibus = []
        self.conta_dois = 0
        for i in range(4):
            self.img_onibus = sprites_onibus.subsurface((i*32,0),(32,32))
            if self.conta_dois > 1:
                self.img_onibus = pygame.transform.scale(self.img_onibus,(32*2.8,32*3)) 
            else:
                self.img_onibus = pygame.transform.scale(self.img_onibus,(32*3,32*3)) 
            self.imagens_onibus.append(self.img_onibus)
            self.conta_dois += 1
        self.image = self.imagens_onibus[numero_s]
        self.rect = self.image.get_rect()
        if numero_s == 0:
            self.rect.center = (eixo_x+5, eixo_y-5)
        if numero_s == 1:
            self.rect.center = (eixo_x+40, eixo_y-5)
        if numero_s == 2:
            self.rect.center = (eixo_x+20, eixo_y+40)
        if numero_s == 3:
            self.rect.center = (eixo_x+20, eixo_y)

class Buraco1(pygame.sprite.Sprite):
    def __init__(self, buraco_x1, buraco_y1, sprites_buraco):
        pygame.sprite.Sprite.__init__(self)
        self.imagens_buraco = []
        self.img_buraco = pygame.transform.scale(sprites_buraco, (32*3, 32*3+30))
        self.imagens_buraco.append(self.img_buraco)
        self.image = self.imagens_buraco[0]
        self.rect = self.image.get_rect()
        self.rect.center = (buraco_x1, buraco_y1+5)

class Buraco2(pygame.sprite.Sprite):
    def __init__(self, buraco_x2, buraco_y2, sprites_buraco):
        pygame.sprite.Sprite.__init__(self)
        self.imagens_buraco = []
        self.img_buraco = pygame.transform.scale(sprites_buraco, (32*3, 32*3+30))
        self.imagens_buraco.append(self.img_buraco)
        self.image = self.imagens_buraco[0]
        self.rect = self.image.get_rect()
        self.rect.center = (buraco_x2, buraco_y2+5)

class Buraco3(pygame.sprite.Sprite):
    def __init__(self, buraco_x3, buraco_y3, sprites_buraco):
        pygame.sprite.Sprite.__init__(self)
        self.imagens_buraco = []
        self.img_buraco = pygame.transform.scale(sprites_buraco, (32*3, 32*3+30))
        self.imagens_buraco.append(self.img_buraco)
        self.image = self.imagens_buraco[0]
        self.rect = self.image.get_rect()
        self.rect.center = (buraco_x3, buraco_y3+5)    

class Ferramenta(pygame.sprite.Sprite):
    def __init__(self, ferramenta_x, ferramenta_y, sprites_ferramenta):
        pygame.sprite.Sprite.__init__(self)
        self.imagens_ferramenta = []
        self.img_ferramenta = pygame.transform.scale(sprites_ferramenta, (32*1.5, 32*1.5))
        self.imagens_ferramenta.append(self.img_ferramenta)
        self.image = self.imagens_ferramenta[0]
        self.rect = self.image.get_rect()
        self.rect.center = (ferramenta_x+20, ferramenta_y+20)

class Estrela(pygame.sprite.Sprite):
    def __init__(self, x, y, sprite_estrela):
        pygame.sprite.Sprite.__init__(self)
        self.imagens_estrela = []
        self.img_estrela = pygame.transform.scale(sprite_estrela, (32*1.5, 32*1.5))
        self.imagens_estrela.append(self.img_estrela)
        self.image = self.imagens_estrela[0]
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)

class Contapxt(pygame.sprite.Sprite):
    def __init__(self, sprite_pxt):
        pygame.sprite.Sprite.__init__(self)
        self.imagens_e = []
        self.img_e = pygame.transform.scale(sprite_pxt, (64*3.5, 32*3.5))
        self.imagens_e.append(self.img_e)
        self.image = self.imagens_e[0]
        self.rect = self.image.get_rect()
        self.rect.center = (500, 30)


def seguirx(personagem_posicaox, inimigo_posicaox, inimigo_velocidade):
    diferenca_x = personagem_posicaox - inimigo_posicaox
    if diferenca_x > 0:
        return inimigo_posicaox + inimigo_velocidade
    else:
        return inimigo_posicaox - inimigo_velocidade

def seguiry(personagem_posicaoy, inimigo_posicaoy, inimigo_velocidade):
    diferenca_x = personagem_posicaoy - inimigo_posicaoy
    if diferenca_x > 0:
        return inimigo_posicaoy + inimigo_velocidade
    else:
        return inimigo_posicaoy - inimigo_velocidade

Game()