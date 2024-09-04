import random
from mesa import Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from mesa.agent import Agent

class CentralSystem:
    def __init__(self, model):
        self.model = model

    def assign_route(self, bot):
        if bot.role == "shelf":
            # Para robots shelf, el índice es el ID menos 1
            if bot.unique_id - 1 < len(self.model.shelf_paths):
                bot.path = self.model.shelf_paths[bot.unique_id - 1]
            else:
                bot.path = []  # Manejar casos donde no hay una ruta asignada
        elif bot.role == "belt":
            # Para robots belt, el índice debe restar 4 para coincidir con la lista belt_paths
            if bot.unique_id - 4 < len(self.model.belt_paths):
                bot.path = self.model.belt_paths[bot.unique_id - 4]
            else:
                bot.path = []  # Manejar casos donde no hay una ruta asignada

    def check_collisions(self):
        collision_map = {}

        # Iterar sobre todos los bots en la simulación
        for agent in self.model.schedule.agents:
            if isinstance(agent, Bot):
                next_position = agent.get_next_position()

                if next_position in collision_map:
                    collision_map[next_position].append(agent)  # Añadir bot al mismo lugar
                else:
                    collision_map[next_position] = [agent]

        # Resolver colisiones
        for position, agents in collision_map.items():
            if len(agents) > 1:
                # Hay más de un bot en esta posición, resolver la colisión aleatoriamente
                chosen_agent = random.choice(agents)  # Elegir aleatoriamente quién sigue
                for agent in agents:
                    if agent == chosen_agent:
                        agent.should_wait = False  # El elegido no espera
                    else:
                        agent.should_wait = True  # Los demás esperan
            else:
                # Solo hay un bot, este sigue sin esperar
                agents[0].should_wait = False

class Bot(Agent):
    def __init__(self, unique_id, model, role):
        super().__init__(unique_id, model)
        self.path = []
        self.role = role
        self.current_step = 0
        self.should_wait = False  # Indica si el bot debe esperar

    def get_next_position(self):
        if self.current_step < len(self.path):
            return self.path[self.current_step]
        return None

    def step(self):
        if not self.should_wait and self.current_step < len(self.path):
            next_position = self.get_next_position()
            if next_position:  # Verificar que exista la siguiente posición
                print(f"Robot {self.unique_id} ({self.role}) moviéndose a {next_position}")
                self.model.grid.move_agent(self, next_position)  # Mover el robot
                self.current_step += 1  # Avanzar al siguiente paso en el path
        else:
            print(f"Robot {self.unique_id} ({self.role}) está esperando o no tiene más pasos")

class Environment(Model):
    DEFAULT_MODEL_DESC = [
        'PPPPPPPPPPPPPPPPPPPP',
        'PPPPFFFFFFFFFFFFFFFP',
        'PPPPFFFFFFFFFFFFFFFP',
        'PPPPFFFFBBBBBBBBBFFP',
        'PPPPXFFFBBBBBBBBBFFP',
        'PPPPXFFFFFFFFFFFFFFP',
        'PPPPXFFFFFFFFFFFFFFP',
        'PXXXFFFFFBBBBBBBBFFP',
        'PFFFFFFFFBBBBBBBBFFP',
        'PFFFFFFFFFFFFFFFFFFP',
        'PFFFFFFFFFFFFFFFFFFP',
        'PFFFFFFFFFFBBBBBBFFP',
        'PCCPCCPPFFFBBBBBBFFP',
        'FCCFCCFPFFFFFFFFFFFP',
        'FCCFCCFPFFFFFFFFFFFP',
        'FFFFFFFPFFFBBBBBBFFP',
        'FFFFFFFPFFFBBBBBBFFP',
        'FFFFFFFPFFFFFFFFFFFP',
        'FFFFFFFPFFFFFFFFFFFP',
        'FFFFFFFPPPPPPPPPPPPP'
    ]
    
    def __init__(self, width, height, shelf_paths, belt_paths, initial_positions):
        super().__init__()  # Inicializa la clase base Model
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        self.width = width  # Asigna width al objeto
        self.height = height  # Asigna height al objeto
        self.shelf_paths = shelf_paths
        self.belt_paths = belt_paths
        self.initial_positions = initial_positions

        # Crear el sistema central
        self.central_system = CentralSystem(self)

        self.build_environment()
        self.create_bots()

    def step(self):
        print("Avanzando un paso en la simulación")
        self.central_system.check_collisions()  # Revisa colisiones antes de mover
        self.schedule.step()  # Ejecuta un paso de la simulación

    def build_environment(self):
        for x in range(self.width):
            for y in range(self.height):
                cell_type = self.DEFAULT_MODEL_DESC[-y-1][x]
                if cell_type == 'P':
                    self.grid.place_agent(Pared(f"P-{x}-{y}", self), (x, y))
                elif cell_type == 'B':
                    self.grid.place_agent(Box(f"B-{x}-{y}", self), (x, y))
                elif cell_type == 'G':
                    self.grid.place_agent(Goal(f"G-{x}-{y}", self), (x, y))
                elif cell_type == 'C':
                    self.grid.place_agent(Camion(f"C-{x}-{y}", self), (x, y))
                elif cell_type == 'X':
                    self.grid.place_agent(Bateria(f"F-{x}-{y}", self), (x, y))

    def create_bots(self):
        # Crear bots que se mueven hacia estantes (primeros 3 robots)
        for i in range(3):  # Los primeros 3 robots son 'shelf'
            bot = Bot(i + 1, self, role="shelf")  # Asigna rol 'shelf'
            self.central_system.assign_route(bot)
            self.grid.place_agent(bot, self.initial_positions[i])
            self.schedule.add(bot)
            print(f"Robot {bot.unique_id} asignado a 'shelf' con ruta: {bot.path}")  # Imprimir rol y ruta

            # Crear bots que se mueven hacia la banda (siguientes 3 robots)
        for i in range(3):  # Los siguientes 3 robots son 'belt'
            bot = Bot(i + 4, self, role="belt")  # Asigna rol 'belt'
            self.central_system.assign_route(bot)
            self.grid.place_agent(bot, self.initial_positions[i + 3])
            self.schedule.add(bot)
            print(f"Robot {bot.unique_id} asignado a 'belt' con ruta: {bot.path}")  # Imprimir rol y ruta

class Box(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

class Goal(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

class Pared(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

class Camion(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

class Bateria(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)