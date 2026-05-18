from direct.showbase.ShowBase import ShowBase
from panda3d.core import Vec3
from direct.gui.OnscreenText import OnscreenText
import random, sys

class ArenaFugaCompleta(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.estado_jogo = "JOGANDO"
        self.timer = 0
        self.LIMITE = 20
        
        self.texto_hud = OnscreenText(text="Sobreviva: 0s", pos=(-1.2, 0.9), scale=0.07, fg=(1,1,1,1))

        # Jogador
        self.jogador = self.loader.loadModel("models/panda-model")
        self.jogador.reparentTo(self.render)
        self.jogador.setScale(0.005)
        self.cam.setPos(0, -60, 40)
        self.cam.lookAt(0, 0, 0)

        # Inimigos
        self.inimigos = []
        for i in range(3):
            inimigo = self.loader.loadModel("models/panda-model")
            inimigo.reparentTo(self.render)
            inimigo.setColor(1, 0.2, 0.2, 1)
            inimigo.setScale(0.003)
            self.inimigos.append(inimigo)
            
            # Spawn Seguro
            while True:
                pos = Vec3(random.uniform(-18, 18), random.uniform(-18, 18), 0)
                if (pos - self.jogador.getPos()).length() > 15:
                    inimigo.setPos(pos)
                    break

        # Controlos WASD
        self.keyMap = {"w":False, "s":False, "a":False, "d":False}
        for k in ["w", "s", "a", "d"]:
            self.accept(k, self.setKey, [k, True])
            self.accept(k+"-up", self.setKey, [k, False])

        self.taskMgr.add(self.game_loop, "GameLoop")

    def setKey(self, key, val): 
        self.keyMap[key] = val

    def game_loop(self, task):
        if self.estado_jogo != "JOGANDO": return task.cont
        
        dt = globalClock.getDt()
        self.timer += dt
        self.texto_hud.setText(f"Sobreviva: {int(self.timer)}s / 30s")

        # Movimentação do Jogador
        p = self.jogador.getPos()
        v = 15 * dt
        if self.keyMap["w"]: p.y += v
        if self.keyMap["s"]: p.y -= v
        if self.keyMap["a"]: p.x -= v
        if self.keyMap["d"]: p.x += v
        
        # Limites de Mundo
        p.x = max(min(p.x, self.LIMITE), -self.LIMITE)
        p.y = max(min(p.y, self.LIMITE), -self.LIMITE)
        self.jogador.setPos(p)

        if self.timer >= 30:
            self.texto_hud.setText("VITORIA! Sobreviveu com sucesso.")
            self.estado_jogo = "FIM"

        alvo_proximo = None
        dist_min = 999
        
        # IA de Inimigos
        for inimigo in self.inimigos:
            d_vec = self.jogador.getPos() - inimigo.getPos()
            dist = d_vec.length()
            
            if dist < 1.2: # Colisão/Derrota
                self.texto_hud.setText("GAME OVER! Apanhado pelo inimigo.")
                self.estado_jogo = "FIM"
            
            if dist < dist_min:
                dist_min = dist
                alvo_proximo = inimigo

            d_vec.normalize()
            inimigo.setPos(inimigo.getPos() + d_vec * 5 * dt) # Steering Pursuit
            inimigo.lookAt(self.jogador)

        if alvo_proximo: 
            self.jogador.lookAt(alvo_proximo) # Auto-Mira
            
        return task.cont

if __name__ == "__main__":
    app = ArenaFugaCompleta()
    app.run()