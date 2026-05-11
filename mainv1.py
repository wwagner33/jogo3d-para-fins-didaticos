from direct.showbase.ShowBase import ShowBase
from panda3d.core import Vec3, loadPrcFileData
import random
import sys

# Configuração da janela do jogo
loadPrcFileData('', 'window-title Oficina 3D: Arena de Fuga')
loadPrcFileData('', 'win-size 800 600')

class ArenaFuga(ShowBase):
    def __init__(self):
        # 1. Inicializa a engine
        ShowBase.__init__(self)

        # 2. Configuração da Câmera (Perspectiva 3D)
        # Afasta a câmera no eixo Y (profundidade) e sobe no eixo Z (altura)
        self.cam.setPos(0, -50, 30)
        self.cam.lookAt(0, 0, 0)

        # 3. Criação do Jogador (Level Design e Grafo de Cena)
        self.jogador = self.loader.loadModel("models/panda-model")
        self.jogador.reparentTo(self.render)
        self.jogador.setScale(0.005)
        self.jogador.setPos(0, 0, 0)
        
        # 4. Criação dos Inimigos
        self.inimigos = []
        for i in range(3):
            inimigo = self.loader.loadModel("models/panda-model")
            inimigo.reparentTo(self.render)
            # Diferenciando os inimigos com uma cor avermelhada
            inimigo.setColor(random.uniform(0.5, 1), 0, 0, 1) 
            inimigo.setScale(0.003)
            self.inimigos.append(inimigo)
            
            # Posiciona o inimigo usando o conceito de Spawn Seguro
            self.spawn_objeto_seguro(inimigo)

        # 5. Mapeamento de Controles (Entradas do Jogador - WASD)
        self.keyMap = {"w": False, "s": False, "a": False, "d": False}
        
        self.accept("w", self.setKey, ["w", True])
        self.accept("w-up", self.setKey, ["w", False])
        self.accept("s", self.setKey, ["s", True])
        self.accept("s-up", self.setKey, ["s", False])
        self.accept("a", self.setKey, ["a", True])
        self.accept("a-up", self.setKey, ["a", False])
        self.accept("d", self.setKey, ["d", True])
        self.accept("d-up", self.setKey, ["d", False])
        self.accept("escape", sys.exit) # Tecla para sair

        # 6. Inicialização do Game Loop
        self.taskMgr.add(self.game_loop, "GameLoop")

    def setKey(self, key, val):
        """Atualiza o estado da tecla pressionada"""
        self.keyMap[key] = val

    def spawn_objeto_seguro(self, obj):
        """Garante que o objeto não nasça muito perto do jogador (Distância Euclidiana)"""
        while True:
            # Sorteia uma posição X e Y aleatória dentro dos limites do mundo
            nova_posicao = Vec3(random.uniform(-18, 18), random.uniform(-18, 18), 0)
            
            # Se a distância entre a nova posição e o jogador for maior que 12, é seguro
            if (nova_posicao - self.jogador.getPos()).length() > 12:
                obj.setPos(nova_posicao)
                break

    def game_loop(self, task):
        """Método executado a cada frame. Concentra as regras contínuas do jogo."""
        # dt (delta time) garante que o movimento seja fluido em qualquer computador
        dt = globalClock.getDt() 
        
        # --- A. MOVIMENTAÇÃO DO JOGADOR ---
        pos = self.jogador.getPos()
        velocidade = 15.0 * dt
        
        if self.keyMap["w"]: pos.y += velocidade
        if self.keyMap["s"]: pos.y -= velocidade
        if self.keyMap["a"]: pos.x -= velocidade
        if self.keyMap["d"]: pos.x += velocidade

        # Limites de Mundo: Impede o jogador de sair do quadrado de -20 a 20 (Eixos X e Y)
        pos.x = max(min(pos.x, 20), -20)
        pos.y = max(min(pos.y, 20), -20)
        self.jogador.setPos(pos)

        # --- B. INTELIGÊNCIA ARTIFICIAL: STEERING E AUTO-MIRA ---
        alvo_proximo = None
        dist_minima = 9999

        for inimigo in self.inimigos:
            # 1. Lógica do Vizinho Mais Próximo (Nearest Neighbor)
            distancia_para_jogador = (inimigo.getPos() - self.jogador.getPos()).length()
            if distancia_para_jogador < dist_minima:
                dist_minima = distancia_para_jogador
                alvo_proximo = inimigo
            
            # 2. Comportamento de Perseguição (Steering Pursuit)
            # Calcula o vetor direção: Destino - Origem
            direcao = (self.jogador.getPos() - inimigo.getPos())
            direcao.normalize() # Mantém apenas a direção, tamanho do vetor vira 1
            
            # Move o inimigo na direção do jogador
            velocidade_inimigo = 3.0 * dt
            inimigo.setPos(inimigo.getPos() + direcao * velocidade_inimigo)
            
            # Orienta o inimigo para olhar para o jogador
            inimigo.lookAt(self.jogador)

        # 3. Execução da Auto-Mira para o Jogador
        if alvo_proximo:
            # O jogador sempre vai rotacionar para encarar a ameaça mais próxima
            self.jogador.lookAt(alvo_proximo)
            
        return task.cont # Mantém o Game Loop rodando

# Executa o motor do jogo
app = ArenaFuga()
app.run()