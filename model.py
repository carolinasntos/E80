from mesa import Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from mesa.agent import Agent

class Bot(Agent):
    def __init__(self, unique_id, model, path, role):
        super().__init__(unique_id, model)
        self.path = path
        self.role = role
        self.current_step = 0

    def step(self):
        if self.current_step < len(self.path):
            new_position = self.path[self.current_step]
            self.model.grid.move_agent(self, new_position)
            self.current_step += 1

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

    def __init__(self, width, height, shelf_paths, belt_paths):
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        self.width = width
        self.height = height

        self.shelf_paths = shelf_paths
        self.belt_paths = belt_paths

        self.build_environment()
        self.create_bots()

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
        # Crear bots que se mueven hacia estantes
        for i, path in enumerate(self.shelf_paths):
            bot = Bot(i + 1, self, path, role="shelf")
            self.grid.place_agent(bot, path[0])
            self.schedule.add(bot)

        # Crear bots que se mueven hacia la banda
        for i, path in enumerate(self.belt_paths):
            bot = Bot(i + len(self.shelf_paths) + 1, self, path, role="belt")
            self.grid.place_agent(bot, path[0])
            self.schedule.add(bot)

    def step(self):
        self.schedule.step()
        
        
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
