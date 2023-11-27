from mesa import Agent
import networkx as nx
import random

class Car(Agent):
    """
    Agent that moves randomly.
    Attributes:
        unique_id: Agent's ID 
        direction: Randomly chosen direction chosen from one of eight directions
    """
    def __init__(self, unique_id, model):
        """
        Creates a new random agent.
        Args:
            unique_id: The agent's ID
            model: Model reference for the agent
        """
        super().__init__(unique_id, model)
        self.current_direction = None # save the current car's direction
        self.next_pos = None
        self.path = None # agent path
        self.destination = self.goal() #Car destination
        self.can_move = True

    #Function to determine the destination of the car   
    def goal(self):
        index = random.randint(0, len(self.model.destination) - 1)
        return self.model.destination[index]
    

    def move(self):
        """ 
        Determines if the agent can move in the direction that was chosen
        """        
        
        # check if agent has crashed
        for a in self.model.grid.get_cell_list_contents(self.pos):
            c = 0
            if isinstance(a, Car):
                c+=1
        
        # print("this is c")
        # print(c)
        if c>1:
            print(f"crashing at pos {self.pos}")
            
            return
        
       
        # check if car agent has reached destination 
        if self.pos == self.destination:
            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)
            return
        
        # Check if agent has no path
        if self.path is None:
            # calculate path
            path = self.find_path(self.pos, self.destination)
            self.path = path
            
        # verify if the next position is defined
        if self.next_pos is None:
            # get next position
            self.next_pos = self.find_next_pos()
            
            while self.next_pos == self.pos:
                self.next_pos = self.find_next_pos()
                
            return
        
        # validate if the agent can move to that position
        else:
            
             # check if there is a stoplight in the next cell of the current direction
            for agent in self.model.grid.get_cell_list_contents(self.next_pos):
                # check if it is a stoplight 
                if isinstance(agent, Traffic_Light):
                    if not agent.state: # Do not move if stoplight is red
                        self.can_move = False
                    else:
                        self.can_move = True
                    
            # move car agent   
            if self.is_valid_pos(self.next_pos) and self.can_move:
                self.model.grid.move_agent(self, self.next_pos)
                self.next_pos = None
        
       
        
        # # check if current direction of the car is not None (This happens when car agent is in a cell where there is also a Traffic Light agent)
        # if self.current_direction is not None:
        #     next_pos = self.find_next_pos(self.current_direction)
        #     if self.is_valid_pos(next_pos): # validate next position
        #         self.model.grid.move_agent(self, next_pos)
        #         self.current_direction = None
        #     return
        
        # # find direction to move based on the current position of the car agent
        # direction = self.find_direction()
                
        
        # check if car agent can move and if next position is valid
        # if self.can_move:
            
            


    # Function to find path using A* pathfinding algorithm
    def find_path(self, start, destination):
        # Use A* algorithm from networkx
        path = nx.astar_path(self.model.graph, start, destination)
        return path
    
    # Function to find the current direction of the road
    def find_direction(self):
        # check direction of the road in the current position
        for agent in self.model.grid.get_cell_list_contents(self.pos):
            if isinstance(agent, Road):      
                direction = agent.direction
            return direction
                

    # Function to move the agent to the proper direction
    def find_next_pos(self):
        
        # next position of the car agent based 
        x, y = self.path[0]
        self.path = self.path[1:]
        return (x,y)
        
        # # move accordingly based on the current direction of the road
        # if direction == "left":
        #     return (x-1, y)
        # elif direction == "Right":
        #     return (x+1, y)
        # elif direction == "Up":
        #     return (x, y+1)
        # elif direction == "Down":
        #     return (x, y-1)
        # else:
        #     return(x,y)
        #     print(f"default case entered, could be an error. Happened at pos: {self.pos}")
                
    # Function to check if the next position is valid
    def is_valid_pos(self, next_pos):
        # check for presence of other car agents and/or obstacles
        for agent in self.model.grid.get_cell_list_contents(next_pos):
            if isinstance(agent, Car):
                return False
        return True
        

    

    def step(self):
        """ 
        Determines the new direction it will take, and then moves
        """
        self.move()

class Traffic_Light(Agent):
    """
    Traffic light. Where the traffic lights are in the grid.
    """
    def __init__(self, unique_id, model, state = False, timeToChange = 10):
        super().__init__(unique_id, model)
        """
        Creates a new Traffic light.
        Args:
            unique_id: The agent's ID
            model: Model reference for the agent
            state: Whether the traffic light is green or red
            timeToChange: After how many step should the traffic light change color 
        """
        self.state = state
        self.timeToChange = timeToChange

    def step(self):
        """ 
        To change the state (green or red) of the traffic light in case you consider the time to change of each traffic light.
        """
        if self.model.schedule.steps % self.timeToChange == 0:
            self.state = not self.state

class Destination(Agent):
    """
    Destination agent. Where each car should go.
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass

class Obstacle(Agent):
    """
    Obstacle agent. Just to add obstacles to the grid.
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass

class Road(Agent):
    """
    Road agent. Determines where the cars can move, and in which direction.
    """
    def __init__(self, unique_id, model, direction= "Left"):
        """
        Creates a new road.
        Args:
            unique_id: The agent's ID
            model: Model reference for the agent
            direction: Direction where the cars can move
        """
        super().__init__(unique_id, model)
        self.direction = direction

    def step(self):
        pass
