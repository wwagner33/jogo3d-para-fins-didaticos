from direct.showbase.ShowBase import ShowBase
from direct.gui.DirectGui import DirectFrame, DirectButton, OnscreenText
from direct.gui.OnscreenText import TextNode
import sys

class MenuJogo(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.setBackgroundColor(0.2, 0.2, 0.3)
        
        # Contentor principal do menu
        self.menu_principal = DirectFrame(frameColor=(0, 0, 0, 0.7),
                                         frameSize=(-0.5, 0.5, -0.7, 0.7))

        # Título
        OnscreenText(text="MEU JOGO 3D", parent=self.menu_principal,
                     pos=(0, 0.5), scale=0.1, fg=(1, 1, 1, 1), align=TextNode.ACenter)

        # Botões
        self.btn_play = DirectButton(text="Jogar", scale=0.1, pos=(0, 0, 0.2),
                                    parent=self.menu_principal, command=self.iniciar_jogo)

        self.btn_tutorial = DirectButton(text="Tutorial", scale=0.1, pos=(0, 0, -0.1),
                                        parent=self.menu_principal, command=self.mostrar_tutorial)

        self.btn_sair = DirectButton(text="Sair", scale=0.1, pos=(0, 0, -0.4),
                                     parent=self.menu_principal, command=sys.exit)

    def iniciar_jogo(self):
        print("A iniciar o jogo...")
        self.menu_principal.hide() # Esconde o menu 

    def mostrar_tutorial(self):
        print("Tutorial: Utilize as teclas W, A, S, D para se mover!")

if __name__ == "__main__":
    app = MenuJogo()
    app.run()