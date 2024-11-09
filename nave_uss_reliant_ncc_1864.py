import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import random

# Inicialização da janela usando pygame
def inicializar_janela():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(45, (display[0] / display[1]), 0.1, 100.0)
    glTranslatef(0.0, 0.0, -50)  # Ajusta a posição da câmera para visualizar o espaço

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

# Função para desenhar a nave
def desenhar_nave():
    glColor3f(1, 0, 0)  # Cor da nave (vermelho)

    # Corpo da nave (triângulo)
    glBegin(GL_TRIANGLES)
    glVertex3f(0, 2, 0)  # Ponta da nave
    glVertex3f(-2, -2, 0)  # Base da nave à esquerda
    glVertex3f(2, -2, 0)  # Base da nave à direita
    glEnd()

    # Asas da nave (retângulos)
    glColor3f(0, 0, 1)  # Cor das asas (azul)

    # Asa esquerda
    glBegin(GL_QUADS)
    glVertex3f(-2, -2, 0)
    glVertex3f(-4, -4, 0)
    glVertex3f(-4, -6, 0)
    glVertex3f(-2, -6, 0)
    glEnd()

    # Asa direita
    glBegin(GL_QUADS)
    glVertex3f(2, -2, 0)
    glVertex3f(4, -4, 0)
    glVertex3f(4, -6, 0)
    glVertex3f(2, -6, 0)
    glEnd()

def main():
    inicializar_janela()
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return

        desenhar_espaco()  # Desenha o fundo com as estrelas
        desenhar_nave()  # Desenha a nave no centro da tela
        pygame.display.flip()  # Atualiza a tela a cada frame
        pygame.time.wait(10)   # Pequena pausa para controlar a taxa de atualização

if __name__ == "__main__":
    main()
