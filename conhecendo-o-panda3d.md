# Oficina de Desenvolvimento de Jogos 3D com Panda3D e Python: conhecendo o Panda3D

_Por Wellington Sarmento_

## Introdução

O **Panda3D** ([https://www.panda3d.org/](https://www.panda3d.org/)) é um motor de jogo (*game engine*) e um *framework* de renderização 3D de código aberto (*open-source*). Diferente de ferramentas focadas puramente em interfaces visuais de arrastar-e-soltar, o Panda3D é utilizado na forma de biblioteca de funções e classes, oferecendo um controle granular sobre a renderização e a lógica do jogo diretamente através do código.

### Um pouco de história

O motor  foi desenvolvido inicialmente em 2002 pelo **Disney VR Studio** para a criação de atrações de realidade virtual em parques temáticos e para o desenvolvimento do famoso MMORPG *Toontown Online*. Pouco tempo depois, a Disney formou uma parceria com a **Carnegie Mellon University (CMU)**, abrindo o código da ferramenta para uso acadêmico e comercial. Até hoje, o Panda3D é mantido de forma colaborativa por uma comunidade global de desenvolvedores.

### Linguagens Suportadas

A arquitetura do Panda3D foi projetada para extrair o melhor de dois mundos. O núcleo da *engine* é inteiramente escrito em **C++**, garantindo processamento de alto desempenho, cálculos matemáticos ultrarrápidos e otimização de memória. No entanto, ele foi concebido com uma integração profunda e nativa para **Python**. Isso significa que você pode escrever toda a lógica do jogo, _scripts_ e interações de forma ágil e limpa em [Python](https://docs.panda3d.org/1.10/python/introduction/index), enquanto o motor em [C++](https://docs.panda3d.org/1.10/cpp/introduction/index) lida com o trabalho pesado nos bastidores de forma transparente.

### Principais Recursos e Arquitetura

A arquitetura do Panda3D diferencia-se pela sua abordagem híbrida: um núcleo escrito em C++, totalmente exposto para uma camada de _script_ em Python. O motor baseia-se fortemente no padrão de **Grafo de Cena** (*Scene Graph*). Em vez de processar listas lineares de objetos, o Panda3D organiza o espaço tridimensional em uma árvore hierárquica de nós (*nodes*), onde a raiz universal é chamada de `render`. Se um **nó pai** sofrer uma transformação (como translação, rotação ou escala) ou for ocultado, todos os seus nós "filhos" herdarão essas propriedades automaticamente.

Abaixo, detalhamos os principais componentes arquiteturais, acompanhados de exemplos práticos de implementação.

#### 1. O Grafo de Cena (Scene Graph) e Manipulação de Nós

Cada elemento no espaço 3D é um `NodePath`, que atua como um ponteiro para um nó no grafo. A manipulação estruturada permite otimizar o gerenciamento de transformações espaciais e a visibilidade dos objetos.

```python
from direct.showbase.ShowBase import ShowBase

class Game(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        
        # Carrega um modelo (gera um NodePath)
        self.carro_pai = self.loader.loadModel("models/carro")
        self.carro_pai.reparentTo(self.render) # Define como filho da raiz espacial
        self.carro_pai.setPos(0, 10, 0)
        
        # Adiciona um objeto filho (ex: uma roda)
        self.roda_filho = self.loader.loadModel("models/roda")
        self.roda_filho.reparentTo(self.carro_pai)
        self.roda_filho.setPos(1, 0, 0) 
        # Se self.carro_pai for movido, self.roda_filho moverá junto mantendo o offset

```

#### 2. Gestor de Tarefas (Task Manager) e o Game Loop

O Panda3D gerencia o ciclo principal do jogo (*Game Loop*) por meio do `taskMgr`. Em vez de forçar o desenvolvedor a lidar com o gerenciamento manual de *threads* assíncronas (o que frequentemente gera condições de corrida), o motor utiliza um sistema assíncrono cooperativo baseado em tarefas (*coroutines*) executadas a cada quadro.

```python
    def iniciar_loop(self):
        # Agenda a tarefa para rodar a cada frame
        self.taskMgr.add(self.atualizar_jogo, "TarefaAtualizar")

    def atualizar_jogo(self, task):
        dt = globalClock.getDt() # Tempo decorrido desde o último frame
        # Rotaciona o carro baseado no tempo
        self.carro_pai.setH(self.carro_pai.getH() + 30 * dt)
        return task.cont # Diz ao Task Manager para continuar executando nos próximos frames

```

#### 3. Suporte a Dispositivos de Entrada (Input Devices)

O motor captura eventos periféricos de forma reativa através de um sistema de mensageria interno (`Messenger`). Ele oferece suporte nativo e unificado para teclado, mouse e mapeamento analógico/digital para *gamepads* (controles de Xbox, PlayStation, etc.).

```python
    def configurar_controles(self):
        # Eventos discretos de teclado
        self.accept("escape", self.userExit)
        self.accept("space", self.disparar_projetil)
        
        # Captura contínua de estado (Keyboard/Gamepad)
        self.is_key_down = self.mouseWatcherNode.is_button_down
        
        # Exemplo no loop de atualização:
        # if self.is_key_down(MouseButton.one()): ...

```

Como carregar um modelo 3D (neste caso, um cubo) e movê-lo de forma fluida registando os eventos do teclado num dicionário (`keyMap`).

```python
from direct.showbase.ShowBase import ShowBase

class MovimentacaoCubo(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        # 1. Carregar o cubo nativo
        self.cubo = self.loader.loadModel("models/box")
        self.cubo.reparentTo(self.render)
        self.cubo.setPos(0, 15, 0) # Afastado no eixo Y para ser visível

        # 2. Dicionário de estado das teclas
        self.keyMap = {"left": False, "right": False, "up": False, "down": False}

        # 3. Mapeamento dos botões (pressionar e largar)
        for key, name in [("arrow_left", "left"), ("arrow_right", "right"), 
                          ("arrow_up", "up"), ("arrow_down", "down")]:
            self.accept(key, self.updateKeyMap, [name, True])
            self.accept(key + "-up", self.updateKeyMap, [name, False])

        # 4. Adicionar o Game Loop
        self.taskMgr.add(self.update, "update")

    def updateKeyMap(self, key, state):
        self.keyMap[key] = state

    def update(self, task):
        dt = globalClock.getDt() # Delta Time
        pos = self.cubo.getPos()
        velocidade = 10 * dt

        if self.keyMap["left"]:  pos.x -= velocidade
        if self.keyMap["right"]: pos.x += velocidade
        if self.keyMap["up"]:    pos.z += velocidade
        if self.keyMap["down"]:  pos.z -= velocidade

        self.cubo.setPos(pos)
        return task.cont

if __name__ == "__main__":
    app = MovimentacaoCubo()
    app.run()

```

#### 4. Gerenciamento de Áudio (Som 3D e Espacialização)

O Panda3D integra gerenciadores de áudio baseados em bibliotecas como *OpenAL* e *FMOD*. Ele suporta tanto canais de som estéreo simples (para trilhas sonoras e interfaces) quanto a espacialização de áudio 3D baseada na posição relativa entre uma fonte sonora e o nó da câmera (o ouvinte).

```python
    def configurar_audio(self):
        # Carrega um som posicional
        self.som_motor = self.loader.load3dSound("audio/motor.ogg")
        # Vincula o som a um nó no espaço para que ele se mova com o objeto
        self.som_motor.attachToNode(self.carro_pai)
        self.som_motor.setLoop(True)
        self.som_motor.play()
        
        # Define as propriedades do Listener (Ouvinte) atreladas à câmera
        self.audio3d.attachListener(self.camera)

```

#### 5. Pipeline de Assets Flexível (`.egg` vs. `.bam`)

O ecossistema possui um pipeline de conversão transparente. Durante a produção, utiliza-se o formato `.egg` (uma sintaxe em texto plano, legível por humanos e ideal para depuração de animações, juntas e materiais). Para a distribuição comercial, a ferramenta utilitária `egg2bam` compila esses arquivos no formato `.bam`, que armazena os dados binários diretamente no formato nativo lido pela GPU, otimizando o tempo de carregamento (*loading screens*).

#### 6. Integração de Física (Bullet e ODE)

Embora possua um sistema de colisão embutido leve para cálculos geométricos simples, o Panda3D integra nativamente o *Bullet Physics*, um motor de simulação profissional de corpos rígidos (*Rigid Bodies*), corpos dinâmicos, cinemáticos, restrições articulares (*constraints*) e detecção de malhas complexas (*Triangle Meshes*).

A integração com o motor de física **Bullet Physics**, permitindo que o nosso personagem não atravesse paredes, mas continue a ser controlado manualmente.

```python
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

```

#### 7. Sistemas de Partículas e Shaders Programáveis

O motor opera com um pipeline moderno de renderização. Ele suporta tanto a configuração de estados de texturização automáticos quanto pipelines customizados baseados em *shaders* escritos em GLSL (OpenGL Shading Language) ou Cg. O gerador de efeitos integrado (*Shader Generator*) habilita automaticamente recursos como sombras em tempo real, mapeamento normal (*Normal Mapping*), brilho (*Bloom*) e High Dynamic Range (HDR).

## 8. Interface Gráfica de Usuário (GUI)

A criação de um ecrã inicial interativo utilizando o `aspect2d` (o espaço 2D dedicado às interfaces do Panda3D).

```python
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

```

### Suporte a Equipamentos de Realidade Virtual (VR/AR)

O Panda3D expandiu sua arquitetura de câmeras para suportar ecossistemas de Realidade Virtual através da integração com a API **OpenXR** e implementações legadas via *OpenVR*. Como a renderização do motor é baseada no gerenciamento de múltiplas janelas de exibição (*Display Regions*), ele consegue segmentar nativamente o processamento de visualização estereoscópica, enviando matrizes de projeção distintas com correlação de paralaxe para os displays de dispositivos como Meta Quest, HTC Vive e Valve Index.

### Portabilidade e Suporte a Plataformas Mobile

Historicamente projetado para sistemas desktop (Windows, Linux e macOS), o Panda3D evoluiu para suportar compilações cross-platform:

* **Android:** Através do uso da biblioteca de empacotamento `pman` e suporte ao compilador embarcado, é possível compilar o núcleo do motor com suporte a chamadas OpenGL ES (versões para dispositivos móveis). O código Python roda sobre um ambiente embarcado Android via *Chaquopy* ou ferramentas similares de deploy de runtime.
* **Web/HTML5:** Com o advento do *WebAssembly (Wasm)* e do projeto *Emscripten*, o código do Panda3D (C++) pode ser portado e compilador diretamente para rodar em navegadores web modernos com aceleração WebGL, estendendo consideravelmente o alcance dos softwares construídos sob a plataforma.


## O Jogo Final: "Arena de Fuga"

A consolidação máxima da nossa oficina. Este código reúne as entradas de teclado contínuas, os *Limites de Mundo*, a IA de perseguição (*Steering*), a lógica do vizinho mais próximo (*Nearest Neighbor*) e as condições de vitória/derrota.

```python
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

```

## Controle de Câmera Dinâmico (Órbita e Zoom)

Por padrão, o Panda3D ativa um controle de câmera automático via mouse (*Trackball*). Para jogos, no entanto, precisamos desativar esse comportamento padrão e criar um script customizado.

Nesta etapa, criaremos uma **Câmera de Terceira Pessoa Orbital**. Utilizaremos a hierarquia do Grafo de Cena a nosso favor: criaremos um nó invisível chamado "Pivô" na mesma posição do jogador. Ao tornarmos a câmera "filha" desse pivô e rotacionarmos o pivô com o mouse, a câmera orbitará o alvo automaticamente, mantendo-se sempre voltada para ele.

```python
from direct.showbase.ShowBase import ShowBase
from panda3d.core import loadPrcFileData
import sys

# Configuração da janela
loadPrcFileData('', 'window-title Controle de Camera Orbital')
loadPrcFileData('', 'win-size 800 600')

class CameraOrbital(ShowBase):
    def __init__(self):
        # 1. Inicializa o motor
        ShowBase.__init__(self)
        self.setBackgroundColor(0.1, 0.1, 0.1)

        # 2. Desativa o controle automático do mouse padrão do Panda3D
        self.disableMouse()

        # 3. Carrega o modelo do personagem (Alvo da Câmera)
        self.jogador = self.loader.loadModel("models/panda-model")
        self.jogador.reparentTo(self.render)
        self.jogador.setScale(0.005)
        self.jogador.setPos(0, 0, 0)

        # 4. CONCEITO DO GRAFO DE CENA: Criação do Nó Pivô
        # Criamos um nó vazio anexado diretamente ao render
        self.pivo_camera = self.render.attachNewNode("PivoCamera")
        self.pivo_camera.setPos(self.jogador.getPos()) # Centralizado no jogador

        # Tornamos a Câmera nativa (self.cam) FILHA do Pivô
        self.cam.reparentTo(self.pivo_camera)
        
        # Define a posição LOCAL da câmera em relação ao seu pai (o pivô)
        # Y = -40 (afastada 40 unidades para trás), Z = 8 (subida 8 unidades)
        self.cam.setPos(0, -40, 8)
        self.cam.lookAt(self.pivo_camera) # Força a câmera a olhar para o centro do pivô

        # 5. Controles de Zoom (Leitura dos eventos de rolagem do mouse)
        self.accept("wheel_up", self.ajustar_zoom, [-2.0])
        self.accept("wheel_down", self.ajustar_zoom, [2.0])
        self.accept("escape", sys.exit)

        # 6. Adiciona a tarefa de atualização da câmera ao Game Loop
        self.taskMgr.add(self.atualizar_camera, "AtualizarCamera")

    def ajustar_zoom(self, quantidade):
        """Altera a distância da câmera movendo-a no eixo local Y do pivô"""
        nova_distancia = self.cam.getY() - quantidade
        
        # Limita o zoom (Clamping) para evitar que a câmera atravesse o modelo ou se afaste demais
        nova_distancia = max(min(nova_distancia, -10.0), -80.0)
        self.cam.setY(nova_distancia)

    def atualizar_camera(self, task):
        """Captura a posição do mouse e rotaciona o pivô a cada frame"""
        if self.mouseWatcherNode.hasMouse():
            # Captura as coordenadas do mouse na janela (variam de -1.0 a 1.0)
            mouse_x = self.mouseWatcherNode.getMouseX()
            mouse_y = self.mouseWatcherNode.getMouseY()

            # Rotaciona o Nó Pivô. Como a câmera é filha dele, ela orbita o centro automaticamente.
            # Heading (H): Rotação no eixo Z (olhar para os lados / rotação horizontal)
            # Pitch (P): Rotação no eixo X (olhar para cima e para baixo / inclinação vertical)
            self.pivo_camera.setH(-mouse_x * 180)
            self.pivo_camera.setP(mouse_y * 45)

        return task.cont

if __name__ == "__main__":
    app = CameraOrbital()
    app.run()

```

## Referências

ANGELO, Glauber Ferreira. **Tutorial para desenvolvimento de jogos eletrônicos 3D na Unity**. 2022. 91 f. Monografia (Bacharelado em Ciência da Computação) - Centro de Informática, Universidade Federal da Paraíba, João Pessoa, 2022.

MARQUES, Gabriel Cavalcanti. **Introdução ao desenvolvimento de jogos digitais utilizando o motor de jogo UDK**. 2015. 129 f. Dissertação (Mestrado em Tecnologias da Inteligência e Design Digital) - Pontifícia Universidade Católica de São Paulo, São Paulo, 2015.

PASSOS, Erick Baptista *et al*. Tutorial: Desenvolvimento de Jogos com Unity 3D. *In*: **VIII Brazilian Symposium on Games and Digital Entertainment**, Rio de Janeiro, RJ, 2009.

PONTES, Rodrigo Garcia. **Aprendendo a programar jogos em Unity: introdução ao desenvolvimento de jogos em 3D**. GameBlast, 2024.

RODRIGUES, Leandro Bezerra; DA SILVA, Júlio César. Framework para Desenvolvimento de Jogos 3D Baseado na API O3D. **Revista Eletrônica TECCEN**, Teresópolis, v. 3, n. 2, p. 1-10, out. 2010.