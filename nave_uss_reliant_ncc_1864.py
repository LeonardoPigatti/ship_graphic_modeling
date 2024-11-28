import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import random
import math
import time

# Função para exibir a imagem e o texto por 10 segundos
def exibir_imagem():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))  # Tamanho da janela de exibição
    imagem = pygame.image.load(r'C:\Users\Pichau\OneDrive\Área de Trabalho\leonard_2.jpg')  # Caminho da imagem
    
    # Exibe a imagem na tela
    screen.blit(imagem, (0, 0))

    # Função para desenhar o quadro com o texto
    def desenhar_texto():
        font = pygame.font.SysFont("Arial", 15)  # Fonte do texto, tamanho ajustado
        texto_original = ("Capitão Kirk, sua missão é conduzir a Enterprise até a zona de neutralidade, "
                          "onde uma disputa entre duas facções galácticas ameaça a paz. Utilize a diplomacia para "
                          "evitar o conflito e, se necessário, empregue a lógica para garantir que nossa presença "
                          "não seja vista como uma ameaça. A sobrevivência da Enterprise e a preservação da paz "
                          "dependem de suas decisões.")
        
        # Quebra o texto em múltiplas linhas para caber no quadro
        palavras = texto_original.split(" ")
        linhas = []
        linha_atual = ""
        for palavra in palavras:
            # Se a linha atual com a próxima palavra for maior que o limite (em pixels), começa uma nova linha
            if font.size(linha_atual + " " + palavra)[0] <= 700:  # 700 é o limite de largura do quadro
                linha_atual += " " + palavra
            else:
                linhas.append(linha_atual)
                linha_atual = palavra
        if linha_atual:
            linhas.append(linha_atual)

        # Desenha o quadro (fundo preto)
        pygame.draw.rect(screen, (0, 0, 0), (50, 450, 700, 150))  # Desenha o quadro com altura ajustada

        # Exibe cada linha de texto no quadro
        y_offset = 470  # Posição inicial vertical do texto
        for linha in linhas:
            texto = font.render(linha, True, (255, 255, 255))  # Texto em branco
            screen.blit(texto, (60, y_offset))  # Exibe o texto
            y_offset += 30  # Ajusta a posição vertical para a próxima linha

    desenhar_texto()  # Chama a função para desenhar o texto com o quadro

    pygame.display.flip()

    # Espera 10 segundos antes de continuar
    time.sleep(1)

    # Fecha a janela
    pygame.quit()

# Função para inicializar a janela OpenGL usando pygame
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

# Função para desenhar os pontos na parte de cima da nave
def desenhar_pontos_nave():
    glPushMatrix()  # Empilha a matriz para não afetar transformações anteriores

    # Translação para posicionar os pontos na parte de cima da nave
    glTranslatef(0.0, 0.0, 0.0)  # Ajusta para um pouco acima da nave

    # Vamos desenhar círculos concêntricos de pontos
    num_circulos = 9
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

# Função para desenhar as turbinas da nave
def desenhar_turbinas():
    glPushMatrix()  # Salva a matriz atual

    # Primeira turbina (lado esquerdo)
    glPushMatrix()
    glTranslatef(-5.5, 0.0, 2.0)  # Move a turbina para baixo e à esquerda da nave
    glRotatef(90, 1, 0, 0)  # Rotaciona para alinhar o cilindro verticalmente

    # Corpo da turbina (cilindro)
    glColor3f(0.5, 0.5, 0.5)  # Cor cinza para o corpo
    gluCylinder(gluNewQuadric(), 0.5, 0.5, 2, 32, 32)  # Desenha o cilindro

    # Tampa superior (cor cinza)
    glPushMatrix()
    glTranslatef(0, 0, 2)  # Move para a tampa superior
    glColor3f(0.5, 0.5, 0.5)  # Cor cinza para a tampa superior
    gluDisk(gluNewQuadric(), 0, 0.5, 32, 32)  # Desenha a tampa superior
    glPopMatrix()

    # Tampa inferior (cor azul)
    glPushMatrix()
    glTranslatef(0, 0, 2)  # Move para a tampa inferior
    glColor3f(0.0, 0.0, 1.0)  # Cor azul para a tampa inferior
    gluDisk(gluNewQuadric(), 0, 0.5, 32, 32)  # Desenha a tampa inferior
    glPopMatrix()

    glPopMatrix()

    # Segunda turbina (lado direito)
    glPushMatrix()
    glTranslatef(5.5, 0.0, 2.0)  # Move a turbina para baixo e à direita da nave
    glRotatef(90, 1, 0, 0)  # Rotaciona para alinhar o cilindro verticalmente

    # Corpo da turbina (cilindro)
    glColor3f(0.5, 0.5, 0.5)  # Cor cinza para o corpo
    gluCylinder(gluNewQuadric(), 0.5, 0.5, 2, 32, 32)  # Desenha o cilindro

    # Tampa superior (cor cinza)
    glPushMatrix()
    glTranslatef(0, 0, 2)  # Move para a tampa superior
    glColor3f(0.5, 0.5, 0.5)  # Cor cinza para a tampa superior
    gluDisk(gluNewQuadric(), 0, 0.5, 32, 32)  # Desenha a tampa superior
    glPopMatrix()

    # Tampa inferior (cor azul)
    glPushMatrix()
    glTranslatef(0, 0, 2)  # Move para a tampa inferior
    glColor3f(0.0, 0.0, 1.0)  # Cor azul para a tampa inferior
    gluDisk(gluNewQuadric(), 0, 0.5, 32, 32)  # Desenha a tampa inferior
    glPopMatrix()

    glPopMatrix()

    glPopMatrix()  # Restaura a matriz original


