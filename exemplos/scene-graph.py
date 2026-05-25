from math import pi, sin, cos

from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor


class SceneGraph(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        # 1. Carrega o ambiente (Pai no render)
        self.scene = self.loader.loadModel("models/environment")
        self.scene.reparentTo(self.render)
        self.scene.setScale(0.25, 0.25, 0.25)
        self.scene.setPos(-8, 42, 0)

        # 2. Configura a câmera
        self.taskMgr.add(self.spinCameraTask, "SpinCameraTask")

        # ==========================================
        # DEMONSTRAÇÃO DO GRAFO DE CENA (PAI E FILHO)
        # ==========================================

        # 3. Cria o NÓ PAI (Panda Pai) e anexa à raiz (render)
        self.pandaPai = Actor("models/panda-model", {"walk": "models/panda-walk4"})
        self.pandaPai.setScale(0.015, 0.015, 0.015)
        self.pandaPai.reparentTo(self.render)
        self.pandaPai.loop("walk")

        # 4. Cria o NÓ FILHO (Panda Filho)
        self.pandaFilho = Actor("models/panda-model", {"walk": "models/panda-walk4"})
        
        # O filho é anexado ao pai, não ao render!
        self.pandaFilho.reparentTo(self.pandaPai)
        
        # Como o filho está no espaço de coordenadas do pai, sua escala e 
        # posição são RELATIVAS ao pai. 
        self.pandaFilho.setScale(0.7, 0.7, 0.7) # Escala relativa ao pai
        self.pandaFilho.setPos(500, -500, 0)    # Posição relativa ao centro do pai
        self.pandaFilho.loop("walk")

        # 5. Adiciona uma tarefa para girar APENAS o Panda Pai
        self.taskMgr.add(self.spinPandaTask, "SpinPandaTask")

    # Procedimento para mover a câmera
    def spinCameraTask(self, task):
        angleDegrees = task.time * 6.0
        angleRadians = angleDegrees * (pi / 180.0)
        self.camera.setPos(20 * sin(angleRadians), -20 * cos(angleRadians), 3)
        self.camera.setHpr(angleDegrees, 0, 0)
        return Task.cont

    # Procedimento para girar o Panda Pai
    def spinPandaTask(self, task):
        # Giramos o Panda Pai em seu próprio eixo (Heading)
        self.pandaPai.setH(task.time * 50.0)
        return Task.cont


app = SceneGraph()
app.run()