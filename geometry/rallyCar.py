import math
from core.attribute import Attribute
from core.uniform import Uniform
from core.matrix import Matrix
from geometry.geometry import Geometry
from material.surface import SurfaceMaterial

class RallyCarGeometry(Geometry):
    
    def __init__(self, scale=1.0, obj_data=None, mtl_path=None):
        super().__init__()
        
        # 🏎️ CONFIGURAÇÕES DO CARRO DE RALLY
        self.scale = scale
        self.car_parts = {}
        
        # 🎨 CORES DOS COMPONENTES DO CARRO
        self.car_colors = {
            # Componentes principais
            "SK_Ford_Puma_Rally1_23_Forwrc": [0.8, 0.2, 0.1],     # Vermelho rally (carroceria)
            "SK_Int_Ford_Puma_Rally1_23_Forwrc": [0.2, 0.2, 0.2], # Cinza escuro (interior)
            "SM_Wheel_Tm_Spare": [0.1, 0.1, 0.1],                 # Preto (pneus)
            
            # Materiais específicos
            "MI_Tm_Tread_Spare": [0.3, 0.3, 0.3],                 # Banda de rodagem
            "MI_Tm_Wheel": [0.9, 0.3, 0.3],                       # Roda vermelha
            "dummy_material_0": [0.8, 0.8, 0.8],                  # Cinza claro (chassis)
            "dummy_material_1": [0.7, 0.7, 0.7],                  # Cinza médio (detalhes)
            "dummy_material_2": [0.6, 0.6, 0.6],                  # Cinza
            "dummy_material_3": [0.5, 0.5, 0.5],                  # Cinza escuro
            "dummy_material_4": [0.9, 0.9, 0.9],                  # Vidros (translúcido)
            "dummy_material_5": [0.4, 0.4, 0.4],                  # Componentes escuros
            "dummy_material_6": [0.85, 0.85, 0.85],               # Metal claro
            "dummy_material_7": [0.75, 0.75, 0.75],               # Metal médio
            "dummy_material_8": [0.65, 0.65, 0.65],               # Metal escuro
            "dummy_material_9": [1.0, 0.8, 0.2],                  # Luzes amarelas
            "dummy_material_10": [0.9, 0.1, 0.1],                 # Luzes vermelhas
            "dummy_material_11": [0.8, 0.8, 0.8],                 # Metálico
            "dummy_material_12": [0.2, 0.2, 0.2],                 # Preto fosco
            "dummy_material_13": [0.7, 0.7, 0.7],                 # Cinza padrão
            "dummy_material_14": [0.6, 0.6, 0.6],                 # Cinza médio
            "dummy_material_15": [0.5, 0.5, 0.5],                 # Cinza escuro
            "dummy_material_16": [0.4, 0.4, 0.4],                 # Muito escuro
            "dummy_material_17": [0.8, 0.4, 0.1],                 # Laranja (detalhes)
            "dummy_material_18": [0.1, 0.3, 0.8],                 # Azul (detalhes)
            "dummy_material_19": [0.8, 0.2, 0.1],                 # Vermelho principal
            "default": [0.6, 0.6, 0.6]                            # Cor padrão
        }
        
        # 🔧 PROPRIEDADES FÍSICAS DO CARRO
        self.car_bounds = None
        self.wheel_positions = []
        self.center_of_mass = [0.0, 0.0, 0.0]
        
        if obj_data:
            self._parse_rally_car_obj(obj_data)
        else:
            self._create_default_rally_car()
    
    def _parse_rally_car_obj(self, obj_data):
        """Parse do arquivo .obj do carro de rally organizando por componentes"""
        print("🏎️ Processando carro de rally...")
        
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
        current_material = "default"
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
            
            # 🏷️ DETECTA OBJETO (carroceria, rodas, etc.)
            if parts[0] == 'o':
                current_object = parts[1] if len(parts) > 1 else "default"
                print(f"   🔧 Processando componente: {current_object}")
                
                # Inicializa componente se não existe
                if current_object not in self.car_parts:
                    self.car_parts[current_object] = {
                        'vertices': [],
                        'normals': [],
                        'uvs': [],
                        'faces': [],
                        'material': current_material,
                        'color': self.car_colors.get(current_object, self.car_colors["default"])
                    }
            
            # 🎨 DETECTA MATERIAL
            elif parts[0] == 'usemtl':
                current_material = parts[1] if len(parts) > 1 else "default"
                
                # Atualiza cor do componente atual baseada no material
                if current_object in self.car_parts:
                    self.car_parts[current_object]['material'] = current_material
                    self.car_parts[current_object]['color'] = self.car_colors.get(
                        current_material, 
                        self.car_colors.get(current_object, self.car_colors["default"])
                    )
            
            # 📍 VÉRTICES
            elif parts[0] == 'v':
                if len(parts) >= 4:
                    vertex = [float(parts[1]) * self.scale, 
                             float(parts[2]) * self.scale, 
                             float(parts[3]) * self.scale]
                    vertices.append(vertex)
                    
                    # Adiciona ao componente atual
                    if current_object in self.car_parts:
                        self.car_parts[current_object]['vertices'].append(vertex)
            
            # 📐 NORMAIS
            elif parts[0] == 'vn':
                if len(parts) >= 4:
                    normal = [float(parts[1]), float(parts[2]), float(parts[3])]
                    normals.append(normal)
                    
                    if current_object in self.car_parts:
                        self.car_parts[current_object]['normals'].append(normal)
            
            # 🗺️ COORDENADAS UV
            elif parts[0] == 'vt':
                if len(parts) >= 3:
                    uv = [float(parts[1]), float(parts[2])]
                    uvs.append(uv)
                    
                    if current_object in self.car_parts:
                        self.car_parts[current_object]['uvs'].append(uv)
            
            # 🔺 FACES
            elif parts[0] == 'f':
                if len(parts) >= 4:
                    face_vertices = []
                    face_uvs = []
                    face_normals = []
                    
                    for vertex_data in parts[1:]:
                        # Parse "v/vt/vn" format
                        indices = vertex_data.split('/')
                        
                        # Índice do vértice (obrigatório)
                        if indices[0]:
                            v_index = int(indices[0]) - 1  # OBJ usa 1-based indexing
                            face_vertices.append(v_index)
                        
                        # Índice da coordenada UV (opcional)
                        if len(indices) > 1 and indices[1]:
                            uv_index = int(indices[1]) - 1
                            face_uvs.append(uv_index)
                        
                        # Índice da normal (opcional)
                        if len(indices) > 2 and indices[2]:
                            n_index = int(indices[2]) - 1
                            face_normals.append(n_index)
                    
                    if current_object in self.car_parts:
                        self.car_parts[current_object]['faces'].append({
                            'vertices': face_vertices,
                            'uvs': face_uvs if face_uvs else None,
                            'normals': face_normals if face_normals else None
                        })
        
        # 🔧 CALCULA PROPRIEDADES FÍSICAS
        self._calculate_car_properties()
        
        # 🔧 GERA GEOMETRIA FINAL
        self._build_rally_car_geometry()
        
        print(f"✅ Carro de rally processado:")
        for component_name, data in self.car_parts.items():
            vertex_count = len(data['vertices'])
            face_count = len(data['faces'])
            material = data['material']
            print(f"   🔧 {component_name}: {vertex_count} vértices, {face_count} faces ({material})")
    
    def _calculate_car_properties(self):
        """Calcula propriedades físicas do carro (centro de massa, rodas, etc.)"""
        all_vertices = []
        wheel_vertices = []
        
        for component_name, component in self.car_parts.items():
            all_vertices.extend(component['vertices'])
            
            # 🛞 DETECTA RODAS
            if 'wheel' in component_name.lower() or 'tm' in component_name.lower():
                wheel_vertices.extend(component['vertices'])
                
                # Calcula centro da roda
                if component['vertices']:
                    center_x = sum(v[0] for v in component['vertices']) / len(component['vertices'])
                    center_y = sum(v[1] for v in component['vertices']) / len(component['vertices'])
                    center_z = sum(v[2] for v in component['vertices']) / len(component['vertices'])
                    
                    self.wheel_positions.append([center_x, center_y, center_z])
        
        # 📏 CALCULA LIMITES DO CARRO
        if all_vertices:
            min_x = min(v[0] for v in all_vertices)
            max_x = max(v[0] for v in all_vertices)
            min_y = min(v[1] for v in all_vertices)
            max_y = max(v[1] for v in all_vertices)
            min_z = min(v[2] for v in all_vertices)
            max_z = max(v[2] for v in all_vertices)
            
            self.car_bounds = {
                'min': [min_x, min_y, min_z],
                'max': [max_x, max_y, max_z],
                'width': max_x - min_x,
                'height': max_y - min_y,
                'length': max_z - min_z
            }
            
            # 📍 CENTRO DE MASSA (aproximado)
            self.center_of_mass = [
                (min_x + max_x) / 2,
                (min_y + max_y) / 2,
                (min_z + max_z) / 2
            ]
            
            print(f"🏎️ Propriedades do carro:")
            print(f"   📏 Dimensões: {self.car_bounds['width']:.2f} x {self.car_bounds['height']:.2f} x {self.car_bounds['length']:.2f}")
            print(f"   📍 Centro de massa: [{self.center_of_mass[0]:.2f}, {self.center_of_mass[1]:.2f}, {self.center_of_mass[2]:.2f}]")
            print(f"   🛞 Rodas detectadas: {len(self.wheel_positions)}")
    
    def _build_rally_car_geometry(self):
        """Constrói a geometria final combinando todos os componentes"""
        all_positions = []
        all_colors = []
        all_normals = []
        all_uvs = []
        
        vertex_global_index = 0  # Índice global de vértices processados
        
        for component_name, component in self.car_parts.items():
            component_color = component['color']
            component_vertices = component['vertices']
            component_faces = component['faces']
            component_normals = component['normals']
            component_uvs = component['uvs']
            
            # 🔺 TRIANGULAÇÃO DAS FACES
            for face in component_faces:
                face_vertices = face['vertices']
                face_normals = face.get('normals', [])
                face_uvs = face.get('uvs', [])
                
                if len(face_vertices) >= 3:
                    # Converte face em triângulos (fan triangulation)
                    for i in range(1, len(face_vertices) - 1):
                        # Triângulo: face[0], face[i], face[i+1]
                        triangle_indices = [face_vertices[0], face_vertices[i], face_vertices[i+1]]
                        
                        for j, vertex_index in enumerate(triangle_indices):
                            if vertex_index < len(component_vertices):
                                # 📍 POSIÇÃO DO VÉRTICE
                                vertex = component_vertices[vertex_index]
                                all_positions.extend(vertex)
                                all_colors.extend(component_color)
                                
                                # 📐 NORMAL
                                if (face_normals and 
                                    j < len(face_normals) and 
                                    face_normals[j] < len(component_normals)):
                                    normal = component_normals[face_normals[j]]
                                    all_normals.extend(normal)
                                else:
                                    # Normal padrão apontando para cima
                                    all_normals.extend([0.0, 1.0, 0.0])
                                
                                # 🗺️ COORDENADAS UV
                                if (face_uvs and 
                                    j < len(face_uvs) and 
                                    face_uvs[j] < len(component_uvs)):
                                    uv = component_uvs[face_uvs[j]]
                                    all_uvs.extend(uv)
                                else:
                                    # UV padrão
                                    all_uvs.extend([vertex[0] * 0.1, vertex[2] * 0.1])
        
        # 📊 ESTATÍSTICAS
        triangle_count = len(all_positions) // 9  # 3 vértices * 3 coordenadas
        print(f"🔧 Geometria do carro construída: {triangle_count} triângulos")
        
        # 🔧 DEFINE ATRIBUTOS
        self.add_attribute("vec3", "vertexPosition", all_positions)
        self.add_attribute("vec3", "vertexColor", all_colors)
        self.add_attribute("vec3", "vertexNormal", all_normals)
        self.add_attribute("vec2", "vertexUV", all_uvs)
        
        if hasattr(self, 'count_vertices'):
            self.count_vertices()
        else:
            # Calcula manualmente
            self.vertexCount = len(all_positions) // 3
            print(f"🔢 Vértices do carro contados: {self.vertexCount}")
    
    def _create_default_rally_car(self):
        """Cria um carro de rally padrão se não houver OBJ"""
        print("🏎️ Criando carro de rally padrão...")
        
        # 🚗 CARRO SIMPLES (caixa com proporções de carro)
        width = 2.0
        height = 1.0
        length = 4.0
        
        positions = []
        colors = []
        normals = []
        uvs = []
        
        # 📦 CARROCERIA PRINCIPAL (caixa)
        car_color = self.car_colors["dummy_material_19"]  # Vermelho rally
        
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
        
        # Define as faces da caixa (2 triângulos por face)
        faces = [
            # Face traseira
            [0, 1, 2], [2, 3, 0],
            # Face frente
            [4, 7, 6], [6, 5, 4],
            # Face esquerda
            [0, 3, 7], [7, 4, 0],
            # Face direita
            [1, 5, 6], [6, 2, 1],
            # Face superior
            [3, 2, 6], [6, 7, 3],
            # Face inferior
            [0, 4, 5], [5, 1, 0]
        ]
        
        # Gera triângulos
        for face in faces:
            for vertex_index in face:
                vertex = vertices[vertex_index]
                positions.extend(vertex)
                colors.extend(car_color)
                normals.extend([0.0, 1.0, 0.0])  # Normal padrão
                uvs.extend([vertex[0] * 0.1, vertex[2] * 0.1])  # UV simples
        
        # 🛞 ADICIONA RODAS SIMPLES
        wheel_color = self.car_colors["MI_Tm_Tread_Spare"]  # Preto
        wheel_radius = 0.3
        wheel_positions_default = [
            [-width/3, 0, -length/3],   # Roda traseira esquerda
            [width/3, 0, -length/3],    # Roda traseira direita
            [-width/3, 0, length/3],    # Roda frente esquerda
            [width/3, 0, length/3]      # Roda frente direita
        ]
        
        for wheel_pos in wheel_positions_default:
            # Roda simples (cilindro baixo)
            for i in range(8):
                angle = i * 2 * math.pi / 8
                x = wheel_pos[0] + wheel_radius * math.cos(angle)
                z = wheel_pos[2] + wheel_radius * math.sin(angle)
                
                # Triângulo da roda
                positions.extend([wheel_pos[0], wheel_pos[1], wheel_pos[2]])  # Centro
                positions.extend([x, wheel_pos[1], z])  # Ponto na circunferência
                
                next_angle = (i + 1) * 2 * math.pi / 8
                next_x = wheel_pos[0] + wheel_radius * math.cos(next_angle)
                next_z = wheel_pos[2] + wheel_radius * math.sin(next_angle)
                positions.extend([next_x, wheel_pos[1], next_z])  # Próximo ponto
                
                # Cor e normais para o triângulo
                for _ in range(3):
                    colors.extend(wheel_color)
                    normals.extend([0.0, 1.0, 0.0])
                    uvs.extend([0.5, 0.5])  # UV central para rodas
        
        # 📏 CALCULA PROPRIEDADES
        self.car_bounds = {
            'min': [-width/2, 0, -length/2],
            'max': [width/2, height, length/2],
            'width': width,
            'height': height,
            'length': length
        }
        
        self.center_of_mass = [0.0, height/2, 0.0]
        self.wheel_positions = wheel_positions_default
        
        # 🔧 DEFINE ATRIBUTOS
        self.add_attribute("vec3", "vertexPosition", positions)
        self.add_attribute("vec3", "vertexColor", colors)
        self.add_attribute("vec3", "vertexNormal", normals)
        self.add_attribute("vec2", "vertexUV", uvs)
        
        if hasattr(self, 'count_vertices'):
            self.count_vertices()
        else:
            # Calcula manualmente
            self.vertexCount = len(positions) // 3
            print(f"🔢 Vértices do carro padrão contados: {self.vertexCount}")

        print(f"✅ Carro padrão criado: {len(positions) // 9} triângulos")
    
    def get_car_bounds(self):
        """Retorna os limites do carro"""
        return self.car_bounds if self.car_bounds else {'min': [-1, 0, -2], 'max': [1, 1, 2]}
    
    def get_center_of_mass(self):
        """Retorna o centro de massa do carro"""
        return self.center_of_mass.copy()
    
    def get_wheel_positions(self):
        """Retorna as posições das rodas"""
        return [pos.copy() for pos in self.wheel_positions]
    
    def get_car_dimensions(self):
        """Retorna as dimensões do carro"""
        if self.car_bounds:
            return {
                'width': self.car_bounds['width'],
                'height': self.car_bounds['height'],
                'length': self.car_bounds['length']
            }
        else:
            return {'width': 2.0, 'height': 1.0, 'length': 4.0}
    
    def create_rally_car_material(self, metallic=0.7, roughness=0.3):
      from material.surface import SurfaceMaterial
      
      try:
          # Tenta criar material simples primeiro
          material = SurfaceMaterial()
          
          # Se SurfaceMaterial suportar propriedades, adiciona depois
          if hasattr(material, 'set_property'):
              material.set_property("useVertexColors", True)
              material.set_property("wireframe", False)
          elif hasattr(material, 'uniforms'):
              # Se usar uniforms
              if "baseColor" in material.uniforms:
                  material.uniforms["baseColor"].data = [0.8, 0.2, 0.1]  # Vermelho rally
          
          return material
          
      except Exception as e:
          print(f"⚠️ Erro ao criar material do carro: {e}")
          # Fallback: usa material básico
          from material.basic import BasicMaterial
          return BasicMaterial()
    
    def get_component_info(self):
        """Retorna informações sobre os componentes do carro"""
        info = {}
        for component_name, component in self.car_parts.items():
            info[component_name] = {
                'vertices': len(component['vertices']),
                'faces': len(component['faces']),
                'material': component['material'],
                'color': component['color']
            }
        return info
    
    def set_component_color(self, component_name, color):
        """Define cor específica para um componente"""
        if component_name in self.car_parts:
            self.car_parts[component_name]['color'] = color
            # Rebuilda geometria se necessário
            print(f"🎨 Cor do componente {component_name} alterada para {color}")
        else:
            print(f"⚠️ Componente {component_name} não encontrado")
    
    def set_material_color(self, material_name, color):
        """Define cor para todos os componentes que usam um material específico"""
        updated_count = 0
        for component in self.car_parts.values():
            if component['material'] == material_name:
                component['color'] = color
                updated_count += 1
        
        if updated_count > 0:
            print(f"🎨 Cor do material {material_name} alterada para {color} ({updated_count} componentes)")
        else:
            print(f"⚠️ Material {material_name} não encontrado")
    
    def optimize_for_rally(self):
        """Otimiza o carro para performance de rally"""
        # 🔧 AJUSTES ESPECÍFICOS PARA RALLY
        
        # Realça cores dos componentes principais
        self.set_material_color("dummy_material_19", [1.0, 0.15, 0.05])  # Vermelho mais vibrante
        self.set_material_color("MI_Tm_Wheel", [0.95, 0.25, 0.25])       # Rodas vermelhas
        self.set_material_color("dummy_material_9", [1.0, 0.9, 0.1])     # Luzes amarelas brilhantes
        
        # Ajusta centro de massa para mais estabilidade
        if self.car_bounds:
            # Centro de massa ligeiramente mais baixo
            self.center_of_mass[1] = self.car_bounds['min'][1] + (self.car_bounds['height'] * 0.4)
            print(f"🏎️ Centro de massa otimizado para rally: {self.center_of_mass}")
        
        print("🏁 Carro otimizado para condições de rally!")