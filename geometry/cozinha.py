from core_ext.object3d import Object3D
from core_ext.mesh import Mesh
from material.texture import TextureMaterial
from core_ext.texture import Texture
from geometry.geometry import Geometry
from material.surface import SurfaceMaterial

def cozinhaGeometry(scale, verticesCozinha):
    cozinha = Object3D()

    # Mapeamento de texturas por nome de objeto (ajuste conforme suas texturas reais)
    texture_map = {
        # Estrutura
        "Parede1": Texture("images/kitchen_scene/parede.jpg"),
        "Parede2": Texture("images/kitchen_scene/parede.jpg"),
        "Parede3": Texture("images/kitchen_scene/parede2.jpg"),
        "Teto": Texture("images/kitchen_scene/teto.jpg"),
        "PlacaFogao": Texture("images/kitchen_scene/fogao.jpg"),
        "Box002": Texture("images/kitchen_scene/mesa.jpg"),
        "Chao": Texture("images/kitchen_scene/chao.jpg"),
        "LinhasDaCozinha": Texture("images/kitchen_scene/parede.jpg"),

        # Armários
        "BalcaoCozinha": Texture("images/kitchen_scene/fogao.jpg"),
        "Armarios2": Texture("images/kitchen_scene/armario.jpg"),
        "Armario1": Texture("images/kitchen_scene/armario.jpg"),

        # Pias
        "KitchenSink1": Texture("images/kitchen_scene/eletrodomestico.jpg"),
        "KitchenSink2": Texture("images/kitchen_scene/eletrodomestico.jpg"),
        "Door_handle_02": Texture("images/kitchen_scene/inox.jpg"),

        # Eletrodomésticos
        "electrolux_2_Part_2": Texture("images/kitchen_scene/fogao.jpg"),
        "Technology_set_by_Miele_Part_6": Texture("images/kitchen_scene/eletrodomestico.jpg"),
        "Technology_set_by_Miele_Part_17": Texture("images/kitchen_scene/eletrodomestico.jpg"),
        "Frigorifico": Texture("images/kitchen_scene/eletrodomestico.jpg"),

        # Decoracao
        "Kuvshin_i_stakan_ALPHA_amethyst_Lobmeyr_Part_2": Texture("images/kitchen_scene/porcelana.jpg"),
        "Kuvshin_i_stakan_ALPHA_amethyst_Lobmeyr_Part_3": Texture("images/kitchen_scene/porcelana.jpg"),
        "Kuvshin_i_stakan_ALPHA_amethyst_Lobmeyr_Part_4": Texture("images/kitchen_scene/porcelana.jpg"),
        "DecoracaoBalcao1": Texture("images/kitchen_scene/porcelana.jpg"),

        # Apoios de pratos (Box)
        "Box006": Texture("images/kitchen_scene/box.jpg"),
        "Box007": Texture("images/kitchen_scene/box.jpg"),
        "Box008": Texture("images/kitchen_scene/box.jpg"),
        "Box009": Texture("images/kitchen_scene/box.jpg"),
        "Box010": Texture("images/kitchen_scene/box.jpg"),
        "Box011": Texture("images/kitchen_scene/box.jpg"),

        # Mesa
        "stol_obed_170_neras_3_Part_2": Texture("images/kitchen_scene/mesa.jpg"),
        "stol_obed_170_neras_3_Part_3": Texture("images/kitchen_scene/mesa.jpg"),
        "stol_obed_170_neras_3_Part_4": Texture("images/kitchen_scene/mesa.jpg"),
        "stol_obed_170_neras_3_Part_5": Texture("images/kitchen_scene/mesa.jpg"),
        "stol_obed_170_neras_3_Part_6": Texture("images/kitchen_scene/mesa.jpg"),
        "stol_obed_170_neras_3_Part_7": Texture("images/kitchen_scene/mesa.jpg"),
        "stol_obed_170_neras_3_Part_8": Texture("images/kitchen_scene/mesa.jpg"),
        "stol_obed_170_neras_3_Part_9": Texture("images/kitchen_scene/mesa.jpg"),
        "stol_obed_170_neras_3_Part_10": Texture("images/kitchen_scene/mesa.jpg"),
        "stol_obed_170_neras_3_Part_11": Texture("images/kitchen_scene/mesa.jpg"),

        # Cadeiras (Douglas)
        "Douglas_Part_4": Texture("images/kitchen_scene/mesa.jpg"),
        "Douglas_Part_007": Texture("images/kitchen_scene/mesa.jpg"),
        "Douglas_Part_016": Texture("images/kitchen_scene/mesa.jpg"),
        "Douglas_Part_019": Texture("images/kitchen_scene/mesa.jpg"),
        "Douglas_Part_022": Texture("images/kitchen_scene/mesa.jpg"),
        "Douglas_Part_025": Texture("images/kitchen_scene/mesa.jpg"),

        # Utensílios (Kitchen_utensils_Part_2 a Part_16)
        **{f"Kitchen_utensils_Part_{i}": Texture("images/kitchen_scene/inox.jpg") for i in range(2, 17)}
    }

    # Material genérico para o restante
    textura_vidro = Texture("images/kitchen_scene/fogao.jpg")
    textura_generica = Texture("images/kitchen_scene/generica.jpg")
    textura_inox = Texture("images/kitchen_scene/inox.jpg")
    textura_porcelana = Texture("images/kitchen_scene/porcelana.jpg")
    textura_fogao = Texture("images/kitchen_scene/fogao.jpg")


    for name, group_vertices, group_uvs in verticesCozinha:
        geometry = Geometry()
        geometry.add_attribute("vec3", "vertexPosition", group_vertices)

        if not group_uvs or len(group_uvs) != len(group_vertices):
            print(f"⚠️ UVs ausentes ou inválidas em {name}, aplicando fallback.")
            group_uvs = [[0.0, 0.0] for _ in group_vertices]

        geometry.add_attribute("vec2", "vertexUV", group_uvs)

        # Escolha da textura
        # pratos e copos porcelana
        if name in [
            "luminarc_Rubans_final_Part_46", "luminarc_Rubans_final_Part_48", "luminarc_Rubans_final_Part_52", "luminarc_Rubans_final_Part_53",
            "luminarc_Rubans_final_Part_060", "luminarc_Rubans_final_Part_061", "luminarc_Rubans_final_Part_062", "luminarc_Rubans_final_Part_063",
            "luminarc_Rubans_final_Part_070", "luminarc_Rubans_final_Part_071", "luminarc_Rubans_final_Part_072", "luminarc_Rubans_final_Part_073",
            "luminarc_Rubans_final_Part_080", "luminarc_Rubans_final_Part_081", "luminarc_Rubans_final_Part_082", "luminarc_Rubans_final_Part_083",
            "luminarc_Rubans_final_Part_090", "luminarc_Rubans_final_Part_091", "luminarc_Rubans_final_Part_092", "luminarc_Rubans_final_Part_093",
            "luminarc_Rubans_final_Part_100", "luminarc_Rubans_final_Part_101", "luminarc_Rubans_final_Part_102", "luminarc_Rubans_final_Part_103"
        ]:
            material = TextureMaterial(textura_porcelana)

        # talheres inox
        elif name in [
            "luminarc_Rubans_final_Part_54", "luminarc_Rubans_final_Part_55", "luminarc_Rubans_final_Part_56", "luminarc_Rubans_final_Part_57", "luminarc_Rubans_final_Part_58", "luminarc_Rubans_final_Part_59",
            "luminarc_Rubans_final_Part_064", "luminarc_Rubans_final_Part_065", "luminarc_Rubans_final_Part_066", "luminarc_Rubans_final_Part_067", "luminarc_Rubans_final_Part_068", "luminarc_Rubans_final_Part_069",
            "luminarc_Rubans_final_Part_074", "luminarc_Rubans_final_Part_075", "luminarc_Rubans_final_Part_076", "luminarc_Rubans_final_Part_077", "luminarc_Rubans_final_Part_078", "luminarc_Rubans_final_Part_079",
            "luminarc_Rubans_final_Part_084", "luminarc_Rubans_final_Part_085", "luminarc_Rubans_final_Part_086", "luminarc_Rubans_final_Part_087", "luminarc_Rubans_final_Part_088", "luminarc_Rubans_final_Part_089",
            "luminarc_Rubans_final_Part_094", "luminarc_Rubans_final_Part_095", "luminarc_Rubans_final_Part_096", "luminarc_Rubans_final_Part_097", "luminarc_Rubans_final_Part_098", "luminarc_Rubans_final_Part_099",
            "luminarc_Rubans_final_Part_104", "luminarc_Rubans_final_Part_105", "luminarc_Rubans_final_Part_106", "luminarc_Rubans_final_Part_107", "luminarc_Rubans_final_Part_108", "luminarc_Rubans_final_Part_109"
        ]:
            material = TextureMaterial(textura_inox)
        elif name == "ODEON_LIGHT_3810-37L_3810-49L_Part_4":
            material = TextureMaterial(textura_porcelana)
        elif name.startswith("ODEON_LIGHT_3810-37L_3810-49L_"):
            material = TextureMaterial(textura_inox)
        elif name == "Lemonade_Part_126":
            material = TextureMaterial(textura_porcelana)
        elif name.startswith("Lemonade_Part_"):
            material = TextureMaterial(Texture("images/kitchen_scene/apple.jpg"))
        elif name.startswith("Vinnye_bokaly_raznoj_formy_"):
            material = TextureMaterial(textura_vidro)
        elif name in texture_map:
            material = TextureMaterial(texture_map[name])
        elif name in [
            "Door_handle_02", "Komponen09", "Komponen08", "Komponen05", "Komponen04",
            "Group70", "Mesh3021", "Mesh3020", "Mesh3019", "Mesh3018", "Mesh3017",
            "Mesh3016", "Mesh3015", "Mesh3014", "Mesh3013", "Mesh3012", "Mesh3011",
            "Mesh3010", "Mesh3009", "Mesh3008", "Mesh3078", "Mesh3077", "Mesh3076",
            "Mesh3075", "Mesh3074", "Mesh3073", "Mesh3072", "Mesh3071", "Mesh3070",
            "Mesh3069", "Mesh3068", "Mesh3067", "Mesh3066", "Mesh3065", "Group47",
            "Mesh3035", "Mesh3034", "Mesh3033", "Mesh3032", "Mesh3031", "Mesh3030",
            "Mesh3029", "Mesh3028", "Mesh2966", "Mesh2965", "Mesh2968", "Mesh2967",
            "Mesh2978", "Mesh2977", "Mesh2976", "Mesh2975", "Mesh2971", "Mesh2970",
            "Mesh2969", "Mesh2974", "Mesh2973", "Mesh2972", "Mesh3143", "Mesh3142",
            "Mesh3141", "Mesh3140", "Mesh3139", "Mesh3138", "Mesh3137", "Mesh3136",
            "Mesh3135", "Mesh3134", "Mesh3133", "Mesh3132", "Mesh3131", "Mesh3130",
            "Mesh3129", "Mesh3128", "Mesh1888", "Mesh1887", "Mesh1886", "Mesh1885",
            "Mesh1884", "Mesh1883", "Mesh1882", "Mesh1881", "Mesh1880", "Mesh1879",
            "Mesh1878", "Mesh1877", "Mesh1902", "Mesh1901", "Mesh1900", "Mesh1899",
            "Mesh1898", "Mesh1897", "Mesh1896", "Mesh1895", "Mesh1894", "Mesh1893",
            "Mesh1892", "Mesh1891", "Group65", "Mesh3092", "Mesh3091", "Mesh3090",
            "Mesh3089", "Mesh3088", "Mesh3087", "Mesh3086", "Mesh3085", "Mesh3084",
            "Mesh3083", "Mesh3102", "Mesh3101", "Mesh3100", "Mesh3099", "Mesh3098",
            "Mesh3097", "Mesh3096", "Mesh3095", "Mesh3094", "Mesh3093", "Mesh3114",
            "Mesh3113", "Mesh3112", "Mesh3111", "Mesh3110", "Mesh3109", "Mesh3108",
            "Mesh3107", "Mesh3106", "Mesh3105", "Mesh3124", "Mesh3123", "Mesh3122",
            "Mesh3121", "Mesh3120", "Mesh3119", "Mesh3118", "Mesh3117", "Mesh3116",
            "Mesh3115", "Mesh2964", "Mesh2963", "Mesh2962", "Mesh2961", "Mesh2960",
            "Mesh3127", "Mesh3126", "Mesh3125", "Mesh3025", "Mesh3024", "Mesh3023",
            "Mesh3022", "Mesh3082", "Mesh3081", "Mesh3080", "Mesh3079", "Mesh3027",
            "Mesh3026", "Mesh3104", "Mesh3103", "_009171_3_", "_009171_04",
            "121340_250", "121340_251", "121340_252", "121340_253",
            "_U392_2", "_U392_1", "Mesh3007", "Mesh3006", "Mesh3005", "Mesh3004",
            "Mesh3003", "Mesh3002", "Mesh3001", "Mesh3000", "Mesh2999", "Mesh2998",
            "Mesh2997", "Mesh2996", "Mesh2995", "Mesh2994", "Mesh2993", "Mesh2992",
            "Mesh2991", "Mesh2990", "Mesh2989", "Mesh2988", "Mesh2987", "Mesh2986",
            "Mesh2985", "Mesh2984", "Mesh2983", "Mesh2982", "Mesh2981", "Mesh2980",
            "Mesh2979", "_U392_4", "_U392_3", "Mesh3064", "Mesh3063", "Mesh3062",
            "Mesh3061", "Mesh3060", "Mesh3059", "Mesh3058", "Mesh3057", "Mesh3056",
            "Mesh3055", "Mesh3054", "Mesh3053", "Mesh3052", "Mesh3051", "Mesh3050",
            "Mesh3049", "Mesh3048", "Mesh3047", "Mesh3046", "Mesh3045", "Mesh3044",
            "Mesh3043", "Mesh3042", "Mesh3041", "Mesh3040", "Mesh3039", "Mesh3038",
            "Mesh3037", "Mesh3036", "Mesh1029", "Group42", "Mesh3157", "Mesh3156",
            "Mesh3155", "Mesh3154", "Mesh3153", "Mesh3152", "Mesh3151", "Mesh3150",
            "Mesh3149", "Mesh3148", "Mesh3147", "Mesh3146", "Mesh3145", "Mesh3144",
            "Mesh3212", "Mesh3211", "Mesh3210", "Mesh3209", "Mesh3208", "Mesh3207",
            "Mesh3206", "Mesh3205", "Mesh3204", "Mesh3203", "Mesh3202", "Mesh3201",
            "Mesh3198", "Mesh3197", "Mesh3196", "Mesh3195", "Mesh3194", "Mesh3193",
            "Mesh3192", "Mesh3191", "Mesh3190", "Mesh3189", "Mesh3188", "Mesh3187",
            "Mesh3184", "Mesh3183", "Mesh3182", "Mesh3181", "Mesh3180", "Mesh3179",
            "Mesh3178", "Mesh3177", "Mesh3176", "Mesh3175", "Mesh3174", "Mesh3173",
            "Mesh3170", "Mesh3169", "Mesh3168", "Mesh3167", "Mesh3166", "Mesh3165",
            "Mesh3164", "Mesh3163", "Mesh3162", "Mesh3161", "Mesh3160", "Mesh3159",
            "Mesh2958", "Mesh2957", "Mesh2956", "Mesh2955", "Mesh2954", "Mesh2953",
            "Mesh2952", "Mesh2951", "Mesh2950", "Mesh2949", "Mesh2948", "Mesh2947",
            "Mesh2944", "Mesh2943", "Mesh2942", "Mesh2941", "Mesh2940", "Mesh2939",
            "Mesh2938", "Mesh2937", "Mesh2936", "Mesh2935", "Mesh2934", "Mesh2933",
            "Group38", "Mesh1028"
        ]:
            material = TextureMaterial(textura_fogao)

        else:
            print(f"⚠️ Sem textura definida para: {name}")
            material = TextureMaterial(textura_generica)

        mesh = Mesh(geometry, material)
        cozinha.add(mesh)

    for child in cozinha.children_list:
        child.scale(scale)

    return cozinha