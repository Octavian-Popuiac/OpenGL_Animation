import math
from animation.base_scene import BaseScene
from geometry.rally import RallyTerrainGeometry
from geometry.box import BoxGeometry
from material.basic import BasicMaterial
from core_ext.mesh import Mesh

from light.directional import DirectionalLight
from light.ambient import AmbientLight
from light.point import PointLight

class RallyScene(BaseScene):
    def __init__(self, scene, camera, renderer, scene_manager):
        super().__init__(scene, camera, renderer)
        self.scene_manager = scene_manager
        
        # 🏁 CONFIGURAÇÕES BÁSICAS
        self.scene_name = "Rally Dream"
        self.scene_duration = 300.0  # 5 minutos
        
        # 🏔️ TERRENO
        self.rally_terrain = None
        self.rally_car = None
        
        # 🚗 POSIÇÕES FIXAS DO CARRO (3 pontos)
        self.car_positions = [
            [0.0, 1.0, -10.0],   # Posição 1: Início
            [5.0, 1.5, 0.0],     # Posição 2: Meio
            [-3.0, 1.2, 8.0]     # Posição 3: Final
        ]
        self.current_position_index = 0
        self.car_position = self.car_positions[0].copy()
        self.target_position = self.car_positions[1].copy()
        
        # 🔄 MOVIMENTO ENTRE POSIÇÕES
        self.movement_progress = 0.0
        self.movement_speed = 0.05  # Velocidade de transição
        self.transition_time = 0.0
        
        # 🎮 CONTROLE
        self.manual_timeline = 0.0
        self.is_finished = False
        
        # 🎮 CONTROLES MANUAIS
        self.manual_control_active = False
        self.car_speed = 0.0
        self.car_rotation = 0.0
        self.movement_speed_manual = 0.1
        self.rotation_speed = 2.0
    
    def initialize(self):
      print(f"\n🏁 ===== RALLY SCENE SIMPLES =====")
      
      # 🏔️ TERRENO
      self._setup_terrain()
      
      # 🏎️ CARRO
      self._setup_car()
      
      # 💡 LUZ BÁSICA
      self._setup_lighting()
      
      # 📷 CONFIGURA CÂMERA INICIAL
      self._setup_initial_camera()
      
      # 🎮 CONTROLES
      if self.scene_manager.free_camera_mode:
          self._enable_manual_controls()
      
      print(f"✅ Rally scene inicializada:")
      print(f"   🏎️ Carro em: {self.car_position}")
      print(f"   🎯 Próximo alvo: {self.target_position}")
      print(f"   ⏱️ Duração: {self.scene_duration}s")
      print(f"   📷 Câmera livre: {'Ativada' if self.scene_manager.free_camera_mode else 'Desativada'}")
    
    def _setup_terrain(self):
        """Configura terreno"""
        if hasattr(self.scene_manager, 'rally_terrain_geometry'):
            terrain_geometry = self.scene_manager.rally_terrain_geometry
            terrain_material = BasicMaterial(use_vertex_colors=True)
            self.rally_terrain = Mesh(terrain_geometry, terrain_material)
            print("🏔️ Terreno carregado do scene_manager")
        else:
            # Terreno padrão simples
            terrain_geometry = RallyTerrainGeometry()
            terrain_material = BasicMaterial(use_vertex_colors=True)
            self.rally_terrain = Mesh(terrain_geometry, terrain_material)
            print("🏔️ Terreno padrão criado")
        
        self.rally_terrain.set_position([0, 0, 0])
        self.scene.add(self.rally_terrain)
    
    def _setup_car(self):
        """Configura carro"""
        if hasattr(self.scene_manager, 'rally_car_geometry'):
            car_geometry = self.scene_manager.rally_car_geometry
            car_material = BasicMaterial(use_vertex_colors=True)
            print("🏎️ Carro carregado do scene_manager")
        else:
            # Carro padrão simples
            car_geometry = BoxGeometry(width=2.0, height=1.0, depth=4.0)
            car_material = BasicMaterial(use_vertex_colors=True)
            print("🏎️ Carro padrão criado")
        
        self.rally_car = Mesh(car_geometry, car_material)
        self.rally_car.set_position(self.car_position)
        self.scene.add(self.rally_car)
    
    def _setup_lighting(self):
        """Iluminação básica"""
        try:
            # Luz direcional
            self.directional_light = DirectionalLight(
                direction=[1, -1, -1],
                color=[1.0, 1.0, 1.0]
            )
            self.scene.add(self.directional_light)
            
            # Luz ambiente
            self.ambient_light = AmbientLight(color=[0.3, 0.3, 0.3])
            self.scene.add(self.ambient_light)
            
            print("💡 Iluminação configurada")
        except Exception as e:
            print(f"⚠️ Erro na iluminação: {e}")

    def _setup_initial_camera(self):
      """Configura posição inicial da câmera"""
      try:
          if self.scene_manager.free_camera_mode:
              # 📷 CÂMERA LIVRE: Posição para ver bem a cena
              self.camera.set_position([10, 8, 5])  # Posição elevada e afastada
              self.camera.look_at([0, 0, 0])        # Olha para o centro da cena
              print("📷 Câmera livre configurada - posição elevada")
          else:
              # 📷 CÂMERA FIXA: Acompanha o carro
              cam_pos = [
                  self.car_position[0] - 8,  # Atrás do carro
                  self.car_position[1] + 5,  # Acima do carro
                  self.car_position[2] - 8   # Afastada do carro
              ]
              self.camera.set_position(cam_pos)
              self.camera.look_at(self.car_position)
              print("📷 Câmera fixa configurada - seguindo carro")
      except Exception as e:
          print(f"⚠️ Erro ao configurar câmera: {e}")
          # Posição padrão de segurança
          self.camera.set_position([0, 10, 10])
          self.camera.look_at([0, 0, 0])
    
    
    def _enable_manual_controls(self):
        """Ativa controles manuais"""
        print("🎮 CONTROLES MANUAIS DE RALLY:")
        print("   ⬆️ W: Mover carro para frente")
        print("   ⬇️ S: Mover carro para trás") 
        print("   ⬅️ A: Mover carro para esquerda")
        print("   ➡️ D: Mover carro para direita")
        print("   🔄 Q: Rotar carro esquerda")
        print("   🔄 E: Rotar carro direita")
        print("   🎮 SPACE: Alternar modo automático/manual")
        print("   📊 ENTER: Mostrar informações do carro e câmera")
        print("   ⏭️ R: Pular para próxima posição fixa")
        print("\n📷 NOTA: Câmera livre está ativa - use mouse para olhar ao redor")
    
    def update(self, delta_time):
      """Atualiza a cena"""
      if self.is_finished:
          return
      
      self.manual_timeline += delta_time
      
      # 🎮 CONTROLES MANUAIS (só se câmera livre estiver ativa)
      if self.scene_manager.free_camera_mode:
          self._handle_manual_controls(delta_time)
      else:
          # 📷 CÂMERA AUTOMÁTICA: Segue o carro
          self._update_automatic_camera()
      
      # 🚗 MOVIMENTO AUTOMÁTICO ENTRE POSIÇÕES (só se não estiver em controle manual)
      if not self.manual_control_active:
          self._update_automatic_movement(delta_time)
      
      # ⏰ VERIFICA FIM
      if self.manual_timeline >= self.scene_duration:
          self.is_finished = True
          print("🏁 Rally scene concluída!")
    
    def _handle_manual_controls(self, delta_time):
        """Controles manuais do carro"""
        if not hasattr(self.scene_manager, 'input') or not self.scene_manager.input:
            return
        
        input_manager = self.scene_manager.input
        
        # 🚗 MOVIMENTO MANUAL
        if input_manager.is_key_pressed("w"):
            move_x = math.sin(self.car_rotation) * self.movement_speed_manual
            move_z = -math.cos(self.car_rotation) * self.movement_speed_manual
            self.car_position[0] += move_x
            self.car_position[2] += move_z
            self.manual_control_active = True
        
        if input_manager.is_key_pressed("s"):
            move_x = -math.sin(self.car_rotation) * self.movement_speed_manual
            move_z = math.cos(self.car_rotation) * self.movement_speed_manual
            self.car_position[0] += move_x
            self.car_position[2] += move_z
            self.manual_control_active = True
        
        if input_manager.is_key_pressed("a"):
            self.car_position[0] -= self.movement_speed_manual
            self.manual_control_active = True
        
        if input_manager.is_key_pressed("d"):
            self.car_position[0] += self.movement_speed_manual
            self.manual_control_active = True
        
        # 🔄 ROTAÇÃO
        if input_manager.is_key_pressed("q"):
            self.car_rotation -= self.rotation_speed * delta_time
            self.manual_control_active = True
        
        if input_manager.is_key_pressed("e"):
            self.car_rotation += self.rotation_speed * delta_time
            self.manual_control_active = True
        
        # 🔄 ALTERNAR MODO
        if input_manager.is_key_pressed("space"):
            self.manual_control_active = not self.manual_control_active
            mode = "Manual" if self.manual_control_active else "Automático"
            print(f"🎮 Modo: {mode}")
        
        # 📍 MOSTRAR POSIÇÃO
        if input_manager.is_key_pressed("return"):
            self._show_car_info()
        
        # ➡️ PRÓXIMA POSIÇÃO FIXA
        if input_manager.is_key_pressed("r"):
            self._next_fixed_position()
        
        # 🔄 APLICA TRANSFORMAÇÕES
        self.rally_car.set_position(self.car_position)
        self.rally_car.set_rotation_y(self.car_rotation)
    
    def _update_automatic_movement(self, delta_time):
        """Movimento automático entre as 3 posições"""
        if self.current_position_index >= len(self.car_positions):
            return
        
        # 📈 PROGRESSO DO MOVIMENTO
        self.movement_progress += self.movement_speed * delta_time
        
        if self.movement_progress >= 1.0:
            # 🎯 CHEGOU AO DESTINO
            self.car_position = self.target_position.copy()
            self.current_position_index += 1
            
            if self.current_position_index < len(self.car_positions):
                # 🔄 PRÓXIMA POSIÇÃO
                self.target_position = self.car_positions[self.current_position_index].copy()
                self.movement_progress = 0.0
                print(f"🎯 Indo para posição {self.current_position_index + 1}: {self.target_position}")
            else:
                print("🏁 Todas as posições visitadas!")
        else:
            # 🚗 INTERPOLAÇÃO LINEAR ENTRE POSIÇÕES
            start_pos = self.car_positions[self.current_position_index - 1] if self.current_position_index > 0 else self.car_positions[0]
            
            self.car_position[0] = start_pos[0] + (self.target_position[0] - start_pos[0]) * self.movement_progress
            self.car_position[1] = start_pos[1] + (self.target_position[1] - start_pos[1]) * self.movement_progress
            self.car_position[2] = start_pos[2] + (self.target_position[2] - start_pos[2]) * self.movement_progress
        
        # 🔄 APLICA POSIÇÃO
        self.rally_car.set_position(self.car_position)

    def _update_automatic_camera(self):
      try:
          # 📷 POSIÇÃO DA CÂMERA: Atrás e acima do carro
          cam_offset = [-8, 5, -8]  # Offset relativo ao carro
          
          # Aplica rotação do carro ao offset
          cos_rot = math.cos(self.car_rotation)
          sin_rot = math.sin(self.car_rotation)
          
          # Rotaciona o offset baseado na rotação do carro
          rotated_x = cam_offset[0] * cos_rot - cam_offset[2] * sin_rot
          rotated_z = cam_offset[0] * sin_rot + cam_offset[2] * cos_rot
          
          cam_pos = [
              self.car_position[0] + rotated_x,
              self.car_position[1] + cam_offset[1],
              self.car_position[2] + rotated_z
          ]
          
          # 🎯 CÂMERA OLHA PARA O CARRO
          self.camera.set_position(cam_pos)
          self.camera.look_at(self.car_position)
          
      except Exception as e:
          pass  # Ignora erros de câmera para não quebrar a cena
    
    def _next_fixed_position(self):
        """Vai para a próxima posição fixa"""
        if self.current_position_index < len(self.car_positions) - 1:
            self.current_position_index += 1
            self.target_position = self.car_positions[self.current_position_index].copy()
            self.movement_progress = 0.0
            print(f"🎯 Saltando para posição {self.current_position_index + 1}: {self.target_position}")
        else:
            # 🔄 VOLTA AO INÍCIO
            self.current_position_index = 0
            self.target_position = self.car_positions[0].copy()
            self.movement_progress = 0.0
            print("🔄 Voltando ao início")
    
    def _show_car_info(self):
      print(f"\n🚗 INFORMAÇÕES DO CARRO:")
      print(f"   📍 Posição atual: [{self.car_position[0]:.2f}, {self.car_position[1]:.2f}, {self.car_position[2]:.2f}]")
      print(f"   🔄 Rotação: {self.car_rotation * 180 / math.pi:.1f}°")
      print(f"   🎯 Posição de destino: {self.current_position_index + 1}/{len(self.car_positions)}")
      print(f"   📈 Progresso: {self.movement_progress * 100:.1f}%")
      print(f"   🎮 Modo: {'Manual' if self.manual_control_active else 'Automático'}")
      print(f"   ⏰ Tempo: {self.manual_timeline:.1f}s / {self.scene_duration:.1f}s")
      
      # 📷 INFORMAÇÕES DA CÂMERA
      try:
          cam_pos = self.camera.get_position() if hasattr(self.camera, 'get_position') else "N/A"
          print(f"\n📷 INFORMAÇÕES DA CÂMERA:")
          print(f"   📍 Posição: {cam_pos}")
          print(f"   🔄 Modo: {'Livre' if self.scene_manager.free_camera_mode else 'Automática'}")
      except Exception as e:
          print(f"📷 Câmera: erro ao obter informações - {e}")
    
    def cleanup_previous_scene(self):
        """Limpa objetos da cena anterior"""
        print("🗑️ Limpeza básica da cena anterior...")
        # Limpeza mínima necessária
    
    # 🔧 MÉTODOS ABSTRATOS OBRIGATÓRIOS
    def get_duration(self):
        return self.scene_duration
    
    def get_name(self):
        return self.scene_name
    
    def is_scene_finished(self):
        return self.is_finished
    
    def reset_scene(self):
        self.manual_timeline = 0.0
        self.is_finished = False
        self.current_position_index = 0
        self.car_position = self.car_positions[0].copy()
        self.target_position = self.car_positions[1].copy()
        self.movement_progress = 0.0
        self.manual_control_active = False
        self.car_rotation = 0.0
        print("🔄 Rally scene resetada")