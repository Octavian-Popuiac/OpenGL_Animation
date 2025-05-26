import math
import time
from animation.base_scene import BaseScene

class KitchenDinnerScene(BaseScene):
    def __init__(self, scene, camera, renderer, scene_manager):
        super().__init__(scene, camera, renderer)
        self.scene_manager = scene_manager
        
        # 🍽️ CONFIGURAÇÕES DA CENA
        self.scene_name = "Cena 2 - Jantar com a Família"
        self.scene_duration = 25
        
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
                "position": [0.040, 0.300, -0.280], 
                "rotation": 0.000,
                "animation": "STATIC",  # Sem animação
                "duration": 25.0,  # Toda a duração da cena
                "description": "Posição do jantar familiar - Humano na mesa",
                "movement_type": "static"
            }
        ]
        
        self.current_waypoint_index = 0
        self.waypoint_start_time = 0
        self.in_transition = False
        
        # 📷 SISTEMA DE CÂMERAS ESPECÍFICO DA SCENE02
        self.camera_keyframes = [
            {
                "position_start": [0.803, 0.904, 1.708],  # Posição inicial que você encontrou
                "position_end": [0.037, 0.898, 0.422],    # Posição final que você encontrou
                "rotation": -0.018,  # -1.0° (Yaw final)
                "duration": 25.0,    # Toda a duração da cena (45s)
                "description": "Aproximação cinematográfica - Vista geral para close-up",
                "movement_type": "smooth_approach",
                "look_at_human": True  # Sempre olha para o humano
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
                "end_time": 8.0,
                "brightness": 1.0,
                "color": [1.0, 1.0, 1.0],  # Luz branca normal
                "description": "Iluminação normal - Ambiente familiar"
            },
            {
                "start_time": 8.0,
                "end_time": 16.0,
                "brightness": 0.8,
                "color": [0.9, 0.8, 0.7],  # Ligeiramente amarelada
                "description": "Início da tensão - Luz mais quente"
            },
            {
                "start_time": 16.0,
                "end_time": 20.0,
                "brightness": 0.6,
                "color": [0.8, 0.7, 0.6],  # Mais escura e amarelada
                "description": "Desconforto - Luz mais escura"
            },
            {
                "start_time": 20.0,
                "end_time": 25.0,
                "brightness": 0.4,
                "color": [0.7, 0.6, 0.5],  # Muito escura e sépia
                "description": "Isolamento - Luz dramática"
            }
        ]
        
        # 🔊 SISTEMA DE ÁUDIO CONCEITUAL
        self.audio_phases = [
            {
                "start_time": 0.0,
                "end_time": 8.0,
                "volume": 1.0,
                "description": "Sons normais - Talheres, conversa"
            },
            {
                "start_time": 8.0,
                "end_time": 16.0,
                "volume": 0.8,
                "description": "Sons começam a abafar"
            },
            {
                "start_time": 16.0,
                "end_time": 20.0,
                "volume": 0.5,
                "description": "Sons mais abafados - Isolamento"
            },
            {
                "start_time": 20.0,
                "end_time": 25.0,
                "volume": 0.2,
                "description": "Quase silêncio - Isolamento total"
            }
        ]
    
    def get_duration(self):
        return self.scene_duration
    
    def initialize(self):
        
        # 🏠 ADICIONA COZINHA
        self._setup_kitchen()
        
        # 🚶 CONFIGURA HUMANO (apenas levantar[0])
        self._setup_human()
        
        # 📷 CONFIGURA SISTEMA DE CÂMERAS
        self._setup_camera_system()
        
        # 🎨 CONFIGURA ILUMINAÇÃO INICIAL
        self._setup_initial_lighting()
        
        print(f"🎬 Scene02 inicializada - Pronta para jantar familiar!")

    def _cleanup_previous_scene(self):
        """Remove todos os objetos da cena anterior"""
        print("🗑️ Limpando objetos da Scene01...")
        
        # Remove sala de música se ainda estiver na cena
        if hasattr(self.scene_manager, 'sala_musica') and self.scene_manager.sala_musica:
            try:
                self.scene.remove(self.scene_manager.sala_musica)
                print("   ✅ Sala de música removida")
            except:
                print("   ⚠️ Sala de música já havia sido removida")
        
        # Remove humano se ainda estiver na cena
        if self.scene_manager.humano:
            try:
                self.scene.remove(self.scene_manager.humano)
                print("   ✅ Humano anterior removido")
            except:
                print("   ⚠️ Humano anterior já havia sido removido")
        
        # Limpa referências
        self.scene_manager.humano = None
        self.scene_manager.human_scene_reference = None
        
        print("✅ Limpeza da Scene01 concluída")

    def _setup_kitchen(self):
        """Configura ambiente da cozinha"""
        if hasattr(self.scene_manager, 'cozinha') and self.scene_manager.cozinha:
            self.cozinha = self.scene_manager.cozinha
            self.cozinha.scale(0.7)
            self.scene.add(self.cozinha)
            print("✅ Cozinha adicionada à Scene02")
        else:
            print("❌ Cozinha não encontrada no scene_manager")

    def _setup_human(self):
        """Configura o humano para a cena da cozinha - APENAS levantar[0]"""
        if hasattr(self.scene_manager, 'levantar_frames') and self.scene_manager.levantar_frames:
            # 🎯 USA APENAS O FRAME levantar[0] (conforme solicitado)
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
            self.scene_manager.human_scene_reference = self.scene
            
            # 🎮 ATIVA CONTROLES MANUAIS EM MODO LIVRE
            if self.scene_manager.free_camera_mode:
                self.scene_manager.enable_human_controls(
                    self.scene, 
                    initial_position, 
                    initial_rotation
                )
                print("🎮 Controles manuais habilitados para posicionamento")
        else:
            print("❌ Frames de animação não encontrados")
    
    def _setup_camera_system(self):
        """Configura sistema de câmera única da Scene02"""
        if not self.scene_manager.free_camera_mode:
            self.camera_system_active = True
            self.current_camera_keyframe = 0
            self.camera_keyframe_start_time = 0
            
            # Aplica posição inicial da câmera
            first_keyframe = self.camera_keyframes[0]
            self.camera.set_position(first_keyframe["position_start"])
            
            # Olha para o humano desde o início
            if first_keyframe.get("look_at_human", False) and self.scene_manager.humano:
                human_pos = self.scene_manager.get_human_look_at_position(0.3)
                self.camera.look_at(human_pos)
            
            print(f"📷 CÂMERA ÚNICA SCENE02 INICIADA")
            print(f"   🎬 {first_keyframe['description']}")
            print(f"   📍 Posição inicial: {first_keyframe['position_start']}")
            print(f"   📍 Posição final: {first_keyframe['position_end']}")
            print(f"   ⏱️ Duração total: {first_keyframe['duration']}s")
            print(f"   👁️ Sempre olhando para o humano")

            if first_keyframe.get("look_at_human", False) and self.scene_manager.humano:
              human_pos = self.scene_manager.get_human_look_at_position(0.3)
              self.camera.look_at(human_pos)

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
        if delta_time > 0.1:  # Máximo 100ms por frame
            print(f"⚠️ DELTA_TIME ALTO: {delta_time:.3f}s - Limitando para 0.016s")
            delta_time = 0.016  # ~60 FPS
        
        # ⏰ ATUALIZA TIMELINE
        self.manual_timeline += delta_time
        
        # 🔍 DEBUG A CADA 0.5 SEGUNDO (mais frequente)
        current_half_second = int(self.manual_timeline * 2)  # A cada 0.5s
        if not hasattr(self, 'last_debug_half_second'):
            self.last_debug_half_second = -1
        
        if current_half_second != self.last_debug_half_second:
            self.last_debug_half_second = current_half_second
            if current_half_second % 10 == 0:  # Debug a cada 5 segundos
                self._debug_scene_status()
        
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
        """Atualiza o waypoint atual - SEM ANIMAÇÃO (só levantar[0])"""
        current_waypoint = self.waypoints[self.current_waypoint_index]
        
        # 🎭 NÃO FAZ ANIMAÇÃO - mantém sempre levantar[0]
        # O humano já está configurado com levantar[0] e não muda
        pass

    def _animate_walking(self, time_in_waypoint):
        """Animação desabilitada - mantém levantar[0]"""
        # NÃO FAZ NADA - mantém frame fixo
        pass

    def _animate_idle(self, time_in_waypoint):
        """Animação desabilitada - mantém levantar[0]"""
        # NÃO FAZ NADA - mantém frame fixo
        pass

    def _animate_standing(self, time_in_waypoint):
        """Animação desabilitada - mantém levantar[0]"""
        # NÃO FAZ NADA - mantém frame fixo
        pass

    def _swap_human_frame(self, new_frame):
        """Troca de frame desabilitada - mantém levantar[0]"""
        # NÃO FAZ NADA - mantém frame fixo
        print("🚫 Troca de frames desabilitada na Scene02 - mantendo levantar[0]")
    
    def _update_camera_system(self, delta_time):
        if not self.camera_system_active or self.current_camera_keyframe >= len(self.camera_keyframes):
            return
        
        current_keyframe = self.camera_keyframes[self.current_camera_keyframe]
        time_in_keyframe = self.manual_timeline - self.camera_keyframe_start_time
        
        # 🔧 DEBUG: Monitora delta_time suspeito
        if delta_time > 1.0:  # Se delta_time for maior que 1 segundo
            print(f"⚠️ DELTA_TIME SUSPEITO: {delta_time:.3f}s - Limitando para 0.016s")
            delta_time = 0.016  # Limita para ~60 FPS
        
        # 🔧 DEBUG detalhado inicial
        if time_in_keyframe < 1.0:  # Primeiros segundos
            print(f"📷 DEBUG INICIAL: timeline={self.manual_timeline:.3f}s, keyframe_time={time_in_keyframe:.3f}s, delta={delta_time:.3f}s")
        
        # ⚠️ SEMPRE ATUALIZA A CÂMERA
        self._update_current_camera_keyframe(time_in_keyframe)
        
        # Só termina quando excede duração
        if time_in_keyframe >= current_keyframe["duration"]:
            print("📷 MOVIMENTO DE CÂMERA CONCLUÍDO")
            self.camera_system_active = False
    
    def _advance_to_next_camera_keyframe(self):
        if self.current_camera_keyframe < len(self.camera_keyframes) - 1:
            self.current_camera_keyframe += 1
            self.camera_keyframe_start_time = self.manual_timeline
            
            next_keyframe = self.camera_keyframes[self.current_camera_keyframe]
            print(f"📷 INICIANDO MOVIMENTO DE CÂMERA:")
            print(f"   🎬 {next_keyframe['description']}")
            print(f"   📍 De: {next_keyframe['position_start']}")
            print(f"   📍 Para: {next_keyframe['position_end']}")
            print(f"   ⏱️ Duração: {next_keyframe['duration']}s")
            
            # Define posição inicial
            self.camera.set_position(next_keyframe["position_start"])
            
            if next_keyframe.get("look_at_human", False) and self.scene_manager.humano:
                human_pos = self.scene_manager.get_human_look_at_position(0.2)
                self.camera.look_at(human_pos)
        else:
            print("📷 MOVIMENTO DE CÂMERA CONCLUÍDO")
            self.camera_system_active = False
    
    def _update_current_camera_keyframe(self, time_in_keyframe):
        current_keyframe = self.camera_keyframes[self.current_camera_keyframe]
        movement_type = current_keyframe["movement_type"]
        
        if movement_type == "smooth_approach":
            # Movimento suave de aproximação ao longo de toda a cena
            progress = time_in_keyframe / current_keyframe["duration"]
            progress = min(1.0, max(0.0, progress))  # ← Garante 0-1
            
            # 🎬 CURVA CINEMATOGRÁFICA
            smooth_progress = self._ease_in_out_cubic(progress)
            
            start_pos = current_keyframe["position_start"]
            end_pos = current_keyframe["position_end"]
            
            # Interpola posição
            current_pos = [
                start_pos[0] + (end_pos[0] - start_pos[0]) * smooth_progress,
                start_pos[1] + (end_pos[1] - start_pos[1]) * smooth_progress,
                start_pos[2] + (end_pos[2] - start_pos[2]) * smooth_progress
            ]
            
            # 🔧 FORÇA ATUALIZAÇÃO DA CÂMERA
            self.camera.set_position(current_pos)
            
            # 👁️ SEMPRE OLHA PARA O HUMANO
            if current_keyframe.get("look_at_human", False) and self.scene_manager.humano:
                human_pos = self.scene_manager.get_human_look_at_position(0.3)
                self.camera.look_at(human_pos)
            
            # 📊 DEBUG mais frequente
            progress_percent = int(progress * 20) * 5  # A cada 5%
            if not hasattr(self, 'last_progress_debug'):
                self.last_progress_debug = -1
            
            if progress_percent != self.last_progress_debug and progress_percent % 20 == 0:
                print(f"📷 PROGRESSO: {progress_percent}% | Pos: [{current_pos[0]:.2f}, {current_pos[1]:.2f}, {current_pos[2]:.2f}]")
                self.last_progress_debug = progress_percent
        
        else:
            # Câmera estática (fallback)
            self.camera.set_position(current_keyframe["position_start"])
            if current_keyframe.get("look_at_human", False) and self.scene_manager.humano:
                human_pos = self.scene_manager.get_human_look_at_position(0.3)
                self.camera.look_at(human_pos)

    def _ease_in_out_cubic(self, t):
        """Curva de animação cinematográfica suave"""
        if t < 0.5:
            return 4 * t * t * t
        else:
            return 1 - pow(-2 * t + 2, 3) / 2
    
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