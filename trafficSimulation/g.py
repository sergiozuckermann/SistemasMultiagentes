import networkx as nx
import matplotlib.pyplot as plt

# Data mapping symbols to their meanings
symbol_mapping = {
    ">" : "Right",
    "<" : "Left",
    "S" : 15,
    "s" : 7,
    "#" : "Obstacle",
    "v" : "Down",
    "^" : "Up",
    "D" : "Destination"
}

# Given map
city_map = """
v<<<<<<<<<<<<<<<<<s<<<<<
v<<<<<<<<<<<<<<<<<s<<<<^
vv#D#########vv#SS###D^^
vv###########vv#^^####^^
vv##########Dvv#^^D###^^
vv#D#########vv#^^####^^
vv<<<<<<s<<<<vv#^^####^^
vv<<<<<<s<<<<vv#^^####^^
vv####SS#####vv#^^####^^
vvD##D^^####Dvv#^^####^^
vv####^^#####vv#^^D###^^
SS####^^#####vv#^^####^^
vvs<<<<<<<<<<<<<<<<<<<<<
vvs<<<<<<<<<<<<<<<<<<<<^
vv##########vv###^^###^^
vv>>>>>>>>>>>>>>>>>>>s^^
vv>>>>>>>>>>>>>>>>>>>s^^
vv####vv##D##vv#^^####SS
vv####vv#####vv#^^####^^
vv####vv#####vv#^^###D^^
vv###Dvv####Dvv#^^####^^
vv####vv#####vv#^^####^^
vv####SS#####SS#^^#D##^^
v>>>>s>>>>>>s>>>>>>>>>>^
>>>>>s>>>>>>s>>>>>>>>>>^
"""

def gen_graph(map_lines):
        # Convert the map into a list of lists
        city_map_lines = [list(line.strip()) for line in map_lines]
        print('called success')
        print(city_map_lines)

        # city_map_lines = [list(line.strip()) for line in city_map.strip().split('\n')]

        # Create a directed graph
        city_graph = nx.DiGraph()

        # Iterate through the map and add nodes and edges to the graph
        n = (len(city_map_lines))
        for i in range(len(city_map_lines)):
                for j in range(len(city_map_lines[i])):
                                symbol = city_map_lines[i][j]
                                if symbol in ('<', '>', 'v', '^', 'D', 's', 'S'):
                                        city_graph.add_node((j, n - 1), type=symbol_mapping[symbol])

                                # Add edges based on the direction of the streets
                                        if (symbol == '<' or symbol == 's') and j > 0 and city_map_lines[i][j - 1] in ('<', 'v', 's'):
                                                city_graph.add_edge((j, n-1), (j-1, n-1))
                                        elif (symbol == '>' or symbol == 's') and j < len(city_map_lines[i]) - 1 and city_map_lines[i][j + 1] in ('>', '^', 's'):
                                                city_graph.add_edge((j, n-1), (j+1, n - 1))
                                        elif (symbol == '^' or symbol == 'S') and i > 0 and city_map_lines[i - 1][j] in ('^', '<', '>', 'S'):
                                                city_graph.add_edge((j, n - 1), (j, n))
                                        elif (symbol == 'v' or symbol == 'S') and i < len(city_map_lines) - 1 and city_map_lines[i + 1][j] in ('v', '>', '<', 'S'):
                                                city_graph.add_edge((j, n-1), (j, n - 2))
                                        
                                        # validate edge cases on intersections
                                        if (symbol == '>' or symbol == '<') and i > 0 and city_map_lines[i - 1][j] == '^':
                                                city_graph.add_edge((j, n-1), (j, n))
                                        elif (symbol == '>' or symbol == '<') and i < len(city_map_lines) - 1 and city_map_lines[i + 1][j] == 'v':
                                                city_graph.add_edge((j, n-1), (j, n-2))
                                        elif (symbol == 'v' or symbol == '^') and j < len(city_map_lines[i]) - 1 and city_map_lines[i][j + 1] == '>':
                                                city_graph.add_edge((j, n-1), (j + 1, n - 1))
                                        elif (symbol == 'v' or symbol == '^') and j > 0 and city_map_lines[i][j - 1] == '<':
                                                city_graph.add_edge((j, n-1), (j - 1, n - 1))
                                                
                                        # # connect Destination nodes
                                        if symbol == 'D':
                                                if i > 0 and city_map_lines[i - 1][j] in ('<', '>', 'v'): #up
                                                        city_graph.add_edge((j, n), (j, n - 1))
                                                elif j < len(city_map_lines[i]) - 1 and city_map_lines[i][j + 1] in ('<', 'v', '^'): #right
                                                        city_graph.add_edge((j + 1, n - 1), (j, n - 1))
                                                elif j > 0 and city_map_lines[i][j - 1] in ( 'v', '^'): #left
                                                        city_graph.add_edge((j - 1, n - 1), (j, n - 1))
                                                elif i < len(city_map_lines) and city_map_lines[i + 1][j] in ( '>', '<'): #down
                                                        city_graph.add_edge((j, n - 2), (j, n - 1))                       
                                                
                n-=1 # decrement n by 1
                
        # Visualize the graph (optional)
        pos = dict((node, node) for node in city_graph.nodes())
        nx.draw(city_graph, pos, with_labels=True, font_weight='bold', node_size=700, node_color='lightgray', arrowsize=20)
        plt.show()
        
        return city_graph
                    
                    

