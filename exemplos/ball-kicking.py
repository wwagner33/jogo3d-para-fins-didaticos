from direct.showbase.ShowBase import ShowBase
from panda3d.bullet import BulletWorld, BulletRigidBodyNode, BulletSphereShape, BulletPlaneShape
from panda3d.core import Vec3, ClockObject

class FisicaQuique(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        
        # Desativa o controle de câmera padrão do mouse para não sumir ao clicar
        self.disableMouse() 
        # Posiciona a câmera para vermos a queda (X, Y, Z)
        self.cam.setPos(0, -30, 5) 

        # 1. Configuração do Mundo Físico
        self.world = BulletWorld()
        self.world.setGravity(Vec3(0, 0, -9.81)) # Gravidade da Terra apontando para baixo (Eixo Z)

        # ==========================================
        # 2. O CHÃO (Objeto Estático)
        # ==========================================
        # Criamos um plano infinito virado para cima (vetor 0, 0, 1)
        forma_chao = BulletPlaneShape(Vec3(0, 0, 1), 0)
        
        no_chao = BulletRigidBodyNode('Chao')
        no_chao.addShape(forma_chao)
        # Elasticidade do chão (0 é chumbo, 1 é borracha perfeita)
        no_chao.setRestitution(0.8) 
        
        np_chao = self.render.attachNewNode(no_chao)
        np_chao.setPos(0, 0, 0)
        self.world.attachRigidBody(no_chao)

        # Representação visual do chão (uma caixa muito larga e achatada)
        visual_chao = self.loader.loadModel("models/box")
        visual_chao.setScale(2000, 500, 0.5)
        visual_chao.setPos(0, 0, -0.1) # Alinha o topo da caixa com a física do plano
        visual_chao.setColor(0.1,0.5,0.2,1)
        visual_chao.reparentTo(np_chao)

        # ==========================================
        # 3. A ESFERA (Objeto Dinâmico)
        # ==========================================
        # Raio da esfera física = 1.0
        forma_esfera = BulletSphereShape(1.0)
        
        no_esfera = BulletRigidBodyNode('Esfera')
        no_esfera.addShape(forma_esfera)
        
        # A MÁGICA ESTÁ AQUI: Dar massa ao objeto faz com que a física o puxe para baixo!
        no_esfera.setMass(1.0)
        # Elasticidade da esfera
        no_esfera.setRestitution(0.7)
        
        np_esfera = self.render.attachNewNode(no_esfera)
        np_esfera.setPos(0, 0, 15) # Começa no alto (Z = 15) para poder cair
        self.world.attachRigidBody(no_esfera)

        # Representação visual da esfera (Usaremos o 'smiley', o modelo padrão clássico do Panda3D)
        visual_esfera = self.loader.loadModel("models/smiley")
        visual_esfera.reparentTo(np_esfera)

        # ==========================================
        # 4. LOOP DE ATUALIZAÇÃO DA FÍSICA
        # ==========================================
        self.taskMgr.add(self.update_fisica, "update_fisica")

    def update_fisica(self, task):
        # Pega a instância do relógio global e extrai o dt (Delta Time)
        dt = ClockObject.getGlobalClock().getDt()
        
        # Atualiza a simulação física
        self.world.doPhysics(dt)
        return task.cont

if __name__ == "__main__":
    app = FisicaQuique()
    app.run()