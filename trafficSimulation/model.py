from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from agent import *
import json
from g import gen_graph

class CityModel(Model):
    """ 
        Creates a model based on a city map.

        Args:
            N: Number of agents in the simulation
    """
    def __init__(self, N):

        # Load the map dictionary. The dictionary maps the characters in the map file to the corresponding agent.
        dataDictionary = json.load(open("city_files/mapDictionary.json"))

        self.traffic_lights = []
        self.obstacles = []
        self.graph = None

        # Load the map file. The map file is a text file where each character represents an agent.
        with open('city_files/t_base.txt') as baseFile:
            print(baseFile)
            lines = baseFile.readlines()
            # generate the graph gicen the city map
            self.graph = gen_graph(lines)
            # print(lines)
            self.width = len(lines[0])
            self.height = len(lines)

            self.grid = MultiGrid(self.width, self.height, torus = False) 
            self.schedule = RandomActivation(self)
            
            # place test car agent
            # c = Car(0, self)
            # self.grid.place_agent(c, (0,0))
            # self.schedule.add(c)
            

            # Goes through each character in the map file and creates the corresponding agent.
            for r, row in enumerate(lines):
                for c, col in enumerate(row):
                    if col in ["v", "^", ">", "<"]:
                        agent = Road(f"r_{r*self.width+c}", self, dataDictionary[col])
                        self.grid.place_agent(agent, (c, self.height - r - 1))

                    elif col in ["S", "s"]:
                        agent = Traffic_Light(f"tl_{r*self.width+c}", self, False if col == "S" else True, int(dataDictionary[col]))
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                        self.schedule.add(agent)
                        self.traffic_lights.append(agent)

                    elif col == "#":
                        agent = Obstacle(f"ob_{r*self.width+c}", self)
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                        self.obstacles.append((c, self.height - r - 1)) # adding all obstacle positions to a list to add costs to the a* algorithm

                    elif col == "D":
                        agent = Destination(f"d_{r*self.width+c}", self)
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                        if c == 3:
                            ca = Car((c, self.height - r - 1), r*c, self)
                            self.grid.place_agent(ca, (0,0))
                            self.schedule.add(ca)
                        

        self.num_agents = N
        self.running = True

    def step(self):
        '''Advance the model by one step.'''
        self.schedule.step()