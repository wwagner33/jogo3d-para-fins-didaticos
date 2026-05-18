from direct.showbase.ShowBase import ShowBase
from panda3d.core import loadPrcFileData
import sys

# Configuração da janela
loadPrcFileData('', 'window-title Controle de Camera Orbital')
loadPrcFileData('', 'win-size 800 600')

class CameraOrbital(ShowBase):
    def __init__(self):
        # 1. Inicializa o motor
        ShowBase.__init__(self)
        self.setBackgroundColor(0.1, 0.1, 0.1)

        # 2. Desativa o controle automático do mouse padrão do Panda3D
        self.disableMouse()

        # 3. Carrega o modelo do personagem (Alvo da Câmera)
        self.jogador = self.loader.loadModel("models/panda-model")
        self.jogador.reparentTo(self.render)
        self.jogador.setScale(0.005)
        self.jogador.setPos(0, 0, 0)

        # 4. CONCEITO DO GRAFO DE CENA: Criação do Nó Pivô
        # Criamos um nó vazio anexado diretamente ao render
        self.pivo_camera = self.render.attachNewNode("PivoCamera")
        self.pivo_camera.setPos(self.jogador.getPos()) # Centralizado no jogador

        # Tornamos a Câmera nativa (self.cam) FILHA do Pivô
        self.cam.reparentTo(self.pivo_camera)
        
        # Define a posição LOCAL da câmera em relação ao seu pai (o pivô)
        # Y = -40 (afastada 40 unidades para trás), Z = 8 (subida 8 unidades)
        self.cam.setPos(0, -40, 8)
        self.cam.lookAt(self.pivo_camera) # Força a câmera a olhar para o centro do pivô

        # 5. Controles de Zoom (Leitura dos eventos de rolagem do mouse)
        self.accept("wheel_up", self.ajustar_zoom, [-2.0])
        self.accept("wheel_down", self.ajustar_zoom, [2.0])
        self.accept("escape", sys.exit)

        # 6. Adiciona a tarefa de atualização da câmera ao Game Loop
        self.taskMgr.add(self.atualizar_camera, "AtualizarCamera")

    def ajustar_zoom(self, quantidade):
        """Altera a distância da câmera movendo-a no eixo local Y do pivô"""
        nova_distancia = self.cam.getY() - quantidade
        
        # Limita o zoom (Clamping) para evitar que a câmera atravesse o modelo ou se afaste demais
        nova_distancia = max(min(nova_distancia, -10.0), -80.0)
        self.cam.setY(nova_distancia)

    def atualizar_camera(self, task):
        """Captura a posição do mouse e rotaciona o pivô a cada frame"""
        if self.mouseWatcherNode.hasMouse():
            # Captura as coordenadas do mouse na janela (variam de -1.0 a 1.0)
            mouse_x = self.mouseWatcherNode.getMouseX()
            mouse_y = self.mouseWatcherNode.getMouseY()

            # Rotaciona o Nó Pivô. Como a câmera é filha dele, ela orbita o centro automaticamente.
            # Heading (H): Rotação no eixo Z (olhar para os lados / rotação horizontal)
            # Pitch (P): Rotação no eixo X (olhar para cima e para baixo / inclinação vertical)
            self.pivo_camera.setH(-mouse_x * 180)
            self.pivo_camera.setP(mouse_y * 45)

        return task.cont

if __name__ == "__main__":
    app = CameraOrbital()
    app.run()