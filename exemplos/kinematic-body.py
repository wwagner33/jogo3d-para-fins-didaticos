from direct.showbase.ShowBase import ShowBase
from panda3d.bullet import BulletWorld, BulletRigidBodyNode, BulletBoxShape
from panda3d.core import Vec3

class FisicaKinematic(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.cam.setPos(0, -20, 5)

        # 1. Configuração do Mundo Físico
        self.world = BulletWorld()
        self.world.setGravity(Vec3(0, 0, -9.81))

        # 2. Criar a forma de colisão (Uma caixa 1x1x1)
        shape = BulletBoxShape(Vec3(0.5, 0.5, 0.5))

        # 3. Criar o Nó do Corpo Rígido
        node = BulletRigidBodyNode('JogadorKinematic')
        node.addShape(shape)

        # --- A CONFIGURAÇÃO CHAVE ---
        node.setKinematic(True) 
        # O motor de física sabe que este objeto existe e bloqueia a passagem
        # de outros objetos, mas só se move quando nós o mandarmos mover.

        # 4. Ligar ao Grafo de Cena e ao Mundo Físico
        self.corpo_np = self.render.attachNewNode(node)
        self.corpo_np.setPos(0, 0, 1)
        self.world.attachRigidBody(node)

        # (Opcional) Carregar modelo visual e colar ao nó físico
        modelo = self.loader.loadModel("models/box")
        modelo.reparentTo(self.corpo_np)

        self.taskMgr.add(self.update_fisica, "update_fisica")

    def update_fisica(self, task):
        dt = globalClock.getDt()
        # Atualiza a simulação física
        self.world.doPhysics(dt)
        return task.cont

if __name__ == "__main__":
    app = FisicaKinematic()
    app.run()