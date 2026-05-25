from direct.showbase.ShowBase import ShowBase
from panda3d.core import ClockObject

globalClock = ClockObject.getGlobalClock()

class MovimentacaoCubo(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        # 1. Carregar o cubo nativo
        self.cubo = self.loader.loadModel("models/box")
        self.cubo.reparentTo(self.render)
        self.cubo.setPos(0, 15, 0) # Afastado no eixo Y para ser visível

        # 2. Dicionário de estado das teclas
        self.keyMap = {"left": False, "right": False, "up": False, "down": False}

        # 3. Mapeamento dos botões (pressionar e largar)
        for key, name in [("arrow_left", "left"), ("arrow_right", "right"), 
                          ("arrow_up", "up"), ("arrow_down", "down")]:
            self.accept(key, self.updateKeyMap, [name, True])
            self.accept(key + "-up", self.updateKeyMap, [name, False])

        # 4. Adicionar o Game Loop
        self.taskMgr.add(self.update, "update")

    def updateKeyMap(self, key, state):
        self.keyMap[key] = state

    def update(self, task):
        dt = globalClock.getDt() # Delta Time
        pos = self.cubo.getPos()
        velocidade = 0.5 * dt

        if self.keyMap["left"]:  pos.x -= velocidade
        if self.keyMap["right"]: pos.x += velocidade
        if self.keyMap["up"]:    pos.z += velocidade
        if self.keyMap["down"]:  pos.z -= velocidade

        self.cubo.setPos(pos)
        return task.cont

if __name__ == "__main__":
    app = MovimentacaoCubo()
    app.run()