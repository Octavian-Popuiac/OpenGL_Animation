#!/usr/bin/python3
import pathlib
import sys

# Setup do caminho
package_dir = str(pathlib.Path(__file__).resolve().parents[2])
if package_dir not in sys.path:
    sys.path.insert(0, package_dir)

from animation.scene_manager import SceneManager

def animation_menu():
    """Menu para escolher modo de câmera na animação"""
    print("\n🎥 Modo de Câmera para Animação:")
    print("1. Câmeras automáticas (cinematográfico) + Pausa com P")
    print("2. Controle livre da câmera (WASD + mouse) - sem pausa")
    
    
    while True:
        escolha = input("Digite 1 ou 2: ").strip()
        if escolha in ["1", "2"]:
            return escolha == "2"  # True = controle livre, False = automático
        print("❌ Escolha inválida. Digite 1 ou 2.")

# Executa a animação
if __name__ == "__main__":
    print("🎬 Iniciando Animação Completa")
    
    # Menu de escolha da câmera
    free_camera = animation_menu()
    
    animation = SceneManager(free_camera_mode=free_camera)
    animation.run()