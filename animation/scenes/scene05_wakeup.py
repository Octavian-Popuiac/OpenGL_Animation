from animation.base_scene import BaseScene
import math

class WakeUpScene(BaseScene):
    def __init__(self, scene, camera, renderer, scene_manager):
        super().__init__(scene, camera, renderer)
        self.scene_manager = scene_manager
        
        # 🌅 IDENTIFICAÇÃO DA CENA
        self.scene_name = "Cena 5 - Acordar e Reflexão"
        self.scene_duration = 20.0 
        
        # 🚶 SISTEMA DE WAYPOINTS PARA HUMANO
        self.waypoints = [
            {
                "position": [-0.860, 0.100, 0.400],  # ← POSIÇÃO CORRETA
                "rotation": math.pi,  # ← 180° (3.142 rad)
                "animation": "ACORDAR_SEQUENCE",
                "duration": 10.0,  # ← CORRIGIDO: 20 segundos
                "description": "Humano acordando com determinação",
                "movement_type": "static"
            },
            {
                # 🚶 WAYPOINT 2: Posição final - em pé olhando
                "position": [-0.700, -0.3, 0.4],  # Posição final em pé
                "rotation": 0.0,  # 0° (olhando para frente)
                "animation": "OLHAR_LOOP",
                "duration": 5.0,  # 5 segundos de loop olhar
                "description": "Humano em pé refletindo",
                "movement_type": "olhar_loop"
            },
            {
                "position": [-0.720, -0.3, 2.180],  # ← NOVA POSIÇÃO FINAL
                "rotation": 0.200,  # ← 11.5° (0.200 rad)
                "animation": "ANDAR_SEQUENCE",
                "duration": 5.0,  # ← 20 segundos de caminhada
                "description": "Humano caminhando para o destino",
                "movement_type": "andar_movimento"
            }
            
        ]
        
        self.camera_keyframes = [
            {
                # 📷 CÂMERA 1: Vista inicial acordar (0-10s)
                "position_start": [-2.416, 0.733, 2.635],  
                "position_end": [-2.416, 0.733, 2.635],    
                "rotation": -0.945,  # -54.1° (Yaw)
                "duration": 10.0,  # ← CORRIGIDO: 10 segundos
                "description": "Vista inicial - humano acordando na cama",
                "movement_type": "static",
                "look_at_human": True
            },
            {
                "position_start": [-2.460, 0.473, 2.329], 
                "position_end": [-2.460, 0.473, 2.329],    
                "rotation": -1.115,  # -63.9° (Yaw)
                "duration": 10.0,  # 20 segundos
                "description": "Vista de caminhada - seguindo o humano",
                "movement_type": "static",
                "look_at_human": True
            }
        ]
        
        # 💡 SISTEMA DE ILUMINAÇÃO
        self.lighting_phases = [
            {
                "start_time": 0.0,
                "end_time": 10.0,  # ← Até acabar acordar
                "brightness": 0.4,
                "color": [0.6, 0.7, 0.9],  # Azul manhã (despertar)
                "description": "Despertar - luz suave da manhã"
            },
            {
                "start_time": 10.0,  # ← Inicia na reflexão
                "end_time": 20.0,   # ← CORRETO: Até final da cena
                "brightness": 0.8,
                "color": [1.0, 0.9, 0.7],  # Dourado (determinação + ação)
                "description": "Determinação e ação - luz quente"
            }
        ]
        
        self.acordar_static_duration = 5.0 
        self.acordar_animation_duration = 5.0 
        self.acordar_animation_started = False
        self.acordar_current_frame = 0
        self.acordar_frame_time = 0.0
        self.acordar_total_frames = 0  # Será definido na inicialização
        self.acordar_frame_duration = 0.0  # Será calculado dinamicamente
        
        self.movement_started = False
        self.movement_start_time = 5.0  # ← Inicia aos 30s
        self.movement_duration = 5.0     # ← Durante 5 segundos
        self.initial_position = [-0.860, 0.100, 0.400]  # Waypoint 1
        self.final_position = [-0.700, -0.3, 0.4]     # Waypoint 2

        self.reflection_started = False
        self.reflection_start_time = 10.0  # ← CORRIGIDO: 8 segundos
        self.parado_loop_started = False
        self.parado_current_frame = 0
        self.parado_frame_time = 0.0
        self.parado_frame_duration = 0.2

        self.manual_timeline = 0.0
        self.is_finished = False

        self.camera_system_active = False
        self.current_camera_keyframe = 0
        self.camera_keyframe_start_time = 0.0

        self.current_waypoint_index = 0
        self.waypoint_start_time = 0.0
        self.waypoint_transition_active = False

        self.last_debug_second = -1

        # 🚶 SISTEMA DE ANIMAÇÃO ANDAR (WAYPOINT 2 → 3)
        self.andar_animation_started = False
        self.andar_start_time = 15.0  # ← Inicia aos 30s
        self.andar_duration = 5.0    # ← 20 segundos de caminhada
        self.andar_current_frame = 0
        self.andar_frame_time = 0.0
        self.andar_total_frames = 0
        self.andar_frame_duration = 0.2
        
        # 🚶 MOVIMENTO WAYPOINT 2 → 3
        self.second_movement_started = False
        self.second_movement_start_time = 15.0
        self.second_movement_duration = 5.0
    
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

        if hasattr(self.scene_manager, 'andar_frames') and self.scene_manager.andar_frames:
            self.andar_total_frames = len(self.scene_manager.andar_frames)
            if self.andar_total_frames > 1:
                self.andar_frame_duration = 0.3  # 0.3s por frame de andar
            else:
                self.andar_frame_duration = 0.5
            
            print(f"🚶 Frames de andar configurados:")
            print(f"   🔢 Total frames: {self.andar_total_frames}")
            print(f"   ⏱️ Duração por frame: {self.andar_frame_duration:.2f}s")
            print(f"   🎬 Animação: {self.andar_start_time}s-{self.andar_start_time + self.andar_duration}s")
        else:
            print("❌ Frames de andar não encontrados")
        
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
      
      # 🕐 FASE 1: ESTÁTICO NA CAMA (0-5s)
      if self.manual_timeline < 5.0:  # ← CORRETO: 5 segundos
          if not hasattr(self, 'acordar_static_logged'):
              print(f"😴 Humano parado no acordar[0] até 5s")
              self.acordar_static_logged = True
      
      # 🎬 FASE 2: ANIMAÇÃO ACORDAR + MOVIMENTO WAYPOINT 1→2 (5-10s)
      elif self.manual_timeline < 10.0:  # ← CORRETO: Até 10s
          if not self.acordar_animation_started:
              self.acordar_animation_started = True
              self.acordar_frame_time = 0.0
              self.movement_started = True
              print(f"🌅 INICIANDO ANIMAÇÃO DE ACORDAR aos {self.manual_timeline:.1f}s")
              print(f"   ⏱️ Duração total: {self.acordar_animation_duration}s")
              print(f"   🔢 Frames: {self.acordar_total_frames}")
              print(f"   📊 {self.acordar_frame_duration:.2f}s por frame")
              print(f"   🚶 Movimento: WAYPOINT 1 → 2")
          
          self._update_movement_during_animation()
          
          self.acordar_frame_time += delta_time
          
          if self.acordar_frame_time >= self.acordar_frame_duration:
              self.acordar_frame_time = 0.0
              
              old_frame = self.acordar_current_frame
              
              if self.acordar_current_frame < self.acordar_total_frames - 1:
                  self.acordar_current_frame += 1
                  print(f"🌅 Acordando: frame {old_frame} → {self.acordar_current_frame}")
                  self._change_waking_frame(self.acordar_current_frame)
              else:
                  print(f"✅ Transição para WAYPOINT 2 concluída (frame {self.acordar_current_frame})")
      
      # 🤔 FASE 3: WAYPOINT 2 - LOOP OLHAR (10-15s)
      elif self.manual_timeline < 15.0:  # ← CORRETO: Até 15s
          if not self.reflection_started:
              self.reflection_started = True
              self.current_waypoint_index = 1
              print(f"🚶 CHEGOU AO WAYPOINT 2 aos {self.manual_timeline:.1f}s")
              print(f"   📍 Posição: {self.waypoints[1]['position']}")
              print(f"   🔄 Rotação: 0° (olhando para frente)")
              print(f"   👀 Inicia loop de olhar por 5 segundos")
              
              # Inicia loop de parado (usa olhar_frames)
              if hasattr(self.scene_manager, 'olhar_frames') and self.scene_manager.olhar_frames:
                  self.parado_loop_started = True
                  self.parado_current_frame = 0
                  self.parado_frame_time = 0.0
                  print(f"   👀 Loop parado: {len(self.scene_manager.olhar_frames)} frames disponíveis")
                  self._change_to_parado_frame(0)
              else:
                  print("   ⚠️ Frames de parado não encontrados")
          
          # 🔄 ATUALIZA LOOP DE PARADO
          if self.parado_loop_started:
              self._update_parado_loop(delta_time)
      
      # 🚶 FASE 4: MOVIMENTO WAYPOINT 2→3 + ANIMAÇÃO ANDAR (15-20s)
      else:
          if not self.andar_animation_started:
              self.andar_animation_started = True
              self.second_movement_started = True
              self.andar_frame_time = 0.0
              self.parado_loop_started = False  # ← PARA LOOP OLHAR
              self.current_waypoint_index = 2
              print(f"🚶 INICIANDO CAMINHADA WAYPOINT 2→3 aos {self.manual_timeline:.1f}s")
              print(f"   📍 Origem: {self.waypoints[1]['position']}")
              print(f"   📍 Destino: {self.waypoints[2]['position']}")
              print(f"   ⏱️ Duração: {self.andar_duration}s")
              print(f"   🔢 Frames andar: {self.andar_total_frames}")
              print(f"   📊 Loop andar: {self.andar_frame_duration:.2f}s por frame")
              print(f"   🔄 CONCEITO: Loop andar contínuo + interpolação de posição")
          
          # 🚶 ATUALIZA MOVIMENTO PARA WAYPOINT 3 (INDEPENDENTE DOS FRAMES)
          self._update_second_movement_during_animation()
          
          # 🎭 ATUALIZA LOOP DE FRAMES DE ANDAR (INDEPENDENTE DO MOVIMENTO)
          self.andar_frame_time += delta_time
          
          if self.andar_frame_time >= self.andar_frame_duration:
              self.andar_frame_time = 0.0
              
              old_frame = self.andar_current_frame
              self.andar_current_frame += 1
              
              # 🔄 LOOP INFINITO - SEMPRE REINICIA
              if self.andar_current_frame >= self.andar_total_frames:
                  self.andar_current_frame = 0
                  # Não imprime reinício para evitar spam
              
              # 🎭 TROCA FRAME DE ANDAR (COM POSIÇÃO INTERPOLADA)
              self._change_andar_frame(self.andar_current_frame)

    def _update_movement_during_animation(self):
      if not self.movement_started:
          return
      
      if self.acordar_total_frames <= 1:
          frame_progress = 0.0
      else:
          frame_progress = self.acordar_current_frame / (self.acordar_total_frames - 1)
      
      # 🔧 INTERPOLAÇÃO SUAVE BASEADA NO FRAME ATUAL
      start_pos = self.waypoints[0]["position"]
      end_pos = self.waypoints[1]["position"]  
      
      # Aplica curva suave ao progresso
      smooth_progress = self._ease_in_out_cubic(frame_progress)
      
      # Calcula posição que será aplicada ao frame atual
      self.interpolated_position = [
          start_pos[0] + (end_pos[0] - start_pos[0]) * smooth_progress, 
          start_pos[1] + (end_pos[1] - start_pos[1]) * smooth_progress,  
          start_pos[2] + (end_pos[2] - start_pos[2]) * smooth_progress   
      ]
    
    def _change_waking_frame(self, new_frame_index):
      if new_frame_index >= len(self.scene_manager.acordar_frames):
          print(f"⚠️ Frame {new_frame_index} inválido - máximo é {len(self.scene_manager.acordar_frames)-1}")
          return
      
      print(f"🔄 Trocando frame acordar: {getattr(self, 'acordar_current_frame', '?')} → {new_frame_index}")
      
      # Remove frame atual
      if hasattr(self, 'humano') and self.humano:
          try:
              self.scene.remove(self.humano)
              print(f"   ✅ Frame anterior removido")
          except:
              print(f"   ⚠️ Frame anterior já estava removido")
      
      # Adiciona novo frame
      self.humano = self.scene_manager.acordar_frames[new_frame_index]
      
      # 🎮 VERIFICA SE CONTROLES MANUAIS ESTÃO ATIVOS
      if self.scene_manager.manual_control_enabled:
          # 🎮 MODO MANUAL: Usa posição atual do scene_manager
          current_position = self.scene_manager.current_human_position.copy()
          humano_rotation = self.scene_manager.current_human_rotation
          print(f"   🎮 MODO MANUAL: Mantendo posição: {current_position}")
      else:
          # 🤖 MODO AUTOMÁTICO: Usa interpolação ou waypoint
          if self.movement_started and hasattr(self, 'interpolated_position'):
              current_position = self.interpolated_position.copy()
              print(f"   🚶 Usando posição interpolada para frame {new_frame_index}: {current_position}")
          else:
              # Antes do movimento, usa posição do waypoint 0
              current_position = self.waypoints[0]["position"].copy()
              print(f"   📍 Usando posição waypoint 0 para frame {new_frame_index}: {current_position}")
          
          humano_rotation = self.waypoints[0]["rotation"]
      
      self.humano.set_position(current_position)
      self.humano.set_rotation_y(humano_rotation)
      
      # Adiciona à scene
      self.scene.add(self.humano)
      print(f"   ✅ Novo frame {new_frame_index} adicionado")
      
      # 🔧 ATUALIZA REFERÊNCIAS DO SCENE_MANAGER
      self.scene_manager.humano = self.humano
      
      # 🎮 SINCRONIZA POSIÇÃO NO SCENE_MANAGER
      if not self.scene_manager.manual_control_enabled:
          self.scene_manager.current_human_position = current_position.copy()
          self.scene_manager.current_human_rotation = humano_rotation
      
      # Define referência da scene para controles manuais
      self.scene_manager.human_scene_reference = self.scene
      
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
      
      # Status do waypoint atual
      if self.manual_timeline < self.acordar_static_duration:
          print(f"   🛏️ WAYPOINT 1: Dormindo na cama (frame 0)")
          print(f"      📍 Posição: {self.waypoints[0]['position']}")
      elif self.manual_timeline < self.acordar_static_duration + self.acordar_animation_duration:
          total_frames = len(self.scene_manager.acordar_frames) if hasattr(self.scene_manager, 'acordar_frames') else 0
          print(f"   🚶 TRANSIÇÃO: Waypoint 1 → 2 (frame {self.acordar_current_frame}/{total_frames-1})")
          if hasattr(self, 'interpolated_position'):
              print(f"      📍 Posição atual: [{self.interpolated_position[0]:.3f}, {self.interpolated_position[1]:.3f}, {self.interpolated_position[2]:.3f}]")
      else:
          if self.parado_loop_started:
              total_parado = len(self.scene_manager.olhar_frames) if hasattr(self.scene_manager, 'olhar_frames') else 0
              print(f"   👀 WAYPOINT 2: Loop parado (frame {self.parado_current_frame}/{total_parado-1})")
              print(f"      📍 Posição: {self.waypoints[1]['position']}")
              print(f"      🔄 Rotação: {self.waypoints[1]['rotation']}° (frente)")
          else:
              print(f"   🚶 WAYPOINT 2: Em pé determinado")
      
      # Status da câmera  
      if self.current_camera_keyframe < len(self.camera_keyframes):
          current_camera = self.camera_keyframes[self.current_camera_keyframe]
          time_in_keyframe = self.manual_timeline - self.camera_keyframe_start_time
          print(f"   📷 Câmera {self.current_camera_keyframe + 1}: {current_camera['description']}")
          print(f"      ⏱️ Tempo: {time_in_keyframe:.1f}/{current_camera['duration']}s")
            
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
          if self.parado_current_frame >= len(self.scene_manager.olhar_frames):
              self.parado_current_frame = 0
              print(f"🔄 Loop parado reiniciado: frame {old_frame} -> {self.parado_current_frame}")
          
          print(f"🧍 Frame parado: {old_frame} -> {self.parado_current_frame}")
          self._change_to_parado_frame(self.parado_current_frame)

    def _change_to_parado_frame(self, new_frame_index):
      if not hasattr(self.scene_manager, 'olhar_frames') or new_frame_index >= len(self.scene_manager.olhar_frames):
          print(f"⚠️ Frame parado {new_frame_index} inválido")
          return
      
      print(f"🔄 Trocando para frame parado: {getattr(self, 'parado_current_frame', '?')} → {new_frame_index}")
      
      # Remove frame atual
      if hasattr(self, 'humano') and self.humano:
          try:
              self.scene.remove(self.humano)
              print(f"   ✅ Frame anterior removido")
          except:
              print(f"   ⚠️ Frame anterior já estava removido")
      
      # Adiciona novo frame parado
      self.humano = self.scene_manager.olhar_frames[new_frame_index]
      
      # 🎮 VERIFICA SE CONTROLES MANUAIS ESTÃO ATIVOS
      if self.scene_manager.manual_control_enabled:
          # 🎮 MODO MANUAL: Usa posição atual do scene_manager
          current_position = self.scene_manager.current_human_position.copy()
          humano_rotation = self.scene_manager.current_human_rotation
          print(f"   🎮 MODO MANUAL: Mantendo posição manual: {current_position}")
          print(f"   🔄 Mantendo rotação manual: {humano_rotation:.3f} rad")
      else:
          # 🤖 MODO AUTOMÁTICO: Usa waypoint 2
          current_position = self.waypoints[1]["position"].copy()
          humano_rotation = self.waypoints[1]["rotation"]
          print(f"   🤖 MODO AUTO: Posição waypoint 2: {current_position}")
          print(f"   🔄 Rotação waypoint 2: {humano_rotation}°")
      
      self.humano.set_position(current_position)
      self.humano.set_rotation_y(humano_rotation)
      
      # Adiciona à scene
      self.scene.add(self.humano)
      print(f"   ✅ Novo frame parado {new_frame_index} adicionado")
      
      # 🔧 ATUALIZA REFERÊNCIAS DO SCENE_MANAGER
      self.scene_manager.humano = self.humano
      
      # 🎮 SINCRONIZA POSIÇÃO NO SCENE_MANAGER (IMPORTANTE!)
      if not self.scene_manager.manual_control_enabled:
          # Só atualiza se não estiver em modo manual
          self.scene_manager.current_human_position = current_position.copy()
          self.scene_manager.current_human_rotation = humano_rotation
      
      # Define referência da scene para controles manuais
      self.scene_manager.human_scene_reference = self.scene
      
      self.parado_current_frame = new_frame_index

    def _update_second_movement_during_animation(self):
      """Atualiza movimento do waypoint 2 para waypoint 3"""
      if not self.second_movement_started:
          return
      
      # Calcula progresso baseado no tempo
      time_since_start = self.manual_timeline - self.second_movement_start_time
      progress = time_since_start / self.second_movement_duration
      progress = min(1.0, max(0.0, progress))  # Limita entre 0 e 1
      
      # 🔧 INTERPOLAÇÃO SUAVE BASEADA NO TEMPO
      start_pos = self.waypoints[1]["position"]  # Waypoint 2
      end_pos = self.waypoints[2]["position"]    # Waypoint 3
      
      # Aplica curva suave ao progresso
      smooth_progress = self._ease_in_out_cubic(progress)
      
      # Calcula posição atual
      self.second_interpolated_position = [
          start_pos[0] + (end_pos[0] - start_pos[0]) * smooth_progress, 
          start_pos[1] + (end_pos[1] - start_pos[1]) * smooth_progress,  
          start_pos[2] + (end_pos[2] - start_pos[2]) * smooth_progress   
      ]
      
      # Calcula rotação gradual também
      start_rot = self.waypoints[1]["rotation"]  # 0°
      end_rot = self.waypoints[2]["rotation"]    # 0.200 rad
      self.second_interpolated_rotation = start_rot + (end_rot - start_rot) * smooth_progress
      
      print(f"   🎯 Progresso caminhada: {progress:.2f} (suave: {smooth_progress:.2f})")
      print(f"   📍 Posição atual: [{self.second_interpolated_position[0]:.3f}, {self.second_interpolated_position[1]:.3f}, {self.second_interpolated_position[2]:.3f}]")

    def _change_andar_frame(self, new_frame_index):
      if not hasattr(self.scene_manager, 'andar_frames') or new_frame_index >= len(self.scene_manager.andar_frames):
          print(f"⚠️ Frame andar {new_frame_index} inválido")
          return
      
      print(f"🔄 Trocando para frame andar: {getattr(self, 'andar_current_frame', '?')} → {new_frame_index}")
      
      # Remove frame atual
      if hasattr(self, 'humano') and self.humano:
          try:
              self.scene.remove(self.humano)
          except:
              pass
      
      # Adiciona novo frame de andar
      self.humano = self.scene_manager.andar_frames[new_frame_index]
      
      # 🎮 VERIFICA SE CONTROLES MANUAIS ESTÃO ATIVOS
      if self.scene_manager.manual_control_enabled:
          # 🎮 MODO MANUAL: Usa posição atual do scene_manager
          current_position = self.scene_manager.current_human_position.copy()
          humano_rotation = self.scene_manager.current_human_rotation
          print(f"   🎮 MODO MANUAL: Mantendo posição: {current_position}")
      else:
          # 🤖 MODO AUTOMÁTICO: Usa interpolação de movimento
          if hasattr(self, 'second_interpolated_position'):
              current_position = self.second_interpolated_position.copy()
              humano_rotation = self.second_interpolated_rotation
              print(f"   🚶 Posição interpolada: {current_position}")
              print(f"   🔄 Rotação interpolada: {humano_rotation:.3f} rad")
          else:
              # Fallback para waypoint 2
              current_position = self.waypoints[1]["position"].copy()
              humano_rotation = self.waypoints[1]["rotation"]
      
      self.humano.set_position(current_position)
      self.humano.set_rotation_y(humano_rotation)
      
      # Adiciona à scene
      self.scene.add(self.humano)
      print(f"   ✅ Frame andar {new_frame_index} adicionado")
      
      # 🔧 ATUALIZA REFERÊNCIAS DO SCENE_MANAGER
      self.scene_manager.humano = self.humano
      
      if not self.scene_manager.manual_control_enabled:
          self.scene_manager.current_human_position = current_position.copy()
          self.scene_manager.current_human_rotation = humano_rotation
      
      # Define referência da scene para controles manuais
      self.scene_manager.human_scene_reference = self.scene
      
      self.andar_current_frame = new_frame_index