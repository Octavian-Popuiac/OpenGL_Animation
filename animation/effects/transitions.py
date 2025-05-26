import math
import time

class SceneTransitions:
    """Sistema de transições cinematográficas entre cenas"""
    
    def __init__(self, scene_manager):
        """Sistema de transições cinematográficas entre cenas"""
        self.scene_manager = scene_manager
        
        # 🔧 VERIFICA SE CÂMERA E RENDERER EXISTEM
        if hasattr(scene_manager, 'camera') and scene_manager.camera:
            self.camera = scene_manager.camera
        else:
            self.camera = None
            print("⚠️ Câmera não disponível no momento da criação das transições")
        
        if hasattr(scene_manager, 'renderer') and scene_manager.renderer:
            self.renderer = scene_manager.renderer
        else:
            self.renderer = None
            print("⚠️ Renderer não disponível no momento da criação das transições")
        
        # 🎬 Estado da transição
        self.transition_active = False
        self.transition_type = None
        self.transition_progress = 0.0
        self.transition_duration = 2.0  # 2 segundos padrão
        self.transition_start_time = 0.0
        
        # 📷 Câmera para transições
        self.transition_camera_start = None
        self.transition_camera_end = None
        
        # 🎨 Efeitos visuais
        self.fade_alpha = 0.0
        self.original_background_color = None
    
    def update_references(self, camera, renderer):
        """Atualiza referências de câmera e renderer após inicialização"""
        self.camera = camera
        self.renderer = renderer
        print("✅ Referências de câmera e renderer atualizadas no sistema de transições")
        
    def start_transition(self, transition_type="fade_black", duration=2.0):
        """Inicia uma transição específica"""
        self.transition_active = True
        self.transition_type = transition_type
        self.transition_duration = duration
        self.transition_progress = 0.0
        self.transition_start_time = time.time()
        
        # Salva cor de fundo original
        if self.renderer and hasattr(self.renderer, 'background_color'):
            self.original_background_color = self.renderer.background_color.copy()
        
        print(f"🌟 TRANSIÇÃO INICIADA: {transition_type} ({duration}s)")
        
        # Configura transição específica
        if transition_type == "fade_black":
            self._setup_fade_transition()
        elif transition_type == "camera_pan":
            self._setup_camera_pan_transition()
        elif transition_type == "zoom_out_in":
            self._setup_zoom_transition()
        elif transition_type == "slide_left":
            self._setup_slide_transition("left")
        elif transition_type == "cross_dissolve":
            self._setup_cross_dissolve()
    
    def update(self, delta_time):
        """Atualiza transição ativa"""
        if not self.transition_active:
            return False
        
        # Atualiza progresso
        elapsed_time = time.time() - self.transition_start_time
        self.transition_progress = min(1.0, elapsed_time / self.transition_duration)
        
        # Aplica efeito baseado no tipo
        if self.transition_type == "fade_black":
            self._update_fade_transition()
        elif self.transition_type == "camera_pan":
            self._update_camera_pan_transition()
        elif self.transition_type == "zoom_out_in":
            self._update_zoom_transition()
        elif self.transition_type == "slide_left":
            self._update_slide_transition()
        elif self.transition_type == "cross_dissolve":
            self._update_cross_dissolve()
        
        # Verifica se terminou
        if self.transition_progress >= 1.0:
            self._finish_transition()
            return True  # Transição concluída
        
        return False  # Ainda em progresso
    
    def _setup_fade_transition(self):
        """Configura transição de fade para preto"""
        self.fade_alpha = 0.0
        print("   🌑 Fade to black configurado")
    
    def _update_fade_transition(self):
        """Atualiza fade para preto"""
        # Primeira metade: fade out (0.0 → 1.0)
        # Segunda metade: fade in (1.0 → 0.0)
        if self.transition_progress <= 0.5:
            # Fade out
            self.fade_alpha = self.transition_progress * 2.0
        else:
            # Fade in
            self.fade_alpha = 2.0 - (self.transition_progress * 2.0)
        
        # Aplica cor de fundo escura
        if self.renderer and hasattr(self.renderer, 'background_color'):
            darkness = self.fade_alpha
            self.renderer.background_color = [
                darkness * 0.0,  # R
                darkness * 0.0,  # G  
                darkness * 0.0   # B
            ]
    
    def _setup_camera_pan_transition(self):
        """Configura transição de câmera panorâmica"""
        # Salva posição atual da câmera
        if self.camera and hasattr(self.camera, 'get_position'):
            self.transition_camera_start = self.camera.get_position()
        else:
            self.transition_camera_start = [0, 1, 0]  # Fallback
        
        # Define posição de destino (vista ampla)
        self.transition_camera_end = [
            self.transition_camera_start[0] + 5.0,  # Move para direita
            self.transition_camera_start[1] + 3.0,  # Sobe
            self.transition_camera_start[2] + 5.0   # Afasta
        ]
        
        print(f"   📷 Pan configurado: {self.transition_camera_start} → {self.transition_camera_end}")
    
    def _update_camera_pan_transition(self):
        """Atualiza movimento panorâmico da câmera"""
        if not self.camera:
            return
            
        # Curva suave para movimento
        smooth_progress = self._ease_in_out(self.transition_progress)
        
        # Interpola posição
        current_pos = [
            self.transition_camera_start[0] + (self.transition_camera_end[0] - self.transition_camera_start[0]) * smooth_progress,
            self.transition_camera_start[1] + (self.transition_camera_end[1] - self.transition_camera_start[1]) * smooth_progress,
            self.transition_camera_start[2] + (self.transition_camera_end[2] - self.transition_camera_start[2]) * smooth_progress
        ]
        
        self.camera.set_position(current_pos)
    
    def _setup_zoom_transition(self):
        """Configura transição de zoom out → zoom in"""
        if self.camera and hasattr(self.camera, 'get_position'):
            self.transition_camera_start = self.camera.get_position()
        else:
            self.transition_camera_start = [0, 1, 0]
        
        # Posição de zoom out máximo
        self.transition_camera_end = [
            self.transition_camera_start[0],
            self.transition_camera_start[1] + 10.0,  # Muito alto
            self.transition_camera_start[2] + 10.0   # Muito longe
        ]
        
        print(f"   🔍 Zoom out/in configurado")
    
    def _update_zoom_transition(self):
        """Atualiza transição de zoom"""
        if not self.camera:
            return
            
        if self.transition_progress <= 0.5:
            # Primeira metade: zoom out
            zoom_progress = self.transition_progress * 2.0
            smooth_zoom = self._ease_out(zoom_progress)
            
            current_pos = [
                self.transition_camera_start[0] + (self.transition_camera_end[0] - self.transition_camera_start[0]) * smooth_zoom,
                self.transition_camera_start[1] + (self.transition_camera_end[1] - self.transition_camera_start[1]) * smooth_zoom,
                self.transition_camera_start[2] + (self.transition_camera_end[2] - self.transition_camera_start[2]) * smooth_zoom
            ]
        else:
            # Segunda metade: zoom in
            zoom_progress = (self.transition_progress - 0.5) * 2.0
            smooth_zoom = self._ease_in(zoom_progress)
            
            current_pos = [
                self.transition_camera_end[0] + (self.transition_camera_start[0] - self.transition_camera_end[0]) * smooth_zoom,
                self.transition_camera_end[1] + (self.transition_camera_start[1] - self.transition_camera_end[1]) * smooth_zoom,
                self.transition_camera_end[2] + (self.transition_camera_start[2] - self.transition_camera_end[2]) * smooth_zoom
            ]
        
        self.camera.set_position(current_pos)
    
    def _setup_slide_transition(self, direction):
        """Configura transição de deslize"""
        self.slide_direction = direction
        
        # Salva posição inicial da câmera
        if self.camera and hasattr(self.camera, 'get_position'):
            self.transition_camera_start = self.camera.get_position()
        else:
            self.transition_camera_start = [0, 1, 0]
            
        print(f"   ↔️ Slide {direction} configurado")
    
    def _update_slide_transition(self):
        """Atualiza transição de deslize"""
        if not self.camera:
            return
            
        # Move câmera lateralmente
        base_pos = self.transition_camera_start or [0, 1, 0]
        
        # Calcula deslocamento
        slide_amount = math.sin(self.transition_progress * math.pi) * 8.0
        
        if self.slide_direction == "left":
            offset_pos = [base_pos[0] - slide_amount, base_pos[1], base_pos[2]]
        else:  # right
            offset_pos = [base_pos[0] + slide_amount, base_pos[1], base_pos[2]]
        
        self.camera.set_position(offset_pos)
    
    def _setup_cross_dissolve(self):
        """Configura transição de cross dissolve"""
        print("   🌫️ Cross dissolve configurado")
    
    def _update_cross_dissolve(self):
        """Atualiza cross dissolve"""
        # Dissolve gradual alterando opacidade/brilho
        dissolve_amount = math.sin(self.transition_progress * math.pi)
        
        if self.renderer and hasattr(self.renderer, 'background_color'):
            # Altera ligeiramente a cor de fundo
            self.renderer.background_color = [
                0.1 + dissolve_amount * 0.05,
                0.1 + dissolve_amount * 0.05,
                0.1 + dissolve_amount * 0.05
            ]
    
    def _ease_in_out(self, t):
        """Curva de animação suave entrada/saída"""
        return t * t * (3 - 2 * t)
    
    def _ease_in(self, t):
        """Curva de animação aceleração"""
        return t * t
    
    def _ease_out(self, t):
        """Curva de animação desaceleração"""
        return 1 - (1 - t) * (1 - t)
    
    def _finish_transition(self):
        """Finaliza transição"""
        self.transition_active = False
        
        # Restaura configurações originais
        if self.original_background_color and self.renderer and hasattr(self.renderer, 'background_color'):
            self.renderer.background_color = self.original_background_color
        
        print(f"✅ TRANSIÇÃO CONCLUÍDA: {self.transition_type}")
        
    def is_active(self):
        """Verifica se há transição ativa"""
        return self.transition_active

