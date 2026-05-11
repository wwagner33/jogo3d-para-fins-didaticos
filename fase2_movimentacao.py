from direct.showbase.ShowBase import ShowBase
from panda3d.core import loadPrcFileData
import sys

loadPrcFileData('', 'window-title Fase 2: Movimentação WASD e Limites')
loadPrcFileData('', 'win-size 800 600')

class Fase2(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        
        # 1. Espaço Virtual e Atores
        self.jogador = self.loader.loadModel("models/panda-model")
        self.jogador.reparentTo(self.render)
        self.jogador.setScale(0.005)
        self.jogador.setPos(0, 0, 0)

        self.LIMITE_X = 20
        self.LIMITE_Y = 20
        
        self.cam.setPos(0, -50, 30)
        self.cam.lookAt(0, 0, 0)

        # 2. Mapa de Teclas (WASD)
        self.keyMap = {"w": False, "s": False, "a": False, "d": False}
        self.accept("w", self.setKey, ["w", True])
        self.accept("w-up", self.setKey, ["w", False])
        self.accept("s", self.setKey, ["s", True])
        self.accept("s-up", self.setKey, ["s", False])
        self.accept("a", self.setKey, ["a", True])
        self.accept("a-up", self.setKey, ["a", False])
        self.accept("d", self.setKey, ["d", True])
        self.accept("d-up", self.setKey, ["d", False])
        self.accept("escape", sys.exit)

        # 3. Inicialização do Game Loop para controle de movimento
        self.taskMgr.add(self.controle_movimento, "ControleMovimento")

    def setKey(self, key, val): 
        self.keyMap[key] = val

    def controle_movimento(self, task):
        dt = globalClock.getDt()
        pos = self.jogador.getPos()
        vel = 15.0 * dt

        # Vetores de movimento
        if self.keyMap["w"]: pos.y += vel
        if self.keyMap["s"]: pos.y -= vel
        if self.keyMap["a"]: pos.x -= vel
        if self.keyMap["d"]: pos.x += vel

        # Aplicação Algébrica dos Limites de Mundo
        pos.x = max(min(pos.x, self.LIMITE_X), -self.LIMITE_X)
        pos.y = max(min(pos.y, self.LIMITE_Y), -self.LIMITE_Y)
        
        self.jogador.setPos(pos)
        return task.cont

if __name__ == "__main__":
    app = Fase2()
    app.run()