from direct.showbase.ShowBase import ShowBase
from panda3d.core import Vec3, loadPrcFileData
from direct.gui.OnscreenText import OnscreenText
import random
import sys

loadPrcFileData('', 'window-title Fase 3: Arena de Fuga Completa')
loadPrcFileData('', 'win-size 800 600')

class JogoCompleto(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        
        # 1. Estado do Jogo e Constantes
        self.estado_jogo = "JOGANDO"
        self.timer_sobrevivencia = 0
        self.LIMITE = 20
        
        # 2. Interface (HUD)
        self.texto_hud = OnscreenText(text="Sobreviva: 0s", pos=(-1.2, 0.9), scale=0.07, fg=(1,1,1,1))

        # 3. Espaço e Atores Principais
        self.jogador = self.loader.loadModel("models/panda-model")
        self.jogador.reparentTo(self.render)
        self.jogador.setScale(0.005)
        
        self.cam.setPos(0, -60, 40)
        self.cam.lookAt(0, 0, 0)

        # 4. Inimigos e Spawn Seguro
        self.inimigos = []
        for i in range(3):
            inimigo = self.loader.loadModel("models/panda-model")
            inimigo.reparentTo(self.render)
            inimigo.setColor(1, 0.2, 0.2, 1) # Inimigo Vermelho
            inimigo.setScale(0.003)
            self.inimigos.append(inimigo)
            self.spawn_seguro(inimigo)

        # 5. Controles WASD
        self.keyMap = {"w":False, "s":False, "a":False, "d":False}
        for k in ["w", "s", "a", "d"]:
            self.accept(k, self.setKey, [k, True])
            self.accept(k+"-up", self.setKey, [k, False])
        self.accept("escape", sys.exit)

        # 6. Inicia o Motor do Jogo
        self.taskMgr.add(self.game_loop, "GameLoop")

    def setKey(self, key, val): 
        self.keyMap[key] = val

    def spawn_seguro(self, obj):
        while True:
            pos = Vec3(random.uniform(-18, 18), random.uniform(-18, 18), 0)
            if (pos - self.jogador.getPos()).length() > 15:
                obj.setPos(pos)
                break

    def game_loop(self, task):
        # Paralisa as atualizações se o jogo acabar
        if self.estado_jogo != "JOGANDO": 
            return task.cont
        
        dt = globalClock.getDt()
        
        # Atualização do Cronômetro
        self.timer_sobrevivencia += dt
        self.texto_hud.setText(f"Sobreviva: {int(self.timer_sobrevivencia)}s / 30s")

        # Movimentação do Jogador
        p = self.jogador.getPos()
        v = 15 * dt
        if self.keyMap["w"]: p.y += v
        if self.keyMap["s"]: p.y -= v
        if self.keyMap["a"]: p.x -= v
        if self.keyMap["d"]: p.x += v
        
        p.x = max(min(p.x, self.LIMITE), -self.LIMITE)
        p.y = max(min(p.y, self.LIMITE), -self.LIMITE)
        self.jogador.setPos(p)

        # Condição de Vitória
        if self.timer_sobrevivencia >= 30:
            self.texto_hud.setText("VITORIA! Voce sobreviveu.")
            self.estado_jogo = "FIM"

        # Lógica de Inteligência Artificial e Colisão
        alvo_proximo = None
        dist_min = 999
        
        for inimigo in self.inimigos:
            d_vec = self.jogador.getPos() - inimigo.getPos()
            dist = d_vec.length()
            
            # Condição de Derrota
            if dist < 1.2:
                self.texto_hud.setText("GAME OVER! O inimigo te pegou.")
                self.estado_jogo = "FIM"
            
            # Identificação do Inimigo Mais Próximo
            if dist < dist_min:
                dist_min = dist
                alvo_proximo = inimigo

            # Comportamento: Steering (Perseguição)
            d_vec.normalize()
            inimigo.setPos(inimigo.getPos() + d_vec * 5 * dt)
            inimigo.lookAt(self.jogador)

        # Comportamento: Auto-Mira do Jogador
        if alvo_proximo: 
            self.jogador.lookAt(alvo_proximo)
            
        return task.cont

if __name__ == "__main__":
    app = JogoCompleto()
    app.run()