import mesa
from model import Environment, Bot, Box, Goal, Pared, Camion, Bateria

from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from model import Environment

BOT_COLORS = ["red", "blue", "green", "purple", "Darksalmon", "Khaki"]  # Definir colores para los bots

def agent_portrayal(agent):
    if isinstance(agent, Bot):
        return {"Shape": "circle", "Filled": "false", "Color": BOT_COLORS[agent.unique_id - 1], "Layer": 1, "r": 1.0,
                "text": "🤖", "text_color": "black"}
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
    # Rutas de Bots que se mueven hacia estante
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

grid = mesa.visualization.CanvasGrid(
    agent_portrayal, 20, 20, 700, 600)

server = ModularServer(
    Environment,
    [grid],
    "Warehouse Robots",
    {"width": 20, "height": 20, "shelf_paths": shelf_paths, "belt_paths": belt_paths}
)

server.port = 8521
server.launch()