# Função para desenhar a nave
def desenhar_nave(x_pos, y_pos, z_pos, rot_x, rot_y, rot_z):
    glPushMatrix()  # Empilha a matriz para que transformações não afetem outros objetos
    glTranslatef(x_pos, y_pos, z_pos)  # Move a nave para a posição x_pos no eixo X

    # Rotação da nave nos eixos X, Y e Z
    glRotatef(rot_x, 1, 0, 0)  # Rotaciona a nave ao redor do eixo X
    glRotatef(rot_y, 0, 1, 0)  # Rotaciona a nave ao redor do eixo Y
    glRotatef(rot_z, 0, 0, 1)  # Rotaciona a nave ao redor do eixo Z

    # Corpo da nave - um disco cinza
    glColor3f(0.5, 0.5, 0.5)  # Cor cinza para a nave
    gluCylinder(gluNewQuadric(), 5, 5, 1.5, 32, 32)  # Desenha um disco com raio 5 e espessura 1
    
    # Base inferior da nave
    glPushMatrix()  # Salva o estado atual da matriz
    glTranslatef(0, 0, 1.5)  # Move para a base inferior
    glColor3f(0.5, 0.5, 0.5)  # Cor cinza para a base inferior
    gluDisk(gluNewQuadric(), 0, 5, 32, 32)  # Cria o disco para a base inferior
    glPopMatrix()  # Restaura o estado da matriz
    
    # Base superior da nave
    glPushMatrix()  # Salva o estado atual da matriz
    glTranslatef(0, 0, 1.5)  # Move para a base superior
    glColor3f(0.5, 0.5, 0.5)  # Cor cinza para a base superior
    gluDisk(gluNewQuadric(), 0, 5, 32, 32)  # Cria o disco para a base superior
    glPopMatrix()  # Restaura o estado da matriz

    # Desenhando os pontos na parte superior da nave
    desenhar_pontos_nave()

    # Adicionando a bola vermelha brilhante na borda da nave

    # Adicionando as turbinas abaixo da nave
    desenhar_turbinas()

    glPopMatrix()  # Restaura a transformação original

# Função principal
def main():
    # Exibe a imagem antes do resto do código
    exibir_imagem()

    # Inicializa a janela OpenGL
    inicializar_janela()
    
    # Posições iniciais da nave (começando à esquerda da tela)
    x_pos = -10.0  # Nave começa fora da tela (à esquerda)
    y_pos = 0.0
    z_pos = -50.0

    # Variáveis de rotação para controlar a nave
    rot_x = 0
    rot_y = 0
    rot_z = 0

    # Variáveis de controle de piscar
    piscar = False  # Controle para ativar/desativar o piscar
    tempo_piscar = 0  # Controla o tempo de piscar

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
        if teclas[K_a]:
            rot_y += 1  # Rotaciona ao redor do eixo Y (sentido anti-horário)
        if teclas[K_d]:
            rot_y -= 1  # Rotaciona ao redor do eixo Y (sentido horário)

        # Ativa/desativa o piscar com a tecla "G"
        if teclas[K_g]:
            x_pos += 0.8  # Move para a direita
            z_pos += 0.8  # Move para a direita
            piscar = True
            tempo_piscar = time.time()  # Marca o tempo de início do piscar

        # Se estiver piscando, alterne a cor da tela
        if piscar:
            # Verifica o tempo de piscar
            if time.time() - tempo_piscar < 0.5:  # Pisca por 0.5 segundos
                if (int(time.time() * 10) % 2) == 0:  # Alterna a cor a cada 0.5 segundos
                    glClearColor(75/255, 224/255, 228/255, 1)  # Cor #4BE0E4
                else:
                    glClearColor(0, 0, 0, 1)  # Cor normal (preto)
            else:
                piscar = False  # Desativa o piscar após o tempo
                glClearColor(0, 0, 0, 1)  # Cor normal (preto)
                
        if teclas[K_f]:
            x_pos -= 0.8  # Move para a direita
            z_pos -= 0.8  # Move para a direita
            piscar = True
            tempo_piscar = time.time()  # Marca o tempo de início do piscar

        # Se estiver piscando, alterne a cor da tela
        if piscar:
            # Verifica o tempo de piscar
            if time.time() - tempo_piscar < 0.5:  # Pisca por 0.5 segundos
                if (int(time.time() * 10) % 2) == 0:  # Alterna a cor a cada 0.5 segundos
                    glClearColor(75/255, 224/255, 228/255, 1)  # Cor #4BE0E4
                else:
                    glClearColor(0, 0, 0, 1)  # Cor normal (preto)
            else:
                piscar = False  # Desativa o piscar após o tempo
                glClearColor(0, 0, 0, 1)  # Cor normal (preto)
        
        # Desenha o espaço e a nave
        desenhar_espaco()
        desenhar_nave(x_pos, y_pos, z_pos, rot_x, rot_y, rot_z)

        # Atualiza a tela
        pygame.display.flip()
        pygame.time.wait(10)  # Pequena pausa para suavizar a animação

if __name__ == "__main__":
    main()
