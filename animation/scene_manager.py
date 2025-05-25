import os
import math
import time
from core.base import Base
from core_ext.camera import Camera
from core_ext.renderer import Renderer
from core_ext.scene import Scene
from core.obj_reader import my_obj_reader
from geometry.sala_musica import sala_musicaGeometry
from geometry.quarto import quartoGeometry
from geometry.cozinha import cozinhaGeometry
from geometry.humano import humanoGeometry
from extras.movement_rig import MovementRig


from animation.scenes.scene01_music_room import MusicRoomScene

class SceneManager(Base):
    
    def __init__(self, free_camera_mode=False, **kwargs):
        self.free_camera_mode = free_camera_mode
        self.is_moving_to_target = False
        self.movement_start_pos = [0, 0, 0]
        self.movement_target_pos = [0, 0, 0]
        self.movement_start_rot = 0.0
        self.movement_target_rot = 0.0
        self.movement_progress = 0.0
        self.movement_duration = 5.0  # 5 segundos para mover
        self.movement_callback = None  # Função chamada quando movimento acaba
        super().__init__(**kwargs)
    
    def initialize(self):
        print("🎬 VideoClip iniciado")
        print(f"📷 Modo câmera: {'Livre' if self.free_camera_mode else 'Automática'}")
        
        self.renderer = Renderer([0.1, 0.1, 0.1])
        self.scene = Scene()
        self.camera = Camera(aspect_ratio=800 / 600)

        print("🏠 Carregando objetos...")

        # 🎼 Sala musical
        self.sala_musica = sala_musicaGeometry(0.1, 0.1, 0.1, my_obj_reader("scenes/music_scene/salamusica.obj"))
        #self.scene.add(self.sala_musica)
        print("✅ Sala de música carregada")

        # 🛏️ Cena do quarto
        #self.quarto = quartoGeometry(0.1, 0.1, 0.1, my_obj_reader("scenes/bedroom_scene/quarto.obj"))
        #self.quarto.set_position([7, 0, 0])
        # self.scene.add(self.quarto)
        print("✅ Quarto carregado")

        # 🍽️ Cena da cozinha
        self.cozinha = cozinhaGeometry(0.1, my_obj_reader("scenes/kitchen_scene/cozinha.obj"))
        #self.cozinha.set_position([14, 0, 0])
        # self.scene.add(self.cozinha)
        print("✅ Cozinha carregada")

        # Carregar frames das animações
        self.andar_frames = []
        self.olhar_frames = []
        self.levantar_frames = []

        # Carrega animação de andar 
        try:
            andar_path = "scenes/human_body/andar"
            andar_files = sorted([f for f in os.listdir(andar_path) if f.endswith('.obj')])
            
            for i in range(0, len(andar_files)):
                file = andar_files[i]
                obj_data = my_obj_reader(os.path.join(andar_path, file))
                frame = humanoGeometry(obj_data, mtl_path="scenes/human_body/andar/humano_andar_1.mtl")
                self.andar_frames.append(frame)
                
            print(f"✅ Carregados {len(self.andar_frames)} frames de andar")
        except Exception as e:
            print(f"❌ Erro ao carregar frames de andar: {e}")

        # Carrega animação parada
        try:
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

        # Carrega animação de levantar
        try:
            levantar_path = "scenes/human_body/sitStand"
            levantar_files = sorted([f for f in os.listdir(levantar_path) if f.endswith('.obj')])
            
            for i in range(0, len(levantar_files)):
                file = levantar_files[i]
                obj_data = my_obj_reader(os.path.join(levantar_path, file))
                frame = humanoGeometry(obj_data, mtl_path="scenes/human_body/sitStand/humano_levantar_1.mtl")
                self.levantar_frames.append(frame)
                
            print(f"✅ Carregados {len(self.levantar_frames)} frames de levantar")
        except Exception as e:
            print(f"❌ Erro ao carregar frames de levantar: {e}")

        self.current_frame = 0
        self.frame_count = 0
        self.frame_rate = 5
        self.humano = None  # Será definido pelas cenas específicas

        # 🎮 SISTEMA DE CONTROLE MANUAL DO HUMANO
        self.manual_control_enabled = False  # Desabilitado por padrão
        self.movement_speed = 0.02  # Velocidade de movimento
        self.rotation_speed = 0.05  # Velocidade de rotação (radianos)
        self.current_human_position = [1.7, 0.09, 0.5]  # Posição padrão
        self.current_human_rotation = -(math.pi/2)  # Rotação atual (radianos)
        self.human_scene_reference = None  # Referência da scene onde o humano está
        
        
        print(f"✅ Pré-processamento concluído:")
        print(f"   🏠 Objetos: Sala música, Quarto, Cozinha")
        print(f"   🎭 Animações: {len(self.andar_frames)} andar, {len(self.olhar_frames)} olhar, {len(self.levantar_frames)} levantar")
        print(f"💡 Objetos e humano serão adicionados pelas cenas específicas")       

        # 📷 Configuração da câmera baseada no modo
        if self.free_camera_mode:
            # Modo livre: usa MovementRig como no mundo livre
            self.camera_rig = MovementRig()
            self.camera_rig.add(self.camera)
            self.camera_rig.set_position([0, 0, 0])  # Posição inicial próxima
            self.scene.add(self.camera_rig)
            
            # Configura controles
            self.camera_rig.KEY_MOVE_FORWARDS = "w"
            self.camera_rig.KEY_MOVE_BACKWARDS = "s"
            self.camera_rig.KEY_MOVE_LEFT = "a"
            self.camera_rig.KEY_MOVE_RIGHT = "d"
            self.camera_rig.KEY_LOOK_UP = "r"
            self.camera_rig.KEY_LOOK_DOWN = "f"
            self.camera_rig.KEY_MOVE_UP = "space"
            self.camera_rig.KEY_MOVE_DOWN = "left shift"
            self.camera_rig.KEY_TURN_LEFT = "q"
            self.camera_rig.KEY_TURN_RIGHT = "e"
            
            print("📷 Controles de câmera livre:")
            print("   WASD: mover, QE: rodar, RF: olhar cima/baixo")
            print("   SPACE: subir, SHIFT: descer")
        else:
            # Modo automático: câmera será controlada pelas cenas
            self.camera_rig = None
            print("📷 Modo automático - câmera será controlada pelas cenas")

        # Lista de cenas
        self.scenes = [
            MusicRoomScene(self.scene, self.camera, self.renderer, self),
            KitchenDinnerScene(self.scene, self.camera, self.renderer, self),
        ]
        
        self.current_scene_index = 0
        self.current_scene = None
        
        # Inicia primeira cena
        self.start_scene(0)
    
    def start_scene(self, index):
        """Inicia uma cena específica"""
        if 0 <= index < len(self.scenes):
            self.current_scene_index = index
            self.current_scene = self.scenes[index]
            self.current_scene.initialize()
            
            print(f"🎬 Iniciando cena {index + 1}/{len(self.scenes)}")
        else:
            print("🎭 Todas as cenas concluídas!")
            self.running = False
    
    def update(self):
        # Atualiza câmera livre se estiver no modo livre
        if self.free_camera_mode and self.camera_rig:
            self.camera_rig.update(self.input, self.delta_time)
        
        # 🚶 ATUALIZA MOVIMENTO INTERPOLADO
        self.update_movement(self.delta_time)
        
        # 🎮 CONTROLES MANUAIS APENAS EM CÂMERA LIVRE (e quando não está movendo)
        if self.free_camera_mode and not self.is_moving_to_target:
            if self.manual_control_enabled:
                self._handle_human_controls()
            else:
                # 🔄 REATIVA CONTROLES MANUAIS (tecla C quando estão desativados)
                if self.input.is_key_pressed("c"):
                    if self.humano:
                        if not self.human_scene_reference and self.current_scene:
                            self.human_scene_reference = self.current_scene.scene
                            print("🔧 Referência da scene restaurada automaticamente")
                        
                        self.manual_control_enabled = True
                        print("🎮 Controles manuais do humano REATIVADOS!")
                        self._show_controls_help()
                    else:
                        print("❌ Humano não encontrado para reativar controles")
        else:
            # 🔧 EM CÂMERA AUTOMÁTICA OU MOVENDO: Desabilita controles se estiverem ativos
            if self.manual_control_enabled and self.is_moving_to_target:
                self.manual_control_enabled = False
                print("🚶 Controles desabilitados durante movimento automático")
        
        if self.current_scene:
            self.current_scene.update(self.delta_time)
            
            # Verifica se a cena terminou
            if self.current_scene.is_finished:
                next_index = self.current_scene_index + 1
                if next_index < len(self.scenes):
                    self.start_scene(next_index)
                else:
                    print("🎭 Todas as cenas concluídas!")
                    self.running = False
        
        # Renderiza
        self.renderer.render(self.scene, self.camera)

    def enable_human_controls(self, scene_reference, initial_position=None, initial_rotation=None):
        """Ativa controles manuais do humano para uma cena específica"""
        self.manual_control_enabled = True
        self.human_scene_reference = scene_reference
        
        if initial_position:
            self.current_human_position = initial_position.copy()
        
        if initial_rotation is not None:
            self.current_human_rotation = initial_rotation
        
        print("🎮 CONTROLES DO HUMANO ATIVADOS:")
        print("   ⬆️ Seta Cima: Mover para frente (Z-)")
        print("   ⬇️ Seta Baixo: Mover para trás (Z+)")
        print("   ⬅️ Seta Esquerda: Mover para esquerda (X-)")
        print("   ➡️ Seta Direita: Mover para direita (X+)")
        print("   🔼 .: Mover para cima (Y+)")
        print("   🔽 -: Mover para baixo (Y-)")
        print("   🔄 Z: Rodar esquerda")
        print("   🔄 X: Rodar direita")
        print("   📍 ENTER: Mostrar posição atual")
        print("   🔄 BACKSPACE: Reset para posição inicial")
        print("   🔀 TAB: Desativar controle manual")
    
    def disable_human_controls(self):
        """Desativa controles manuais do humano"""
        self.manual_control_enabled = False
        self.human_scene_reference = None
        print("🤖 Controles manuais do humano DESATIVADOS")
    
    def _handle_human_controls(self):
        """Controla o humano manualmente usando as setas"""
        if not self.humano or not self.human_scene_reference:
            return
        
        moved = False
        rotated = False
        
        # 🎮 MOVIMENTO COM SETAS
        if self.input.is_key_pressed("up"):    # ⬆️ Frente (Z-)
            self.current_human_position[2] -= self.movement_speed
            moved = True
        
        if self.input.is_key_pressed("down"):  # ⬇️ Trás (Z+)
            self.current_human_position[2] += self.movement_speed
            moved = True
        
        if self.input.is_key_pressed("left"):  # ⬅️ Esquerda (X-)
            self.current_human_position[0] -= self.movement_speed
            moved = True
        
        if self.input.is_key_pressed("right"): # ➡️ Direita (X+)
            self.current_human_position[0] += self.movement_speed
            moved = True
        
        if self.input.is_key_pressed("."):   # 🔼 Cima (Y+)
            self.current_human_position[1] += self.movement_speed
            moved = True
        
        if self.input.is_key_pressed("-"): # 🔽 Baixo (Y-)
            self.current_human_position[1] -= self.movement_speed
            moved = True
        
        if self.input.is_key_pressed("z"):     # 🔄 Rodar esquerda
            self.current_human_rotation += self.rotation_speed
            rotated = True
        
        if self.input.is_key_pressed("x"):     # 🔄 Rodar direita
            self.current_human_rotation -= self.rotation_speed
            rotated = True

        # 🧹 LIMPA HUMANOS DUPLICADOS (tecla L)
        if self.input.is_key_pressed("l"):
            self.clean_duplicate_humans()
        
        # 📍 MOSTRA POSIÇÃO ATUAL (com debounce)
        if self.input.is_key_pressed("return"):  # ENTER
            current_time = time.time() if 'time' in globals() else 0
            if not hasattr(self, 'last_enter_time'):
                self.last_enter_time = 0
            
            # 🔧 DEBOUNCE: só executa se passou 1 segundo desde último ENTER
            if current_time - self.last_enter_time > 1.0:
                self.last_enter_time = current_time
                self._show_current_human_transform()

        # 🔍 DEBUG: Verificar sincronização (tecla 'i')
        if self.input.is_key_pressed("i"):
            self.debug_human_reference()
        
        # 🔄 RESET POSIÇÃO E ROTAÇÃO
        if self.input.is_key_pressed("backspace"):
            self.current_human_position = [1.700, 0.090, 0.500]  
            self.current_human_rotation = -(math.pi/2) 
            moved = True
            rotated = True
            print("🔄 Reset para posição correta: [1.700, 0.090, 0.500] e rotação: -90°")
        
        # 🔀 DESATIVA CONTROLE MANUAL
        if self.input.is_key_pressed("tab"):
            self.disable_human_controls()
            print("💡 Pressione 'C' para reativar controles manuais")
        
        # ⚡ ATUALIZA POSIÇÃO SE MOVEU
        if moved or rotated:
            self._update_human_transform()
    
    def _update_human_transform(self):
        """Atualiza a posição e rotação do humano na scene"""
        if self.humano and self.human_scene_reference:
            print(f"🔧 Atualizando transformação:")
            print(f"   📍 Nova posição: {self.current_human_position}")
            print(f"   🔄 Nova rotação: {self.current_human_rotation:.3f} rad")
            
            # 🔧 NÃO REMOVE/ADICIONA - só atualiza transformação
            self.humano.set_position(self.current_human_position)
            self.humano.set_rotation_y(self.current_human_rotation)
            
            # Verifica se foi aplicado
            actual_pos = self.humano.local_position
            print(f"   ✅ Posição após aplicação: [{actual_pos[0]:.3f}, {actual_pos[1]:.3f}, {actual_pos[2]:.3f}]")
            
            # Atualiza câmera para seguir humano (se modo automático)
            if not self.free_camera_mode:
                self.camera.look_at(self.current_human_position)
    
    def _show_current_human_transform(self):
        """Mostra posição e rotação atual detalhada do humano"""
        if self.humano:
            actual_pos = self.humano.local_position
            
            # 🔧 CORRIGIDO: Extrai rotação Y da matriz de transformação
            transform_matrix = self.humano.local_matrix
            # Para rotação Y, usamos atan2(sin, cos) da matriz de rotação
            actual_rotation_y = math.atan2(transform_matrix[2, 0], transform_matrix[2, 2])
            
            # Converte radianos para graus para melhor visualização
            rotation_degrees = self.current_human_rotation * 180.0 / math.pi
            actual_rot_degrees = actual_rotation_y * 180.0 / math.pi
            
            print("📍 TRANSFORMAÇÃO ATUAL DO HUMANO:")
            print(f"   📍 POSIÇÃO:")
            print(f"      🎯 Definida: [{self.current_human_position[0]:.3f}, {self.current_human_position[1]:.3f}, {self.current_human_position[2]:.3f}]")
            print(f"      📍 Real: [{actual_pos[0]:.3f}, {actual_pos[1]:.3f}, {actual_pos[2]:.3f}]")
            
            print(f"   🔄 ROTAÇÃO:")
            print(f"      🎯 Definida: {rotation_degrees:.1f}° ({self.current_human_rotation:.3f} rad)")
            print(f"      📍 Real: {actual_rot_degrees:.1f}° ({actual_rotation_y:.3f} rad)")
            
            # Calcula diferença de posição
            pos_diff = [actual_pos[i] - self.current_human_position[i] for i in range(3)]
            pos_distance = sum(abs(x) for x in pos_diff)
            
            # Calcula diferença de rotação
            rot_diff = actual_rotation_y - self.current_human_rotation
            
            print(f"   📏 DIFERENÇAS:")
            print(f"      Posição: [{pos_diff[0]:.3f}, {pos_diff[1]:.3f}, {pos_diff[2]:.3f}] (total: {pos_distance:.3f})")
            print(f"      Rotação: {rot_diff * 180.0 / math.pi:.1f}° ({rot_diff:.3f} rad)")
            
            # 📋 COPIA PARA CÓDIGO
            print(f"📋 Para usar no código:")
            print(f"   initial_position = [{actual_pos[0]:.3f}, {actual_pos[1]:.3f}, {actual_pos[2]:.3f}]")
            print(f"   initial_rotation = {actual_rotation_y:.3f}  # {actual_rot_degrees:.1f}°")
            
            # 🧭 ORIENTAÇÃO
            direction_names = {
                0: "Norte (frente original)",
                90: "Oeste (esquerda)",
                180: "Sul (trás)",
                270: "Leste (direita)"
            }
            
            # Normaliza ângulo para 0-360
            normalized_degrees = (rotation_degrees % 360 + 360) % 360
            closest_direction = min(direction_names.keys(), key=lambda x: abs(normalized_degrees - x))
            
            print(f"   🧭 Orientação aproximada: {direction_names[closest_direction]}")
            
            # 🔍 DEBUG: Mostra matriz de transformação para debug avançado
            print(f"   🔍 DEBUG - Matriz de transformação:")
            print(f"      Row 0: [{transform_matrix[0,0]:.3f}, {transform_matrix[0,1]:.3f}, {transform_matrix[0,2]:.3f}, {transform_matrix[0,3]:.3f}]")
            print(f"      Row 1: [{transform_matrix[1,0]:.3f}, {transform_matrix[1,1]:.3f}, {transform_matrix[1,2]:.3f}, {transform_matrix[1,3]:.3f}]")
            print(f"      Row 2: [{transform_matrix[2,0]:.3f}, {transform_matrix[2,1]:.3f}, {transform_matrix[2,2]:.3f}, {transform_matrix[2,3]:.3f}]")
            print(f"      Row 3: [{transform_matrix[3,0]:.3f}, {transform_matrix[3,1]:.3f}, {transform_matrix[3,2]:.3f}, {transform_matrix[3,3]:.3f}]")
            
        else:
            print("❌ Humano não encontrado!")
        self._show_camera_info()

    def _show_camera_info(self):
        """Mostra informações detalhadas da câmera atual"""
        import math
        
        # 📷 OBTER POSIÇÃO CORRETA DA CÂMERA
        try:
            if self.free_camera_mode and self.camera_rig:
                # Modo livre: tenta camera_rig.get_position()
                if hasattr(self.camera_rig, 'get_position'):
                    camera_pos = self.camera_rig.get_position()
                else:
                    # Fallback: extrai da matriz diretamente
                    camera_pos = [self.camera_rig._matrix[0][3], 
                                 self.camera_rig._matrix[1][3], 
                                 self.camera_rig._matrix[2][3]]
                print(f"\n📷 INFORMAÇÕES DA CÂMERA ATUAL (Modo Livre):")
            else:
                # Modo automático: câmera direta
                if hasattr(self.camera, 'get_position'):
                    camera_pos = self.camera.get_position()
                else:
                    # Fallback: extrai da matriz diretamente
                    camera_pos = [self.camera._matrix[0][3], 
                                 self.camera._matrix[1][3], 
                                 self.camera._matrix[2][3]]
                print(f"\n📷 INFORMAÇÕES DA CÂMERA ATUAL (Modo Automático):")
        except Exception as pos_error:
            # Último fallback: posição [0,0,0]
            camera_pos = [0.0, 0.0, 0.0]
            print(f"\n📷 INFORMAÇÕES DA CÂMERA ATUAL (ERRO - usando padrão):")
            print(f"   ❌ Erro ao obter posição: {pos_error}")
        
        print(f"   📍 POSIÇÃO:")
        print(f"      📍 Atual: [{camera_pos[0]:.3f}, {camera_pos[1]:.3f}, {camera_pos[2]:.3f}]")
        
        # 📷 CÁLCULO DA DIREÇÃO QUE A CÂMERA ESTÁ OLHANDO
        try:
            # Sempre usa a matriz da câmera para direção (independente do rig)
            view_matrix = self.camera.view_matrix
            
            # A direção "forward" da câmera é -Z na matriz de view
            forward_x = -view_matrix[0, 2]
            forward_y = -view_matrix[1, 2] 
            forward_z = -view_matrix[2, 2]
            
            # Calcula rotação Y (yaw) baseada na direção
            camera_yaw = math.atan2(forward_x, -forward_z)
            camera_yaw_degrees = camera_yaw * 180.0 / math.pi
            
            # Calcula rotação X (pitch) baseada na direção
            camera_pitch = math.asin(max(-1.0, min(1.0, -forward_y)))  # Clamp para evitar erros
            camera_pitch_degrees = camera_pitch * 180.0 / math.pi
            
            print(f"   🔄 ROTAÇÃO:")
            print(f"      🎯 Yaw (Y): {camera_yaw_degrees:.1f}° ({camera_yaw:.3f} rad)")
            print(f"      🎯 Pitch (X): {camera_pitch_degrees:.1f}° ({camera_pitch:.3f} rad)")
            
            print(f"   👁️ DIREÇÃO:")
            print(f"      🎯 Looking at: [{forward_x:.3f}, {forward_y:.3f}, {forward_z:.3f}]")
            
            # 📋 CÓDIGO PARA CAMERA KEYFRAMES
            print(f"\n📋 Para usar em camera_keyframes:")
            print(f'{{')
            print(f'    "position_start": [{camera_pos[0]:.3f}, {camera_pos[1]:.3f}, {camera_pos[2]:.3f}],')
            print(f'    "position_end": [{camera_pos[0]:.3f}, {camera_pos[1]:.3f}, {camera_pos[2]:.3f}],')
            print(f'    "rotation": {camera_yaw:.3f},  # {camera_yaw_degrees:.1f}° (Yaw)')
            print(f'    "duration": 5.0,')
            print(f'    "description": "Nova câmera - {self._get_camera_direction_name(camera_yaw_degrees)}",')
            print(f'    "movement_type": "static"')
            print(f'}}')
            
            # 🎯 PONTO PARA ONDE A CÂMERA ESTÁ OLHANDO (1 unidade à frente)
            look_at_point = [
                camera_pos[0] + forward_x,
                camera_pos[1] + forward_y,
                camera_pos[2] + forward_z
            ]
            
            print(f"\n🎯 PONTO DE FOCO (onde a câmera olha):")
            print(f"   📍 Look-at point: [{look_at_point[0]:.3f}, {look_at_point[1]:.3f}, {look_at_point[2]:.3f}]")
            
            # 📏 DISTÂNCIA ATÉ O HUMANO
            if self.humano:
                human_pos = self.humano.get_position() if hasattr(self.humano, 'get_position') else self.humano.local_position
                distance_to_human = math.sqrt(
                    (camera_pos[0] - human_pos[0])**2 + 
                    (camera_pos[1] - human_pos[1])**2 + 
                    (camera_pos[2] - human_pos[2])**2
                )
                print(f"   📏 Distância ao humano: {distance_to_human:.3f} unidades")
                
                # Verifica se câmera está aproximadamente olhando para o humano
                direction_to_human = [
                    human_pos[0] - camera_pos[0],
                    human_pos[1] - camera_pos[1], 
                    human_pos[2] - camera_pos[2]
                ]
                
                # Normaliza direção para o humano
                dist = math.sqrt(sum(x*x for x in direction_to_human))
                if dist > 0:
                    direction_to_human = [x/dist for x in direction_to_human]
                    
                    # Calcula similaridade (produto escalar)
                    similarity = (forward_x * direction_to_human[0] + 
                                 forward_y * direction_to_human[1] + 
                                 forward_z * direction_to_human[2])
                    
                    if similarity > 0.8:
                        print(f"   ✅ Câmera está olhando para o humano (similaridade: {similarity:.2f})")
                    else:
                        print(f"   ⚠️ Câmera NÃO está olhando para o humano (similaridade: {similarity:.2f})")
                        
                        # Sugere rotação para olhar para o humano
                        suggested_yaw = math.atan2(direction_to_human[0], -direction_to_human[2])
                        suggested_yaw_degrees = suggested_yaw * 180.0 / math.pi
                        print(f"   💡 Para olhar para humano, use rotation: {suggested_yaw:.3f} ({suggested_yaw_degrees:.1f}°)")
                        
                        # 📏 Mostra vetor direção para o humano
                        print(f"   📐 Direção para humano: [{direction_to_human[0]:.3f}, {direction_to_human[1]:.3f}, {direction_to_human[2]:.3f}]")
            
            # 🔍 DEBUG ADICIONAL - IMPLEMENTAÇÃO NOVA
            if self.free_camera_mode:
                print(f"\n🔍 DEBUG MODO LIVRE:")
                print(f"   📷 Camera_rig posição: [{camera_pos[0]:.3f}, {camera_pos[1]:.3f}, {camera_pos[2]:.3f}]")
                
                # Verifica métodos disponíveis
                print(f"   🔧 Métodos do camera_rig:")
                methods = [m for m in dir(self.camera_rig) if not m.startswith('_') and callable(getattr(self.camera_rig, m))]
                position_methods = [m for m in methods if 'position' in m.lower()]
                print(f"      📍 Métodos de posição: {position_methods}")
                
                # Testa camera interna
                try:
                    if hasattr(self.camera, 'get_position'):
                        actual_camera_pos = self.camera.get_position()
                    else:
                        actual_camera_pos = [self.camera._matrix[0][3], 
                                           self.camera._matrix[1][3], 
                                           self.camera._matrix[2][3]]
                    
                    print(f"   📹 Camera interna posição: [{actual_camera_pos[0]:.3f}, {actual_camera_pos[1]:.3f}, {actual_camera_pos[2]:.3f}]")
                    
                    # Verifica se há diferença
                    diff = [camera_pos[i] - actual_camera_pos[i] for i in range(3)]
                    total_diff = sum(abs(x) for x in diff)
                    if total_diff > 0.001:
                        print(f"   ⚠️ Diferença detectada: [{diff[0]:.3f}, {diff[1]:.3f}, {diff[2]:.3f}]")
                    else:
                        print(f"   ✅ Posições sincronizadas")
                        
                except Exception as camera_error:
                    print(f"   ❌ Erro ao acessar camera interna: {camera_error}")
                    
                # Debug da matriz do camera_rig
                try:
                    print(f"   🔍 Camera_rig matrix debug:")
                    matrix = self.camera_rig._matrix
                    print(f"      Posição na matriz: [{matrix[0][3]:.3f}, {matrix[1][3]:.3f}, {matrix[2][3]:.3f}]")
                except Exception as matrix_error:
                    print(f"   ❌ Erro na matriz: {matrix_error}")
            
        except Exception as e:
            print(f"   ❌ Erro ao calcular direção da câmera: {e}")
            print(f"   📍 Posição disponível: [{camera_pos[0]:.3f}, {camera_pos[1]:.3f}, {camera_pos[2]:.3f}]")
            
            # 🔧 DEBUG da matriz de view
            try:
                print(f"   🔍 View Matrix debug:")
                view_matrix = self.camera.view_matrix
                print(f"      Row 2: [{view_matrix[0,2]:.3f}, {view_matrix[1,2]:.3f}, {view_matrix[2,2]:.3f}]")
            except Exception as debug_e:
                print(f"   ❌ Erro na matriz: {debug_e}")

    def _get_camera_direction_name(self, yaw_degrees):
        """Converte ângulo da câmera em nome de direção"""
        # Normaliza para 0-360
        normalized = (yaw_degrees % 360 + 360) % 360
        
        if 315 <= normalized or normalized < 45:
            return "olhando Norte"
        elif 45 <= normalized < 135:
            return "olhando Leste"
        elif 135 <= normalized < 225:
            return "olhando Sul"
        elif 225 <= normalized < 315:
            return "olhando Oeste"
        else:
            return f"olhando {yaw_degrees:.1f}°"
    
    def set_human_position(self, position):
        """Define posição do humano (para uso pelas cenas)"""
        self.current_human_position = position.copy()
        if self.humano and self.human_scene_reference:
            self._update_human_transform()
    
    def set_human_rotation(self, rotation):
        """Define rotação do humano (para uso pelas cenas)"""
        self.current_human_rotation = rotation
        if self.humano and self.human_scene_reference:
            self._update_human_transform()
    
    def get_human_position(self):
        """Retorna posição atual do humano"""
        return self.current_human_position.copy()
    
    def get_human_rotation(self):
        """Retorna rotação atual do humano"""
        return self.current_human_rotation
    
    def _show_controls_help(self):
        """Mostra ajuda dos controles"""
        print("🎮 CONTROLES DO HUMANO REATIVADOS:")
        print("   ⬆️⬇️⬅️➡️ Setas: Mover X/Z")
        print("   🔼🔽 . / -: Mover Y")
        print("   🔄 Z/X: Rodar")
        print("   📍 ENTER: Ver posição")
        print("   🔄 BACKSPACE: Reset")
        print("   🔀 TAB: Desativar")
    
    def debug_human_reference(self):
        """Debug para verificar se humano está sincronizado"""
        if self.humano:
            pos = self.humano.local_position
            print(f"🔍 DEBUG Scene_Manager.humano:")
            print(f"   📍 Posição: [{pos[0]:.3f}, {pos[1]:.3f}, {pos[2]:.3f}]")
            print(f"   🔄 Controles ativos: {self.manual_control_enabled}")
            print(f"   🎮 Scene ref: {self.human_scene_reference is not None}")
        else:
            print("❌ Scene_Manager.humano = None")
    
    def clean_duplicate_humans(self):
        """Remove humanos duplicados da scene"""
        if not self.current_scene:
            return
            
        scene = self.current_scene.scene
        humans_found = []
        
        # Encontra todos os objetos que parecem ser humanos
        for obj in scene.children:
            if hasattr(obj, 'geometry') and hasattr(obj.geometry, 'vertex_list'):
                # Se tem muitos vértices, provavelmente é um humano
                if len(obj.geometry.vertex_list) > 1000:
                    humans_found.append(obj)
        
        print(f"🔍 Encontrados {len(humans_found)} objetos tipo humano na scene")
        
        # Remove todos exceto o humano oficial
        removed_count = 0
        for obj in humans_found:
            if obj != self.humano:
                try:
                    scene.remove(obj)
                    removed_count += 1
                    print(f"🗑️ Removido humano duplicado")
                except:
                    pass
        
        print(f"✅ Limpeza concluída: {removed_count} duplicados removidos")
    
    def start_movement_to(self, target_position, target_rotation=None, duration=5.0, callback=None, auto_face_while_moving=False):
        """Inicia movimento suave para uma posição alvo"""
        if not self.humano:
            print("❌ Não é possível mover - humano não encontrado")
            return False
        
        # 🚶 CONFIGURA MOVIMENTO
        self.is_moving_to_target = True
        self.movement_start_pos = self.current_human_position.copy()
        self.movement_target_pos = target_position.copy()
        self.movement_start_rot = self.current_human_rotation
        self.movement_duration = duration
        self.movement_callback = callback
        self.movement_progress = 0.0
        
        # 🧭 DECIDE ROTAÇÃO DURANTE MOVIMENTO
        if auto_face_while_moving:
            # Calcula direção do movimento para rotação durante deslocamento
            dx = target_position[0] - self.current_human_position[0]
            dz = target_position[2] - self.current_human_position[2]
            
            if abs(dx) > 0.001 or abs(dz) > 0.001:
                import math
                # Rotação para a direção do movimento
                self.movement_auto_rotation = math.atan2(dx, -dz)
                print(f"🧭 Rotação durante movimento: {self.movement_auto_rotation:.3f} rad ({self.movement_auto_rotation * 180 / math.pi:.1f}°)")
            else:
                self.movement_auto_rotation = self.current_human_rotation
                
            # Rotação final (depois do movimento)
            self.movement_target_rot = target_rotation if target_rotation is not None else self.movement_auto_rotation
            self.auto_face_while_moving = True
            
            print(f"🎯 Rotação final após movimento: {self.movement_target_rot:.3f} rad ({self.movement_target_rot * 180 / math.pi:.1f}°)")
            
        else:
            # Comportamento original (rotação direta)
            if target_rotation is not None:
                self.movement_target_rot = self.optimize_target_rotation(self.movement_auto_rotation, target_rotation)
            else:
                self.movement_target_rot = self.movement_auto_rotation
            self.auto_face_while_moving = False
        
        # 📊 CALCULA DISTÂNCIA E VELOCIDADE
        distance = self._calculate_distance(self.movement_start_pos, self.movement_target_pos)
        speed = distance / duration
        
        print(f"🚶 INICIANDO MOVIMENTO BIFÁSICO:")
        print(f"   📍 De: [{self.movement_start_pos[0]:.3f}, {self.movement_start_pos[1]:.3f}, {self.movement_start_pos[2]:.3f}]")
        print(f"   🎯 Para: [{target_position[0]:.3f}, {target_position[1]:.3f}, {target_position[2]:.3f}]")
        print(f"   📏 Distância: {distance:.3f} unidades")
        print(f"   ⏱️ Duração total: {duration:.1f}s")
        print(f"   🏃 Velocidade: {speed:.3f} unidades/s")
        
        if auto_face_while_moving:
            print(f"   🔄 Fase 1: Vira para direção e anda")
            print(f"   🔄 Fase 2: Vira para rotação final")
        
        return True
    
    def _calculate_rotation_difference(self, start_rot, end_rot):
        """Calcula a diferença de rotação pelo caminho mais curto"""
        import math
        
        # Normaliza ângulos para [-π, π]
        def normalize_angle(angle):
            while angle > math.pi:
                angle -= 2 * math.pi
            while angle < -math.pi:
                angle += 2 * math.pi
            return angle
        
        start_norm = normalize_angle(start_rot)
        end_norm = normalize_angle(end_rot)
        
        diff = end_norm - start_norm
        
        # 🔧 FORÇA CAMINHO MAIS CURTO
        if diff > math.pi:
            diff -= 2 * math.pi
        elif diff < -math.pi:
            diff += 2 * math.pi
            
        return diff
    
    def update_movement(self, delta_time):
        """Atualiza movimento interpolado bifásico"""
        if not self.is_moving_to_target:
            return
        
        # 📈 ATUALIZA PROGRESSO
        self.movement_progress += delta_time / self.movement_duration
        
        if self.movement_progress >= 1.0:
            # ✅ MOVIMENTO CONCLUÍDO
            self.movement_progress = 1.0
            self.is_moving_to_target = False
            
            # Define posição final exata
            self.current_human_position = self.movement_target_pos.copy()
            self.current_human_rotation = self.movement_target_rot
            self._update_human_transform()
            
            print("✅ Movimento bifásico concluído!")
            print(f"   📍 Posição final: [{self.current_human_position[0]:.3f}, {self.current_human_position[1]:.3f}, {self.current_human_position[2]:.3f}]")
            print(f"   🔄 Rotação final: {self.current_human_rotation:.3f} rad ({self.current_human_rotation * 180 / 3.14159:.1f}°)")
            
            # 📞 CHAMA CALLBACK SE DEFINIDO
            if self.movement_callback:
                self.movement_callback()
                self.movement_callback = None
            
        else:
            # 🔄 INTERPOLAÇÃO BIFÁSICA
            progress = self.movement_progress
            
            # 📍 POSIÇÃO (sempre linear)
            for i in range(3):
                self.current_human_position[i] = (
                    self.movement_start_pos[i] + 
                    (self.movement_target_pos[i] - self.movement_start_pos[i]) * progress
                )
            
            # 🧭 ROTAÇÃO BIFÁSICA
            if hasattr(self, 'auto_face_while_moving') and self.auto_face_while_moving:
                # FASE 1 (0-80%): Vira para direção do movimento e anda
                if progress < 0.8:
                    # Rotação para direção do movimento
                    rot_progress = progress / 0.8  # Normaliza para 0-1 na primeira fase
                    rot_diff = self._calculate_rotation_difference(self.movement_start_rot, self.movement_auto_rotation)
                    self.current_human_rotation = self.movement_start_rot + (rot_diff * rot_progress)
                
                # FASE 2 (80-100%): Anda e vira para rotação final
                else:
                    # Rotação para orientação final
                    rot_progress = (progress - 0.8) / 0.2  # Normaliza para 0-1 na segunda fase
                    rot_diff = self._calculate_rotation_difference(self.movement_auto_rotation, self.movement_target_rot)
                    self.current_human_rotation = self.movement_auto_rotation + (rot_diff * rot_progress)
            else:
                # Rotação linear tradicional
                rot_diff = self._calculate_rotation_difference(self.movement_start_rot, self.movement_target_rot)
                self.current_human_rotation = self.movement_start_rot + (rot_diff * progress)
            
            # Normaliza rotação final
            import math
            while self.current_human_rotation > math.pi:
                self.current_human_rotation -= 2 * math.pi
            while self.current_human_rotation < -math.pi:
                self.current_human_rotation += 2 * math.pi
            
            self._update_human_transform()

    def _calculate_distance(self, pos1, pos2):
        """Calcula distância euclidiana entre duas posições"""
        import math
        dx = pos2[0] - pos1[0]
        dy = pos2[1] - pos1[1]
        dz = pos2[2] - pos1[2]
        return math.sqrt(dx*dx + dy*dy + dz*dz)

    def is_currently_moving(self):
        """Verifica se está movendo atualmente"""
        return self.is_moving_to_target

    def stop_movement(self):
        """Para movimento atual"""
        if self.is_moving_to_target:
            self.is_moving_to_target = False
            print("⏹️ Movimento interrompido")

    def optimize_target_rotation(self, current_rot, target_rot):
        """Otimiza ângulo alvo para evitar voltas desnecessárias"""
        import math
        
        # Testa target_rot e target_rot ± 2π para ver qual é mais próximo
        options = [
            target_rot,
            target_rot + 2 * math.pi,
            target_rot - 2 * math.pi
        ]
        
        best_option = target_rot
        smallest_diff = abs(self._calculate_rotation_difference(current_rot, target_rot))
        
        for option in options:
            diff = abs(self._calculate_rotation_difference(current_rot, option))
            if diff < smallest_diff:
                smallest_diff = diff
                best_option = option
        
        if best_option != target_rot:
            print(f"🔧 Ângulo otimizado:")
            print(f"   ❌ Original: {target_rot:.3f} rad ({target_rot * 180 / math.pi:.1f}°)")
            print(f"   ✅ Otimizado: {best_option:.3f} rad ({best_option * 180 / math.pi:.1f}°)")
            print(f"   📏 Economia: {abs(target_rot - best_option) * 180 / math.pi:.1f}° de rotação")
        
        return best_option
    
    def get_human_look_at_position(self, height_offset=0.8):
        """Retorna posição do humano ajustada para câmeras olharem para cima"""
        human_pos = self.get_human_position()
        return [
            human_pos[0],
            human_pos[1] + height_offset,  # Adiciona altura (padrão: 0.8m)
            human_pos[2]
        ]