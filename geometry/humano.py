from core_ext.object3d import Object3D
from core_ext.mesh import Mesh
from material.surface import SurfaceMaterial
from material.texture import TextureMaterial
from core_ext.texture import Texture
from geometry.geometry import Geometry

# Dicionário de cores RGB para cada parte do corpo
MATERIAL_COLORS = {
    "piel.002":      [1.0, 0.8, 0.6],
    "pelos.002":     [0.2, 0.1, 0.05],
    "gorrita.002":   [1.0, 0.0, 0.0],
    "remera.002":    [0.0, 0.0, 1.0],
    "zapatos.002":   [0.1, 0.1, 0.1],
    "ojos.002":      [0.8, 0.8, 1.0],
    "pupilas.004":   [0.0, 0.0, 0.0],
    "pupilas.005":   [0.0, 0.0, 0.0],
    "bordegorra.002":[0.5, 0.5, 0.5],
    "Material.001":  [1.0, 0.0, 1.0],
    
}

def parse_mtl_colors(mtl_path):
    colors = {}
    current = None
    with open(mtl_path, "r") as f:
        for line in f:
            if line.startswith("newmtl "):
                current = line.strip().split()[1]
            elif line.startswith("Kd ") and current:
                parts = line.strip().split()
                colors[current] = [float(parts[1]), float(parts[2]), float(parts[3])]
    return colors

def humanoGeometry(verticesHumano, texture_path=None, mtl_path=None):
    humano = Object3D()
    mtl_colors = {}
    if mtl_path:
        mtl_colors = parse_mtl_colors(mtl_path)

    for name, group_vertices, group_uvs in verticesHumano:
        geometry = Geometry()
        geometry.add_attribute("vec3", "vertexPosition", group_vertices)

        if not group_uvs or len(group_uvs) != len(group_vertices):
            group_uvs = [[0.0, 0.0] for _ in group_vertices]
        geometry.add_attribute("vec2", "vertexUV", group_uvs)

        if name in mtl_colors:
          color = mtl_colors[name]
          material = SurfaceMaterial(property_dict={"baseColor": color})
        else:
          material = SurfaceMaterial(property_dict={"baseColor": [1.0, 0.0, 1.0]})  # magenta para debug

        mesh = Mesh(geometry, material)
        humano.add(mesh)

    return humano