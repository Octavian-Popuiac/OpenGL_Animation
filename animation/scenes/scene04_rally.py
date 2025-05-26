from animation.base_scene import BaseScene

class RallyScene(BaseScene):
    def __init__(self, scene, camera, renderer, scene_manager):
        super().__init__(scene, camera, renderer)
        self.scene_manager = scene_manager
        
        # 🏁 CONFIGURAÇÕES BÁSICAS
        self.scene_name = "Rally Dream"
        self.scene_duration = 30.0  # ← 30 segundos
        
        # 🎮 CONTROLE - INICIALIZADO NO CONSTRUCT
        self.manual_timeline = 0.0
        self.is_finished = False
        
        # 🔧 DEBUG TIMER
        self.debug_timer = 0.0
        self.debug_interval = 5.0  # Debug a cada 5 segundos
        
        print(f"🏁 RallyScene construído - duração: {self.scene_duration}s")

    def initialize(self):
        """Inicializa a cena de rally - TELA PRETA por 30s"""
        print(f"\n🏁 ===== RALLY SCENE - TELA PRETA (30s) =====")
        
        # 🔄 RESET FORÇADO DOS TIMERS
        self.manual_timeline = 0.0
        self.debug_timer = 0.0
        self.is_finished = False
        
        print(f"⏱️ RESET FORÇADO - manual_timeline: {self.manual_timeline}")
        print(f"⏱️ RESET FORÇADO - debug_timer: {self.debug_timer}")
        
        # 🔧 LIMPEZA COMPLETA
        self._clean_scene()
        
        # 📷 CONFIGURA CÂMERA BÁSICA
        self._setup_camera()
        
        print(f"✅ Rally scene inicializada:")
        print(f"   ⬛ Tela preta por {self.scene_duration} segundos")
        print(f"   📷 Câmera configurada")
        print(f"   🚫 Sem objetos")
        print(f"   ⏱️ Timer GARANTIDO em 0.0s")

    def _clean_scene(self):
        """Limpeza completa da scene"""
        print("🧹 Limpeza completa da scene...")
        
        try:
            if hasattr(self.scene, 'children_list'):
                scene_objects = self.scene.children_list.copy()
                
                for obj in scene_objects:
                    # Remove TODOS os objetos
                    self.scene.remove(obj)
                    print(f"   🗑️ Removido: {type(obj).__name__}")
                        
            print(f"✅ Limpeza completa - scene vazia")
            
        except Exception as e:
            print(f"⚠️ Erro na limpeza: {e}")

    def _setup_camera(self):
        """Configura câmera básica"""
        try:
            # Posição da câmera neutra
            camera_position = [0, 0, 0]
            
            print(f"📷 Configurando câmera: {camera_position}")
            
            if self.scene_manager.free_camera_mode:
                if hasattr(self.scene_manager, 'camera_rig') and self.scene_manager.camera_rig:
                    self.scene_manager.camera_rig.set_position(camera_position)
                    print(f"📷 Camera_rig configurado")
                else:
                    self.camera.set_position(camera_position)
                    print(f"📷 Câmera direta configurada")
            else:
                self.camera.set_position(camera_position)
                print(f"📷 Câmera fixa configurada")
                
        except Exception as e:
            print(f"⚠️ Erro ao configurar câmera: {e}")

    def update(self, delta_time):
        """Atualiza a cena - termina após 30s"""
        if self.is_finished:
            return
        
        # 📊 DEBUG do estado antes da atualização
        old_timeline = self.manual_timeline
        
        self.manual_timeline += delta_time
        self.debug_timer += delta_time
        
        # 📊 DEBUG da atualização
        if old_timeline == 0.0 and self.manual_timeline > 0.0:
            print(f"🚀 PRIMEIRA ATUALIZAÇÃO: {old_timeline:.3f}s → {self.manual_timeline:.3f}s (delta: {delta_time:.3f}s)")
        
        # ⏱️ VERIFICA SE TERMINOU (30 segundos)
        if self.manual_timeline >= self.scene_duration:
            self.is_finished = True
            print(f"\n🏁 TELA PRETA TERMINADA após {self.manual_timeline:.1f}s (duração: {self.scene_duration}s)")
            return
        
        # Debug automático a cada 5 segundos
        if self.debug_timer >= self.debug_interval:
            self.debug_timer = 0.0
            remaining = self.scene_duration - self.manual_timeline
            print(f"\n⏰ TELA PRETA - {self.manual_timeline:.1f}s / {self.scene_duration}s (restam {remaining:.1f}s)")
        
        # Controles de debug
        if hasattr(self.scene_manager, 'input') and self.scene_manager.input:
            if self.scene_manager.input.is_key_pressed("return"):
                remaining = self.scene_duration - self.manual_timeline
                print(f"\n⬛ TELA PRETA - {self.manual_timeline:.1f}s / {self.scene_duration}s (restam {remaining:.1f}s)")
            
            if self.scene_manager.input.is_key_pressed("i"):
                self._debug_camera()
            
            # 🚀 PULAR SCENE (tecla SPACE)
            if self.scene_manager.input.is_key_pressed("space"):
                self.is_finished = True
                print(f"\n🚀 TELA PRETA PULADA aos {self.manual_timeline:.1f}s")

    def _debug_camera(self):
        """Debug da câmera"""
        remaining = self.scene_duration - self.manual_timeline
        print(f"\n📷 DEBUG CÂMERA (t={self.manual_timeline:.1f}s, restam {remaining:.1f}s):")
        
        try:
            if self.scene_manager.free_camera_mode:
                if hasattr(self.scene_manager, 'camera_rig') and self.scene_manager.camera_rig:
                    if hasattr(self.scene_manager.camera_rig, 'get_position'):
                        rig_pos = self.scene_manager.camera_rig.get_position()
                        print(f"   📍 Camera_rig: {rig_pos}")
                else:
                    print(f"   ❌ Camera_rig não encontrado")
            
            if hasattr(self.camera, 'get_position'):
                cam_pos = self.camera.get_position()
                print(f"   📍 Camera: {cam_pos}")
            
            print(f"   🎮 Modo: {'LIVRE' if self.scene_manager.free_camera_mode else 'FIXO'}")
            print(f"   ⬛ Scene: TELA PRETA")
            print(f"   ⏱️ Progresso: {self.manual_timeline:.1f}s / {self.scene_duration}s")
            
        except Exception as e:
            print(f"   ❌ Erro no debug da câmera: {e}")

    def cleanup_previous_scene(self):
        """Limpa cena anterior"""
        print("🗑️ Limpeza da cena anterior...")

    # Métodos obrigatórios
    def get_duration(self):
        return self.scene_duration

    def get_name(self):
        return self.scene_name

    def is_scene_finished(self):
        return self.is_finished

    def reset_scene(self):
        """Reset completo da scene"""
        print(f"🔄 RESET_SCENE CHAMADO - antes: timeline={self.manual_timeline:.1f}s")
        
        self.manual_timeline = 0.0
        self.is_finished = False
        self.debug_timer = 0.0
        
        print(f"🔄 RESET_SCENE CONCLUÍDO - depois: timeline={self.manual_timeline:.1f}s")
        print(f"🔄 Rally scene resetada - TELA PRETA ({self.scene_duration}s)")