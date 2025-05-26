import time

class MusicTimeline:
    """Sistema de timeline musical - define música por intervalos de tempo"""
    
    def __init__(self, audio_manager):
        self.audio_manager = audio_manager
        
        # 🎵 TIMELINE DE MÚSICA
        self.music_timeline = []
        self.current_timeline_index = 0
        self.timeline_start_time = 0.0
        self.timeline_active = False
        
        # 🔧 CONTROLE
        self.last_music_change = 0.0
        self.fade_duration = 2.0  # Tempo de fade entre músicas
        
    def set_timeline(self, timeline_config):
        """Define timeline de música
        
        Formato:
        [
            {"start": 0, "end": 20, "music": "drigsan_code", "volume": 0.7, "loop": True},
            {"start": 25, "end": 40, "music": "happy", "volume": 0.8, "loop": True},
            {"start": 45, "end": 60, "music": None, "volume": 0.0, "loop": False},  # Silêncio
        ]
        """
        self.music_timeline = timeline_config.copy()
        self.music_timeline.sort(key=lambda x: x["start"])  # Ordena por tempo de início
        
        print(f"🎵 TIMELINE MUSICAL CONFIGURADA:")
        for i, entry in enumerate(self.music_timeline):
            music_name = entry["music"] or "SILÊNCIO"
            print(f"   {i+1}. {entry['start']:3d}s - {entry['end']:3d}s: {music_name}")
        
    def start_timeline(self):
        """Inicia timeline musical"""
        if not self.music_timeline:
            print("❌ Timeline musical não configurada")
            return False
        
        self.timeline_start_time = time.time()
        self.timeline_active = True
        self.current_timeline_index = 0
        
        print(f"🎵 TIMELINE MUSICAL INICIADA")
        
        # Inicia primeira música se existir
        first_entry = self.music_timeline[0]
        if first_entry["start"] == 0 and first_entry["music"]:
            self._play_timeline_music(first_entry)
        
        return True
    
    def update(self, manual_timeline=None):
        """Atualiza timeline musical baseado no tempo
        
        Args:
            manual_timeline: Se fornecido, usa este tempo em vez do tempo real
        """
        if not self.timeline_active or not self.music_timeline:
            return
        
        # 🕐 CALCULA TEMPO ATUAL
        if manual_timeline is not None:
            current_time = manual_timeline
        else:
            current_time = time.time() - self.timeline_start_time
        
        # 🔍 ENCONTRA ENTRADA ATUAL DA TIMELINE
        target_entry = None
        target_index = -1
        
        for i, entry in enumerate(self.music_timeline):
            if entry["start"] <= current_time < entry["end"]:
                target_entry = entry
                target_index = i
                break
        
        # 🎵 VERIFICA SE PRECISA MUDAR MÚSICA
        if target_index != self.current_timeline_index:
            self.current_timeline_index = target_index
            
            if target_entry:
                print(f"🎵 MUDANÇA DE MÚSICA aos {current_time:.1f}s:")
                print(f"   ⏰ Intervalo: {target_entry['start']}s - {target_entry['end']}s")
                print(f"   🎶 Música: {target_entry['music'] or 'SILÊNCIO'}")
                
                self._play_timeline_music(target_entry)
            else:
                # Fora de qualquer intervalo - silêncio
                print(f"🔇 SILÊNCIO aos {current_time:.1f}s - fora dos intervalos")
                self._stop_current_music()
    
    def _play_timeline_music(self, entry):
        """Reproduz música de uma entrada da timeline"""
        if not entry["music"]:
            # Entrada de silêncio
            self._stop_current_music()
            return
        
        # Para música atual se estiver tocando
        if self.audio_manager.is_music_playing:
            self.audio_manager.stop_music(fade_out_time=self.fade_duration)
        
        # Define volume
        if "volume" in entry:
            self.audio_manager.set_music_volume(entry["volume"])
        
        # Inicia nova música
        loop = entry.get("loop", True)
        fade_in = entry.get("fade_in", self.fade_duration)
        
        success = self.audio_manager.play_music(
            entry["music"], 
            loop=loop, 
            fade_in_time=fade_in
        )
        
        if success:
            print(f"✅ Música '{entry['music']}' iniciada com volume {entry.get('volume', 'padrão')}")
        else:
            print(f"❌ Erro ao iniciar música '{entry['music']}'")
    
    def _stop_current_music(self):
        """Para música atual com fade-out"""
        if self.audio_manager.is_music_playing:
            self.audio_manager.stop_music(fade_out_time=self.fade_duration)
            print(f"🔇 Música parada com fade-out de {self.fade_duration}s")
    
    def stop_timeline(self):
        """Para timeline musical"""
        self.timeline_active = False
        self._stop_current_music()
        print("⏹️ Timeline musical parada")
    
    def pause_timeline(self):
        """Pausa timeline musical"""
        self.timeline_active = False
        self.audio_manager.pause_music()
        print("⏸️ Timeline musical pausada")
    
    def resume_timeline(self):
        """Resume timeline musical"""
        self.timeline_active = True
        self.audio_manager.resume_music()
        print("▶️ Timeline musical resumida")
    
    def get_current_entry(self, manual_timeline=None):
        """Retorna entrada atual da timeline"""
        if manual_timeline is not None:
            current_time = manual_timeline
        else:
            current_time = time.time() - self.timeline_start_time if self.timeline_active else 0
        
        for entry in self.music_timeline:
            if entry["start"] <= current_time < entry["end"]:
                return entry
        
        return None
    
    def set_fade_duration(self, seconds):
        """Define duração dos fades entre músicas"""
        self.fade_duration = seconds
        print(f"🎚️ Duração de fade configurada: {seconds}s")
    
    def debug_timeline_status(self, manual_timeline=None):
        """Debug do status atual da timeline"""
        if manual_timeline is not None:
            current_time = manual_timeline
        else:
            current_time = time.time() - self.timeline_start_time if self.timeline_active else 0
        
        print(f"\n🎵 DEBUG TIMELINE MUSICAL:")
        print(f"   ⏰ Tempo atual: {current_time:.1f}s")
        print(f"   🎯 Ativa: {self.timeline_active}")
        print(f"   🔢 Índice atual: {self.current_timeline_index}")
        
        current_entry = self.get_current_entry(manual_timeline)
        if current_entry:
            print(f"   🎶 Música atual: {current_entry['music'] or 'SILÊNCIO'}")
            print(f"   📊 Intervalo: {current_entry['start']}s - {current_entry['end']}s")
            remaining = current_entry['end'] - current_time
            print(f"   ⏳ Tempo restante: {remaining:.1f}s")
        else:
            print(f"   🔇 Fora de qualquer intervalo")
        
        print(f"   🎚️ Volume música: {self.audio_manager.music_volume:.1f}")
        print(f"   🔊 Tocando: {self.audio_manager.is_music_playing}")