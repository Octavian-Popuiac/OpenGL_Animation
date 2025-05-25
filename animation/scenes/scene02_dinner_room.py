import math
import time
from animation.base_scene import BaseScene

class KitchenDinnerScene(BaseScene):
    def __init__(self, scene, camera, renderer, scene_manager):
        super().__init__(scene, camera, renderer)
        self.scene_manager = scene_manager
        
        # 🍽️ CONFIGURAÇÕES DA CENA
        self.scene_name = "Cena 2 - Jantar com a Família"
        self.scene_duration = 45.0  # 45 segundos total
        
        # ⏰ TIMELINE MANUAL PARA DEBUG
        self.manual_timeline = 0.0
        self.last_debug_second = -1
        
        # 🎭 OBJETOS DA CENA
        self.cozinha = None
        self.humano = None
        self.family_objects = []  # Mesa, cadeiras, pratos, etc.
        
        # 🚶 SISTEMA DE WAYPOINTS DO HUMANO
        self.waypoints = [
            {
                "position": [14.0, 0.090, 0.0],  # Posição inicial na cozinha
                "rotation": 0.0,  # Olhando para frente
                "animation": "STANDING",
                "duration": 3.0,
                "description": "Entrada na cozinha - Chegando para jantar",
                "movement_type": "static"
            },
            {
                "position": [14.5, 0.090, -0.5],  # Se aproxima da mesa
                "rotation": -(math.pi / 4),  # Vira para a mesa
                "animation": "WALKING",
                "duration": 2.0,
                "description": "Caminhando para a mesa",
                "movement_type": "smooth",
                "auto_face_while_moving": True
            },
            {
                "position": [14.5, 0.090, -0.5],  # Parado na mesa
                "rotation": -(math.pi / 4),
                "animation": "IDLE",
                "duration": 8.0,
                "description": "Sentado à mesa - Conversa inicial normal",
                "movement_type": "static"
            },
            {
                "position": [14.5, 0.090, -0.5],  # Mesma posição
                "rotation": -(math.pi / 2),  # Vira ligeiramente (desconforto)
                "animation": "IDLE",
                "duration": 10.0,
                "description": "Pergunta sobre o futuro - Começa tensão",
                "movement_type": "static"
            },
            {
                "position": [14.3, 0.090, -0.3],  # Recua ligeiramente
                "rotation": -(math.pi / 3),  # Vira mais (fuga)
                "animation": "IDLE",
                "duration": 12.0,
                "description": "Hesitação e desconforto - Isolamento",
                "movement_type": "smooth"
            },
            {
                "position": [14.0, 0.090, 0.0],  # Volta para posição inicial
                "rotation": math.pi,  # De costas (isolamento total)
                "animation": "IDLE",
                "duration": 10.0,
                "description": "Isolamento emocional - Final da cena",
                "movement_type": "smooth"
            }
        ]
        
        self.current_waypoint_index = 0
        self.waypoint_start_time = 0
        self.in_transition = False
        
        # 📷 SISTEMA DE CÂMERAS ESPECÍFICO DA SCENE02
        self.camera_keyframes = [
            {
                "position_start": [15.0, 1.2, 1.0],  # Vista geral inicial
                "position_end": [14.8, 1.0, 0.8],    # Se aproxima ligeiramente
                "rotation": -2.356,  # -135° (olha para a mesa)
                "duration": 5.0,
                "description": "Estabelece ambiente familiar",
                "movement_type": "smooth_zoom_in"
            },
            {
                "position_start": [14.2, 0.8, -0.2],  # Close-up da conversa
                "position_end": [14.2, 0.8, -0.2],    # Estática
                "rotation": 0.785,  # 45° (foco no humano)
                "duration": 8.0,
                "description": "Conversa normal - Close-up",
                "movement_type": "static",
                "look_at_human": True
            },
            {
                "position_start": [15.2, 1.5, -0.8],  # Vista elevada (tensão)
                "position_end": [15.2, 1.5, -0.8],    # Estática
                "rotation": -1.571,  # -90° (ângulo tenso)
                "duration": 10.0,
                "description": "Pergunta sobre futuro - Ângulo de tensão",
                "movement_type": "static",
                "look_at_human": False
            },
            {
                "position_start": [13.5, 0.5, 0.5],   # Câmera baixa (opressão)
                "position_end": [13.5, 0.5, 0.5],     # Estática
                "rotation": 0.524,  # 30° (ângulo opressivo)
                "duration": 12.0,
                "description": "Hesitação e desconforto - Câmera opressiva",
                "movement_type": "static",
                "look_at_human": True
            },
            {
                "position_start": [13.0, 0.3, -1.0],  # Muito baixa (isolamento)
                "position_end": [13.0, 0.3, -1.0],    # Estática
                "rotation": 1.047,  # 60° (isolamento total)
                "duration": 10.0,
                "description": "Isolamento emocional - Câmera de isolamento",
                "movement_type": "static",
                "look_at_human": False
            }
        ]
        
        # 📷 ESTADO ATUAL DA CÂMERA
        self.current_camera_keyframe = 0
        self.camera_keyframe_start_time = 0
        self.camera_system_active = False
        
        # 🎨 SISTEMA DE ILUMINAÇÃO DINÂMICA
        self.lighting_phases = [
            {
                "start_time": 0.0,
                "end_time": 13.0,
                "brightness": 1.0,
                "color": [1.0, 1.0, 1.0],  # Luz branca normal
                "description": "Iluminação normal - Ambiente familiar"
            },
            {
                "start_time": 13.0,
                "end_time": 25.0,
                "brightness": 0.8,
                "color": [0.9, 0.8, 0.7],  # Ligeiramente amarelada
                "description": "Início da tensão - Luz mais quente"
            },
            {
                "start_time": 25.0,
                "end_time": 35.0,
                "brightness": 0.6,
                "color": [0.8, 0.7, 0.6],  # Mais escura e amarelada
                "description": "Desconforto - Luz mais escura"
            },
            {
                "start_time": 35.0,
                "end_time": 45.0,
                "brightness": 0.4,
                "color": [0.7, 0.6, 0.5],  # Muito escura e sépia
                "description": "Isolamento - Luz dramática"
            }
        ]
        
        # 🔊 SISTEMA DE ÁUDIO CONCEITUAL
        self.audio_phases = [
            {
                "start_time": 0.0,
                "end_time": 13.0,
                "volume": 1.0,
                "description": "Sons normais - Talheres, conversa"
            },
            {
                "start_time": 13.0,
                "end_time": 25.0,
                "volume": 0.8,
                "description": "Sons começam a abafar"
            },
            {
                "start_time": 25.0,
                "end_time": 35.0,
                "volume": 0.5,
                "description": "Sons mais abafados - Isolamento"
            },
            {
                "start_time": 35.0,
                "end_time": 45.0,
                "volume": 0.2,
                "description": "Quase silêncio - Isolamento total"
            }
        ]
    
    def get_duration(self):
        """Retorna duração total da cena"""
        return self.scene_duration
    
    def initialize(self):
        """Inicializa a cena da cozinha"""
        print(f"\n🍽️ ========== {self.scene_name.upper()} ==========")
        print(f"⏱️ Duração estimada: {self.scene_duration}s")
        
        # 🏠 ADICIONA COZINHA
        if hasattr(self.scene_manager, 'cozinha') and self.scene_manager.cozinha:
            self.cozinha = self.scene_manager.cozinha
            self.scene.add(self.cozinha)
            print("✅ Cozinha adicionada à cena")
        else:
            print("❌ Cozinha não encontrada no scene_manager")
        
        # 🚶 CONFIGURA HUMANO
        self._setup_human()
        
        # 📷 CONFIGURA SISTEMA DE CÂMERAS
        self._setup_camera_system()
        
        # 🎨 CONFIGURA ILUMINAÇÃO INICIAL
        self._setup_initial_lighting()
        
        print(f"🎬 Scene02 inicializada - Pronta para jantar familiar!")
        print(f"🎯 Foco: Pressão social sobre o futuro")
        
    def _setup_human(self):
        """Configura o humano para a cena da cozinha"""
        if hasattr(self.scene_manager, 'levantar_frames') and self.scene_manager.levantar_frames:
            # Usa primeiro frame da animação de levantar
            self.humano = self.scene_manager.levantar_frames[0]
            
            # Define posição inicial
            initial_position = self.waypoints[0]["position"]
            initial_rotation = self.waypoints[0]["rotation"]
            
            self.humano.set_position(initial_position)
            self.humano.set_rotation_y(initial_rotation)
            
            # Adiciona à scene
            self.scene.add(self.humano)
            
            # Registra no scene_manager
            self.scene_manager.humano = self.humano
            self.scene_manager.current_human_position = initial_position.copy()
            self.scene_manager.current_human_rotation = initial_rotation
            
            print(f"✅ Humano configurado na cozinha:")
            print(f"   📍 Posição: {initial_position}")
            print(f"   🔄 Rotação: {initial_rotation:.3f} rad ({initial_rotation * 180 / math.pi:.1f}°)")
            
            # 🎮 ATIVA CONTROLES MANUAIS EM MODO LIVRE
            if self.scene_manager.free_camera_mode:
                self.scene_manager.enable_human_controls(
                    self.scene, 
                    initial_position, 
                    initial_rotation
                )
        else:
            print("❌ Frames de animação não encontrados")
    
    def _setup_camera_system(self):
        """Configura sistema de câmeras da Scene02"""
        if not self.scene_manager.free_camera_mode:
            self.camera_system_active = True
            self.current_camera_keyframe = 0
            self.camera_keyframe_start_time = 0
            
            # Aplica primeira câmera
            first_keyframe = self.camera_keyframes[0]
            self.camera.set_position(first_keyframe["position_start"])
            self._set_camera_rotation(first_keyframe["rotation"])
            
            print(f"📷 SISTEMA DE CÂMERAS SCENE02 INICIADO")
            print(f"   🎬 Keyframe 1/{len(self.camera_keyframes)}: {first_keyframe['description']}")
            print(f"   📍 Posição inicial: {first_keyframe['position_start']}")
            print(f"   🔄 Rotação: {first_keyframe['rotation']:.3f} rad")
        else:
            print("📷 Modo câmera livre - Sistema automático desabilitado")
    
    def _setup_initial_lighting(self):
        """Configura iluminação inicial"""
        # 🎨 A iluminação será atualizada no update() baseada na timeline
        initial_phase = self.lighting_phases[0]
        print(f"💡 Iluminação inicial: {initial_phase['description']}")
        print(f"   🔆 Brilho: {initial_phase['brightness']}")
        print(f"   🎨 Cor: {initial_phase['color']}")
    
    def update(self, delta_time):
        """Atualiza a cena da cozinha"""
        # ⏰ ATUALIZA TIMELINE
        self.manual_timeline += delta_time
        
        # 🔍 DEBUG A CADA SEGUNDO
        current_second = int(self.manual_timeline)
        if current_second != self.last_debug_second and current_second % 5 == 0:
            self.last_debug_second = current_second
            self._debug_scene_status()
        
        # 🚶 ATUALIZA WAYPOINTS DO HUMANO
        if not self.scene_manager.free_camera_mode:
            self._update_human_waypoints(delta_time)
        
        # 📷 ATUALIZA SISTEMA DE CÂMERAS
        if not self.scene_manager.free_camera_mode and self.camera_system_active:
            self._update_camera_system(delta_time)
        
        # 🎨 ATUALIZA ILUMINAÇÃO
        self._update_lighting()
        
        # 🔊 ATUALIZA ÁUDIO (conceitual)
        self._update_audio()
        
        # ✅ VERIFICA SE CENA TERMINOU
        if self.manual_timeline >= self.scene_duration:
            self.is_finished = True
            print(f"\n🍽️ ========== SCENE02 CONCLUÍDA ==========")
            print(f"⏱️ Duração total: {self.manual_timeline:.1f}s")
            print(f"🎯 Narrativa: Pressão social estabelecida")
            print(f"🎨 Efeito visual: Escurecimento progressivo")
    
    def _update_human_waypoints(self, delta_time):
        """Atualiza movimento do humano pelos waypoints"""
        if self.current_waypoint_index >= len(self.waypoints):
            return
        
        current_waypoint = self.waypoints[self.current_waypoint_index]
        time_in_waypoint = self.manual_timeline - self.waypoint_start_time
        
        if time_in_waypoint >= current_waypoint["duration"]:
            # Avança para próximo waypoint
            self._advance_to_next_waypoint()
        else:
            # Atualiza waypoint atual
            self._update_current_waypoint(time_in_waypoint)
    
    def _advance_to_next_waypoint(self):
        """Avança para o próximo waypoint"""
        if self.current_waypoint_index < len(self.waypoints) - 1:
            self.current_waypoint_index += 1
            self.waypoint_start_time = self.manual_timeline
            
            next_waypoint = self.waypoints[self.current_waypoint_index]
            
            print(f"🚶 WAYPOINT {self.current_waypoint_index + 1}/{len(self.waypoints)}:")
            print(f"   📍 {next_waypoint['description']}")
            print(f"   🎯 Posição: {next_waypoint['position']}")
            print(f"   ⏱️ Duração: {next_waypoint['duration']}s")
            
            # Inicia movimento se necessário
            if next_waypoint["movement_type"] == "smooth":
                self.scene_manager.start_movement_to(
                    next_waypoint["position"],
                    next_waypoint["rotation"],
                    duration=min(next_waypoint["duration"], 3.0),
                    auto_face_while_moving=next_waypoint.get("auto_face_while_moving", False)
                )
            elif next_waypoint["movement_type"] == "static":
                # Teleporte para posição
                self.scene_manager.set_human_position(next_waypoint["position"])
                self.scene_manager.set_human_rotation(next_waypoint["rotation"])
    
    def _update_current_waypoint(self, time_in_waypoint):
        """Atualiza o waypoint atual"""
        current_waypoint = self.waypoints[self.current_waypoint_index]
        
        # Animação baseada no tipo
        if current_waypoint["animation"] == "WALKING":
            self._animate_walking(time_in_waypoint)
        elif current_waypoint["animation"] == "IDLE":
            self._animate_idle(time_in_waypoint)
        elif current_waypoint["animation"] == "STANDING":
            self._animate_standing(time_in_waypoint)
    
    def _animate_walking(self, time_in_waypoint):
        """Animação de caminhada"""
        if hasattr(self.scene_manager, 'andar_frames') and self.scene_manager.andar_frames:
            frame_rate = 8  # 8 FPS para caminhada
            frame_index = int((time_in_waypoint * frame_rate) % len(self.scene_manager.andar_frames))
            
            new_frame = self.scene_manager.andar_frames[frame_index]
            if new_frame != self.humano:
                self._swap_human_frame(new_frame)
    
    def _animate_idle(self, time_in_waypoint):
        """Animação parada (olhando)"""
        if hasattr(self.scene_manager, 'olhar_frames') and self.scene_manager.olhar_frames:
            frame_rate = 5  # 5 FPS para movimentos sutis
            frame_index = int((time_in_waypoint * frame_rate) % len(self.scene_manager.olhar_frames))
            
            new_frame = self.scene_manager.olhar_frames[frame_index]
            if new_frame != self.humano:
                self._swap_human_frame(new_frame)
    
    def _animate_standing(self, time_in_waypoint):
        """Animação de levantar"""
        if hasattr(self.scene_manager, 'levantar_frames') and self.scene_manager.levantar_frames:
            frame_rate = 6  # 6 FPS para levantar
            frame_index = int((time_in_waypoint * frame_rate) % len(self.scene_manager.levantar_frames))
            
            new_frame = self.scene_manager.levantar_frames[frame_index]
            if new_frame != self.humano:
                self._swap_human_frame(new_frame)
    
    def _swap_human_frame(self, new_frame):
        """Troca o frame do humano mantendo posição e rotação"""
        if self.humano:
            # Salva transformação atual
            current_pos = self.scene_manager.current_human_position.copy()
            current_rot = self.scene_manager.current_human_rotation
            
            # Remove frame atual
            self.scene.remove(self.humano)
            
            # Adiciona novo frame
            self.humano = new_frame
            self.humano.set_position(current_pos)
            self.humano.set_rotation_y(current_rot)
            self.scene.add(self.humano)
            
            # Atualiza referência no scene_manager
            self.scene_manager.humano = self.humano
    
    def _update_camera_system(self, delta_time):
        """Atualiza sistema de câmeras"""
        if self.current_camera_keyframe >= len(self.camera_keyframes):
            return
        
        current_keyframe = self.camera_keyframes[self.current_camera_keyframe]
        time_in_keyframe = self.manual_timeline - self.camera_keyframe_start_time
        
        if time_in_keyframe >= current_keyframe["duration"]:
            # Avança para próxima câmera
            self._advance_to_next_camera_keyframe()
        else:
            # Atualiza câmera atual
            self._update_current_camera_keyframe(time_in_keyframe)
    
    def _advance_to_next_camera_keyframe(self):
        """Avança para o próximo keyframe de câmera"""
        if self.current_camera_keyframe < len(self.camera_keyframes) - 1:
            self.current_camera_keyframe += 1
            self.camera_keyframe_start_time = self.manual_timeline
            
            next_keyframe = self.camera_keyframes[self.current_camera_keyframe]
            
            print(f"📷 MUDANÇA DE CÂMERA:")
            print(f"   🎬 Keyframe {self.current_camera_keyframe + 1}/{len(self.camera_keyframes)}: {next_keyframe['description']}")
            print(f"   📍 Nova posição: {next_keyframe['position_start']}")
            
            # Define posição inicial do novo keyframe
            self.camera.set_position(next_keyframe["position_start"])
            
            if next_keyframe.get("look_at_human", False):
                if self.scene_manager.humano:
                    human_pos = self.scene_manager.get_human_look_at_position()
                    self.camera.look_at(human_pos)
            else:
                self._set_camera_rotation(next_keyframe["rotation"])
        else:
            print("📷 SISTEMA DE CÂMERAS SCENE02 CONCLUÍDO")
            self.camera_system_active = False
    
    def _update_current_camera_keyframe(self, time_in_keyframe):
        """Atualiza posição da câmera no keyframe atual"""
        current_keyframe = self.camera_keyframes[self.current_camera_keyframe]
        movement_type = current_keyframe["movement_type"]
        
        if movement_type == "smooth_zoom_in":
            # Movimento suave de zoom in
            progress = time_in_keyframe / current_keyframe["duration"]
            progress = min(1.0, progress)
            
            # Curva suave
            smooth_progress = progress * progress * (3 - 2 * progress)
            
            start_pos = current_keyframe["position_start"]
            end_pos = current_keyframe["position_end"]
            
            current_pos = [
                start_pos[0] + (end_pos[0] - start_pos[0]) * smooth_progress,
                start_pos[1] + (end_pos[1] - start_pos[1]) * smooth_progress,
                start_pos[2] + (end_pos[2] - start_pos[2]) * smooth_progress
            ]
            
            self.camera.set_position(current_pos)
            
            # Sempre olha para o humano durante zoom
            if self.scene_manager.humano:
                human_pos = self.scene_manager.get_human_look_at_position()
                self.camera.look_at(human_pos)
        
        elif movement_type == "static":
            # Câmera estática
            self.camera.set_position(current_keyframe["position_start"])
            
            if current_keyframe.get("look_at_human", False):
                if self.scene_manager.humano:
                    human_pos = self.scene_manager.get_human_look_at_position()
                    self.camera.look_at(human_pos)
            else:
                self._set_camera_rotation(current_keyframe["rotation"])
    
    def _set_camera_rotation(self, rotation_y):
        """Define rotação Y da câmera"""
        if hasattr(self.camera, 'set_rotation_y'):
            self.camera.set_rotation_y(rotation_y)
        else:
            # Fallback: usa matriz de rotação
            self.camera.look_at([
                math.sin(rotation_y),
                0,
                -math.cos(rotation_y)
            ])
    
    def _update_lighting(self):
        """Atualiza iluminação baseada na timeline"""
        current_phase = None
        
        # Encontra fase atual de iluminação
        for phase in self.lighting_phases:
            if phase["start_time"] <= self.manual_timeline <= phase["end_time"]:
                current_phase = phase
                break
        
        if current_phase:
            # A iluminação seria aplicada aqui no sistema de renderização
            # Por agora, apenas log conceitual
            phase_progress = (self.manual_timeline - current_phase["start_time"]) / (current_phase["end_time"] - current_phase["start_time"])
            
            # Debug a cada mudança significativa
            if hasattr(self, 'last_lighting_phase') and self.last_lighting_phase != current_phase:
                print(f"💡 MUDANÇA DE ILUMINAÇÃO: {current_phase['description']}")
                print(f"   🔆 Brilho: {current_phase['brightness']}")
                print(f"   🎨 Cor: {current_phase['color']}")
                self.last_lighting_phase = current_phase
    
    def _update_audio(self):
        """Atualiza áudio baseado na timeline"""
        current_audio = None
        
        # Encontra fase atual de áudio
        for audio in self.audio_phases:
            if audio["start_time"] <= self.manual_timeline <= audio["end_time"]:
                current_audio = audio
                break
        
        if current_audio:
            # Debug a cada mudança de áudio
            if hasattr(self, 'last_audio_phase') and self.last_audio_phase != current_audio:
                print(f"🔊 MUDANÇA DE ÁUDIO: {current_audio['description']}")
                print(f"   📢 Volume: {current_audio['volume']}")
                self.last_audio_phase = current_audio
    
    def _debug_scene_status(self):
        """Debug do status da cena"""
        current_waypoint = self.waypoints[self.current_waypoint_index] if self.current_waypoint_index < len(self.waypoints) else None
        current_camera = self.camera_keyframes[self.current_camera_keyframe] if self.current_camera_keyframe < len(self.camera_keyframes) else None
        
        print(f"\n🍽️ STATUS SCENE02 - {self.manual_timeline:.1f}s:")
        
        if current_waypoint:
            print(f"   🚶 Waypoint {self.current_waypoint_index + 1}: {current_waypoint['description']}")
        
        if current_camera:
            print(f"   📷 Câmera {self.current_camera_keyframe + 1}: {current_camera['description']}")
        
        # Status da iluminação
        for phase in self.lighting_phases:
            if phase["start_time"] <= self.manual_timeline <= phase["end_time"]:
                print(f"   💡 Iluminação: {phase['description']} (Brilho: {phase['brightness']})")
                break