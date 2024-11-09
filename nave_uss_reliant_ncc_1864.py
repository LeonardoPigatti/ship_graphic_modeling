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

# Função para desenhar uma nave em 3D
def desenhar_nave(x_pos, y_pos, z_pos, rot_x, rot_y, rot_z):
    # Corpo da nave - um cubo para representar a base
    glColor3f(1, 0, 0)  # Cor da nave (vermelho)
    glPushMatrix()  # Empilha a matriz para que transformações não afetem outros objetos
    glTranslatef(x_pos, y_pos, z_pos)  # Move a nave para a posição x_pos no eixo X

    # Rotação da nave nos eixos X, Y e Z
    glRotatef(rot_x, 1, 0, 0)  # Rotaciona a nave ao redor do eixo X
    glRotatef(rot_y, 0, 1, 0)  # Rotaciona a nave ao redor do eixo Y
    glRotatef(rot_z, 0, 0, 1)  # Rotaciona a nave ao redor do eixo Z

    # Corpo principal da nave (cubos)
    glBegin(GL_QUADS)
    
    # Frente da nave (um quadrado)
    glVertex3f(-3, -1, 2)
    glVertex3f(3, -1, 2)
    glVertex3f(3, 1, 2)
    glVertex3f(-3, 1, 2)
    
    # Traseira da nave (um quadrado)
    glVertex3f(-3, -1, -2)
    glVertex3f(3, -1, -2)
    glVertex3f(3, 1, -2)
    glVertex3f(-3, 1, -2)
    
    # Lados da nave (quatro quadrados)
    # Lado esquerdo
    glVertex3f(-3, -1, 2)
    glVertex3f(-3, -1, -2)
    glVertex3f(-3, 1, -2)
    glVertex3f(-3, 1, 2)
    
    # Lado direito
    glVertex3f(3, -1, 2)
    glVertex3f(3, -1, -2)
    glVertex3f(3, 1, -2)
    glVertex3f(3, 1, 2)
    
    # Topo
    glVertex3f(-3, 1, 2)
    glVertex3f(3, 1, 2)
    glVertex3f(3, 1, -2)
    glVertex3f(-3, 1, -2)
    
    # Fundo
    glVertex3f(-3, -1, 2)
    glVertex3f(3, -1, 2)
    glVertex3f(3, -1, -2)
    glVertex3f(-3, -1, -2)
    
    glEnd()

    # Asa superior - uma pirâmide
    glPushMatrix()
    glTranslatef(0, 2.5, 0)  # Move a asa superior para cima
    glColor3f(0, 0, 1)  # Cor da asa (azul)
    glBegin(GL_TRIANGLES)
    
    # Triângulo da asa
    glVertex3f(-4, 0, 2)
    glVertex3f(4, 0, 2)
    glVertex3f(0, 2, 0)
    
    glVertex3f(-4, 0, -2)
    glVertex3f(4, 0, -2)
    glVertex3f(0, 2, 0)
    
    glEnd()
    glPopMatrix()

    glPopMatrix()  # Restaura a transformação original

def main():
    inicializar_janela()
    
    # Posições iniciais da nave
    x_pos = 0.0
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
        if teclas[K_w]:
            z_pos += 0.1  # Move para frente (para o plano da tela)
        if teclas[K_s]:
            z_pos -= 0.1  # Move para trás

        # Rotação da nave
        if teclas[K_a]:
            rot_y += 1  # Rotaciona ao redor do eixo Y (sentido anti-horário)
        if teclas[K_d]:
            rot_y -= 1  # Rotaciona ao redor do eixo Y (sentido horário)
        if teclas[K_q]:
            rot_x += 1  # Rotaciona ao redor do eixo X
        if teclas[K_e]:
            rot_x -= 1  # Rotaciona ao redor do eixo X

        # Desenha o fundo com as estrelas
        desenhar_espaco()

        # Desenha a nave 3D na posição e rotação especificada
        desenhar_nave(x_pos, y_pos, z_pos, rot_x, rot_y, rot_z)

        pygame.display.flip()  # Atualiza a tela a cada frame
        pygame.time.wait(10)  # Pequena pausa para controlar a taxa de atualização

if __name__ == "__main__":
    main()
