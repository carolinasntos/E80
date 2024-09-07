import random
from mesa import Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from mesa.agent import Agent

import json

class CentralSystem:
    def __init__(self, model):
        self.model = model
        self.robot_data = {}  # Para almacenar datos de los robots
        # Colas circulares para las rutas adicionales
        self.shelf_paths_queue = list(model.shelf_paths)
        self.belt_paths_queue = list(model.belt_paths)
        self.initial_routes_assigned = {}
    """
    def track_movement(self, bot, wait=False):
        #Registrar el movimiento del robot en el formato adecuado
        next_position = bot.get_next_position()
        
        # Lista de coordenadas que se consideran un "goal"
        goal_positions = [(14, 17), (10, 14), (15, 13), (11, 10), (12, 9), (13, 6), (12, 5), (12, 2)]
        
        if next_position:  # Verificar que get_next_position no devuelva None
            x, y = next_position
            
            # Verificar si la posición actual está en la lista de posiciones objetivo
            goal = (x, y) in goal_positions
            
            self.robot_data[bot.unique_id]["path"].append({
                "x": x,
                "y": y,
                "wait": wait,
                "goal": goal  # True si la posición es una de las dadas, False si no
            })
        else:
            print(f"El robot {bot.unique_id} no tiene más movimientos.")
    """
    
    def track_movement(self, bot, wait=False, custom_position=None):
        """ Registrar el movimiento del robot en el formato adecuado """
        # Usar custom_position si el bot está esperando en su lugar
        next_position = custom_position if custom_position is not None else bot.get_next_position()
        
        if next_position:  # Verificar que get_next_position no devuelva None
            x, y = next_position
            goal_positions = [(14, 17), (10, 14), (15, 13), (11, 10), (12, 9), (13, 6), (12, 5), (12, 2)]
            goal = (x, y) in goal_positions
            
            self.robot_data[bot.unique_id]["path"].append({
                "x": x,
                "y": y,
                "wait": wait,
                "goal": goal  # True si la posición es una de las dadas, False si no
            })
        else:
            print(f"El robot {bot.unique_id} no tiene más movimientos.")

    def assign_initial_route(self, bot):
        if bot.role == "shelf":
            initial_route = self.model.initial_shelf_routes[bot.unique_id - 1]
        elif bot.role == "belt":
            initial_route = self.model.initial_belt_routes[bot.unique_id - 4]

        bot.path = initial_route
        self.initial_routes_assigned[bot.unique_id] = True
        # Guardar posición inicial
        self.robot_data[bot.unique_id] = {
            "spawnPosition": {"x": self.model.initial_positions[bot.unique_id - 1][0], "y": self.model.initial_positions[bot.unique_id - 1][1]},
            "path": []
        }
        print(f"Asignando ruta inicial a robot {bot.unique_id}: {bot.path}")

    def assign_additional_route(self, bot):
        if not hasattr(self, 'assigned_paths'):
            # Inicializar el registro de rutas asignadas si no existe
            self.assigned_paths = set()

        if bot.role == "shelf":
            if len(self.shelf_paths_queue) == 0:
                self.shelf_paths_queue = list(self.model.shelf_paths)

            # Verificar que la ruta no esté asignada
            available_route = None
            while self.shelf_paths_queue:
                potential_route = self.shelf_paths_queue.pop(0)
                if tuple(potential_route) not in self.assigned_paths:
                    available_route = potential_route
                    break

            if available_route:
                bot.path = available_route
                self.assigned_paths.add(tuple(bot.path))  # Registrar la ruta asignada
                print(f"Asignando nueva ruta a robot {bot.unique_id} (shelf): {bot.path}")
            else:
                print(f"No hay rutas disponibles para robot {bot.unique_id} (shelf)")

        elif bot.role == "belt":
            if len(self.belt_paths_queue) == 0:
                self.belt_paths_queue = list(self.model.belt_paths)

            # Verificar que la ruta no esté asignada
            available_route = None
            while self.belt_paths_queue:
                potential_route = self.belt_paths_queue.pop(0)
                if tuple(potential_route) not in self.assigned_paths:
                    available_route = potential_route
                    break

            if available_route:
                bot.path = available_route
                self.assigned_paths.add(tuple(bot.path))  # Registrar la ruta asignada
                print(f"Asignando nueva ruta a robot {bot.unique_id} (belt): {bot.path}")
            else:
                print(f"No hay rutas disponibles para robot {bot.unique_id} (belt)")

    def manage_routes(self, bot):
        if bot.unique_id not in self.initial_routes_assigned:
            self.assign_initial_route(bot)
        else:
            self.assign_additional_route(bot)

    """
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
                        # Añadir dos veces su mismo lugar de espera
                        agent.wait_positions = [position, position]  # Lista con dos veces la misma posición
                        self.track_movement(agent, wait=True)  # Registrar movimiento con espera
            else:
                # Solo hay un bot, este sigue sin esperar
                agents[0].should_wait = False
                self.track_movement(agents[0], wait=False)  # Registrar movimiento sin espera
    """
    
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
                        self.track_movement(agent, wait=True)  # Registrar movimiento con espera
            else:
                # Solo hay un bot, este sigue sin esperar
                agents[0].should_wait = False
                self.track_movement(agents[0], wait=False)  # Registrar movimiento sin espera

        
    def save_simulation_data(self, filename="simulation_data.json"):
        """ Guardar los datos de la simulación en formato JSON """
        with open(filename, 'w') as f:
            json.dump({"robots": list(self.robot_data.values())}, f, indent=4)
        print(f"Datos de la simulación guardados en {filename}")

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
    
    def get_target_position(self):
        # Devuelve la última posición de la ruta como el destino
        if len(self.path) > 0:
            return self.path[-1]  # Última posición como objetivo final
        return None  # Si no hay ruta, no hay objetivo

    def step(self):
        if not self.should_wait and self.current_step < len(self.path):
            next_position = self.get_next_position()
            if next_position:  # Verificar que exista la siguiente posición
                print(f"Robot {self.unique_id} ({self.role}) moviéndose a {next_position}")
                self.model.grid.move_agent(self, next_position)  # Mover el robot
                self.current_step += 1  # Avanzar al siguiente paso en el path
        else:
            if self.current_step >= len(self.path):  # Si ya completó su ruta
                print(f"Robot {self.unique_id} ({self.role}) completó su ruta. Asignando nueva ruta.")
                self.model.central_system.manage_routes(self)  # Gestionar la nueva ruta
                self.current_step = 0  # Reiniciar el paso actual
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
        'PXXXFFFFFFFFFFFFFFFP',
        'PFFFFFFFFFFFFFFFFFFP',
        'PFFFFFFFFBBBBBBBBFFP',
        'PFFFFFFFFBBBBBBBBFFP',
        'PFFFFFFFFFFFFFFFFFFP',
        'PFFFFFFFFFFFFFFFFFFP',
        'PFFFFFFFFFFFFFFFFFFP',
        'PFFFFFFFFFFFFFFFFFFP',
        'PFFFFFFFFFFBBBBBBFFP',
        'PCCPCCPPFFFBBBBBBFFP',
        'FCCFCCFPFFFFFFFFFFFP',
        'FCCFCCFPFFFFFFFFFFFP',
        'FFFFFFFPFFFFFFFFFFFP',
        'FFFFFFFPFFFFFFFFFFFP',
        'FFFFFFFPFFFBBBBBBFFP',
        'FFFFFFFPFFFBBBBBBFFP',
        'FFFFFFFPFFFFFFFFFFFP',
        'FFFFFFFPFFFFFFFFFFFP',
        'FFFFFFFPPPPPPPPPPPPP'
    ]
    
    def __init__(self, width, height, shelf_paths, belt_paths, initial_positions, initial_shelf_routes, initial_belt_routes):
        super().__init__()
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        self.width = width
        self.height = height
        self.shelf_paths = shelf_paths
        self.belt_paths = belt_paths
        self.initial_positions = initial_positions
        self.initial_shelf_routes = initial_shelf_routes
        self.initial_belt_routes = initial_belt_routes
        self.current_step = 0
        self.max_steps = 100  # Limitar la simulación a 100 pasos

        self.central_system = CentralSystem(self)

        self.build_environment()
        self.create_bots()

    def step(self):
        if self.current_step < self.max_steps:
            print(f"Step {self.current_step + 1}")
            self.central_system.check_collisions()
            self.schedule.step()
            self.current_step += 1
        else:
            print("Simulación terminada. Se alcanzó el límite de 50 steps.")
            self.running = False
            self.central_system.save_simulation_data("simulation_data.json")

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
            self.central_system.manage_routes(bot)  # Llama a 'manage_routes' en lugar de 'assign_route'
            self.grid.place_agent(bot, self.initial_positions[i])
            self.schedule.add(bot)
            print(f"Robot {bot.unique_id} asignado a 'shelf' con ruta: {bot.path}")  # Imprimir rol y ruta

        # Crear bots que se mueven hacia la banda (siguientes 3 robots)
        for i in range(3):  # Los siguientes 3 robots son 'belt'
            bot = Bot(i + 4, self, role="belt")  # Asigna rol 'belt'
            self.central_system.manage_routes(bot)  # Llama a 'manage_routes' en lugar de 'assign_route'
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