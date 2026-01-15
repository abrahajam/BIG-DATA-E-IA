import osmnx as ox
import numpy as np
import rasterio
from rasterio import features
from rasterio.transform import from_origin
import matplotlib.pyplot as plt

# --- 1. CONFIGURACIÓN DEL ENTORNO (CONSTANTES) ---
print("--- Iniciando Configuración ---")

# Valores del Grid
BUILDING = 0      # Espacio no transitable (Negro)
ROAD_NORMAL = 1   # Calle transitable (Blanco)

# Configuración Geográfica (Lavapiés, Madrid)
LOCATION_POINT = (40.4087, -3.7005)
# Metros de radio alrededor del punto (Mapa de aprox 900x900m)
DIST_RADIO = 450

# --- CALIDAD VISUAL (ALTA DEFINICIÓN) ---
# 0.5 metros por pixel.
# Significa que un pixel representa una baldosa de 50x50cm.
CELL_SIZE = 0.5

# Ancho de la carretera en metros.
# Usamos un radio de 3.5m para que la calle total sea de 7 metros de ancho.
ROAD_BUFFER_METERS = 3.5


def generar_mapa_madrid_hd():
    # 1. DESCARGAR
    print(f"1. Descargando mapa de Madrid (Radio: {DIST_RADIO}m)...")
    graph = ox.graph_from_point(
        LOCATION_POINT, dist=DIST_RADIO, network_type='all')

    # 2. PROYECTAR
    # Importante: Convertir latitud/longitud a Metros reales (UTM)
    graph_proj = ox.project_graph(graph)

    # Extraer solo las "aristas" (calles)
    nodes, edges = ox.graph_to_gdfs(graph_proj)

    # 3. GEOMETRÍA
    print("2. Aplicando grosor a las calles para suavizar bordes...")
    # Convertimos las líneas finas en polígonos gruesos
    shapes_geometry = edges.geometry.buffer(ROAD_BUFFER_METERS)

    # 4. PREPARAR GRID
    # Calcular los límites totales del mapa en metros
    minx, miny, maxx, maxy = shapes_geometry.total_bounds

    # Calcular cuántos píxeles tendrá nuestra matriz final
    width = int((maxx - minx) / CELL_SIZE)
    height = int((maxy - miny) / CELL_SIZE)

    print(f"   Tamaño de la matriz resultante: {height}x{width} píxeles")

    # Crear la transformación (Matemáticas que vinculan GPS con Píxeles)
    transform = from_origin(minx, maxy, CELL_SIZE, CELL_SIZE)

    # 5. RASTERIZAR (PINTAR)
    print("3. Generando matriz binaria (Rasterizando)...")

    # Preparamos las formas para rasterio: (geometría, valor_a_pintar)
    shapes_to_burn = ((geom, ROAD_NORMAL) for geom in shapes_geometry)

    # Quemamos las calles en una matriz de ceros
    grid = features.rasterize(
        shapes=shapes_to_burn,
        out_shape=(height, width),
        transform=transform,
        fill=BUILDING,      # Fondo (Edificios)
        default_value=ROAD_NORMAL,  # Calles
        dtype=np.uint8
    )

    return grid


# --- EJECUCIÓN PRINCIPAL ---
if __name__ == "__main__":
    try:
        # Generar
        mapa = generar_mapa_madrid_hd()

        # Guardar archivo .npy para tu IA
        filename = "madrid_hd.npy"
        np.save(filename, mapa)
        print(f"\n✅ ¡LISTO! Mapa guardado como '{filename}'")

        # --- VISUALIZAR RESULTADO ---
        print("Mostrando vista previa (Cierra la ventana para terminar)...")
        plt.figure(figsize=(12, 12), dpi=100)  # Imagen grande

        # Usamos 'gray' (Negro=0, Blanco=1)
        plt.imshow(mapa, cmap='gray', origin='upper')

        plt.title(
            f"Grid Madrid HD (Lavapiés)\nResolución: {CELL_SIZE}m/px | Dim: {mapa.shape}")
        plt.axis('off')  # Quitar ejes para ver solo el mapa
        plt.tight_layout()
        plt.show()

    except Exception as e:
        print(f"\n❌ ERROR CRÍTICO:\n{e}")
        print("Revisa haber instalado las librerías: pip install osmnx geopandas rasterio numpy matplotlib")
