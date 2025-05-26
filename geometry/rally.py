import math
from geometry.geometry import Geometry

class RallyTerrainGeometry(Geometry):
    
    def __init__(self, scale=1.0, obj_data=None):
        super().__init__()
        
        print("🏁 RallyTerrainGeometry: CRIANDO TERRENO COM NORMAIS CORRETAS")
        
        # Sempre cria terreno simples - ignora OBJ por enquanto
        self._create_simple_terrain()

    def _create_simple_terrain(self):
        """Cria um terreno simples com NORMAIS CORRETAS"""
        print("🏁 Criando terreno com normais para cima...")
        
        # Terreno simples: plano com algumas ondulações
        size = 20.0
        segments = 10
        
        positions = []
        normals = []
        uvs = []
        
        for i in range(segments):
            for j in range(segments):
                if i < segments - 1 and j < segments - 1:
                    # Calcula posições dos 4 cantos do quad
                    x1 = (i / segments - 0.5) * size
                    z1 = (j / segments - 0.5) * size
                    x2 = ((i + 1) / segments - 0.5) * size
                    z2 = ((j + 1) / segments - 0.5) * size
                    
                    # Altura com ondulações simples
                    y1 = math.sin(x1 * 0.2) * math.cos(z1 * 0.2) * 1.0
                    y2 = math.sin(x2 * 0.2) * math.cos(z1 * 0.2) * 1.0
                    y3 = math.sin(x1 * 0.2) * math.cos(z2 * 0.2) * 1.0
                    y4 = math.sin(x2 * 0.2) * math.cos(z2 * 0.2) * 1.0
                    
                    # 🔺 TRIÂNGULO 1 - Ordem correta para normal para cima
                    positions.extend([x1, y1, z1])  # v1
                    positions.extend([x2, y2, z1])  # v2
                    positions.extend([x1, y3, z2])  # v3
                    
                    # Normais para cima (positivo Y)
                    normals.extend([0.0, 1.0, 0.0])  # v1
                    normals.extend([0.0, 1.0, 0.0])  # v2
                    normals.extend([0.0, 1.0, 0.0])  # v3
                    
                    # UVs
                    uvs.extend([i/segments, j/segments])        # v1
                    uvs.extend([(i+1)/segments, j/segments])    # v2
                    uvs.extend([i/segments, (j+1)/segments])    # v3
                    
                    # 🔺 TRIÂNGULO 2 - Ordem correta para normal para cima
                    positions.extend([x2, y2, z1])  # v2
                    positions.extend([x2, y4, z2])  # v4
                    positions.extend([x1, y3, z2])  # v3
                    
                    # Normais para cima (positivo Y)
                    normals.extend([0.0, 1.0, 0.0])  # v2
                    normals.extend([0.0, 1.0, 0.0])  # v4
                    normals.extend([0.0, 1.0, 0.0])  # v3
                    
                    # UVs
                    uvs.extend([(i+1)/segments, j/segments])    # v2
                    uvs.extend([(i+1)/segments, (j+1)/segments]) # v4
                    uvs.extend([i/segments, (j+1)/segments])    # v3
        
        # Adiciona atributos
        self.add_attribute("vec3", "vertexPosition", positions)
        self.add_attribute("vec3", "vertexNormal", normals)
        self.add_attribute("vec2", "vertexUV", uvs)
        
        triangle_count = len(positions) // 9
        print(f"✅ Terreno criado: {triangle_count} triângulos com normais para CIMA")