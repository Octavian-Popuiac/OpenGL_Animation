from animation.base_scene import BaseScene
import math

class WakeUpScene(BaseScene):
    def __init__(self, scene, camera, renderer, scene_manager):
        super().__init__(scene, camera, renderer)
        self.scene_manager = scene_manager
        
        # 🌅 IDENTIFICAÇÃO DA CENA
        self.scene_name = "Cena 5 - Acordar e Reflexão"
        self.scene_duration = 60.0  # 20 segundos total
        
        # 🚶 SISTEMA DE WAYPOINTS PARA HUMANO
        self.waypoints = [
            {
                "position": [-0.860, 0.100, 0.400],  # ← POSIÇÃO CORRETA
                "rotation": math.pi,  # ← 180° (3.142 rad)
                "animation": "ACORDAR_SEQUENCE",
                "duration": 20.0,  # ← CORRIGIDO: 20 segundos
                "description": "Humano acordando com determinação",
                "movement_type": "static"
            }
        ]
        
        # 📷 SISTEMA DE CÂMERA (TEMPORÁRIO - POSIÇÃO 0,0,0)
        self.camera_keyframes = [
            {
                # 📷 CÂMERA 1: Vista inicial (0-10s)
                "position_start": [0.861, 1.139, -0.663],  # ← POSIÇÃO CORRETA
                "position_end": [0.861, 1.139, -0.663],    # ← ESTÁTICA
                "rotation": 1.629,  # 93.4° (Yaw)
                "duration": 10.0,  # 10 segundos
                "description": "Vista inicial - humano acordando",
                "movement_type": "static",
                "look_at_human": True
            },
            {
                # 📷 CÂMERA 2: Aproximação (10-20s)
                "position_start": [0.861, 1.139, -0.663],  # ← INICIA NA POSIÇÃO ATUAL
                "position_end": [0.0, 0.8, 0.0],           # ← APROXIMA DO HUMANO
                "rotation": -2.124,  # -121.7° (para olhar humano)
                "duration": 10.0,  # 10 segundos
                "description": "Aproximação - reflexão e determinação",
                "movement_type": "smooth_approach",
                "look_at_human": True
            }
        ]
        
        # 💡 SISTEMA DE ILUMINAÇÃO
        self.lighting_phases = [
            {
                "start_time": 0.0,
                "end_time": 8.0,
                "brightness": 0.4,
                "color": [0.6, 0.7, 0.9],  # Azul manhã (despertar)
                "description": "Despertar - luz suave da manhã"
            },
            {
                "start_time": 8.0,
                "end_time": 20.0,
                "brightness": 0.8,
                "color": [1.0, 0.9, 0.7],  # Dourado (determinação)
                "description": "Determinação - luz quente e inspiradora"
            }
        ]
        
        # 🎭 SISTEMA DE ANIMAÇÃO ACORDAR
        self.acordar_static_duration = 30.0 
        self.acordar_animation_duration = 10.0 
        self.acordar_animation_started = False
        self.acordar_current_frame = 0
        self.acordar_frame_time = 0.0
        self.acordar_total_frames = 0  # Será definido na inicialização
        self.acordar_frame_duration = 0.0  # Será calculado dinamicamente
        
        # 🚶 SISTEMA DE MOVIMENTO NO EIXO X
        self.movement_started = False
        self.movement_start_time = 4.0  # Inicia quando começar a animação
        self.movement_duration = 4.0    # Durante toda a animação
        self.movement_distance_z = 1.360   # Move 0.5 unidades no X negativo
        self.initial_position = [-0.860, 0.100, 0.400]  # Posição inicial
        self.final_position = [-0.960, -0.160, 1.760]   # ← NOVA: Posição final

        # 🤔 FASE DE REFLEXÃO + LOOP PARADO (após acordar)
        self.reflection_started = False
        self.reflection_start_time = 8.0  # ← CORRIGIDO: 8 segundos
        self.parado_loop_started = False
        self.parado_current_frame = 0
        self.parado_frame_time = 0.0
        self.parado_frame_duration = 0.8

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
        """Inicializa a cena de acordar"""
        print(f"\n🌅 ===== SCENE05 - WAKE UP INICIALIZANDO =====")
        
        # 🗑️ LIMPA OBJETOS DA CENA ANTERIOR
        self._cleanup_previous_scene()
        
        # 🏠 ADICIONA QUARTO (MESMO DA SCENE03)
        self._setup_bedroom()
        
        # 🚶 CONFIGURA HUMANO COM ANIMAÇÃO ACORDAR
        self._setup_human_waking_up()
        
        # 📷 CONFIGURA SISTEMA DE CÂMERA
        self._setup_camera_system()
        
        # 💡 CONFIGURA ILUMINAÇÃO
        self._setup_initial_lighting()
        
        print(f"🌅 Scene05 inicializada - Pronta para acordar e reflexão!")
    
    def get_duration(self):
        return self.scene_duration
    
    def _cleanup_previous_scene(self):
        """Remove objetos da cena anterior"""
        print("🗑️ Limpando objetos da cena anterior...")
        
        # Remove humano anterior (se existir)
        if self.scene_manager.humano:
            try:
                self.scene.remove(self.scene_manager.humano)
                print("   ✅ Humano anterior removido")
            except:
                print("   ⚠️ Humano anterior já havia sido removido")
        
        print("✅ Limpeza concluída")
    
    def _setup_bedroom(self):
        """Adiciona quarto à cena (mesmo da Scene03)"""
        if hasattr(self.scene_manager, 'quarto'):
            # Verifica se já está na cena
            try:
                self.scene.remove(self.scene_manager.quarto)
            except:
                pass  # Não estava na cena
                
            self.scene_manager.quarto.set_position([0, 0, 0])  # Reset para origem
            self.scene.add(self.scene_manager.quarto)
            print("✅ Quarto adicionado à Scene05")
        else:
            print("❌ Quarto não encontrado no scene_manager")
    
    def _setup_human_waking_up(self):
        """Configura humano com animação de acordar"""
        if hasattr(self.scene_manager, 'acordar_frames') and self.scene_manager.acordar_frames:
            # Inicia com acordar_frames[0]
            self.humano = self.scene_manager.acordar_frames[0]
            
            # Calcula duração de cada frame para animação
            self.acordar_total_frames = len(self.scene_manager.acordar_frames)
            if self.acordar_total_frames > 1:
                self.acordar_frame_duration = self.acordar_animation_duration / (self.acordar_total_frames - 1)
            else:
                self.acordar_frame_duration = self.acordar_animation_duration
            
            # Posição (mesma da Scene03)
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
            
            print(f"✅ Humano posicionado para acordar em {humano_position}")
            print(f"   📅 Estático até {self.acordar_static_duration}s")
            print(f"   🎬 Animação: {self.acordar_static_duration}s-{self.acordar_static_duration + self.acordar_animation_duration}s")
            print(f"   🔢 Total frames: {self.acordar_total_frames}")
            print(f"   ⏱️ Duração por frame: {self.acordar_frame_duration:.2f}s")
            print(f"   🤔 Reflexão: {self.reflection_start_time}s-{self.scene_duration}s")
            
        else:
            print("❌ Frames de acordar não encontrados")
        
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
        else:
            print("📷 Modo câmera livre - Sistema automático desabilitado")
    
    def _setup_initial_lighting(self):
        """Configura iluminação inicial"""
        initial_phase = self.lighting_phases[0]
        print(f"💡 Iluminação inicial: {initial_phase['description']}")
        print(f"   🔆 Brilho: {initial_phase['brightness']}")
        print(f"   🎨 Cor: {initial_phase['color']}")
    
    def update(self, delta_time):
        """Atualiza a cena de acordar"""
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
        
        # 🚶 ATUALIZA ANIMAÇÃO DE ACORDAR
        self._update_waking_animation(delta_time)
        
        # 📷 ATUALIZA SISTEMA DE CÂMERA
        self._update_camera_system(delta_time)
        
        # 💡 ATUALIZA ILUMINAÇÃO
        self._update_lighting()
        
        # ⏰ VERIFICA SE CENA TERMINOU
        if self.manual_timeline >= self.scene_duration:
            self.is_finished = True
            print("🌅 Scene05 concluída - Pronto para o próximo desafio!")
    
    def _update_waking_animation(self, delta_time):
      if not hasattr(self, 'humano') or not self.humano:
          return
      
      if self.manual_timeline < self.acordar_static_duration:
          if not hasattr(self, 'acordar_static_logged'):
              print(f"😴 Humano ainda dormindo - frame 0 até {self.acordar_static_duration}s")
              self.acordar_static_logged = True
      
      elif self.manual_timeline < self.acordar_static_duration + self.acordar_animation_duration:
          if not self.acordar_animation_started:
              self.acordar_animation_started = True
              self.acordar_frame_time = 0.0
              self.movement_started = True
              print(f"🌅 INICIANDO ANIMAÇÃO DE ACORDAR aos {self.manual_timeline:.1f}s")
              print(f"   ⏱️ Duração total: {self.acordar_animation_duration}s")
              print(f"   🔢 Frames: {self.acordar_total_frames}")
              print(f"   📊 {self.acordar_frame_duration:.2f}s por frame")
          
          # 🚶 ATUALIZA MOVIMENTO NO EIXO X
          self._update_movement_during_animation()
          
          self.acordar_frame_time += delta_time
          
          if self.acordar_frame_time >= self.acordar_frame_duration:
              self.acordar_frame_time = 0.0
              
              # Próximo frame
              old_frame = self.acordar_current_frame
              
              if self.acordar_current_frame < self.acordar_total_frames - 1:
                  self.acordar_current_frame += 1
                  print(f"🌅 Acordando: frame {old_frame} -> {self.acordar_current_frame}")
                  self._change_waking_frame(self.acordar_current_frame)
              else:
                  print(f"✅ Animação de acordar concluída (frame {self.acordar_current_frame})")
      
      else:
          if not self.reflection_started:
              self.reflection_started = True
              print(f"🤔 INICIANDO FASE DE REFLEXÃO aos {self.manual_timeline:.1f}s")
              print(f"   💭 Humano reflete sobre seus sonhos e determina o próximo passo")
              print(f"   🔄 Inicia loop de frames parado")
              
              # Inicia loop de parado
              if hasattr(self.scene_manager, 'parado_frames') and self.scene_manager.parado_frames:
                  self.parado_loop_started = True
                  self.parado_current_frame = 0
                  self.parado_frame_time = 0.0
                  print(f"   🧍 Loop parado: {len(self.scene_manager.parado_frames)} frames disponíveis")
                  self._change_to_parado_frame(0)
              else:
                  print("   ⚠️ Frames de parado não encontrados - mantém último frame de acordar")
          
          if self.parado_loop_started:
              self._update_parado_loop(delta_time)

    def _update_movement_during_animation(self):
      if not self.movement_started:
          return
      
      # Calcula progresso do movimento (0.0 a 1.0)
      time_since_movement = self.manual_timeline - self.movement_start_time
      progress = min(1.0, max(0.0, time_since_movement / self.movement_duration))
      
      # 🔧 INTERPOLAÇÃO SUAVE DE TODA A POSIÇÃO
      start_pos = self.initial_position
      end_pos = self.final_position
      
      # Aplica curva suave ao progresso
      smooth_progress = self._ease_in_out_cubic(progress)
      
      # Calcula nova posição interpolando X, Y e Z
      current_position = [
          start_pos[0] + (end_pos[0] - start_pos[0]) * smooth_progress,  # X: -0.860 → -0.960
          start_pos[1] + (end_pos[1] - start_pos[1]) * smooth_progress,  # Y: 0.100 → -0.160
          start_pos[2] + (end_pos[2] - start_pos[2]) * smooth_progress   # Z: 0.400 → 1.760
      ]
      
      # Aplica nova posição ao humano
      if hasattr(self, 'humano') and self.humano:
          self.humano.set_position(current_position)
          
          # Atualiza referência no scene_manager
          self.scene_manager.current_human_position = current_position.copy()
      
      # 📊 DEBUG do movimento
      if not hasattr(self, 'last_movement_debug'):
          self.last_movement_debug = 0
      
      current_debug_second = int(time_since_movement * 10)  # Debug a cada 0.1s
      if current_debug_second != self.last_movement_debug and current_debug_second % 10 == 0:
          print(f"🚶 MOVIMENTO: progresso={progress:.2f}")
          print(f"   📍 Posição: [{current_position[0]:.3f}, {current_position[1]:.3f}, {current_position[2]:.3f}]")
          print(f"   🎯 Final: [{end_pos[0]}, {end_pos[1]}, {end_pos[2]}]")
          self.last_movement_debug = current_debug_second
    
    def _change_waking_frame(self, new_frame_index):
      if new_frame_index >= len(self.scene_manager.acordar_frames):
          print(f"⚠️ Frame {new_frame_index} inválido - máximo é {len(self.scene_manager.acordar_frames)-1}")
          return
      
      print(f"🔄 Trocando frame acordar: {getattr(self, 'acordar_current_frame', '?')} -> {new_frame_index}")
      
      # Remove frame atual
      if hasattr(self, 'humano') and self.humano:
          try:
              self.scene.remove(self.humano)
              print(f"   ✅ Frame anterior removido")
          except:
              print(f"   ⚠️ Frame anterior já estava removido")
      
      # Adiciona novo frame
      self.humano = self.scene_manager.acordar_frames[new_frame_index]
      
      if self.movement_started:
          # Durante movimento, usa interpolação suave
          time_since_movement = self.manual_timeline - self.movement_start_time
          progress = min(1.0, max(0.0, time_since_movement / self.movement_duration))
          smooth_progress = self._ease_in_out_cubic(progress)
          
          # Interpola entre posição inicial e final
          start_pos = self.initial_position
          end_pos = self.final_position
          
          current_position = [
              start_pos[0] + (end_pos[0] - start_pos[0]) * smooth_progress,
              start_pos[1] + (end_pos[1] - start_pos[1]) * smooth_progress,
              start_pos[2] + (end_pos[2] - start_pos[2]) * smooth_progress
          ]
      else:
          # Antes do movimento, usa posição inicial
          current_position = self.initial_position.copy()
      
      humano_rotation = self.waypoints[0]["rotation"]
      
      self.humano.set_position(current_position)
      self.humano.set_rotation_y(humano_rotation)
      
      # Adiciona à scene
      self.scene.add(self.humano)
      print(f"   ✅ Novo frame {new_frame_index} adicionado em {current_position}")
      
      # Atualiza referência no scene_manager
      self.scene_manager.humano = self.humano
      self.scene_manager.current_human_position = current_position.copy()
      self.acordar_current_frame = new_frame_index
    
    def _update_camera_system(self, delta_time):
        """Atualiza sistema de câmeras"""
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
      print(f"\n🌅 STATUS SCENE05 - {self.manual_timeline:.1f}s:")
      
      # Status do humano acordando
      if self.manual_timeline < self.acordar_static_duration:
          print(f"   😴 Humano: Ainda dormindo (frame 0)")
      elif self.manual_timeline < self.acordar_static_duration + self.acordar_animation_duration:
          total_frames = len(self.scene_manager.acordar_frames) if hasattr(self.scene_manager, 'acordar_frames') else 0
          print(f"   🌅 Humano: Acordando (frame {self.acordar_current_frame}/{total_frames-1})")

      else:
          if self.parado_loop_started:
              total_parado = len(self.scene_manager.parado_frames) if hasattr(self.scene_manager, 'parado_frames') else 0
              print(f"   🤔 Humano: Reflexão - loop parado (frame {self.parado_current_frame}/{total_parado-1})")
          else:
              print(f"   🤔 Humano: Reflexão e determinação (frame final)")
      
      # Status da câmera
      if self.current_camera_keyframe < len(self.camera_keyframes):
          current_camera = self.camera_keyframes[self.current_camera_keyframe]
          time_in_keyframe = self.manual_timeline - self.camera_keyframe_start_time
          print(f"   📷 Câmera {self.current_camera_keyframe + 1}: {current_camera['description']}")
          print(f"      ⏱️ Tempo no keyframe: {time_in_keyframe:.1f}/{current_camera['duration']}s")
      
      # Status da iluminação
      for phase in self.lighting_phases:
          if phase["start_time"] <= self.manual_timeline <= phase["end_time"]:
              print(f"   💡 Iluminação: {phase['description']}")
              break
            
    def _update_parado_loop(self, delta_time):
      if not self.parado_loop_started:
          return
      
      self.parado_frame_time += delta_time
      
      if self.parado_frame_time >= self.parado_frame_duration:
          self.parado_frame_time = 0.0
          
          # Próximo frame do loop
          old_frame = self.parado_current_frame
          self.parado_current_frame += 1
          
          # Se chegou ao fim, reinicia o loop
          if self.parado_current_frame >= len(self.scene_manager.parado_frames):
              self.parado_current_frame = 0
              print(f"🔄 Loop parado reiniciado: frame {old_frame} -> {self.parado_current_frame}")
          
          print(f"🧍 Frame parado: {old_frame} -> {self.parado_current_frame}")
          self._change_to_parado_frame(self.parado_current_frame)

    def _change_to_parado_frame(self, new_frame_index):
      if not hasattr(self.scene_manager, 'parado_frames') or new_frame_index >= len(self.scene_manager.parado_frames):
          print(f"⚠️ Frame parado {new_frame_index} inválido")
          return
      
      print(f"🔄 Trocando para frame parado: {getattr(self, 'parado_current_frame', '?')} -> {new_frame_index}")
      
      # Remove frame atual
      if hasattr(self, 'humano') and self.humano:
          try:
              self.scene.remove(self.humano)
              print(f"   ✅ Frame anterior removido")
          except:
              print(f"   ⚠️ Frame anterior já estava removido")
      
      # Adiciona novo frame parado
      self.humano = self.scene_manager.parado_frames[new_frame_index]
      
      # 🚶 MANTÉM POSIÇÃO FINAL DO MOVIMENTO
      current_position = self.final_position.copy()  # ← USA POSIÇÃO FINAL
      humano_rotation = self.waypoints[0]["rotation"]
      
      self.humano.set_position(current_position)
      self.humano.set_rotation_y(humano_rotation)
      
      # Adiciona à scene
      self.scene.add(self.humano)
      print(f"   ✅ Novo frame parado {new_frame_index} adicionado em {current_position}")
      
      # Atualiza referência no scene_manager
      self.scene_manager.humano = self.humano
      self.scene_manager.current_human_position = current_position.copy()
      self.parado_current_frame = new_frame_index