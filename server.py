import mesa
from model import Environment, Bot, Box, Goal, Pared, Camion, Bateria

from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer

# Definir colores específicos para los bots según su tipo de ruta
SHELF_COLOR = "blue"   # Color para los robots con rutas shelf_paths
BELT_COLOR = "green"   # Color para los robots con rutas belt_paths

def agent_portrayal(agent):
    if isinstance(agent, Bot):
        # Asigna color según el tipo de ruta que sigue el robot
        if agent.role == "shelf":
            color = SHELF_COLOR
        elif agent.role == "belt":
            color = BELT_COLOR
        else:
            color = "black"  # Color predeterminado si no tiene rol
        
        return {
            "Shape": "circle", 
            "Filled": "false", 
            "Color": color, 
            "Layer": 1, 
            "r": 1.0,
            "text": "🤖", 
            "text_color": "black"
        }
    elif isinstance(agent, Box):
        return {"Shape": "rect", "Filled": "true", "Layer": 0, "w": 0.9, "h": 0.9, "text_color": "Black",
                "Color": "moccasin", "text": "📦"}
    elif isinstance(agent, Goal):
        return {"Shape": "rect", "Filled": "true", "Layer": 0, "w": 1, "h": 1, "text_color": "Black",
                "Color": "White", "text": "️⛳️"}
    elif isinstance(agent, Pared):
        return {"Shape": "rect", "Filled": "true", "Layer": 0, "w": 0.9, "h": 0.9, "text_color": "Black",
                "Color": "Gray", "text": "🗿"}
    elif isinstance(agent, Camion):
        return {"Shape": "rect", "Filled": "true", "Layer": 0, "w": 0.9, "h": 0.9, "text_color": "Black",
                "Color": "#008000", "text": "🚛"}
    elif isinstance(agent, Bateria):
        return {"Shape": "rect", "Filled": "true", "Layer": 0, "w": 0.9, "h": 0.9, "text_color": "Black",
                "Color": "aquamarine", "text": "🔋"}
    else:
        return {"Shape": "rect", "Filled": "true", "Layer": 0, "w": 0.9, "h": 0.9, "text_color": "Black",
                "Color": "white", "text": ""}

# Define paths for the bots to follow (example paths)
"""
shelf_paths = [
    [(4, 15), (6, 15), (7, 15), (8, 15)],
    [(4, 14), (7, 14), (8, 14), (9, 14)],  # No colisiona en la última coordenada
    [(4, 13), (6, 13), (7, 14), (8, 14)]   # No colisiona en la última coordenada
]

belt_paths = [
    [(3, 12), (6, 10), (7, 10), (8, 10)],
    [(2, 12), (7, 9), (9, 9), (10, 9)],     # No colisiona en la última coordenada
    [(1, 12), (6, 8), (9, 9), (9, 10)]       # No colisiona en la última coordenada
]
"""
shelf_paths = [
    [(5, 15), (5, 17), (16, 17),
     (5, 17), (5, 11), (4, 11), (4, 11), (4, 8), (2, 8)], #Rojo
    
    [(5, 14), (6, 14), (6, 13),(16, 13),
     (5, 17), (5, 13), (5, 8), (5, 9), (1, 9), (1, 8)], #Azul
    
    [(5, 13), (5, 9), (8, 9), (8, 2), (16, 2),
     (8, 2), (8, 8), (5, 8), (5, 9), (1, 9), (1, 8)]  #Verde
    
]
    # Rutas de Bots que se mueven hacia las bandas transportadoras
belt_paths = [
    [(1, 11), (1, 8), (1, 9), (10, 9), (10, 6), (16, 6),
     (9, 6), (9, 10), (1, 10), (1, 8)], #Morado
    
    [(2, 11), (1, 11), (1, 8), (3, 8), (3, 9), (16, 9),
     (9, 9), (9, 10), (1, 10), (1, 8)], #Rosa
    
    [(3, 11), (2, 11), (2, 8), (3, 8), (3, 10), (16, 10),
     (1, 10), (1, 8)] #Amarillo

]

# Definir ubicaciones iniciales para los robots
initial_positions = [
    (4, 15),  # Robot 1 (shelf_paths)
    (4, 14),  # Robot 2 (shelf_paths)
    (4, 13),  # Robot 3 (shelf_paths)
    (3, 12),  # Robot 4 (belt_paths)
    (2, 12),   # Robot 5 (belt_paths)
    (1, 12)    # Robot 6 (belt_paths)
]

grid = mesa.visualization.CanvasGrid(agent_portrayal, 20, 20, 700, 600)

server = ModularServer(
    Environment,
    [grid],
    "Warehouse Robots",
    {"width": 20, "height": 20, "shelf_paths": shelf_paths, "belt_paths": belt_paths, "initial_positions": initial_positions}
)

server.port = 8521
server.launch()