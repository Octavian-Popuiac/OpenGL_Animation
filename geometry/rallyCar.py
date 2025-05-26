import math
from geometry.geometry import Geometry

class RallyCarGeometry(Geometry):
    
    def __init__(self, scale=1.0, obj_data=None):
        super().__init__()
        
        print("🏎️ RallyCarGeometry: CRIANDO CARRO COM NORMAIS CORRETAS")
        
        # Sempre cria carro simples - ignora OBJ por enquanto
        self._create_simple_car()

    def _create_simple_car(self):
        """Cria um carro simples com NORMAIS CORRETAS"""
        print("🏎️ Criando carro com normais corretas...")
        
        # Carro simples: caixa com proporções de carro
        width = 2.0
        height = 1.0
        length = 4.0
        
        positions = []
        normals = []
        uvs = []
        
        # Define os 8 vértices de uma caixa
        vertices = [
            [-width/2, 0, -length/2],      # 0: traseira esquerda inferior
            [width/2, 0, -length/2],       # 1: traseira direita inferior
            [width/2, height, -length/2],  # 2: traseira direita superior
            [-width/2, height, -length/2], # 3: traseira esquerda superior
            [-width/2, 0, length/2],       # 4: frente esquerda inferior
            [width/2, 0, length/2],        # 5: frente direita inferior
            [width/2, height, length/2],   # 6: frente direita superior
            [-width/2, height, length/2]   # 7: frente esquerda superior
        ]
        
        # Define as faces da caixa com NORMAIS CORRETAS
        faces_with_normals = [
            # Face traseira (normal: [0, 0, -1])
            ([0, 2, 1], [0.0, 0.0, -1.0]),
            ([0, 3, 2], [0.0, 0.0, -1.0]),
            
            # Face frente (normal: [0, 0, 1])
            ([4, 5, 6], [0.0, 0.0, 1.0]),
            ([4, 6, 7], [0.0, 0.0, 1.0]),
            
            # Face esquerda (normal: [-1, 0, 0])
            ([0, 4, 7], [-1.0, 0.0, 0.0]),
            ([0, 7, 3], [-1.0, 0.0, 0.0]),
            
            # Face direita (normal: [1, 0, 0])
            ([1, 2, 6], [1.0, 0.0, 0.0]),
            ([1, 6, 5], [1.0, 0.0, 0.0]),
            
            # Face superior (normal: [0, 1, 0])
            ([3, 7, 6], [0.0, 1.0, 0.0]),
            ([3, 6, 2], [0.0, 1.0, 0.0]),
            
            # Face inferior (normal: [0, -1, 0])
            ([0, 1, 5], [0.0, -1.0, 0.0]),
            ([0, 5, 4], [0.0, -1.0, 0.0])
        ]
        
        # Gera triângulos do corpo com normais corretas
        for face_data in faces_with_normals:
            face_indices, face_normal = face_data
            
            for vertex_index in face_indices:
                vertex = vertices[vertex_index]
                positions.extend(vertex)
                normals.extend(face_normal)  # Normal específica da face
                uvs.extend([0.0, 0.0])
        
        # 🛞 RODAS - com normais corretas também
        wheel_size = 0.3
        wheel_positions = [
            [-width/3, -0.2, -length/3],   # Roda traseira esquerda
            [width/3, -0.2, -length/3],    # Roda traseira direita
            [-width/3, -0.2, length/3],    # Roda frente esquerda
            [width/3, -0.2, length/3]      # Roda frente direita
        ]
        
        for wheel_pos in wheel_positions:
            # Pequeno cubo para roda
            wheel_vertices = [
                [wheel_pos[0] - wheel_size/2, wheel_pos[1], wheel_pos[2] - wheel_size/2],
                [wheel_pos[0] + wheel_size/2, wheel_pos[1], wheel_pos[2] - wheel_size/2],
                [wheel_pos[0] + wheel_size/2, wheel_pos[1] + wheel_size/2, wheel_pos[2] - wheel_size/2],
                [wheel_pos[0] - wheel_size/2, wheel_pos[1] + wheel_size/2, wheel_pos[2] - wheel_size/2],
                [wheel_pos[0] - wheel_size/2, wheel_pos[1], wheel_pos[2] + wheel_size/2],
                [wheel_pos[0] + wheel_size/2, wheel_pos[1], wheel_pos[2] + wheel_size/2],
                [wheel_pos[0] + wheel_size/2, wheel_pos[1] + wheel_size/2, wheel_pos[2] + wheel_size/2],
                [wheel_pos[0] - wheel_size/2, wheel_pos[1] + wheel_size/2, wheel_pos[2] + wheel_size/2]
            ]
            
            # Faces da roda com normais corretas
            for face_data in faces_with_normals:
                face_indices, face_normal = face_data
                
                for vertex_index in face_indices:
                    vertex = wheel_vertices[vertex_index]
                    positions.extend(vertex)
                    normals.extend(face_normal)  # Normal específica da face
                    uvs.extend([0.0, 0.0])
        
        # Adiciona atributos
        self.add_attribute("vec3", "vertexPosition", positions)
        self.add_attribute("vec3", "vertexNormal", normals)
        self.add_attribute("vec2", "vertexUV", uvs)
        
        triangle_count = len(positions) // 9
        print(f"✅ Carro criado: {triangle_count} triângulos com normais CORRETAS")