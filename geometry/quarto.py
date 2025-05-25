from core_ext.object3d import Object3D
from core_ext.mesh import Mesh
from material.texture import TextureMaterial
from core_ext.texture import Texture
from geometry.geometry import Geometry
from material.surface import SurfaceMaterial  # Para debug


def quartoGeometry(sx, sy, sz, verticesQuarto):
    quarto = Object3D()

    # Texturas diretas (objetos da cena do quarto)
    texture_map = {
        "plane.147": Texture("images/bedroom_scene/chao.jpg"),
        "plane.002": Texture("images/bedroom_scene/parede.jpg"),
        "plane.074": Texture("images/bedroom_scene/parede.jpg"),
        "plane.181": Texture("images/bedroom_scene/secretaria.jpg"),
        "plane.143": Texture("images/bedroom_scene/quadro.jpg"),
        "plane.144": Texture("images/bedroom_scene/moldura.jpg"),
        "Cube.003": Texture("images/bedroom_scene/parede.jpg"),
        "Plane.019_Plane.023": Texture("images/bedroom_scene/teclado.jpg"),
        "plane.196": Texture("images/bedroom_scene/cadeira.jpg"),
        "cube.071": Texture("images/bedroom_scene/chapa.jpg"),
        "cube.062": Texture("images/bedroom_scene/teclado.jpg"),
        "plane.153": Texture("images/bedroom_scene/teclado.jpg"),
        "circle.072": Texture("images/bedroom_scene/teclado.jpg"),
        "plane.201": Texture("images/bedroom_scene/cordas.jpg"),
        "plane.054": Texture("images/bedroom_scene/cabo_guitarra.jpg"),
        "circle.078": Texture("images/bedroom_scene/botoes_guitarras.jpg"),
        "plane.159": Texture("images/bedroom_scene/botoes_guitarras.jpg"),

        # Guitarras
        "vert.044": Texture("images/bedroom_scene/guitarra_preta.jpg"),
        "vert.035": Texture("images/bedroom_scene/guitarra_azul.jpg"),
        "vert.014": Texture("images/bedroom_scene/guitarra_castanha.jpg"),
        "vert.037": Texture("images/bedroom_scene/guitarra_vermelha.jpg"),

        # Outros objetos
        "door": Texture("images/bedroom_scene/secretaria.jpg"),
        "cama": Texture("images/bedroom_scene/botoes_guitarras.jpg"),

        # Adicionando texturas para os objetos que estavam sem textura

        "Vert.014": Texture("images/bedroom_scene/guitarra_castanha.jpg"),
        "Plane.054": Texture("images/bedroom_scene/cabo_guitarra.jpg"),
        "Plane.074": Texture("images/bedroom_scene/parede.jpg"),
        "Plane.147": Texture("images/bedroom_scene/chao.jpg"),
        "Plane.153": Texture("images/bedroom_scene/teclado.jpg"),

        "Plane.159": Texture("images/bedroom_scene/botoes_guitarras.jpg"),
        "Vert.035": Texture("images/bedroom_scene/guitarra_azul.jpg"),
        "Plane.181": Texture("images/bedroom_scene/secretaria.jpg"),
        "Circle.072": Texture("images/bedroom_scene/teclado.jpg"),
        "Cube.062": Texture("images/bedroom_scene/teclado.jpg"),
        "Cube.071": Texture("images/bedroom_scene/chapa.jpg"),
        "Plane.002": Texture("images/bedroom_scene/parede.jpg"),

        "Plane.143": Texture("images/bedroom_scene/quadro.jpg"),
        "Plane.144": Texture("images/bedroom_scene/moldura.jpg"),
        "Vert.037": Texture("images/bedroom_scene/guitarra_vermelha.jpg"),

        "Plane.196": Texture("images/bedroom_scene/cadeira.jpg"),
        "Vert.044": Texture("images/bedroom_scene/guitarra_preta.jpg"),
        "Plane.201": Texture("images/bedroom_scene/cordas.jpg"),
        "Circle.078": Texture("images/bedroom_scene/botoes_guitarras.jpg"),
    }

    # Construção da cena
    for name, group_vertices, group_uvs in verticesQuarto:
        geometry = Geometry()
        geometry.add_attribute("vec3", "vertexPosition", group_vertices)

        if not group_uvs or len(group_uvs) != len(group_vertices):
            print(f"⚠️ UVs ausentes ou inválidas em {name}, aplicando fallback.")
            group_uvs = [[0.0, 0.0] for _ in group_vertices]

        geometry.add_attribute("vec2", "vertexUV", group_uvs)

        # Escolher o material certo
        if name in texture_map:
            material = TextureMaterial(texture_map[name])
        else:
            print(f"⚠️ Sem textura definida para: {name}")
            material = SurfaceMaterial(property_dict={"baseColor": [1.0, 0.0, 1.0]})  # Magenta

        mesh = Mesh(geometry, material)
        quarto.add(mesh)

    # ✅ Aplica a escala a todos os filhos corretamente
    for child in quarto.children_list:
        child.scale(sx)

    return quarto