from typing import List, Tuple

def my_obj_reader(filename: str) -> List[Tuple[str, List[List[float]], List[List[float]]]]:
    """Lê os vértices e UVs do ficheiro .obj e agrupa-os por nome de material."""
    grouped_data = []
    is_humano = "human" in filename or "humano" in filename
    current_object = "Default"
    vertices = []
    uvs = []

    vertex_lookup = []
    uv_lookup = []

    with open(filename, 'r') as in_file:
        for line in in_file:
            if line.startswith('v '):
                point = [float(value) for value in line.strip().split()[1:]]
                vertex_lookup.append(point)
            elif line.startswith('vt '):
                tex = [float(value) for value in line.strip().split()[1:]]
                uv_lookup.append(tex)
            elif is_humano and line.startswith('usemtl '):
                if vertices:
                    grouped_data.append((current_group, vertices, uvs))
                current_group = line.strip().split()[1]
                vertices = []
                uvs = []
            elif not is_humano and line.startswith('o '):  # usa o nome do objeto em vez do material
                if vertices:
                    grouped_data.append((current_object, vertices, uvs))
                current_object = line.strip().split()[1]
                vertices = []
                uvs = []
            elif line.startswith('f '):
                face_data = line.strip().split()[1:]
                for item in face_data:
                    indices = item.split('/')
                    v_idx = int(indices[0]) - 1
                    vt_idx = int(indices[1]) - 1 if len(indices) > 1 and indices[1] else None

                    if 0 <= v_idx < len(vertex_lookup):
                        vertices.append(vertex_lookup[v_idx])
                        if vt_idx is not None and 0 <= vt_idx < len(uv_lookup):
                            uvs.append(uv_lookup[vt_idx])
                        else:
                            # fallback UV: mapeamento automático
                            uvs.append([0.0, 0.0])
                    else:
                        print(f"[Aviso] Índice fora do alcance: {v_idx}")

    if vertices:
        grouped_data.append((current_object, vertices, uvs))

    return grouped_data
