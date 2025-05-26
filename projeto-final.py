import pathlib
import sys
import pygame
import os
import math
import subprocess

# Caminho para o pacote
package_dir = str(pathlib.Path(__file__).resolve().parents[2])
if package_dir not in sys.path:
    sys.path.insert(0, package_dir)

from core.base import Base
from core_ext.camera import Camera
from core_ext.renderer import Renderer
from core_ext.scene import Scene
from core.obj_reader import my_obj_reader
from extras.movement_rig import MovementRig
from geometry.sala_musica import sala_musicaGeometry
from geometry.quarto import quartoGeometry
from geometry.cozinha import cozinhaGeometry
from geometry.humano import humanoGeometry
from core.matrix import Matrix

def menu():
    print("Escolha o modo:")
    print("1. Mundo livre")
    print("2. Ver animação")
    modo = input("Digite 1 ou 2: ").strip()
    print("Deseja fullscreen? (s/n)")
    fullscreen = input().strip().lower() == "s"
    return modo, fullscreen

class Example(Base):
    def initialize(self):
        print("🎬 VideoClip iniciado")
        self.renderer = Renderer([0.1, 0.1, 0.1])
        self.scene = Scene()
        self.camera = Camera(aspect_ratio=800 / 600)

        # 🎼 Sala musical
        self.sala_musica = sala_musicaGeometry(0.1, 0.1, 0.1, my_obj_reader("scenes/music_scene/salamusica.obj"))
        self.scene.add(self.sala_musica)

        # 🛏️ Cena do quarto
        self.quarto = quartoGeometry(0.1, 0.1, 0.1, my_obj_reader("scenes/bedroom_scene/quarto.obj"))
        self.quarto.set_position([7, 0, 0])  # mover o quarto para o lado
        self.scene.add(self.quarto)

        # 🍽️ Cena da cozinha
        self.cozinha = cozinhaGeometry(0.1, my_obj_reader("scenes/kitchen_scene/cozinha.obj"))
        self.cozinha.set_position([14, 0, 0])  # Posição para a direita do quarto
        self.scene.add(self.cozinha)

        # 👤 Personagem com animações
        self.frame_count = 0
        self.frame_rate = 5  # Velocidade da animação (menor = mais rápido)
        self.is_walking = False  # Estado: andando ou parado
        
        # 🔍 Variável para controlar debug (a cada 30 frames)
        self.debug_counter = 0

        # Carregar frames das animações
        self.andar_frames = []
        self.olhar_frames = []

        # Carrega animação de andar 
        try:
            # Obtém a lista de arquivos da pasta andar
            andar_path = "scenes/human_body/andar"
            andar_files = sorted([f for f in os.listdir(andar_path) if f.endswith('.obj')])
            
            for i in range(0, len(andar_files)):
                file = andar_files[i]
                # Primeiro lê os dados do OBJ
                obj_data = my_obj_reader(os.path.join(andar_path, file))
                # Depois converte em objeto 3D usando o construtor humanoGeometry
                frame = humanoGeometry(obj_data, mtl_path="scenes/human_body/andar/humano_andar_1.mtl")
                self.andar_frames.append(frame)
                
            print(f"✅ Carregados {len(self.andar_frames)} frames de andar")
        except Exception as e:
            print(f"❌ Erro ao carregar frames de andar: {e}")

        # Carrega animação parada
        try:
            # Obtém a lista de arquivos da pasta olhar
            olhar_path = "scenes/human_body/olhar"
            olhar_files = sorted([f for f in os.listdir(olhar_path) if f.endswith('.obj')])
            
            for i in range(0, len(olhar_files)):
                file = olhar_files[i]
                obj_data = my_obj_reader(os.path.join(olhar_path, file))
                frame = humanoGeometry(obj_data, mtl_path="scenes/human_body/olhar/humano_olhar_1.mtl")
                self.olhar_frames.append(frame)
                
            print(f"✅ Carregados {len(self.olhar_frames)} frames de olhar")
        except Exception as e:
            print(f"❌ Erro ao carregar frames de olhar: {e}")

        # Inicia com personagem parado
        if self.olhar_frames:  # Verifica se carregou frames
            self.current_frame = 0
            self.humano = self.olhar_frames[0]
            # Posiciona o personagem à frente da câmera
            self.humano.set_position([0, 0, 0])  # Ajuste conforme necessário
            self.scene.add(self.humano)
            print("✅ Personagem adicionado à cena")
        else:
            self.humano = None
            print("❌ Não foi possível carregar o personagem")

        self.human_rotation = 0

        # 📷 Câmera POV
        self.camera_rig = MovementRig()
        self.camera_rig.add(self.camera)
        self.camera_rig.set_position([0, 1.10, 1])
        self.scene.add(self.camera_rig)

        self.configure_keys()

    def configure_keys(self):
        # Movimento com WASD
        self.camera_rig.KEY_MOVE_FORWARDS = "w"
        self.camera_rig.KEY_MOVE_BACKWARDS = "s"
        self.camera_rig.KEY_MOVE_LEFT = "a"
        self.camera_rig.KEY_MOVE_RIGHT = "d"
        self.camera_rig.KEY_LOOK_UP = "r"
        self.camera_rig.KEY_LOOK_DOWN = "f"
        self.camera_rig.KEY_MOVE_UP = None
        self.camera_rig.KEY_MOVE_DOWN = None
        self.camera_rig.KEY_TURN_LEFT = "q"
        self.camera_rig.KEY_TURN_RIGHT = "e"

    def update(self):
        # Detecta se está andando com base nas teclas pressionadas
        walking = any([
            self.input.is_key_pressed(self.camera_rig.KEY_MOVE_FORWARDS),
            self.input.is_key_pressed(self.camera_rig.KEY_MOVE_BACKWARDS),
            self.input.is_key_pressed(self.camera_rig.KEY_MOVE_LEFT),
            self.input.is_key_pressed(self.camera_rig.KEY_MOVE_RIGHT)
        ])

        # 🔧 CORRIGIDO: Controle de altura do humano
        if not hasattr(self, 'human_height_offset'):
            self.human_height_offset = 0  # Altura inicial
        
        # Detecta SPACE/SHIFT para altura
        if self.input.is_key_pressed("space"):
            self.human_height_offset += 0.05  # Sobe devagar
        elif self.input.is_key_pressed("left shift"):
            self.human_height_offset -= 0.05  # Desce devagar
        
        # Limita a altura
        self.human_height_offset = max(-3, min(5, self.human_height_offset))

        # 🔧 CORRIGIDO: Ângulos das direções
        key_angle_map = {
            frozenset(['w']): 0,      # W = para frente = 0°
            frozenset(['s']): 180,    # S = para trás = 180°
            frozenset(['a']): 270,     # A = esquerda = 90° 
            frozenset(['d']): 90,    # D = direita = 270°
            frozenset(['w', 'a']): 315,    # W+A = diagonal frente-esquerda
            frozenset(['w', 'd']): 45,   # W+D = diagonal frente-direita 
            frozenset(['s', 'a']): 225,   # S+A = diagonal trás-esquerda 
            frozenset(['s', 'd']): 135,   # S+D = diagonal trás-direita 
        }

        # Detecta teclas pressionadas
        pressed = set()
        if self.input.is_key_pressed(self.camera_rig.KEY_MOVE_FORWARDS):  # "w"
            pressed.add('w')
        if self.input.is_key_pressed(self.camera_rig.KEY_MOVE_BACKWARDS):  # "s"
            pressed.add('s')
        if self.input.is_key_pressed(self.camera_rig.KEY_MOVE_LEFT):  # "a"
            pressed.add('a')
        if self.input.is_key_pressed(self.camera_rig.KEY_MOVE_RIGHT):  # "d"
            pressed.add('d')

        # Atualiza a rotação apenas se alguma combinação está no mapa
        if pressed:
            angle = key_angle_map.get(frozenset(pressed))
            if angle is not None:
                self.human_rotation = angle

        self.camera_rig.update(self.input, self.delta_time)

        if hasattr(self, 'humano') and self.humano:
            # Atualiza estado de animação
            if walking != self.is_walking:
                self.is_walking = walking
                self.current_frame = 0  # Reinicia animação ao mudar estado
            
            # Atualiza frame a cada X frames do jogo
            self.frame_count += 1
            if self.frame_count >= self.frame_rate:
                self.frame_count = 0
                
                # Remove o frame atual
                self.scene.remove(self.humano)
                
                # Escolhe a animação correta
                animation = self.andar_frames if self.is_walking else self.olhar_frames
                
                # Avança o frame da animação
                if animation:  # Se tiver frames
                    self.current_frame = (self.current_frame + 1) % len(animation)
                    self.humano = animation[self.current_frame]
                    
                    # 🔧 SIMPLIFICADO: Posicionamento mais direto
                    cam_pos = self.camera_rig.global_position
                    
                    # 🔧 SIMPLIFICADO: Usa matriz global para calcular direção
                    camera_matrix = self.camera_rig.global_matrix
                    
                    # 🔧 CORRIGIDO: Direção "para frente" (eixo Z negativo)
                    forward_x = -camera_matrix[0][2]
                    forward_z = -camera_matrix[2][2]
                    
                    # Normaliza apenas X e Z (ignora Y para não voar)
                    length = math.sqrt(forward_x**2 + forward_z**2)
                    if length > 0:
                        forward_x = forward_x / length
                        forward_z = forward_z / length
                    
                    # 🔧 POSIÇÃO: Sempre à frente da câmera
                    distance = 2.0  # Aumentei distância para ver melhor
                    human_x = cam_pos[0] + forward_x * distance
                    human_z = cam_pos[2] + forward_z * distance
                    human_y = self.human_height_offset  # Altura controlável
                    
                    self.humano.set_position([human_x, human_y, human_z])
                    
                    # 🔧 ROTAÇÃO: Baseada na direção da câmera + movimento
                    camera_angle = math.atan2(forward_x, forward_z)
                    movement_offset = math.radians(self.human_rotation)
                    final_rotation = camera_angle - movement_offset
                    
                    self.humano.set_rotation_y(final_rotation)

                    # Adiciona o novo frame à cena
                    self.scene.add(self.humano)
                    
                    # 🔧 CÂMERA ACOMPANHA ALTURA: Ajusta depois de posicionar humano
                    current_cam_y = cam_pos[1]
                    target_cam_y = human_y + 1.5  # 1.5m acima do humano
                    
                    self.camera_rig.set_position([cam_pos[0], target_cam_y, cam_pos[2]])

        # 🔍 DEBUG: Mostra posições a cada 30 frames
        self.debug_counter += 1
        if self.debug_counter >= 30:
            self.debug_counter = 0
            
            try:
                # Posição da câmera
                cam_pos = self.camera_rig.global_position
                print(f"📷 Câmera: X={cam_pos[0]:.2f}, Y={cam_pos[1]:.2f}, Z={cam_pos[2]:.2f}")
                
                # Posição do humano
                if hasattr(self, 'humano') and self.humano:
                    human_pos = None
                    if hasattr(self.humano, 'get_position'):
                        human_pos = self.humano.get_position()
                    elif hasattr(self.humano, '_matrix'):
                        human_pos = [self.humano._matrix[0][3], self.humano._matrix[1][3], self.humano._matrix[2][3]]
                    elif hasattr(self.humano, 'matrix'):
                        human_pos = [self.humano.matrix[0][3], self.humano.matrix[1][3], self.humano.matrix[2][3]]
                    else:
                        human_pos = [0, 0, 0]
                    
                    print(f"👤 Humano: X={human_pos[0]:.2f}, Y={human_pos[1]:.2f}, Z={human_pos[2]:.2f}")
                    print(f"🚶 Andando: {walking}, Frame: {getattr(self, 'current_frame', 'N/A')}")
                    print(f"🔄 Rotação humano: {self.human_rotation}°")
                    print(f"📏 Altura offset: {self.human_height_offset:.2f}m")

                    if human_pos:
                        distance = math.sqrt((cam_pos[0] - human_pos[0])**2 + (cam_pos[2] - human_pos[2])**2)
                        print(f"📏 Distância: {distance:.2f}m")
                        
                        # 🔧 ADICIONA: Verifica se humano está na frente da câmera
                        camera_matrix = self.camera_rig.global_matrix
                        forward_x = -camera_matrix[0][2]
                        forward_z = -camera_matrix[2][2]
                        
                        # Direção da câmera para o humano
                        to_human_x = human_pos[0] - cam_pos[0]
                        to_human_z = human_pos[2] - cam_pos[2]
                        
                        # Produto escalar para verificar se está na frente
                        dot_product = forward_x * to_human_x + forward_z * to_human_z
                        print(f"🎯 Humano na frente? {'SIM' if dot_product > 0 else 'NÃO'}")
                else:
                    print("👤 Humano: (não carregado)")
                    
                print("=" * 60)
                
            except Exception as e:
                print(f"🔍 Erro no debug: {e}")
        
        self.renderer.render(self.scene, self.camera)

# Inicia o programa
if __name__ == "__main__":
    escolha, fullscreen = menu()
    if escolha == "2":
        subprocess.run(
            [sys.executable, "videoclip/animation.py"],
            check=True
        )
        sys.exit(0)
    if fullscreen:
        print("Modo fullscreen")
        pygame.init()
        info = pygame.display.Info()
        screen_size = [info.current_w, info.current_h]
    else:
        print("Modo janela")
        screen_size = [800, 600]
    Example(screen_size=screen_size, fullscreen=fullscreen).run()