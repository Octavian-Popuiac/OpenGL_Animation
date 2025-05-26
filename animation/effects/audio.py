import pygame
import os
import threading
import time

class AudioManager:
    """Sistema de gerenciamento de áudio para o projeto"""
    
    def __init__(self):
        """Inicializa o sistema de áudio"""
        self.initialized = False
        self.current_music = None
        self.music_volume = 0.7  # Volume da música (0.0 - 1.0)
        self.sfx_volume = 0.8    # Volume dos efeitos sonoros
        self.master_volume = 1.0 # Volume geral
        
        # 🎵 CANAIS DE SOM
        self.music_channel = None
        self.sfx_channels = []
        
        # 📂 CACHE DE SONS CARREGADOS
        self.loaded_sounds = {}
        self.loaded_music = {}
        
        # 🎬 CONTROLE DE REPRODUÇÃO
        self.is_music_playing = False
        self.current_music_file = None
        self.music_position = 0.0
        
        # 🔄 SISTEMA DE FADE
        self.fade_thread = None
        self.fade_active = False
        
        self._initialize_pygame_audio()

    def _initialize_pygame_audio(self):
        """Inicializa o sistema de áudio do pygame"""
        try:
            # 🎵 INICIALIZA PYGAME MIXER
            pygame.mixer.pre_init(
                frequency=44100,    # Taxa de amostragem
                size=-16,           # 16-bit signed
                channels=2,         # Estéreo
                buffer=512          # Buffer pequeno para baixa latência
            )
            pygame.mixer.init()
            
            # 🎵 CONFIGURA CANAIS
            pygame.mixer.set_num_channels(8)  # 8 canais para efeitos
            
            self.initialized = True
            print("🎵 AudioManager inicializado com sucesso")
            print(f"   📊 Frequency: {pygame.mixer.get_init()[0]} Hz")
            print(f"   📊 Channels: {pygame.mixer.get_init()[2]}")
            print(f"   📊 Buffer: {pygame.mixer.get_init()[1]} bytes")
            
        except Exception as e:
            print(f"❌ Erro ao inicializar áudio: {e}")
            self.initialized = False

    def load_music(self, file_path, name=None):
        """Carrega música de fundo"""
        if not self.initialized:
            print("❌ Sistema de áudio não inicializado")
            return False
        
        try:
            # 📂 VERIFICA SE ARQUIVO EXISTE
            full_path = self._get_audio_path(file_path)
            if not os.path.exists(full_path):
                print(f"❌ Arquivo não encontrado: {full_path}")
                return False
            
            # 🎵 CARREGA MÚSICA
            pygame.mixer.music.load(full_path)
            
            music_name = name or os.path.basename(file_path)
            self.loaded_music[music_name] = {
                "file_path": full_path,
                "name": music_name
            }
            
            print(f"🎵 Música carregada: {music_name}")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao carregar música {file_path}: {e}")
            return False

    def play_music(self, file_path_or_name, loop=True, fade_in_time=0.0):
        """Reproduz música de fundo"""
        if not self.initialized:
            print("❌ Sistema de áudio não inicializado")
            return False
        
        try:
            # 🔍 ENCONTRA MÚSICA
            music_info = None
            
            # Tenta por nome primeiro
            if file_path_or_name in self.loaded_music:
                music_info = self.loaded_music[file_path_or_name]
            else:
                # Tenta carregar arquivo diretamente
                if self.load_music(file_path_or_name):
                    music_name = os.path.basename(file_path_or_name)
                    music_info = self.loaded_music[music_name]
            
            if not music_info:
                print(f"❌ Música não encontrada: {file_path_or_name}")
                return False
            
            # 🎵 PARA MÚSICA ATUAL SE ESTIVER TOCANDO
            if self.is_music_playing:
                pygame.mixer.music.stop()
            
            # 🎵 CONFIGURA VOLUME
            pygame.mixer.music.set_volume(self.music_volume * self.master_volume)
            
            # 🎵 REPRODUZ MÚSICA
            loops = -1 if loop else 0  # -1 = loop infinito
            
            if fade_in_time > 0:
                pygame.mixer.music.play(loops, fade_ms=int(fade_in_time * 1000))
                print(f"🎵 Música iniciada com fade-in: {music_info['name']} ({fade_in_time}s)")
            else:
                pygame.mixer.music.play(loops)
                print(f"🎵 Música iniciada: {music_info['name']}")
            
            self.is_music_playing = True
            self.current_music_file = music_info['name']
            
            return True
            
        except Exception as e:
            print(f"❌ Erro ao reproduzir música: {e}")
            return False

    def load_sound(self, file_path, name=None):
        """Carrega efeito sonoro"""
        if not self.initialized:
            print("❌ Sistema de áudio não inicializado")
            return False
        
        try:
            # 📂 VERIFICA SE ARQUIVO EXISTE
            full_path = self._get_audio_path(file_path)
            if not os.path.exists(full_path):
                print(f"❌ Arquivo não encontrado: {full_path}")
                return False
            
            # 🔊 CARREGA SOM
            sound = pygame.mixer.Sound(full_path)
            
            sound_name = name or os.path.basename(file_path)
            self.loaded_sounds[sound_name] = {
                "sound": sound,
                "file_path": full_path,
                "name": sound_name
            }
            
            print(f"🔊 Som carregado: {sound_name}")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao carregar som {file_path}: {e}")
            return False

    def play_sound(self, file_path_or_name, volume=1.0, loop=False):
        """Reproduz efeito sonoro"""
        if not self.initialized:
            print("❌ Sistema de áudio não inicializado")
            return False
        
        try:
            # 🔍 ENCONTRA SOM
            sound_info = None
            
            # Tenta por nome primeiro
            if file_path_or_name in self.loaded_sounds:
                sound_info = self.loaded_sounds[file_path_or_name]
            else:
                # Tenta carregar arquivo diretamente
                if self.load_sound(file_path_or_name):
                    sound_name = os.path.basename(file_path_or_name)
                    sound_info = self.loaded_sounds[sound_name]
            
            if not sound_info:
                print(f"❌ Som não encontrado: {file_path_or_name}")
                return False
            
            # 🔊 CONFIGURA VOLUME
            sound = sound_info["sound"]
            sound.set_volume(volume * self.sfx_volume * self.master_volume)
            
            # 🔊 REPRODUZ SOM
            loops = -1 if loop else 0
            channel = sound.play(loops)
            
            if channel:
                print(f"🔊 Som reproduzido: {sound_info['name']}")
                return True
            else:
                print(f"⚠️ Todos os canais ocupados para: {sound_info['name']}")
                return False
            
        except Exception as e:
            print(f"❌ Erro ao reproduzir som: {e}")
            return False

    def stop_music(self, fade_out_time=0.0):
        """Para música de fundo"""
        if not self.initialized or not self.is_music_playing:
            return
        
        try:
            if fade_out_time > 0:
                pygame.mixer.music.fadeout(int(fade_out_time * 1000))
                print(f"🔇 Música parando com fade-out ({fade_out_time}s)")
            else:
                pygame.mixer.music.stop()
                print("🔇 Música parada")
            
            self.is_music_playing = False
            self.current_music_file = None
            
        except Exception as e:
            print(f"❌ Erro ao parar música: {e}")

    def pause_music(self):
        """Pausa música de fundo"""
        if not self.initialized or not self.is_music_playing:
            return
        
        try:
            pygame.mixer.music.pause()
            print("⏸️ Música pausada")
        except Exception as e:
            print(f"❌ Erro ao pausar música: {e}")

    def resume_music(self):
        """Resume música de fundo"""
        if not self.initialized:
            return
        
        try:
            pygame.mixer.music.unpause()
            print("▶️ Música resumida")
        except Exception as e:
            print(f"❌ Erro ao resumir música: {e}")

    def set_music_volume(self, volume):
        """Define volume da música (0.0 - 1.0)"""
        self.music_volume = max(0.0, min(1.0, volume))
        if self.initialized and self.is_music_playing:
            pygame.mixer.music.set_volume(self.music_volume * self.master_volume)
        print(f"🎵 Volume da música: {self.music_volume:.1f}")

    def set_sfx_volume(self, volume):
        """Define volume dos efeitos sonoros (0.0 - 1.0)"""
        self.sfx_volume = max(0.0, min(1.0, volume))
        print(f"🔊 Volume dos efeitos: {self.sfx_volume:.1f}")

    def set_master_volume(self, volume):
        """Define volume geral (0.0 - 1.0)"""
        self.master_volume = max(0.0, min(1.0, volume))
        if self.initialized and self.is_music_playing:
            pygame.mixer.music.set_volume(self.music_volume * self.master_volume)
        print(f"🔊 Volume geral: {self.master_volume:.1f}")

    def _get_audio_path(self, file_path):
        if os.path.isabs(file_path):
            return file_path
        
        base_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))  # Volta 3 níveis para pasta do projeto
        audio_path = os.path.join(base_path, "audio", file_path)
        
        return audio_path

    def list_loaded_audio(self):
        """Lista todos os áudios carregados"""
        print("\n🎵 ÁUDIOS CARREGADOS:")
        
        print(f"📀 Músicas ({len(self.loaded_music)}):")
        for name, info in self.loaded_music.items():
            print(f"   🎵 {name}: {info['file_path']}")
        
        print(f"🔊 Efeitos ({len(self.loaded_sounds)}):")
        for name, info in self.loaded_sounds.items():
            print(f"   🔊 {name}: {info['file_path']}")
        
        print(f"🎛️ Status:")
        print(f"   🎵 Música tocando: {self.is_music_playing}")
        print(f"   🎵 Música atual: {self.current_music_file}")
        print(f"   🔊 Volume música: {self.music_volume:.1f}")
        print(f"   🔊 Volume efeitos: {self.sfx_volume:.1f}")
        print(f"   🔊 Volume geral: {self.master_volume:.1f}")

    def cleanup(self):
        """Limpa recursos de áudio"""
        try:
            if self.is_music_playing:
                pygame.mixer.music.stop()
            
            pygame.mixer.quit()
            print("🧹 AudioManager limpo")
            
        except Exception as e:
            print(f"⚠️ Erro na limpeza do áudio: {e}")

# 🎵 INSTÂNCIA GLOBAL
audio_manager = AudioManager()