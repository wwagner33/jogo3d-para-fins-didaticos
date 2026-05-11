from direct.showbase.ShowBase import ShowBase
from direct.gui.OnscreenText import OnscreenText
from panda3d.core import TextNode, PerspectiveLens, OrthographicLens
import sys

class VisualizadorDimensoes(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        
        # Configurações Iniciais
        self.is_3d_mode = True
        self.disableMouse() # Vamos controlar a câmera via código
        
        # 1. Carregar o Objeto de Teste (Um Cubo)
        # Note que mesmo no "2D", o objeto é 3D, mas a lente dita como o vemos.
        self.objeto = self.loader.loadModel("models/box")
        self.objeto.reparentTo(self.render)
        self.objeto.setPos(0, 20, 0) # X=0, Y=20 (distância da cam), Z=0
        self.objeto.setScale(2)
        
        # 2. Interface de Instruções
        self.info_text = OnscreenText(
            text="Pressione [ESPAÇO] para alternar entre 2D e 3D\nModo Atual: 3D (Perspectiva)",
            pos=(-1.3, 0.9), scale=0.07, fg=(1, 1, 1, 1), align=TextNode.ALeft
        )

        # 3. Definição das Lentes
        # Perspectiva: Objetos distantes parecem menores (Eixo Z/Y real)
        self.lens_3d = PerspectiveLens()
        self.lens_3d.setFov(70)

        # Ortográfica: Projeção plana (Percepção 2D, profundidade ignorada visualmente)
        self.lens_2d = OrthographicLens()
        self.lens_2d.setFilmSize(20, 20) 

        # 4. Controles
        self.accept("space", self.alternar_modo)
        self.accept("escape", sys.exit)
        
        # Rodar uma tarefa para rotacionar o objeto e evidenciar a tridimensionalidade
        self.taskMgr.add(self.rotacionar_objeto, "RotacaoTask")

    def alternar_modo(self):
        if self.is_3d_mode:
            # Muda para "Modo 2D"
            self.cam.node().setLens(self.lens_2d)
            self.info_text.setText("Pressione [ESPAÇO] para alternar entre 2D e 3D\nModo Atual: 2D (Ortográfico)")
            self.is_3d_mode = False
        else:
            # Muda para "Modo 3D"
            self.cam.node().setLens(self.lens_3d)
            self.info_text.setText("Pressione [ESPAÇO] para alternar entre 2D e 3D\nModo Atual: 3D (Perspectiva)")
            self.is_3d_mode = True

    def rotacionar_objeto(self, task):
        # Rotaciona o cubo em dois eixos (H e P)
        self.objeto.setH(self.objeto.getH() + 1)
        self.objeto.setP(self.objeto.getP() + 0.5)
        return task.cont

visualizador = VisualizadorDimensoes()
visualizador.run()