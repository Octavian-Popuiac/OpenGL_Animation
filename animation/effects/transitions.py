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
        self.transition_duration = 5.0  # ← SEMPRE 5 segundos
        self.transition_start_time = 0.0
        
        # 📷 Câmera para transições
        self.transition_camera_start = None
        self.transition_camera_end = None
        
        # 🎨 Efeitos visuais
        self.fade_alpha = 0.0
        self.original_background_color = None
        
        # 🧹 LIMPEZA DE CENA
        self.scene_cleaned = False
    
    def update_references(self, camera, renderer):
        """Atualiza referências de câmera e renderer após inicialização"""
        self.camera = camera
        self.renderer = renderer
        print("✅ Referências de câmera e renderer atualizadas no sistema de transições")
        
    def start_transition(self, transition_type="fade_black", duration=5.0):
        """Inicia uma transição específica - SEMPRE 5s e limpa cena primeiro"""
        print(f"🌟 INICIANDO TRANSIÇÃO: {transition_type}")
        
        # 🧹 LIMPA CENA IMEDIATAMENTE
        self._cleanup_scene_immediately()
        
        # 🎬 CONFIGURA TRANSIÇÃO
        self.transition_active = True
        self.transition_type = transition_type
        self.transition_duration = 5.0  # ← FORÇA 5 segundos sempre
        self.transition_progress = 0.0
        self.transition_start_time = time.time()
        self.scene_cleaned = True
        
        # Salva cor de fundo original
        if self.renderer and hasattr(self.renderer, 'background_color'):
            self.original_background_color = self.renderer.background_color.copy()
        
        print(f"🌟 TRANSIÇÃO CONFIGURADA: {transition_type} (SEMPRE 5.0s)")
        
        # Configura transição específica - todas são FADE BLACK simples
        self._setup_simple_fade_transition()
    
    def _cleanup_scene_immediately(self):
        """LIMPA TUDO da scene imediatamente"""
        print("🧹 LIMPEZA COMPLETA DA SCENE - INICIANDO...")
        
        if not hasattr(self.scene_manager, 'scene') or not self.scene_manager.scene:
            print("❌ Scene não encontrada")
            return
        
        try:
            scene = self.scene_manager.scene
            objects_to_remove = []
            
            # 🗑️ COLETA TODOS OS OBJETOS para remover
            for obj in scene.children:
                # Preserva apenas câmera e camera_rig
                if (obj != self.scene_manager.camera and 
                    obj != getattr(self.scene_manager, 'camera_rig', None)):
                    objects_to_remove.append(obj)
            
            # 🗑️ REMOVE TODOS OS OBJETOS
            removed_count = 0
            for obj in objects_to_remove:
                try:
                    scene.remove(obj)
                    removed_count += 1
                except Exception as e:
                    print(f"   ⚠️ Erro ao remover {type(obj).__name__}: {e}")
            
            print(f"✅ LIMPEZA COMPLETA: {removed_count} objetos removidos")
            
            # 🔧 RESET REFERENCIAS DO SCENE MANAGER
            if hasattr(self.scene_manager, 'humano'):
                self.scene_manager.humano = None
            if hasattr(self.scene_manager, 'human_scene_reference'):
                self.scene_manager.human_scene_reference = None
            if hasattr(self.scene_manager, 'manual_control_enabled'):
                self.scene_manager.manual_control_enabled = False
            
            # 🔧 RESET OBJETOS ESPECÍFICOS
            reset_objects = ['sala_musica', 'cozinha', 'quarto', 'rally_terrain', 'rally_car']
            for obj_name in reset_objects:
                if hasattr(self.scene_manager, obj_name):
                    setattr(self.scene_manager, obj_name, None)
            
            print("✅ Scene completamente limpa - apenas câmera permanece")
            
        except Exception as e:
            print(f"❌ Erro na limpeza da scene: {e}")
    
    def _setup_simple_fade_transition(self):
        """Configura transição FADE simples - sempre igual"""
        self.fade_alpha = 0.0
        
        # 🌑 TELA PRETA IMEDIATAMENTE
        if self.renderer and hasattr(self.renderer, 'background_color'):
            self.renderer.background_color = [0.0, 0.0, 0.0]  # Preto total
        
        print("   🌑 Fade simples configurado - 5s de tela preta")
    
    def update(self, delta_time):
        """Atualiza transição ativa"""
        if not self.transition_active:
            return False
        
        # Atualiza progresso
        elapsed_time = time.time() - self.transition_start_time
        self.transition_progress = min(1.0, elapsed_time / self.transition_duration)
        
        # 🌑 APLICA FADE SIMPLES (sempre igual)
        self._update_simple_fade_transition()
        
        # Debug do progresso
        if int(elapsed_time) != int(elapsed_time - delta_time):  # A cada segundo
            remaining = self.transition_duration - elapsed_time
            print(f"🌟 Transição: {elapsed_time:.1f}s / {self.transition_duration}s (restam {remaining:.1f}s)")
        
        # Verifica se terminou
        if self.transition_progress >= 1.0:
            self._finish_transition()
            return True  # Transição concluída
        
        return False  # Ainda em progresso
    
    def _update_simple_fade_transition(self):
        """Atualiza fade simples - 5s de tela preta"""
        # 🌑 MANTÉM TELA PRETA durante toda a transição
        if self.renderer and hasattr(self.renderer, 'background_color'):
            # Ligeira variação de intensidade para efeito sutil
            intensity = 0.02 * math.sin(self.transition_progress * math.pi * 4)  # Pulsação sutil
            self.renderer.background_color = [intensity, intensity, intensity]
    
    def _finish_transition(self):
        """Finaliza transição"""
        self.transition_active = False
        self.scene_cleaned = False
        
        # 🔧 RESTAURA COR DE FUNDO PADRÃO
        if self.renderer and hasattr(self.renderer, 'background_color'):
            # Restaura cor padrão do renderer (cinza escuro)
            self.renderer.background_color = [0.1, 0.1, 0.1]
        
        print(f"✅ TRANSIÇÃO CONCLUÍDA - Scene limpa e pronta para próxima cena")
        
    def is_active(self):
        """Verifica se há transição ativa"""
        return self.transition_active

# 🎬 PRESETS DE TRANSIÇÕES SIMPLIFICADOS
class TransitionPresets:
    """Presets de transições - TODOS iguais (5s fade black)"""
    
    @staticmethod
    def get_scene_transition(from_scene_type, to_scene_type):
        """Retorna transição - SEMPRE igual (5s fade black)"""
        return {
            "type": "fade_black",
            "duration": 5.0,  # ← SEMPRE 5 segundos
            "description": f"Transição {from_scene_type} → {to_scene_type} (5s tela preta)"
        }
    
    @staticmethod
    def get_emotional_transition(emotion_from, emotion_to):
        """Retorna transição emocional - SEMPRE igual (5s fade black)"""
        return {
            "type": "fade_black",
            "duration": 5.0,  # ← SEMPRE 5 segundos
            "description": f"Transição emocional {emotion_from} → {emotion_to} (5s tela preta)"
        }