import requests
import json
from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from trafficSimulation.agent import *
import json
from trafficSimulation.g import gen_graph
import random

class CityModel(Model):
    """ 
        Creates a model based on a city map.

        Args:
            N: Number of agents in the simulation
    """
    def __init__(self):

        # Load the map dictionary. The dictionary maps the characters in the map file to the corresponding agent.
        dataDictionary = json.load(open("static/city_files/mapDictionary.json"))

        self.graph = None   
        self.traffic_lights = [] #List of traffic lights
        self.obstacles = [] #List of obstacles
        self.destination = [] #List of destinations
        self.ids = 0 #Initialize the IDs used for the cars
        self.index = 0 #The index for the spawn positions

        # Load the map file. The map file is a text file where each character represents an agent.
        with open('static/city_files/2023_base.txt') as baseFile:
            lines = baseFile.readlines()
            # generate the graph gicen the city map
            self.graph = gen_graph(lines)
            self.width = len(lines[0])
            self.height = len(lines)
            self.border = [(0,0), (0,24), (23,0), (23,24)]
            self.grid = MultiGrid(self.width, self.height, torus = False) 
            self.schedule = RandomActivation(self)

            dict_r = {}
            for r, row in enumerate(lines):
                dict_c = {}
                for c, col in enumerate(row):
                    dict_c[c] = col
                dict_r[r] = dict_c

            # Goes through each character in the map file and creates the corresponding agent.
            for r, row in enumerate(lines):
                for c, col in enumerate(row):
                    if col in ["v", "^", ">", "<"]:
                        agent = Road(f"r_{r*self.width+c}", self, dataDictionary[col])
                        self.grid.place_agent(agent, (c, self.height - r - 1))

                    elif col == "s":
                        agent = Traffic_Light(f"tl_{r*self.width+c}", self, True, int(dataDictionary[col]))
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                        self.schedule.add(agent)
                        self.traffic_lights.append(agent)
                        if c + 1 < 25 and c - 1 > -1: 
                            if dict_r[r][c + 1] == ">":
                                agent.direction = "right"
                            elif dict_r[r][c + 1] == "<":
                                agent.direction = "left"
                            elif dict_r[r][c - 1] == ">":
                                agent.direction = "right"
                            elif dict_r[r][c - 1] == "<":
                                agent.direction = "left"                    


                    elif col == "S":
                        agent = Traffic_Light(f"tl_{r*self.width+c}", self, False, int(dataDictionary[col]))
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                        self.schedule.add(agent)
                        self.traffic_lights.append(agent)
                        if r + 1 < 25 and r - 1 > -1: 
                            if dict_r[r + 1][c] == "v":
                                agent.direction = "down"
                            elif dict_r[r + 1][c] == "^":
                                agent.direction = "up"
                            elif dict_r[r - 1][c] == "v":
                                agent.direction = "down"
                            elif dict_r[r - 1][c] == "^":
                                agent.direction = "up"

                    elif col == "#":
                        agent = Obstacle(f"ob_{r*self.width+c}", self)
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                        self.obstacles.append((c, self.height - r - 1)) # adding all obstacle positions to a list to add costs to the a* algorithm

                    elif col == "D":
                        agent = Destination(f"d_{r*self.width+c}", self)
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                        self.destination.append((c, self.height - r - 1))

            #Initialize the first cars
            for i in range (4):
                self.spawn()
                
        # self.num_agents = N
        self.running = True
        self.steps = 0 #Steps taken
        self.arrived = 0 #Total Cars that arrived

    #Function to generate positions for cars to spawn in
    def pos_gen(self):
        Flag1=True
        print(self.index)
        if self.index == 3:
            self.index -= 3
        elif self.index < 3:
            self.index +=1
        check = self.grid.get_cell_list_contents(self.border[self.index])
        for element in check:
            if isinstance(element, Car):
                Flag1=False
        if Flag1:
            return self.border[self.index]
        else:
            return False

    #Function to create cars
    def spawn(self):
        pos = self.pos_gen()
        if pos is not False:
            self.ids += 1
            a = Car(self.ids, self) 
            self.schedule.add(a)
            self.grid.place_agent(a, pos)

    def step(self):
        
        self.steps += 1
        print(self.arrived)
        print(self.steps)
        #Every ten steps new cars spawn
        if self.steps % 6 == 0:
            self.arrived += 2
            for i in range(4):
                self.spawn()
        self.schedule.step()
        
        if self.steps % 100 == 0:
            
            url = "http://52.1.3.19:8585/api/"
            endpoint = "attempts"

            data = {
                "year" : 2023,
                "classroom" : 302,
                "name" : "Santiago y Sergio",
                "num_cars": self.arrived
            }

            headers = {
                "Content-Type": "application/json"
            }

            response = requests.post(url+endpoint, data=json.dumps(data), headers=headers)

            print("Request " + "successful" if response.status_code == 200 else "failed", "Status code:", response.status_code)
            print("Response:", response)
        if self.steps % 1000 == 0:
            self.running = False
        # check if cars are cras
        # for a_list,b in self.grid.coord_iter():
        #     for agent in a_list:
        #         c = 0
        #         if isinstance(agent, Car):
        #             c+=1
        #     if c > 1:
        #         print("estan chocando")
        #         self.running = False
        #         return
        #     else:
        #         print("fine")