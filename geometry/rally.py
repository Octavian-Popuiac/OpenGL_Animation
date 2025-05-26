import math
from core.attribute import Attribute
from core.uniform import Uniform
from core.matrix import Matrix
from geometry.geometry import Geometry
from material.surface import SurfaceMaterial

class RallyTerrainGeometry(Geometry):
    
    def __init__(self, scale=1.0, obj_data=None):
        super().__init__()
        
        # 🏁 CONFIGURAÇÕES DO RALLY
        self.scale = scale
        self.terrain_segments = {}
        
        # 🎨 CORES TEMPORÁRIAS PARA CADA ELEMENTO
        self.terrain_colors = {
            "montanha1": [0.4, 0.3, 0.2],    # Marrom montanha
            "montanha2": [0.3, 0.5, 0.3],    # Verde montanha
            "montanha3": [0.5, 0.4, 0.3],    # Bege montanha
            "estrada": [0.2, 0.2, 0.2],      # Cinza escuro estrada
            "rampa": [0.6, 0.5, 0.4],        # Marrom claro rampa
            "default": [0.5, 0.5, 0.5]       # Cinza padrão
        }
        
        if obj_data:
            self._parse_rally_obj(obj_data)
        else:
            self._create_default_rally_terrain()
    
    def _parse_rally_obj(self, obj_data):
        print("🏁 Processando terreno de rally...")
    
        # 🔧 CORRIGE FORMATO DOS DADOS - obj_data pode ser lista de strings ou tuplas
        if isinstance(obj_data, list):
            # Se for lista, converte cada item para string e junta
            try:
                obj_string = '\n'.join(str(item) if not isinstance(item, (list, tuple)) else ' '.join(map(str, item)) for item in obj_data)
            except Exception as e:
                print(f"⚠️ Erro ao processar obj_data como lista: {e}")
                # Fallback: tenta converter diretamente
                obj_string = str(obj_data)
        elif isinstance(obj_data, str):
            obj_string = obj_data
        else:
            print(f"⚠️ Formato inesperado de obj_data: {type(obj_data)}")
            # Tenta converter para string
            obj_string = str(obj_data)
        
        current_object = "default"
        vertices = []
        normals = []
        uvs = []
        
        # Parse das linhas do OBJ
        for line in obj_string.split('\n'):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            parts = line.split()
            if not parts:
                continue
            
            # 🏷️ DETECTA OBJETO (montanha1, estrada, etc.)
            if parts[0] == 'o':
                current_object = parts[1] if len(parts) > 1 else "default"
                print(f"   📍 Processando objeto: {current_object}")
                
                # Inicializa segmento se não existe
                if current_object not in self.terrain_segments:
                    self.terrain_segments[current_object] = {
                        'vertices': [],
                        'normals': [],
                        'uvs': [],
                        'faces': [],
                        'color': self.terrain_colors.get(current_object, self.terrain_colors["default"])
                    }
            
            # 📍 VÉRTICES
            elif parts[0] == 'v':
                if len(parts) >= 4:
                    try:
                        vertex = [float(parts[1]) * self.scale, 
                                 float(parts[2]) * self.scale, 
                                 float(parts[3]) * self.scale]
                        vertices.append(vertex)
                        
                        # Adiciona ao objeto atual
                        if current_object in self.terrain_segments:
                            self.terrain_segments[current_object]['vertices'].append(vertex)
                    except ValueError as e:
                        print(f"⚠️ Erro ao processar vértice: {parts} - {e}")
            
            # 📐 NORMAIS
            elif parts[0] == 'vn':
                if len(parts) >= 4:
                    try:
                        normal = [float(parts[1]), float(parts[2]), float(parts[3])]
                        normals.append(normal)
                        
                        if current_object in self.terrain_segments:
                            self.terrain_segments[current_object]['normals'].append(normal)
                    except ValueError as e:
                        print(f"⚠️ Erro ao processar normal: {parts} - {e}")
            
            # 🗺️ COORDENADAS UV
            elif parts[0] == 'vt':
                if len(parts) >= 3:
                    try:
                        uv = [float(parts[1]), float(parts[2])]
                        uvs.append(uv)
                        
                        if current_object in self.terrain_segments:
                            self.terrain_segments[current_object]['uvs'].append(uv)
                    except ValueError as e:
                        print(f"⚠️ Erro ao processar UV: {parts} - {e}")
            
            # 🔺 FACES
            elif parts[0] == 'f':
                if len(parts) >= 4:
                    try:
                        face_vertices = []
                        for vertex_data in parts[1:]:
                            # Parse "v/vt/vn" format
                            indices = vertex_data.split('/')
                            v_index = int(indices[0]) - 1  # OBJ usa 1-based indexing
                            face_vertices.append(v_index)
                        
                        if current_object in self.terrain_segments:
                            self.terrain_segments[current_object]['faces'].append(face_vertices)
                    except ValueError as e:
                        print(f"⚠️ Erro ao processar face: {parts} - {e}")
        
        # 🔧 GERA GEOMETRIA FINAL
        self._build_rally_geometry()
        
        print(f"✅ Rally terrain processado:")
        for obj_name, data in self.terrain_segments.items():
            vertex_count = len(data['vertices'])
            face_count = len(data['faces'])
            print(f"   🏔️ {obj_name}: {vertex_count} vértices, {face_count} faces")
    
    def _build_rally_geometry(self):
        """Constrói a geometria final combinando todos os segmentos"""
        all_positions = []
        all_colors = []
        all_normals = []
        all_uvs = []
        
        for obj_name, segment in self.terrain_segments.items():
            obj_color = segment['color']
            obj_vertices = segment['vertices']
            obj_faces = segment['faces']
            
            # 🔺 TRIANGULAÇÃO DAS FACES
            for face in obj_faces:
                if len(face) >= 3:
                    # Converte face em triângulos
                    for i in range(1, len(face) - 1):
                        # Triângulo: face[0], face[i], face[i+1]
                        triangle_indices = [face[0], face[i], face[i+1]]
                        
                        for vertex_index in triangle_indices:
                            if 0 <= vertex_index < len(obj_vertices):  # ← VALIDAÇÃO DE ÍNDICE
                                vertex = obj_vertices[vertex_index]
                                all_positions.extend(vertex)
                                all_colors.extend(obj_color)
                                
                                # 📐 NORMAL CALCULADA (temporária)
                                all_normals.extend([0.0, 1.0, 0.0])  # Normal para cima
                                
                                # 🗺️ UV TEMPORÁRIO
                                all_uvs.extend([vertex[0] * 0.1, vertex[2] * 0.1])
                            else:
                                print(f"⚠️ Índice de vértice inválido: {vertex_index}")
        
        # 📊 ESTATÍSTICAS
        triangle_count = len(all_positions) // 9  # 3 vértices * 3 coordenadas
        print(f"🔧 Geometria rally construída: {triangle_count} triângulos")
        
        # 🔧 DEFINE ATRIBUTOS
        self.add_attribute("vec3", "vertexPosition", all_positions)
        self.add_attribute("vec3", "vertexColor", all_colors)
        self.add_attribute("vec3", "vertexNormal", all_normals)
        self.add_attribute("vec2", "vertexUV", all_uvs)
        
        # 🔧 CORRIGIDO: count_vertices não existe, use count_vertices_direct
        if hasattr(self, 'count_vertices'):
            self.count_vertices()
        else:
            # Calcula manualmente
            self.vertexCount = len(all_positions) // 3
            print(f"🔢 Vértices contados: {self.vertexCount}")
    
    def _create_default_rally_terrain(self):
        """Cria um terreno de rally padrão se não houver OBJ"""
        print("🏁 Criando terreno de rally padrão...")
        
        # 🏔️ TERRENO BASE (plano com ondulações)
        size = 20.0
        resolution = 50
        
        positions = []
        colors = []
        normals = []
        uvs = []
        
        for i in range(resolution):
            for j in range(resolution):
                # 📍 POSIÇÕES COM ONDULAÇÕES
                x = (i / (resolution - 1) - 0.5) * size
                z = (j / (resolution - 1) - 0.5) * size
                
                # 🌊 ALTURA VARIADA (simulando montanhas e vales)
                y = (math.sin(x * 0.3) * math.cos(z * 0.2) * 2.0 + 
                     math.sin(x * 0.1) * 1.5 + 
                     math.cos(z * 0.15) * 1.0)
                
                # 🎨 COR BASEADA NA ALTURA
                if y > 1.5:
                    color = self.terrain_colors["montanha1"]  # Montanha alta
                elif y > 0.5:
                    color = self.terrain_colors["montanha2"]  # Montanha média
                elif abs(x) < 2.0 and abs(z) < 15.0:  # Estrada no centro
                    color = self.terrain_colors["estrada"]
                else:
                    color = self.terrain_colors["montanha3"]  # Base
                
                # 🔺 CRIA TRIÂNGULOS
                if i < resolution - 1 and j < resolution - 1:
                    # Dois triângulos por quad
                    # Triângulo 1
                    positions.extend([x, y, z])
                    colors.extend(color)
                    normals.extend([0.0, 1.0, 0.0])
                    uvs.extend([i / resolution, j / resolution])
                    
                    x1 = ((i + 1) / (resolution - 1) - 0.5) * size
                    y1 = (math.sin(x1 * 0.3) * math.cos(z * 0.2) * 2.0 + 
                          math.sin(x1 * 0.1) * 1.5 + math.cos(z * 0.15) * 1.0)
                    positions.extend([x1, y1, z])
                    colors.extend(color)
                    normals.extend([0.0, 1.0, 0.0])
                    uvs.extend([(i + 1) / resolution, j / resolution])
                    
                    z1 = ((j + 1) / (resolution - 1) - 0.5) * size
                    y2 = (math.sin(x * 0.3) * math.cos(z1 * 0.2) * 2.0 + 
                          math.sin(x * 0.1) * 1.5 + math.cos(z1 * 0.15) * 1.0)
                    positions.extend([x, y2, z1])
                    colors.extend(color)
                    normals.extend([0.0, 1.0, 0.0])
                    uvs.extend([i / resolution, (j + 1) / resolution])
        
        # 🔧 DEFINE ATRIBUTOS
        self.add_attribute("vec3", "vertexPosition", positions)
        self.add_attribute("vec3", "vertexColor", colors)
        self.add_attribute("vec3", "vertexNormal", normals)
        self.add_attribute("vec2", "vertexUV", uvs)
        
        # 🔧 CORRIGIDO: count_vertices pode não existir
        if hasattr(self, 'count_vertices'):
            self.count_vertices()
        else:
            # Calcula manualmente
            self.vertexCount = len(positions) // 3
            print(f"🔢 Vértices contados: {self.vertexCount}")
        
        print(f"✅ Terreno padrão criado: {len(positions) // 9} triângulos")
    
    def get_terrain_bounds(self):
        """Retorna os limites do terreno para posicionamento de objetos"""
        if not hasattr(self, 'attributes') or 'vertexPosition' not in self.attributes:
            return {'min': [-10, -5, -10], 'max': [10, 5, 10]}
        
        positions = self.attributes['vertexPosition'].data
        
        min_x = min_y = min_z = float('inf')
        max_x = max_y = max_z = float('-inf')
        
        for i in range(0, len(positions), 3):
            x, y, z = positions[i], positions[i+1], positions[i+2]
            
            min_x = min(min_x, x)
            max_x = max(max_x, x)
            min_y = min(min_y, y)
            max_y = max(max_y, y)
            min_z = min(min_z, z)
            max_z = max(max_z, z)
        
        return {
            'min': [min_x, min_y, min_z],
            'max': [max_x, max_y, max_z]
        }
    
    def get_height_at_position(self, x, z):
        """Retorna a altura do terreno numa posição X,Z específica"""
        # 🔍 IMPLEMENTAÇÃO SIMPLIFICADA
        # Em um sistema mais avançado, faria interpolação dos vértices próximos
        
        # Por agora, usa a fórmula matemática do terreno padrão
        y = (math.sin(x * 0.3) * math.cos(z * 0.2) * 2.0 + 
             math.sin(x * 0.1) * 1.5 + 
             math.cos(z * 0.15) * 1.0)
        
        return y
    
    def get_road_center_line(self, start_z=-15, end_z=15, num_points=20):
        """Retorna pontos centrais da estrada para navegação do carro"""
        road_points = []
        
        for i in range(num_points):
            progress = i / (num_points - 1)
            z = start_z + (end_z - start_z) * progress
            x = 0.0  # Estrada no centro
            y = self.get_height_at_position(x, z) + 0.1  # Ligeiramente acima do terreno
            
            road_points.append([x, y, z])
        
        return road_points
    
    def create_rally_material(self):
      from material.surface import SurfaceMaterial
      
      try:
          # Tenta criar material simples primeiro
          material = SurfaceMaterial()
          
          # Se SurfaceMaterial suportar propriedades, adiciona depois
          if hasattr(material, 'set_property'):
              material.set_property("useVertexColors", True)
              material.set_property("wireframe", False)
              material.set_property("doubleSide", True)
          elif hasattr(material, 'uniforms'):
              # Se usar uniforms
              if "baseColor" in material.uniforms:
                  material.uniforms["baseColor"].data = [0.8, 0.7, 0.6]
          
          return material
          
      except Exception as e:
          print(f"⚠️ Erro ao criar material rally: {e}")
          # Fallback: usa material básico
          from material.basic import BasicMaterial
          return BasicMaterial()