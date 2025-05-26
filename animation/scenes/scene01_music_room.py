import math
from animation.base_scene import BaseScene

class MusicRoomScene(BaseScene):
    
    def __init__(self, scene, camera, renderer, scene_manager):
        super().__init__(scene, camera, renderer)
        self.scene_name = "Scene01 - Sala de Música"
        self.scene_manager = scene_manager
        self.manual_timeline = 0
        self.time_scale = 1.0  # Velocidade normal
        

        # 🎭 SISTEMA DE ESTADOS DE ANIMAÇÃO
        self.animation_state = "WAITING"
        self.frame_index = 0
        self.frame_count = 0

        # 🗺️ SISTEMA DE WAYPOINTS - PERCURSO DO HUMANO
        self.waypoints = [
            {
                "position": [1.700, 0.090, 0.500],  # Posição inicial (sentado)
                "rotation": -(math.pi / 2),  # -90° (esquerda)
                "animation": "STANDING",  # Animação de levantar
                "duration": 8.0,  # 5s parado + 3s animação
                "description": "Posição inicial - Levantando",
                "movement_type": "static"  # Sem movimento
            },
            {
                "position": [1.460, 0.090, 0.500],  # Segunda posição
                "rotation": -(math.pi / 2),  # -90° (esquerda)
                "animation": "IDLE",  # Animação de parado
                "duration": 5.0,  # 5 segundos olhando
                "description": "Segunda posição - Observando",
                "movement_type": "teleport"  # Teletransporte (como antes)
            },
            {
                "position": [1.460, 0.090, -0.020],  # Terceiro ponto
                "rotation": 2.771,  # 🎯 ROTAÇÃO FINAL: 158.8° (Sul/trás)
                "animation": "WALKING",  # Animação de andar
                "duration": 2.5,  # Tempo para chegar lá
                "description": "Primeiro movimento - Andando para Sul",
                "movement_type": "smooth",  # Movimento suave
                "auto_face_while_moving": True  # 🔧 VIRA-SE DURANTE MOVIMENTO
            },
            {
                "position": [0.740, 0.090, -0.020],  # Quarto ponto
                "rotation": -0.179,  # 🎯 ROTAÇÃO FINAL: -10.3° (Norte)
                "animation": "WALKING",  # Animação de andar
                "duration": 2.5,  # Tempo para chegar lá
                "description": "Segundo movimento - Andando para Oeste",
                "movement_type": "smooth",  # Movimento suave
                "auto_face_while_moving": True  # 🔧 VIRA-SE DURANTE MOVIMENTO
            },
            {
                "position": [0.740, 0.090, -0.020],  # Mesmo ponto (parado)
                "rotation": -0.179,  # Mantém rotação
                "animation": "IDLE",  # Animação de olhar (parado)
                "duration": 5.0,  # 5 segundos parado observando
                "description": "Primeira pausa - Observando ambiente",
                "movement_type": "static"  # Sem movimento
            },
            {
                "position": [1.780, 0.090, -0.800],  # Quinto ponto
                "rotation": -3.071,  # 🎯 ROTAÇÃO FINAL: -176.0° (Sul)
                "animation": "WALKING",  # Animação de andar
                "duration": 3.0,  # Tempo para chegar lá
                "description": "Terceiro movimento - Andando para Sudeste",
                "movement_type": "smooth",  # Movimento suave
                "auto_face_while_moving": True  # 🔧 VIRA-SE DURANTE MOVIMENTO
            },
            {
                "position": [1.780, 0.090, -0.800],  # Mesmo ponto (parado)
                "rotation": -3.071,  # Mantém rotação Sul
                "animation": "IDLE",  # Animação de olhar (parado)
                "duration": 5.0,  # 5 segundos parado observando
                "description": "Segunda pausa - Observando outro ângulo",
                "movement_type": "static"  # Sem movimento
            },
            {
                "position": [-0.680, 0.090, 0.020],  # Sexto ponto
                "rotation": 2.712,  # 🎯 ROTAÇÃO FINAL: 155.4° (Sul)
                "animation": "WALKING",  # Animação de andar
                "duration": 5.0,  # Tempo para chegar lá
                "description": "Quarto movimento - Andando para Oeste/Norte",
                "movement_type": "smooth",  # Movimento suave
                "auto_face_while_moving": True  # 🔧 VIRA-SE DURANTE MOVIMENTO
            },
            {
                "position": [-0.680, 0.090, 0.020],  # Mesmo ponto (parado)
                "rotation": 2.712,  # Mantém rotação Sul
                "animation": "IDLE",  # Animação de olhar (parado)
                "duration": 5.0,  # 5 segundos parado observando
                "description": "Terceira pausa - Observação final",
                "movement_type": "static"  # Sem movimento
            },
            {
                "position": [-1.440, 0.090, 1.520],  # Ponto final
                "rotation": -0.238,  # 🎯 ROTAÇÃO FINAL: -13.6° (Norte)
                "animation": "WALKING",  # Animação de andar
                "duration": 4.0,  # Tempo para chegar lá
                "description": "Movimento final - Chegando ao destino",
                "movement_type": "smooth",  # Movimento suave
                "auto_face_while_moving": True 
            },
            {
                "position": [-1.440, 0.090, 1.520],  # Mesmo ponto (final)
                "rotation": -0.238,  # Mantém rotação Norte
                "animation": "IDLE",  # Animação de olhar (parado)
                "duration": 1.0,  # 3 segundos finais
                "description": "Posição final - Cena concluída",
                "movement_type": "static"  # Sem movimento
            }
        ]
        
        self.current_waypoint_index = 0
        self.waypoint_start_time = 0
        self.in_transition = False

        # 📷 SISTEMA DE CÂMERAS ESPECÍFICO DA SCENE01
        self.camera_keyframes = [
            {
                "position_start": [1.6, 0.9, 0.5],  # Close-up real capturado
                "position_end": [1.1, 0.9, 0.5],    # Se afasta para posição média
                "rotation": 1.519,  # 87.0° (olha diretamente para o humano)
                "duration": 4.0,     # 4 segundos
                "description": "Close-up inicial com zoom out real",
                "movement_type": "smooth_zoom_out"
            },
            {
                "position_start": [0.175, 0.405, 0.868],  # Posição real capturada
                "position_end": [0.175, 0.405, 0.868],    # Sem movimento (estática)
                "rotation": 0.567,  # 32.5° (olha diretamente para o humano)
                "duration": 19.0,   # 11 segundos
                "description": "Câmera média fixa - olhando humano",
                "movement_type": "static",
                "look_at_human": True 
            },
            {
                "position_start": [2.7, 0.900, -1.228],  # Posição real capturada para Câmera 3
                "position_end": [2.7, 0.900, -1.228],    # Sem movimento
                "rotation": -2.200,   # -126.0° (para olhar diretamente para o humano)
                "duration": 8.0,     # 8 segundos
                "description": "Câmera lateral direita - vista elevada",
                "movement_type": "static",
                "look_at_human": False
            },
            {
                "position_start": [2.687, 0.900, 1.407],   # Posição real capturada para Câmera 4
                "position_end": [2.687, 0.900, 1.407],     # Sem movimento
                "rotation": -1.180,   # -67.6° (para olhar diretamente para o humano)
                "duration": 12.0,    # 12 segundos
                "description": "Câmera lateral traseira - vista panorâmica",
                "movement_type": "static",
                "look_at_human": True
            },
            {
                "position_start": [-1.595, 0.814, 1.924],  # Posição real capturada para Câmera 5
                "position_end": [-1.595, 0.814, 1.924],    # Sem movimento
                "rotation": 0.366,   # 21.0° (para olhar diretamente para o humano)
                "duration": 3.0,     # 3 segundos finais
                "description": "Câmera final próxima - close-up final",
                "movement_type": "static",
                "look_at_human": False
            }
        ]
        
        # 📷 ESTADO ATUAL DA CÂMERA
        self.current_camera_keyframe = 0
        self.camera_keyframe_start_time = 0
        self.camera_system_active = False

        
    def get_duration(self):
        total_duration = sum(waypoint["duration"] for waypoint in self.waypoints)
        print(f"⏱️ Duração total calculada: {total_duration}s")
        return total_duration
    
    def initialize(self):
        print("🎵 Cena 1: Sala de Música - Levantando")
        print("⏱️ Duração: Infinita (modo teste)")
        
        # 🏠 ADICIONAR SALA DE MÚSICA
        if hasattr(self.scene_manager, 'sala_musica'):
            self.scene.add(self.scene_manager.sala_musica)
            print("✅ Sala de música adicionada à cena")
        else:
            print("❌ Sala de música não encontrada!")
        
        # 🎭 ADICIONAR HUMANO (primeiro frame de levantar)
        if hasattr(self.scene_manager, 'levantar_frames') and self.scene_manager.levantar_frames:
            self.scene_manager.humano = self.scene_manager.levantar_frames[0]
            
            # 🧪 POSIÇÃO INICIAL
            initial_position = [1.7, 0.09, 0.5]
            initial_rotation = -(math.pi / 2)

            # 🔧 1. APLICA TRANSFORMAÇÕES
            self.scene_manager.humano.set_position(initial_position)
            print(f"   ✅ Posição aplicada: {self.scene_manager.humano.local_position}")

            self.scene_manager.humano.set_rotation_y(initial_rotation)
            print(f"   ✅ Rotação aplicada")

            # 🔧 2. SINCRONIZA SCENE_MANAGER
            self.scene_manager.current_human_position = initial_position.copy()
            self.scene_manager.current_human_rotation = initial_rotation
            self.scene_manager.human_scene_reference = self.scene
            
            # 🔧 3. ADICIONA À CENA
            self.scene.add(self.scene_manager.humano)

            actual_pos = self.scene_manager.humano.local_position
            transform_matrix = self.scene_manager.humano.local_matrix
            
            print(f"✅ Humano adicionado:")
            print(f"   📍 Posição real após aplicação: [{actual_pos[0]:.3f}, {actual_pos[1]:.3f}, {actual_pos[2]:.3f}]")
            print(f"   🔍 Matriz [0,3]: {transform_matrix[0,3]:.3f}, [1,3]: {transform_matrix[1,3]:.3f}, [2,3]: {transform_matrix[2,3]:.3f}")
            
            
            # 🎮 ATIVA CONTROLES MANUAIS APENAS EM CÂMERA LIVRE
            if not self.scene_manager.free_camera_mode:
                self.start_camera_system()
                print("📷 Sistema de câmeras Scene01 iniciado")
            else:
                # Câmera livre - posição inicial próxima do humano
                if hasattr(self.scene_manager, 'camera_rig'):
                    self.scene_manager.camera_rig.set_position([1.5, 1.0, 1.5])
                    print("📷 Câmera livre posicionada próxima do humano")
            
        else:
            print("❌ Frames de levantar não encontrados!")
        
        # 📷 CONFIGURAR CÂMERA para visualizar a animação
        if not self.scene_manager.free_camera_mode:
            # Câmera automática - posição para ver o humano
            camera_position = [1.5, 1.0, 1.5]
            human_position = self.scene_manager.get_human_position()
            
            self.camera.set_position(camera_position)
            self.camera.look_at(human_position)
            
            print(f"📷 Câmera posicionada em: {camera_position}")
            print(f"👁️ Olhando para: {human_position}")
        else:
            # Câmera livre - posição inicial próxima do humano
            if hasattr(self.scene_manager, 'camera_rig'):
                self.scene_manager.camera_rig.set_position([1.5, 1.0, 1.5])
                print("📷 Câmera livre posicionada próxima do humano")
        
        print("🎬 Cena inicializada")
        # 🕰️ INICIALIZA TIMELINE DE WAYPOINTS
        self.waypoint_start_time = 0
        print(f"⏰ Waypoint timer iniciado - Duracao do waypoint 1: {self.waypoints[0]['duration']}s")

        print("🎵 Scene01 iniciada - música 'Drigsan - Code' já tocando")
        
        # 🔊 APENAS CARREGA EFEITOS SONOROS ESPECÍFICOS DA SCENE
        if self.scene_manager.audio_manager:
            # Exemplo: aplausos no final da performance
            print("🔊 Efeitos sonoros da sala de música carregados")
    
    def update(self, delta_time):
        # Verifica se a cena já foi finalizada
        if getattr(self, 'is_finished', False):
            return  # Para de processar se a cena terminou
        
        # Limite delta_time para evitar saltos grandes
        if delta_time > 0.1:
            delta_time = 0.1
        
        # Atualiza timeline
        self.manual_timeline += delta_time * self.time_scale
        
        # 📷 ATUALIZA SISTEMA DE CÂMERAS (apenas modo automático)
        if not self.scene_manager.free_camera_mode:
            self.update_camera_system(delta_time)
        
        # 🎭 ANIMAÇÃO AUTOMÁTICA só roda se controles desativados ou câmera automática
        should_animate = (not self.scene_manager.manual_control_enabled or 
                         not self.scene_manager.free_camera_mode)
        
        if should_animate:
            self._update_animation_state()

        if self.manual_timeline > 20.0 and not hasattr(self, 'played_applause'):
            if self.scene_manager.audio_manager:
                self.scene_manager.audio_manager.play_sound("aplausos", volume=0.6)
                print("👏 Aplausos reproduzidos")
            self.played_applause = True
        
        # 📊 MOSTRA PROGRESSO (menos frequente)
        if int(self.manual_timeline) % 5 == 0 and int(self.manual_timeline) != getattr(self, 'last_logged_time', -1):
            self.last_logged_time = int(self.manual_timeline)
            
            status = self._get_current_status()
            
            if self.scene_manager.manual_control_enabled and self.scene_manager.free_camera_mode:
                print(f"⏰ {int(self.manual_timeline)}s - Modo controle manual ativo")
            else:
                print(f"⏰ {int(self.manual_timeline)}s - {status}")

    def _get_current_status(self):
        """Retorna status atual baseado no waypoint e estado"""
        waypoint_info = self.get_current_waypoint_info()
        
        if waypoint_info:
            base_status = {
                "WAITING": "Aguardando início",
                "STANDING": "Levantando",
                "WALKING": "Caminhando",
                "IDLE": "Parado observando"
            }.get(self.animation_state, "Estado desconhecido")
            
            waypoint_status = (f"Waypoint {waypoint_info['index']}/{waypoint_info['total']} - "
                              f"{base_status} ({waypoint_info['time_remaining']:.1f}s restantes)")
            
            # Adiciona status da câmera em modo automático
            if not self.scene_manager.free_camera_mode and self.camera_system_active:
                camera_status = self.get_camera_system_status()
                return f"{waypoint_status} | {camera_status}"
            else:
                return waypoint_status
        
        return "Sistema de waypoints não inicializado"

    def _update_animation_state(self):
        """Máquina de estados com sistema de waypoints"""
        
        # 🗺️ VERIFICA SE DEVE AVANÇAR PARA PRÓXIMO WAYPOINT
        current_waypoint = self.waypoints[self.current_waypoint_index]
        
        # Calcula tempo no waypoint atual
        time_in_waypoint = self.manual_timeline - self.waypoint_start_time
        
        # 🔄 TRANSIÇÃO PARA PRÓXIMO WAYPOINT
        if time_in_waypoint >= current_waypoint["duration"] and not self.in_transition:
            self._advance_to_next_waypoint()
            return
        
        # 🎭 EXECUTA ANIMAÇÃO DO WAYPOINT ATUAL
        target_animation = current_waypoint["animation"]
        
        if self.animation_state != target_animation and not self.in_transition:
            self._transition_to_animation(target_animation)
        
        # Executa animação atual
        if self.animation_state == "WAITING":
            self._animate_waiting()
        elif self.animation_state == "STANDING":
            self._animate_standing()
        elif self.animation_state == "WALKING":
            self._animate_walking()
        elif self.animation_state == "IDLE":
            self._animate_idle()
    
    def _animate_waiting(self):
        """Estado 1: Mantém no frame 0"""
        if self.frame_index != 0:
            self.frame_index = 0
            self._switch_to_frame('levantar_frames', 0)
    
    def _animate_standing(self):
        """Estado 2: 5s no frame 0, depois continua frames 1-13"""
        if not hasattr(self.scene_manager, 'levantar_frames'):
            return
        
        # 🕰️ CALCULA TEMPO NO WAYPOINT ATUAL
        time_in_waypoint = self.manual_timeline - self.waypoint_start_time
        
        # 🔧 FASE 1: 0-5s fica no frame 0 (SEM PRINT REPETIDO)
        if time_in_waypoint < 6.0:
            if self.frame_index != 0:
                self.frame_index = 0
                self._switch_to_frame('levantar_frames', 0)
                print("📍 STANDING: Esperando 5s no frame 0...")
            return  # Para aqui, não faz mais nada
        
        # 🔧 FASE 2: Após 5s, continua animação
        if time_in_waypoint >= 6.0 and not hasattr(self, 'animation_phase_started'):
            self.animation_phase_started = True
            print("🎬 Iniciando fase de animação após 5s...")
        
        self.frame_count += 1
        frame_speed = 10
        
        if self.frame_count >= frame_speed:
            self.frame_count = 0
            
            if self.frame_index < len(self.scene_manager.levantar_frames) - 1:
                self.frame_index += 1
                self._switch_to_frame('levantar_frames', self.frame_index)
                print(f"📽️ Levantar Frame {self.frame_index + 1}/{len(self.scene_manager.levantar_frames)}")
            else:
                print("✅ Animação de levantar concluída!")

    def _animate_walking(self):
        """Estado 3: Loop infinito de andar"""
        if not hasattr(self.scene_manager, 'andar_frames'):
            print("❌ Frames de andar não encontrados!")
            # Fallback para IDLE se não tiver frames de andar
            self.animation_state = "IDLE"
            return
        
        self.frame_count += 1
        frame_speed = 6  # Velocidade do andar
        
        if self.frame_count >= frame_speed:
            self.frame_count = 0
            
            # Loop infinito dos frames de andar
            current_frame = self.frame_index % len(self.scene_manager.andar_frames)
            self._switch_to_frame('andar_frames', current_frame)
            print(f"🚶 Andar Frame {current_frame + 1}/{len(self.scene_manager.andar_frames)}")
            
            self.frame_index += 1

    def _animate_idle(self):
        """Estado 4: Loop infinito de olhar (parado)"""
        if not hasattr(self.scene_manager, 'olhar_frames'):
            print("❌ Frames de olhar não encontrados!")
            return
        
        self.frame_count += 1
        frame_speed = 8  # Velocidade do olhar
        
        if self.frame_count >= frame_speed:
            self.frame_count = 0
            
            # Loop infinito dos frames de olhar
            current_frame = self.frame_index % len(self.scene_manager.olhar_frames)
            self._switch_to_frame('olhar_frames', current_frame)
            print(f"👀 Olhar Frame {current_frame + 1}/{len(self.scene_manager.olhar_frames)}")
            
            self.frame_index += 1

    def _switch_to_frame(self, frames_attr, frame_index):
        """Utilitário para trocar frames removendo o antigo corretamente"""
        frames = getattr(self.scene_manager, frames_attr, None)
        if not frames or frame_index >= len(frames):
            return
        
        new_humano = frames[frame_index]
        
        # Se é o mesmo frame, não faz nada
        if self.scene_manager.humano == new_humano:
            return
        
        # 🔧 REMOVE HUMANO ANTIGO DA SCENE (se existir)
        if self.scene_manager.humano:
            try:
                self.scene.remove(self.scene_manager.humano)
                print(f"🗑️ Humano antigo removido da scene")
            except:
                print("⚠️ Humano antigo não estava na scene")
        
        # 🔧 ATUALIZA REFERÊNCIA
        self.scene_manager.humano = new_humano
        self.scene_manager.human_scene_reference = self.scene
        
        # 🔧 APLICA POSIÇÃO E ROTAÇÃO
        current_pos = self.scene_manager.get_human_position()
        current_rot = self.scene_manager.get_human_rotation()
        
        new_humano.set_position(current_pos)
        new_humano.set_rotation_y(current_rot)
        
        # 🔧 ADICIONA NOVO HUMANO
        self.scene.add(new_humano)
        print(f"✅ Novo humano adicionado à scene")

    def force_state_transition(self, new_state):
        """Método para forçar transição de estado (útil para testes)"""
        valid_states = ["WAITING", "STANDING", "WALKING", "IDLE"]
        if new_state in valid_states:
            old_state = self.animation_state
            self.animation_state = new_state
            self.frame_index = 0
            self.frame_count = 0
            print(f"🔄 Transição forçada: {old_state} → {new_state}")
        else:
            print(f"❌ Estado inválido: {new_state}. Use: {valid_states}")

    def sync_human_with_scene_manager(self):
        """Força sincronização do humano atual com scene_manager"""
        if hasattr(self, 'scene_manager') and self.scene_manager.humano:
            # Garante que o scene_manager tem a referência correta
            current_pos = self.scene_manager.get_human_position()
            current_rot = self.scene_manager.get_human_rotation()
            
            # Aplica posição/rotação no humano atual
            self.scene_manager.humano.set_position(current_pos)
            self.scene_manager.humano.set_rotation_y(current_rot)
            
            print(f"🔗 Humano sincronizado com scene_manager")
            print(f"   📍 Posição: {current_pos}")
            print(f"   🔄 Rotação: {current_rot:.3f} rad")

    def _advance_to_next_waypoint(self):
        """Avança para o próximo waypoint com tipo de movimento apropriado"""
        
        # 🔧 LIMPA VARIÁVEIS DO ESTADO ANTERIOR
        if hasattr(self, 'animation_phase_started'):
            delattr(self, 'animation_phase_started')
        
        if self.current_waypoint_index < len(self.waypoints) - 1:
            self.current_waypoint_index += 1
            self.waypoint_start_time = self.manual_timeline
            
            next_waypoint = self.waypoints[self.current_waypoint_index]
            
            print(f"🗺️ WAYPOINT {self.current_waypoint_index + 1}/{len(self.waypoints)}")
            print(f"   📍 Nova posição: {next_waypoint['position']}")
            print(f"   🔄 Nova rotação: {next_waypoint['rotation']:.3f} rad")
            print(f"   🎭 Animação: {next_waypoint['animation']}")
            print(f"   ⏱️ Duração: {next_waypoint['duration']}s")
            print(f"   📝 Descrição: {next_waypoint['description']}")
            print(f"   🚶 Movimento: {next_waypoint['movement_type']}")
            
            # 🚶 EXECUTA MOVIMENTO BASEADO NO TIPO
            movement_type = next_waypoint.get("movement_type", "teleport")
            
            if movement_type == "smooth":
                # Movimento suave interpolado
                def on_movement_complete():
                    print("✅ Movimento suave concluído!")
                
                # 🧭 VERIFICA CONFIGURAÇÕES DE ROTAÇÃO
                target_rotation = next_waypoint["rotation"]
                auto_face = next_waypoint.get("auto_face_while_moving", False)
                
                print(f"🔧 Configuração de rotação:")
                print(f"   🎯 Rotação final: {target_rotation:.3f} rad")
                print(f"   🧭 Auto-virar durante movimento: {auto_face}")
                
                success = self.scene_manager.start_movement_to(
                    target_position=next_waypoint["position"],
                    target_rotation=target_rotation,
                    duration=next_waypoint["duration"],
                    callback=on_movement_complete,
                    auto_face_while_moving=auto_face
                )
                
                if success:
                    print("🚶 Iniciando movimento bifásico...")
                else:
                    print("❌ Falha ao iniciar movimento - usando teletransporte")
                    self._move_to_waypoint(next_waypoint)
            
            else:
                # Teletransporte tradicional
                self._move_to_waypoint(next_waypoint)
            
        else:
            # 🎬 FINALIZA A CENA QUANDO TODOS OS WAYPOINTS TERMINAM
            print(f"🎬 TODOS OS WAYPOINTS CONCLUÍDOS!")
            print(f"   📍 Posição final: {self.scene_manager.get_human_position()}")
            print(f"   🔄 Rotação final: {self.scene_manager.get_human_rotation():.3f} rad")
            print(f"   ⏱️ Tempo total: {self.manual_timeline:.1f}s")
            print(f"🎭 CENA 1 FINALIZADA - Transicionando para próxima cena...")
            
            # 🗑️ REMOVE HUMANO DA CENA
            if self.scene_manager.humano:
                self.scene.remove(self.scene_manager.humano)
            
            # 🏠 REMOVE SALA DE MÚSICA DA CENA
            if hasattr(self.scene_manager, 'sala_musica') and self.scene_manager.sala_musica:
                self.scene.remove(self.scene_manager.sala_musica)
            
            # 🔧 LIMPA REFERÊNCIAS
            self.scene_manager.humano = None
            self.scene_manager.human_scene_reference = None
            
            # Marca a cena como finalizada
            self.is_finished = True

    def _move_to_waypoint(self, waypoint):
        """Move o humano para um waypoint específico"""
        target_pos = waypoint["position"]
        target_rot = waypoint["rotation"]
        
        # Atualiza posição no scene_manager
        self.scene_manager.current_human_position = target_pos.copy()
        self.scene_manager.current_human_rotation = target_rot
        
        # Aplica transformação no humano atual
        if self.scene_manager.humano:
            self.scene_manager.humano.set_position(target_pos)
            self.scene_manager.humano.set_rotation_y(target_rot)
            
            print(f"✅ Humano movido para waypoint:")
            print(f"   📍 Posição: {target_pos}")
            print(f"   🔄 Rotação: {target_rot:.3f} rad")

    def _transition_to_animation(self, target_animation):
      """Faz transição para nova animação"""
      old_animation = self.animation_state
      self.animation_state = target_animation
      
      # 🔧 SEMPRE RESET FRAME_COUNT E FRAME_INDEX
      self.frame_count = 0
      self.frame_index = 0
      
      print(f"🎬 Transição animação: {old_animation} → {target_animation}")

    def get_current_waypoint_info(self):
        """Retorna informações do waypoint atual"""
        if self.current_waypoint_index < len(self.waypoints):
            waypoint = self.waypoints[self.current_waypoint_index]
            time_in_waypoint = self.manual_timeline - self.waypoint_start_time
            remaining_time = waypoint["duration"] - time_in_waypoint
            
            return {
                "index": self.current_waypoint_index + 1,
                "total": len(self.waypoints),
                "description": waypoint["description"],
                "animation": waypoint["animation"],
                "time_elapsed": time_in_waypoint,
                "time_remaining": max(0, remaining_time),
                "duration": waypoint["duration"]
            }
        return None

    def add_waypoint(self, position, rotation, animation="IDLE", duration=5.0, description="Waypoint personalizado"):
        """Adiciona um novo waypoint dinamicamente"""
        waypoint = {
            "position": position.copy(),
            "rotation": rotation,
            "animation": animation,
            "duration": duration,
            "description": description
        }
        self.waypoints.append(waypoint)
        print(f"➕ Waypoint adicionado: {description}")
        print(f"   📍 Posição: {position}")
        print(f"   🎭 Animação: {animation} por {duration}s")
    
    def start_camera_system(self):
        """Inicia o sistema de câmeras automáticas da Scene01"""
        if not self.scene_manager.free_camera_mode:
            self.camera_system_active = True
            self.current_camera_keyframe = 0
            self.camera_keyframe_start_time = 0
            
            # Inicia primeira câmera
            first_keyframe = self.camera_keyframes[0]
            self.camera.set_position(first_keyframe["position_start"])
            self._set_camera_rotation(first_keyframe["rotation"])
            
            print("📷 SISTEMA DE CÂMERAS SCENE01 INICIADO")
            print(f"   🎬 Keyframe 1/5: {first_keyframe['description']}")
            print(f"   📍 Posição inicial: {first_keyframe['position_start']}")
            print(f"   🔄 Rotação: {first_keyframe['rotation']:.3f} rad ({first_keyframe['rotation'] * 180 / math.pi:.1f}°)")
            print(f"   ⏱️ Duração: {first_keyframe['duration']}s")
        else:
            print("📷 Sistema de câmeras ignorado - modo livre ativo")

    def _set_camera_rotation(self, rotation_y):
        """Define rotação da câmera usando apenas Y (yaw)"""
        # Converte rotação Y para direção de olhar
        import math
        
        # Calcula direção baseada na rotação Y
        direction_x = math.sin(rotation_y)
        direction_z = -math.cos(rotation_y)  # -cos porque Z negativo é "frente"
        
        # Posição atual da câmera
        camera_pos = self.camera.local_position
        
        # Ponto para onde olhar (1 unidade na direção calculada)
        look_at_point = [
            camera_pos[0] + direction_x,
            camera_pos[1],  # Mantém altura atual
            camera_pos[2] + direction_z
        ]
        
        # Aplica look_at
        self.camera.look_at(look_at_point)
        
        print(f"   🎯 Câmera olhando para direção: [{direction_x:.3f}, 0, {direction_z:.3f}]")

    def update_camera_system(self, delta_time):
        """Atualiza sistema de câmeras automáticas da Scene01"""
        if not self.camera_system_active or self.scene_manager.free_camera_mode:
            return
        
        # Verifica se deve avançar para próximo keyframe
        current_keyframe = self.camera_keyframes[self.current_camera_keyframe]
        time_in_keyframe = self.manual_timeline - self.camera_keyframe_start_time
        
        if time_in_keyframe >= current_keyframe["duration"]:
            self._advance_to_next_camera_keyframe()
            return
        
        # Atualiza posição da câmera baseado no tipo de movimento
        self._update_current_camera_keyframe(time_in_keyframe)

    def _update_current_camera_keyframe(self, time_in_keyframe):
        """Atualiza posição da câmera no keyframe atual"""
        current_keyframe = self.camera_keyframes[self.current_camera_keyframe]
        movement_type = current_keyframe["movement_type"]
        
        if movement_type == "smooth_zoom_out":
            # Movimento suave de zoom out (primeira câmera)
            progress = time_in_keyframe / current_keyframe["duration"]
            progress = min(1.0, progress)  # Limita a 1.0
            
            # 🎬 CURVA SUAVE (ease-out) para movimento mais cinematográfico
            smooth_progress = 1 - (1 - progress) ** 2
            
            # Interpolação linear entre posição inicial e final
            start_pos = current_keyframe["position_start"]
            end_pos = current_keyframe["position_end"]
            
            current_pos = [
                start_pos[0] + (end_pos[0] - start_pos[0]) * smooth_progress,
                start_pos[1] + (end_pos[1] - start_pos[1]) * smooth_progress,
                start_pos[2] + (end_pos[2] - start_pos[2]) * smooth_progress
            ]
            
            self.camera.set_position(current_pos)
            
            # 🎯 SEMPRE OLHA PARA O HUMANO DURANTE ZOOM OUT (COM ALTURA AJUSTADA)
            if self.scene_manager.humano:
                human_pos = self.scene_manager.get_human_position()
                
                # 📏 AJUSTA ALTURA DO PONTO DE FOCO (olha mais para cima)
                look_at_target = [
                    human_pos[0],
                    human_pos[1] + 0.4,  
                    human_pos[2]
                ]
                
                self.camera.look_at(look_at_target)
                
                # Debug da câmera (apenas a cada 0.5s)
                if int(time_in_keyframe * 2) != getattr(self, 'last_zoom_debug', -1):
                    self.last_zoom_debug = int(time_in_keyframe * 2)
                    distance = ((current_pos[0] - human_pos[0])**2 + 
                              (current_pos[1] - human_pos[1])**2 + 
                              (current_pos[2] - human_pos[2])**2) ** 0.5
                    print(f"📷 Zoom out: {progress:.1%} | Distância: {distance:.2f}m | Foco: [{look_at_target[0]:.2f}, {look_at_target[1]:.2f}, {look_at_target[2]:.2f}]")
            else:
                # Fallback: usa rotação fixa se humano não encontrado
                self._set_camera_rotation(current_keyframe["rotation"])
            
        elif movement_type == "static":
            # Câmera estática - mantém posição fixa
            self.camera.set_position(current_keyframe["position_start"])
            
            # 🎯 VERIFICA SE DEVE OLHAR PARA O HUMANO CONTINUAMENTE
            if current_keyframe.get("look_at_human", False):
                # Sempre atualiza look_at para seguir o humano em movimento
                if self.scene_manager.humano:
                    human_pos = self.scene_manager.get_human_position()
                    
                    # 📏 AJUSTA ALTURA DO PONTO DE FOCO (olha mais para cima)
                    look_at_target = [
                        human_pos[0],
                        human_pos[1] + 0.4,
                        human_pos[2]
                    ]
                    
                    self.camera.look_at(look_at_target)
                    
                    # Debug a cada 2 segundos para câmeras que seguem humano
                    if int(time_in_keyframe) % 2 == 0 and int(time_in_keyframe) != getattr(self, 'last_static_debug', -1):
                        self.last_static_debug = int(time_in_keyframe)
                        camera_pos = self.camera.get_position() if hasattr(self.camera, 'get_position') else current_keyframe["position_start"]
                        distance = ((camera_pos[0] - human_pos[0])**2 + 
                                  (camera_pos[1] - human_pos[1])**2 + 
                                  (camera_pos[2] - human_pos[2])**2) ** 0.5
                        print(f"📷 Câmera seguindo humano | Dist: {distance:.2f}m | Foco: [{look_at_target[0]:.2f}, {look_at_target[1]:.2f}, {look_at_target[2]:.2f}]")
                else:
                    # Fallback para rotação fixa
                    self._set_camera_rotation(current_keyframe["rotation"])
            else:
                # Câmera com rotação fixa (não segue humano)
                self._set_camera_rotation(current_keyframe["rotation"])

    def _advance_to_next_camera_keyframe(self):
        """Avança para o próximo keyframe de câmera"""
        if self.current_camera_keyframe < len(self.camera_keyframes) - 1:
            self.current_camera_keyframe += 1
            self.camera_keyframe_start_time = self.manual_timeline
            
            next_keyframe = self.camera_keyframes[self.current_camera_keyframe]
            
            print(f"📷 MUDANÇA DE CÂMERA:")
            print(f"   🎬 Keyframe {self.current_camera_keyframe + 1}/5: {next_keyframe['description']}")
            print(f"   📍 Nova posição: {next_keyframe['position_start']}")
            print(f"   🔄 Nova rotação: {next_keyframe['rotation']:.3f} rad ({next_keyframe['rotation'] * 180 / math.pi:.1f}°)")
            print(f"   ⏱️ Duração: {next_keyframe['duration']}s")
            
            # Define posição inicial do novo keyframe
            self.camera.set_position(next_keyframe["position_start"])
            
            # 🎯 VERIFICA SE É CÂMERA QUE SEGUE HUMANO
            if next_keyframe.get("look_at_human", False):
                if self.scene_manager.humano:
                    human_pos = self.scene_manager.get_human_position()
                    
                    # 📏 AJUSTA ALTURA DO PONTO DE FOCO (olha mais para cima)
                    look_at_target = [
                        human_pos[0],
                        human_pos[1] + 0.8,  # +0.8m para olhar para a cabeça/peito
                        human_pos[2]
                    ]
                    
                    self.camera.look_at(look_at_target)
                    
                    # Calcula distância inicial
                    camera_pos = next_keyframe["position_start"]
                    distance = ((camera_pos[0] - human_pos[0])**2 + 
                              (camera_pos[1] - human_pos[1])**2 + 
                              (camera_pos[2] - human_pos[2])**2) ** 0.5
                    
                    print(f"   🎯 Câmera configurada para seguir humano (altura ajustada)")
                    print(f"   📏 Distância inicial: {distance:.2f}m")
                    print(f"   📍 Humano em: [{human_pos[0]:.3f}, {human_pos[1]:.3f}, {human_pos[2]:.3f}]")
                    print(f"   🎯 Foco ajustado: [{look_at_target[0]:.3f}, {look_at_target[1]:.3f}, {look_at_target[2]:.3f}]")
                else:
                    # Fallback para rotação fixa
                    self._set_camera_rotation(next_keyframe["rotation"])
                    print(f"   ⚠️ Humano não encontrado - usando rotação fixa")
            else:
                # Câmera com rotação fixa
                self._set_camera_rotation(next_keyframe["rotation"])
                
        else:
            print("📷 SISTEMA DE CÂMERAS SCENE01 CONCLUÍDO")
            self.camera_system_active = False

    def get_camera_system_status(self):
        """Retorna status atual do sistema de câmeras"""
        if not self.camera_system_active:
            return "Sistema de câmeras inativo"
        
        current_keyframe = self.camera_keyframes[self.current_camera_keyframe]
        time_in_keyframe = self.manual_timeline - self.camera_keyframe_start_time
        remaining_time = current_keyframe["duration"] - time_in_keyframe
        
        return (f"Câmera {self.current_camera_keyframe + 1}/5 - "
                f"{current_keyframe['description']} "
                f"({remaining_time:.1f}s restantes)")