from direct.showbase.ShowBase import ShowBase

class InicializacaoPanda(ShowBase):
    def __init__(self):
        # 1. Inicializa o motor do jogo
        ShowBase.__init__(self)
        
        # 2. Exemplo prático de manipulação do Scene Graph:
        # Alterar a cor de fundo da câmara principal
        self.setBackgroundColor(0.5, 0.4, 0.2)
        
        #3. Carrega um modelo 3D e o adiciona à cena
        self.scene = self.loader.loadModel("models/environment")
        self.scene.reparentTo(self.render)
        self.scene.setScale(0.25, 0.25, 0.25)
        self.scene.setPos(-8, 42, 0)
        

app = InicializacaoPanda()
app.run()