# 🎬 PRESETS DE TRANSIÇÕES CINEMATOGRÁFICAS
class TransitionPresets:
    """Presets de transições para diferentes tipos de cenas"""
    
    @staticmethod
    def get_scene_transition(from_scene_type, to_scene_type):
        """Retorna transição adequada baseada nos tipos de cena"""
        
        # 🎼 Sala de música → 🍽️ Cozinha
        if from_scene_type == "music_room" and to_scene_type == "kitchen":
            return {
                "type": "fade_black",
                "duration": 3.0,
                "description": "Fade dramático - Mudança de ambiente"
            }
        
        # 🍽️ Cozinha → 🛏️ Quarto  
        elif from_scene_type == "kitchen" and to_scene_type == "bedroom":
            return {
                "type": "zoom_out_in", 
                "duration": 2.5,
                "description": "Zoom out/in - Isolamento crescente"
            }
        
        # 🛏️ Quarto → 🌃 Exterior
        elif from_scene_type == "bedroom" and to_scene_type == "exterior":
            return {
                "type": "slide_left",
                "duration": 2.0,
                "description": "Slide lateral - Movimento para fora"
            }
        
        # Padrão
        else:
            return {
                "type": "cross_dissolve",
                "duration": 1.5,
                "description": "Dissolve suave - Transição genérica"
            }
    
    @staticmethod
    def get_emotional_transition(emotion_from, emotion_to):
        """Retorna transição baseada na mudança emocional"""
        
        # Neutro → Tensão
        if emotion_from == "neutral" and emotion_to == "tension":
            return {
                "type": "camera_pan",
                "duration": 2.0,
                "description": "Pan dramático - Aumento de tensão"
            }
        
        # Tensão → Isolamento
        elif emotion_from == "tension" and emotion_to == "isolation":
            return {
                "type": "zoom_out_in",
                "duration": 3.0,
                "description": "Zoom out/in - Isolamento emocional"
            }
        
        # Isolamento → Reflexão
        elif emotion_from == "isolation" and emotion_to == "reflection":
            return {
                "type": "fade_black",
                "duration": 4.0,
                "description": "Fade longo - Momento reflexivo"
            }
        
        # Padrão
        else:
            return {
                "type": "cross_dissolve",
                "duration": 2.0,
                "description": "Dissolve emocional"
            }