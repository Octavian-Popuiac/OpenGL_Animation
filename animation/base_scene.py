import math
from abc import ABC, abstractmethod

class BaseScene(ABC):
    def __init__(self, scene, camera, renderer):
        self.scene = scene
        self.camera = camera
        self.renderer = renderer
        self.timeline = 0
        self.is_finished = False
    
    @abstractmethod
    def get_duration(self):
        """Retorna a duração da cena em segundos"""
        pass
    
    @abstractmethod
    def initialize(self):
        """Inicializa a cena (carrega objetos, define posições, etc)"""
        pass
    
    @abstractmethod
    def update(self, delta_time):
        """Atualiza a cena a cada frame"""
        pass
    
    def interpolate(self, start, end, progress):
        """Interpolação linear entre dois valores"""
        return start + (end - start) * progress
    
    def smooth_step(self, progress):
        """Suaviza a interpolação (ease-in-out)"""
        return progress * progress * (3 - 2 * progress)