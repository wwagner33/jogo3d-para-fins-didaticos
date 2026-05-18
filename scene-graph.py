from direct.showbase.ShowBase import ShowBase

class InicializacaoPanda(ShowBase):
    def __init__(self):
        # 1. Inicializa o motor do jogo
        ShowBase.__init__(self)
        
        # 2. Exemplo prático de manipulação do Scene Graph:
        # Alterar a cor de fundo da câmara principal
        self.setBackgroundColor(0.1, 0.1, 0.2)

if __name__ == "__main__":
    app = InicializacaoPanda()
    app.run()
