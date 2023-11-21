from mesa import Agent
import networkx as nx


class Car(Agent):
    """
    Agent that moves randomly.
    Attributes:
        unique_id: Agent's ID 
        direction: Randomly chosen direction chosen from one of eight directions
    """
    def __init__(self, goal, unique_id, model):
        """
        Creates a new random agent.
        Args:
            unique_id: The agent's ID
            model: Model reference for the agent
        """
        super().__init__(unique_id, model)
        self.current_direction = None # save the current car's direction
        self.path = [] # agent path
        self.goal = goal
        
    def move(self):
        """ 
        Determines if the agent can move in the direction that was chosen
        """        
        
        # t_path = self.find_path(self.pos, self.goal)
        # print("seeing test path")
        # print(t_path)
        # # return
        # if self.pos == self.goal:
        #     return
        # if len(self.path) == 0:
        #     self.path = t_path
        # self.model.grid.move_agent(self, self.path[0])
        # self.path = self.path[1:]
        # return
        
        # check if current direction of the car is not None (This happens when car agent is in a cell where there is also a Traffic Light agent)
        if self.current_direction is not None:
            next_pos = self.find_next_pos(self.current_direction)
            if self.is_valid_pos(next_pos): # validate next position
                self.model.grid.move_agent(self, next_pos)
                self.current_direction = None
            return
        
        # find direction to move based on the current position of the car agent
        direction = self.find_direction()
        
        # get next position
        next_pos = self.find_next_pos(direction)
        
        # check if next position is valid
        if self.is_valid_pos(next_pos):
            # check if there is a stoplight in the next cell of the current direction
            for agent in self.model.grid.get_cell_list_contents(next_pos):
                # check if it is a stoplight 
                if isinstance(agent, Traffic_Light):
                    if not agent.state: # Do not move if stoplight is red
                        return
                    else: # store current_direction of the car
                        self.current_direction = direction    
            # move car agent   
            self.model.grid.move_agent(self, next_pos)
                
    # Function to find path using A* pathfinding algorithm
    def find_path(self, start, goal):
        # Use A* algorithm from networkx
        graph = nx.grid_2d_graph(self.model.grid.width, self.model.grid.height)
    
        
        # Iterate through the cells of your MultiGrid
        for a, p in self.model.grid.coord_iter():
                print(a)
            # If the cell contains an obstacle, remove the corresponding node from the graph
                if len(a) > 0 and isinstance(a[0], Obstacle):
                    graph.remove_node(p)
                            
        print(list(graph.nodes.data()))          

     
        # Use A* algorithm from networkx with custom cost function
        path = nx.astar_path(graph, start, goal)
        return path
    
    # Function to find the current direction of the road
    def find_direction(self):
        # check direction of the road in the current position
        for agent in self.model.grid.get_cell_list_contents(self.pos):
            if isinstance(agent, Road):      
                direction = agent.direction
        return direction
    
    # Function to move the agent to the proper direction
    def find_next_pos(self, direction):
        
        # current position of the car agent
        x, y = self.pos
        
        # move accordingly based on the current direction of the road
        match direction:
            case "Left":
                return (x-1, y)
            case "Right":
                return (x+1, y)
            case "Up":
                return (x, y+1)
            case "Down":
                return (x, y-1)
            case _:
                print(f"default case entered, could be an error. Happened at pos: {self.pos}")
                
    # Function to check if the next position is valid
    def is_valid_pos(self, next_pos):
        # check for presence of other car agents and/or obstacles
        for agent in self.model.grid.get_cell_list_contents(next_pos):
            if isinstance(agent, Obstacle) or isinstance(agent, Car):
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
