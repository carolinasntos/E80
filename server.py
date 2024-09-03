import mesa
from model import Environment, Bot, Box, Goal, Pared, Camion, Bateria

from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from model import Environment

BOT_COLORS = ["red", "blue", "green", "purple"]  # Definir colores para los bots

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
shelf_paths = [
    [(1, 1), (2, 2), (3, 3)],
    [(1, 2), (2, 3), (3, 4)]
]

belt_paths = [
    [(1, 8), (2, 8), (3, 8)],
    [(1, 9), (2, 9), (3, 9)]
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