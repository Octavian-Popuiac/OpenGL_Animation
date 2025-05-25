from core_ext.object3d import Object3D
from core_ext.mesh import Mesh
from material.texture import TextureMaterial
from core_ext.texture import Texture
from geometry.geometry import Geometry
from material.surface import SurfaceMaterial  # Para debug

def sala_musicaGeometry(sx, sy, sz, verticesSala):
    sala = Object3D()

    # Mapear nomes diretamente para texturas (toda a cena, flauta, cello, harpa, tuba, etc.)
    texture_map = {
        # Cena
        "Cube": Texture("images/music_scene/piso.jpg"),
        "Plane.004": Texture("images/music_scene/tapete.jpg"),
        "Cube.002": Texture("images/music_scene/sofa.jpg"),
        "Cube.003": Texture("images/music_scene/sofa.jpg"),
        "Cube.012": Texture("images/music_scene/sofa.jpg"),
        "Cylinder.022": Texture("images/music_scene/mesa.jpg"),
        "Cube.001": Texture("images/music_scene/parede.jpg"),
        "Cube.007": Texture("images/music_scene/parede.jpg"),
        "Cube.008": Texture("images/music_scene/parede.jpg"),
        "Cube.009": Texture("images/music_scene/teto.jpg"),
        "Ceiling_Lamp_IKEA_NYMANE": Texture("images/music_scene/lampada.jpg"),
        "Plane": Texture("images/music_scene/cinzento.jpg"),
        "Plane.001": Texture("images/music_scene/cinzento.jpg"),
        "Plane.002": Texture("images/music_scene/cinzento.jpg"),
        "Plane.003": Texture("images/music_scene/cinzento.jpg"),
        "Plane.005": Texture("images/music_scene/cinzento.jpg"),
        "Cube.010": Texture("images/music_scene/parede.jpg"),
        "OutBoddy_Cube.002": Texture("images/music_scene/madeira_corpo.jpg"),
        "DoorBoddy_Cube.001": Texture("images/music_scene/madeira_corpo.jpg"),

        # Flauta
        "Cylinder.002": Texture("images/music_scene/madeira_arpa.jpg"),
        "Cylinder.005": Texture("images/music_scene/preto.jpg"),

        # Arpa – madeira
        "Cylinder.003": Texture("images/music_scene/madeira_arpa.jpg"),
        "Cylinder.001": Texture("images/music_scene/madeira_arpa.jpg"),
        "Cylinder.023": Texture("images/music_scene/madeira_arpa.jpg"),
        "Cylinder.007": Texture("images/music_scene/madeira_arpa.jpg"),
        "Cylinder.030": Texture("images/music_scene/madeira_arpa.jpg"),
        "Cube.004": Texture("images/music_scene/madeira_arpa.jpg"),
        "Cube.005": Texture("images/music_scene/madeira_arpa.jpg"),
        "Cube.006": Texture("images/music_scene/madeira_arpa.jpg"),

        # Arpa – metal
        "Cylinder.052": Texture("images/music_scene/metal.jpg"),
        "Cylinder.103": Texture("images/music_scene/metal.jpg"),
        "Cylinder.113": Texture("images/music_scene/metal.jpg"),
        **{f"Cylinder.{i}": Texture("images/music_scene/metal.jpg") for i in range(635, 660)},

        # Tuba
        "Tuba": Texture("images/music_scene/dourado.jpg"),

        # Cello
        "cello_body_cello_body": Texture("images/music_scene/madeira_corpo.jpg"),
        "cello_black_cello_black": Texture("images/music_scene/preto.jpg"),
        "cello_metal_cello_metal": Texture("images/music_scene/metal.jpg"),
        "knob1_knob1": Texture("images/music_scene/preto.jpg"),
        "knob2_knob2": Texture("images/music_scene/preto.jpg"),
        "knob3_knob3": Texture("images/music_scene/preto.jpg"),
        "knob4_knob4": Texture("images/music_scene/preto.jpg"),
        "string1_string1": Texture("images/music_scene/metal.jpg"),
        "string2_string2": Texture("images/music_scene/metal.jpg"),
        "string3_string3": Texture("images/music_scene/metal.jpg"),
        "string4_string4": Texture("images/music_scene/metal.jpg"),
    }

    # Construção da cena
    for name, group_vertices, group_uvs in verticesSala:
        geometry = Geometry()
        geometry.add_attribute("vec3", "vertexPosition", group_vertices)

        if not group_uvs or len(group_uvs) != len(group_vertices):
            print(f"⚠️ UVs ausentes ou inválidas em {name}, aplicando fallback.")
            group_uvs = [[0.0, 0.0] for _ in group_vertices]

        geometry.add_attribute("vec2", "vertexUV", group_uvs)

        # Aplica a textura se existir, ou usa magenta para debug
        if name in texture_map:
            material = TextureMaterial(texture_map[name])
        else:
            print(f"⚠️ Sem textura definida para: {name}")
            material = SurfaceMaterial(property_dict={"baseColor": [1.0, 0.0, 1.0]})

        mesh = Mesh(geometry, material)
        sala.add(mesh)

    # Aplica a escala
    for child in sala.children_list:
        child.scale(sx)

    return sala