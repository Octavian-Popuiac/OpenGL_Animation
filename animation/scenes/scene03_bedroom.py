from animation.base_scene import BaseScene
import math

class BedroomScene(BaseScene):
    def __init__(self, scene, camera, renderer, scene_manager):
        super().__init__(scene, camera, renderer)
        self.scene_manager = scene_manager
        
        # 🛏️ IDENTIFICAÇÃO DA CENA
        self.scene_name = "Cena 3 - Tentativa de Dormir"
        self.scene_duration = 20.0  # 30 segundos total
        
        self.waypoints = [
            {
                "position": [-0.960, -0.240, -0.780],  # ← POSIÇÃO 
                "rotation": 0.0,  # ← ROTAÇÃO
                "animation": "DORMIR_SEQUENCE",
                "duration": 30.0,  # Toda a duração da cena
                "description": "Humano tentando dormir - inquieto na cama",
                "movement_type": "static"
            }
        ]

        self.camera_keyframes = [
            {
                # 📷 CÂMERA 1: Vista geral (0-5s)
                "position_start": [-1.814, 1.394, 1.733],  # ← POSIÇÃO ATUAL
                "position_end": [-1.814, 1.394, 1.733],    # ← ESTÁTICA
                "rotation": -0.781,  # -44.8° (Yaw)
                "duration": 5.0,  # 5 segundos
                "description": "Vista geral do quarto - humano dormindo",
                "movement_type": "static",
                "look_at_human": True
            },
            {
                # 📷 CÂMERA 2: Aproximação (15-20s)
                "position_start": [-1.814, 1.394, 1.733],  # ← INICIA NA POSIÇÃO ATUAL
                "position_end": [-1.200, 0.400, -0.200],   # ← APROXIMA DO HUMANO
                "rotation": 0.328,  # 18.8° (para olhar humano)
                "duration": 15.0,  # 15 segundos
                "description": "Aproximação ao humano inquieto",
                "movement_type": "smooth_approach",
                "look_at_human": True
            }
        ]
        
        # 💡 SISTEMA DE ILUMINAÇÃO
        self.lighting_phases = [
            {
                "start_time": 0.0,
                "end_time": 10.0,
                "brightness": 0.3,
                "color": [0.2, 0.2, 0.4],  # Azul escuro (noite)
                "description": "Noite calma - início do sono"
            },
            {
                "start_time": 10.0,
                "end_time": 20.0,
                "brightness": 0.4,
                "color": [0.3, 0.2, 0.2],  # Vermelho escuro (inquietação)
                "description": "Inquietação crescente - pensamentos perturbadores"
            }
        ]
        
        # 🎭 SISTEMA DE ANIMAÇÃO DORMIR
        self.dormir_static_duration = 7.0  # 10 segundos estático no frame[0]
        self.dormir_animation_started = False
        self.dormir_current_frame = 0
        self.dormir_frame_time = 0.0
        self.dormir_frame_duration = 0.3
        self.dormir_loop_start_frame = 4  # Loop a partir do frame 4
        
        # ⏰ SISTEMA DE TIMELINE
        self.manual_timeline = 0.0
        self.is_finished = False
        
        # 🎬 SISTEMA DE CÂMERA
        self.camera_system_active = False
        self.current_camera_keyframe = 0
        self.camera_keyframe_start_time = 0.0
        
        # 🚶 SISTEMA DE WAYPOINTS
        self.current_waypoint_index = 0
        self.waypoint_start_time = 0.0
        
        # 📊 DEBUG
        self.last_debug_second = -1
    
    def initialize(self):
        """Inicializa a cena do quarto"""
        print(f"\n🛏️ ===== SCENE03 - BEDROOM INICIALIZANDO =====")
        
        # 🗑️ LIMPA OBJETOS DA CENA ANTERIOR
        self._cleanup_previous_scene()
        
        # 🏠 ADICIONA QUARTO
        self._setup_bedroom()
        
        # 🚶 CONFIGURA HUMANO COM ANIMAÇÃO DORMIR
        self._setup_human_sleeping()
        
        # 📷 CONFIGURA SISTEMA DE CÂMERA
        self._setup_camera_system()
        
        # 💡 CONFIGURA ILUMINAÇÃO
        self._setup_initial_lighting()
        
        print(f"🛏️ Scene03 inicializada - Pronta para tentativa de dormir!")
    
    def get_duration(self):
      return self.scene_duration
    
    def _cleanup_previous_scene(self):
        """Remove objetos da cena anterior"""
        print("🗑️ Limpando objetos da Scene02...")
        
        # Remove cozinha
        if hasattr(self.scene_manager, 'cozinha'):
            try:
                self.scene.remove(self.scene_manager.cozinha)
                print("   ✅ Cozinha removida")
            except:
                print("   ⚠️ Cozinha já havia sido removida")
        
        # Remove humano anterior
        if self.scene_manager.humano:
            try:
                self.scene.remove(self.scene_manager.humano)
                print("   ✅ Humano anterior removido")
            except:
                print("   ⚠️ Humano anterior já havia sido removido")
        
        # Remove mãe se existir
        if hasattr(self.scene_manager.current_scene, 'mae'):
            try:
                self.scene.remove(self.scene_manager.current_scene.mae)
                print("   ✅ Mãe removida")
            except:
                print("   ⚠️ Mãe já havia sido removida")
        
        print("✅ Limpeza da Scene02 concluída")
    
    def _setup_bedroom(self):
        """Adiciona quarto à cena"""
        if hasattr(self.scene_manager, 'quarto'):
            self.scene_manager.quarto.set_position([0, 0, 0])  # Reset para origem
            self.scene.add(self.scene_manager.quarto)
            print("✅ Quarto adicionado à Scene03")
        else:
            print("❌ Quarto não encontrado no scene_manager")
    
    def _setup_human_sleeping(self):
        """Configura humano com animação de dormir"""
        if hasattr(self.scene_manager, 'dormir_frames') and self.scene_manager.dormir_frames:
            # Inicia com dormir_frames[0]
            self.humano = self.scene_manager.dormir_frames[0]
            
            # Posição temporária
            humano_position = self.waypoints[0]["position"]
            humano_rotation = self.waypoints[0]["rotation"]
            
            self.humano.set_position(humano_position)
            self.humano.set_rotation_y(humano_rotation)
            
            # Adiciona à scene
            self.scene.add(self.humano)
            
            # Registra no scene_manager
            self.scene_manager.humano = self.humano
            self.scene_manager.current_human_position = humano_position.copy()
            self.scene_manager.current_human_rotation = humano_rotation
            self.scene_manager.human_scene_reference = self.scene
            
            print(f"✅ Humano posicionado para dormir em {humano_position}")
            print(f"   📅 Estático até {self.dormir_static_duration}s, depois anima")
            print(f"   🔄 Loop a partir do frame {self.dormir_loop_start_frame}")
            
        else:
            print("❌ Frames de dormir não encontrados")
        
        # 🎮 CONTROLES MANUAIS EM MODO LIVRE
        if self.scene_manager.free_camera_mode:
            self.scene_manager.enable_human_controls(
                self.scene, 
                humano_position, 
                humano_rotation
            )
            print("🎮 Controles manuais habilitados para humano")
    
    def _setup_camera_system(self):
        """Configura sistema de câmera"""
        if not self.scene_manager.free_camera_mode:
            self.camera_system_active = True
            self.current_camera_keyframe = 0
            self.camera_keyframe_start_time = 0.0
            
            # Posiciona câmera inicial
            first_keyframe = self.camera_keyframes[0]
            self.camera.set_position(first_keyframe["position_start"])
            
            # Olha para humano se configurado
            if first_keyframe.get("look_at_human", False) and self.scene_manager.humano:
                human_pos = self.scene_manager.get_human_look_at_position(0.3)
                self.camera.look_at(human_pos)
            
            print(f"📷 Sistema de câmera ativado")
            print(f"   🎯 Keyframes: {len(self.camera_keyframes)}")
            print(f"   📍 Posição inicial: {first_keyframe['position_start']}")
            print(f"   ⏱️ Duração total: {first_keyframe['duration']}s")
        else:
            print("📷 Modo câmera livre - Sistema automático desabilitado")
    
    def _setup_initial_lighting(self):
        """Configura iluminação inicial"""
        initial_phase = self.lighting_phases[0]
        print(f"💡 Iluminação inicial: {initial_phase['description']}")
        print(f"   🔆 Brilho: {initial_phase['brightness']}")
        print(f"   🎨 Cor: {initial_phase['color']}")
    
    def update(self, delta_time):
        """Atualiza a cena do quarto"""
        # 🔧 LIMITA DELTA_TIME
        if delta_time > 0.1:
            print(f"⚠️ DELTA_TIME ALTO: {delta_time:.3f}s - Limitando para 0.016s")
            delta_time = 0.016
        
        # ⏰ ATUALIZA TIMELINE
        self.manual_timeline += delta_time
        
        # 🔍 DEBUG A CADA 5 SEGUNDOS
        current_second = int(self.manual_timeline)
        if current_second != self.last_debug_second and current_second % 5 == 0:
            self.last_debug_second = current_second
            self._debug_scene_status()
        
        # 🚶 ATUALIZA ANIMAÇÃO DE DORMIR
        self._update_sleeping_animation(delta_time)
        
        # 📷 ATUALIZA SISTEMA DE CÂMERA
        self._update_camera_system(delta_time)
        
        # 💡 ATUALIZA ILUMINAÇÃO
        self._update_lighting()
        
        # ⏰ VERIFICA SE CENA TERMINOU
        if self.manual_timeline >= self.scene_duration:
            self.is_finished = True
            print("🛏️ Scene03 concluída!")
    
    def _update_sleeping_animation(self, delta_time):
        """Atualiza animação de dormir do humano"""
        if not hasattr(self, 'humano') or not self.humano:
            return
        
        # 🕐 FASE 1: ESTÁTICO (0-5s)
        if self.manual_timeline < self.dormir_static_duration:
            # Humano fica estático no frame 0
            if not hasattr(self, 'dormir_was_static_logged'):
                print(f"😴 Humano dormindo estático - frame 0 até {self.dormir_static_duration}s")
                self.dormir_was_static_logged = True
        
        # 🎬 FASE 2: ANIMAÇÃO (5-20s)
        else:
            if not self.dormir_animation_started:
                self.dormir_animation_started = True
                self.dormir_frame_time = 0.0
                print(f"😰 INICIANDO ANIMAÇÃO DE INQUIETAÇÃO aos {self.manual_timeline:.1f}s")
            
            # 📊 DEBUG: Estado da animação
            if not hasattr(self, 'last_dormir_debug_time'):
                self.last_dormir_debug_time = 0
            
            if int(self.manual_timeline) != self.last_dormir_debug_time and int(self.manual_timeline) % 3 == 0:
                print(f"😰 HUMANO INQUIETO: tempo={self.manual_timeline:.1f}s, frame={self.dormir_current_frame}")
                self.last_dormir_debug_time = int(self.manual_timeline)
            
            # Atualiza frame da animação
            self.dormir_frame_time += delta_time
            
            if self.dormir_frame_time >= self.dormir_frame_duration:
                self.dormir_frame_time = 0.0
                
                # Próximo frame
                old_frame = self.dormir_current_frame
                self.dormir_current_frame += 1
                
                # 🔄 SISTEMA DE LOOP: frames 4 até última
                total_frames = len(self.scene_manager.dormir_frames)
                
                if self.dormir_current_frame >= total_frames:
                    # Reinicia no frame de loop
                    self.dormir_current_frame = self.dormir_loop_start_frame
                    print(f"🔄 Loop de inquietação: frame {old_frame} -> {self.dormir_current_frame} (frames {self.dormir_loop_start_frame}-{total_frames-1})")
                
                print(f"😴 Mudando frame dormir: {old_frame} -> {self.dormir_current_frame}")
                self._change_sleeping_frame(self.dormir_current_frame)
    
    def _change_sleeping_frame(self, new_frame_index):
        """Troca frame do humano dormindo"""
        if new_frame_index >= len(self.scene_manager.dormir_frames):
            print(f"⚠️ Frame {new_frame_index} inválido - máximo é {len(self.scene_manager.dormir_frames)-1}")
            return
        
        print(f"🔄 Trocando frame dormir: {getattr(self, 'dormir_current_frame', '?')} -> {new_frame_index}")
        
        # Remove frame atual
        if hasattr(self, 'humano') and self.humano:
            try:
                self.scene.remove(self.humano)
                print(f"   ✅ Frame anterior removido")
            except:
                print(f"   ⚠️ Frame anterior já estava removido")
        
        # Adiciona novo frame
        self.humano = self.scene_manager.dormir_frames[new_frame_index]
        
        # Mantém posição e rotação
        humano_position = self.waypoints[0]["position"]
        humano_rotation = self.waypoints[0]["rotation"]
        
        self.humano.set_position(humano_position)
        self.humano.set_rotation_y(humano_rotation)
        
        # Adiciona à scene
        self.scene.add(self.humano)
        print(f"   ✅ Novo frame {new_frame_index} adicionado")
        
        # Atualiza referência no scene_manager
        self.scene_manager.humano = self.humano
        self.dormir_current_frame = new_frame_index
    
    def _update_camera_system(self, delta_time):
      if not self.camera_system_active or self.current_camera_keyframe >= len(self.camera_keyframes):
          return
      
      current_keyframe = self.camera_keyframes[self.current_camera_keyframe]
      time_in_keyframe = self.manual_timeline - self.camera_keyframe_start_time
      
      # 📊 DEBUG de mudança de câmera
      if not hasattr(self, 'camera_debug_logged'):
          self.camera_debug_logged = {}
      
      camera_key = f"camera_{self.current_camera_keyframe}"
      if camera_key not in self.camera_debug_logged:
          print(f"📷 INICIANDO CÂMERA {self.current_camera_keyframe + 1}: {current_keyframe['description']}")
          print(f"   📍 De: {current_keyframe['position_start']}")
          print(f"   🎯 Para: {current_keyframe['position_end']}")
          print(f"   ⏱️ Duração: {current_keyframe['duration']}s")
          self.camera_debug_logged[camera_key] = True
      
      # Atualiza posição da câmera
      self._update_current_camera_keyframe(time_in_keyframe)
      
      # 🔄 AVANÇA PARA PRÓXIMA CÂMERA
      if time_in_keyframe >= current_keyframe["duration"]:
          if self.current_camera_keyframe < len(self.camera_keyframes) - 1:
              self.current_camera_keyframe += 1
              self.camera_keyframe_start_time = self.manual_timeline
              print(f"📷 MUDANDO PARA CÂMERA {self.current_camera_keyframe + 1}")
          else:
              print("📷 TODAS AS CÂMERAS CONCLUÍDAS")
              self.camera_system_active = False
    
    def _update_current_camera_keyframe(self, time_in_keyframe):
        """Atualiza posição da câmera no keyframe atual"""
        current_keyframe = self.camera_keyframes[self.current_camera_keyframe]
        movement_type = current_keyframe["movement_type"]
        
        if movement_type == "smooth_approach":
            # Movimento suave de aproximação
            progress = time_in_keyframe / current_keyframe["duration"]
            progress = min(1.0, max(0.0, progress))
            
            # DEBUG do progresso
            if not hasattr(self, 'last_camera_progress'):
                self.last_camera_progress = -1
            
            progress_percent = int(progress * 100)
            if progress_percent != self.last_camera_progress and progress_percent % 10 == 0:
                print(f"📷 CÂMERA PROGRESSO: {progress_percent}% (tempo={time_in_keyframe:.2f}s)")
                self.last_camera_progress = progress_percent
            
            # Curva suave
            smooth_progress = self._ease_in_out_cubic(progress)
            
            start_pos = current_keyframe["position_start"]
            end_pos = current_keyframe["position_end"]
            
            # Interpola posição
            current_pos = [
                start_pos[0] + (end_pos[0] - start_pos[0]) * smooth_progress,
                start_pos[1] + (end_pos[1] - start_pos[1]) * smooth_progress,
                start_pos[2] + (end_pos[2] - start_pos[2]) * smooth_progress
            ]
            
            self.camera.set_position(current_pos)
            
            # Sempre olha para o humano
            if current_keyframe.get("look_at_human", False) and self.scene_manager.humano:
                human_pos = self.scene_manager.get_human_look_at_position(0.3)
                self.camera.look_at(human_pos)
        
        else:
            # Câmera estática
            self.camera.set_position(current_keyframe["position_start"])
            if current_keyframe.get("look_at_human", False) and self.scene_manager.humano:
                human_pos = self.scene_manager.get_human_look_at_position(0.3)
                self.camera.look_at(human_pos)
    
    def _ease_in_out_cubic(self, t):
        """Curva de interpolação suave (ease-in-out cubic)"""
        if t < 0.5:
            return 4 * t * t * t
        else:
            return 1 - pow(-2 * t + 2, 3) / 2
    
    def _update_lighting(self):
        """Atualiza iluminação baseada no tempo"""
        current_phase = None
        
        for phase in self.lighting_phases:
            if phase["start_time"] <= self.manual_timeline <= phase["end_time"]:
                current_phase = phase
                break
        
        if current_phase:
            # Aqui você pode aplicar a iluminação ao renderer
            # self.renderer.set_lighting(current_phase["brightness"], current_phase["color"])
            pass
    
    def _debug_scene_status(self):
        """Debug do status da cena"""
        current_waypoint = self.waypoints[self.current_waypoint_index]
        current_camera = self.camera_keyframes[self.current_camera_keyframe] if self.current_camera_keyframe < len(self.camera_keyframes) else None
        
        print(f"\n🛏️ STATUS SCENE03 - {self.manual_timeline:.1f}s:")
        
        # Status do humano dormindo
        if self.manual_timeline < self.dormir_static_duration:
            print(f"   😴 Humano: Dormindo calmo (frame 0)")
        else:
            total_frames = len(self.scene_manager.dormir_frames) if hasattr(self.scene_manager, 'dormir_frames') else 0
            print(f"   😰 Humano: Inquieto (frame {self.dormir_current_frame}/{total_frames-1})")
        
        # Status da câmera
        if current_camera:
            print(f"   📷 Câmera: {current_camera['description']}")
        
        # Status da iluminação
        for phase in self.lighting_phases:
            if phase["start_time"] <= self.manual_timeline <= phase["end_time"]:
                print(f"   💡 Iluminação: {phase['description']}")
                break