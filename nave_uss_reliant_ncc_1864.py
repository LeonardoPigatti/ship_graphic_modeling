import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import random
import math

# Inicialização da janela usando pygame
def inicializar_janela():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(30, (display[0] / display[1]), 0.1, 100.0)  # Ajuste do FOV (campo de visão)
    glTranslatef(0.0, 0.0, -20)  # Ajusta a posição da câmera para visualizar o espaço (mais próximo)

# Função para desenhar estrelas no espaço
def desenhar_espaco():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # Limpa a tela
    glBegin(GL_POINTS)  # Inicia o desenho de pontos para as "estrelas"
    for _ in range(200):  # Número de estrelas
        glColor3f(1, 1, 1)  # Cor branca para as estrelas
        glVertex3f(
            random.uniform(-40, 40),  # Distribui as estrelas no eixo X
            random.uniform(-30, 30),  # Distribui as estrelas no eixo Y
            random.uniform(-100, 0)   # Distribui as estrelas no eixo Z para profundidade
        )
    glEnd()

# Função para desenhar a nave (agora como um disco cinza)
def desenhar_nave(x_pos, y_pos, z_pos, rot_x, rot_y, rot_z):
    glPushMatrix()  # Empilha a matriz para que transformações não afetem outros objetos
    glTranslatef(x_pos, y_pos, z_pos)  # Move a nave para a posição x_pos no eixo X

    # Rotação da nave nos eixos X, Y e Z
    glRotatef(rot_x, 1, 0, 0)  # Rotaciona a nave ao redor do eixo X
    glRotatef(rot_y, 0, 1, 0)  # Rotaciona a nave ao redor do eixo Y
    glRotatef(rot_z, 0, 0, 1)  # Rotaciona a nave ao redor do eixo Z

    # Corpo da nave - um disco cinza
    glColor3f(0.5, 0.5, 0.5)  # Cor cinza para a nave
    gluDisk(gluNewQuadric(), 0, 5, 32, 1)  # Desenha um disco com raio 5 e espessura 1

    # Desenhando os pontos na parte superior da nave (círculos de pontos)
    desenhar_pontos_nave()

    # Adicionando a bola vermelha brilhante na borda da nave
    desenhar_bola_vermelha()

    glPopMatrix()  # Restaura a transformação original

# Função para desenhar os pontos na parte de cima da nave
def desenhar_pontos_nave():
    glPushMatrix()  # Empilha a matriz para não afetar transformações anteriores

    # Translação para posicionar os pontos na parte de cima da nave
    glTranslatef(0.0, 0.0, 0.5)  # Ajusta para um pouco acima da nave

    # Vamos desenhar círculos concêntricos de pontos
    num_circulos = 9 #ESSA PARTE TEM QUE SER AUMENTADA CASO AUMENTE O TAMNHO DA NAVE
    for i in range(num_circulos):
        raio = 0.5 + i * 0.5  # Aumenta o raio conforme o número de círculos
        num_pontos = 12 + i * 6  # Aumenta o número de pontos por círculo

        # Desenha o círculo de pontos
        glBegin(GL_POINTS)
        for j in range(num_pontos):
            angulo = 2 * math.pi * j / num_pontos  # Usando math.pi em vez de pygame.math
            x = raio * math.cos(angulo)  # Posição X dos pontos
            y = raio * math.sin(angulo)  # Posição Y dos pontos
            
            # Alterar a cor dos pontos alternando entre branco e amarelo
            if i % 2 == 0:
                glColor3f(1, 1, 1)  # Branco
            else:
                glColor3f(1, 1, 0)  # Amarelo
            glVertex3f(x, y, 0)  # Adiciona o ponto à cena
        glEnd()

    glPopMatrix()  # Restaura a transformação original

# Função para desenhar a bola vermelha brilhante na borda da nave
def desenhar_bola_vermelha():
    glPushMatrix()  # Empilha a matriz para que transformações não afetem outros objetos

    # Translação para posicionar a bola na borda da nave (canto superior direito)
    glTranslatef(5.0, 0.0, 1.0)  # Ajuste para a borda da nave

    # Desenha a esfera vermelha
    glColor3f(1, 0, 0)  # Cor vermelha para a bola
    quadric = gluNewQuadric()  # Cria um objeto quadrático para desenhar a esfera
    gluSphere(quadric, 0.5, 10, 10)  # Desenha a esfera sólida com raio 0.5

    glPopMatrix()  # Restaura a transformação original

def main():
    inicializar_janela()
    
    # Posições iniciais da nave (começando à esquerda da tela)
    x_pos = -10.0  # Nave começa fora da tela (à esquerda)
    y_pos = 0.0
    z_pos = -50.0

    # Variáveis de rotação para controlar a nave
    rot_x = 0
    rot_y = 0
    rot_z = 0

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return

        # Captura das teclas pressionadas para mover e rotacionar a nave
        teclas = pygame.key.get_pressed()
        
        # Movimento da nave
        if teclas[K_LEFT]:
            x_pos -= 0.1  # Move para a esquerda
        if teclas[K_RIGHT]:
            x_pos += 0.1  # Move para a direita
        if teclas[K_UP]:
            y_pos += 0.1  # Move para cima
        if teclas[K_DOWN]:
            y_pos -= 0.1  # Move para baixo

        # Rotação da nave
        if teclas[K_w]:
            rot_x += 1  # Rotaciona ao redor do eixo X (sentido anti-horário)
        if teclas[K_s]:
            rot_x -= 1  # Rotaciona ao redor do eixo X (sentido horário)
        
        # Apenas as teclas W e S devem rotacionar a nave ao redor do eixo Y
        if teclas[K_a]:
            rot_y += 1  # Rotaciona ao redor do eixo Y (sentido anti-horário)
        if teclas[K_d]:
            rot_y -= 1  # Rotaciona ao redor do eixo Y (sentido horário)

        # Animação da nave chegando à tela
        if x_pos < 0:
            x_pos += 0.1  # A nave se move para a direita até alcançar a posição inicial na tela

        # Desenha o fundo com as estrelas
        desenhar_espaco()

        # Desenha a nave 3D (agora um disco cinza) na posição e rotação especificada
        desenhar_nave(x_pos, y_pos, z_pos, rot_x, rot_y, rot_z)

        pygame.display.flip()  # Atualiza a tela a cada frame
        pygame.time.wait(10)  # Pequena pausa para controlar a taxa de atualização

if __name__ == "__main__":
    main()
