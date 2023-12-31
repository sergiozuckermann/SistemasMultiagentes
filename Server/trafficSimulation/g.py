import networkx as nx
import matplotlib.pyplot as plt
import json


# function to generate the graph that represents the city
def gen_graph(map_lines):
        # Convert the map into a list of lists
        city_map_lines = [list(line.strip()) for line in map_lines]

        # Create a directed graph
        city_graph = nx.DiGraph()
        
        # Specify the path to the JSON file (symbol representation)
        file_path = './static/city_files/mapDictionary.json'

        # Open the JSON file for reading
        with open(file_path, 'r') as file:
                # Load the JSON data from the file
                symbol_mapping = json.load(file)

        # # Print the loaded data
        # print(data)

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
                                        
                                # Add edges to indicate change of lane
                                if (symbol == '<' or symbol == '>') and j > 1 and j < len(city_map_lines[i]) - 1:
                                        # connect top to bottom
                                        if (i + 1 <= len(city_map_lines) - 1) and city_map_lines[i+1][j-1] == '<':
                                                        city_graph.add_edge((j, n-1), (j-1, n-2))
                                        elif (i + 1 <= len(city_map_lines) - 1) and city_map_lines[i+1][j+1] == '>':
                                                        city_graph.add_edge((j, n-1), (j+1, n-2))
                                        #connect bottom to top
                                        elif (i - 1 >= 0) and city_map_lines[i-1][j-1] == '<':
                                                        city_graph.add_edge((j, n-1), (j-1, n))
                                        elif (i - 1 >= 0) and city_map_lines[i-1][j+1] == '>':
                                                        city_graph.add_edge((j, n-1), (j+1, n))
                                
                                elif (symbol == '^' or symbol == 'v') and i > 2 and i < len(city_map_lines[i]) - 2:
                                        # connect left to right
                                        if j + 1 <= len(city_map_lines[i]) - 1 and city_map_lines[i+1][j+1] == 'v':
                                                city_graph.add_edge((j, n-1), (j+1, n-2))
                                        elif j + 1 <= len(city_map_lines[i]) - 1 and city_map_lines[i-1][j+1] == '^':
                                                city_graph.add_edge((j, n-1), (j+1, n))
                                        # connect right lo left
                                        elif j - 1 >= 0 and city_map_lines[i+1][j-1] == 'v':
                                                city_graph.add_edge((j, n-1), (j-1, n-2))
                                        elif j - 1 >= 0 and city_map_lines[i-1][j-1] == '^':
                                                city_graph.add_edge((j, n-1), (j-1, n))
                                        
                                
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
        # pos = dict((node, node) for node in city_graph.nodes())
        # nx.draw(city_graph, pos, with_labels=True, font_weight='bold', node_size=700, node_color='lightgray', arrowsize=20)
        # plt.show()

        return city_graph
                    
                    

# with open('static/city_files/2023_base.txt') as baseFile:
#             lines = baseFile.readlines()
#             # generate the graph gicen the city map
#             gen_graph(lines)
