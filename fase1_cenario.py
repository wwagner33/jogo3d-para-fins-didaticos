from direct.showbase.ShowBase import ShowBase
from panda3d.core import loadPrcFileData

# Configuração da janela
loadPrcFileData('', 'window-title Fase 1: Cenário e Atores')
loadPrcFileData('', 'win-size 800 600')

class Fase1(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        
        # 1. Criação do Espaço Virtual e Atores
        self.jogador = self.loader.loadModel("models/panda-model")
        self.jogador.reparentTo(self.render)
        self.jogador.setScale(0.005)
        self.jogador.setPos(0, 0, 0) # Posição central inicial

        # 2. Definição dos Limites de Mundo
        self.LIMITE_X = 20
        self.LIMITE_Y = 20
        
        # 3. Posicionamento da câmera
        self.cam.setPos(0, -50, 30)
        self.cam.lookAt(0, 0, 0)

# Executa o código
if __name__ == "__main__":
    app = Fase1()
    app.run()