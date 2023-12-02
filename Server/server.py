# TC2008B. Sistemas Multiagentes y Gráficas Computacionales
# Python flask server to interact with Unity. Based on the code provided by Sergio Ruiz.
# Octavio Navarro. October 2023git

from flask import Flask, request, jsonify
from trafficSimulation.model import CityModel
from trafficSimulation.agent import Car, Traffic_Light

# Variables
cityModel = None
currentStep = 0

app = Flask("City Simulation")

# endpoint to initiate the city model in mesa
@app.route('/init', methods=['GET', 'POST'])
def initModel():
    global currentStep, cityModel, number_agents, width, height

    if request.method == 'POST':
    
        cityModel = CityModel()

        return jsonify({"message":"Parameters recieved, model initiated."})
    elif request.method == 'GET':
      
        cityModel = CityModel()

        return jsonify({"message":"Default parameters recieved, model initiated."})


@app.route('/validate_attempt', methods=['POST'])
def validate_attempt():
    global cityModel

    if request.method == 'POST':
        data = [{"year": 2023, "classroom": 302, "name": "Equipo1 Santiago Benitez y Sergio Zuckermann", "num_cars": cityModel.arrived}
                        #   for a, (x, z) in cityModel.grid.coord_iter()
                        #   for element in a  
                        #   if isinstance(element, Car)
                        ]
        # print(data)
        return jsonify({'data': data})

@app.route('/getAgents', methods=['GET'])
def getAgents():
    global cityModel

    if request.method == 'GET':

        agentPositions = [{"id": str(element.unique_id), "x": x, "y":.06, "z":z}
                          for a, (x, z) in cityModel.grid.coord_iter()
                          for element in a  
                          if isinstance(element, Car)]

        return jsonify({'positions':agentPositions})
    
# endpoint to get semaphores data
@app.route('/getSemaphore', methods=['GET'])
def getSemaphore():
    global cityModel

    if request.method == 'GET':
        agentState = [{"state": str(element.state), "id": str(element.unique_id), "x": x, "y":0, "z":z, "direction": element.direction}
       
                           for a, (x, z) in cityModel.grid.coord_iter()
                           for element in a  
                           if isinstance(element, Traffic_Light)]

        return jsonify({'positions':agentState})

# endpoint to get destination positions
@app.route('/getDestinations', methods=['GET'])
def getDestinations():
    global cityModel
    
    if request.method == 'GET':
        destinations = [{"id": str(element.unique_id), "x": element.destination[0], "y":.06, "z":element.destination[1]} 
                          for a, (x, z) in cityModel.grid.coord_iter()
                          for element in a  
                          if isinstance(element, Car)]
        return jsonify({'positions':destinations})

# endpoint to update the model's step
@app.route('/update', methods=['GET'])
def updateModel():
    global currentStep, cityModel
    if request.method == 'GET':
        cityModel.step()
        currentStep += 1
        return jsonify({'message':f'Model updated to step {currentStep}.', 'currentStep':currentStep})


if __name__=='__main__':
    app.run(host="localhost", port=8585, debug=True)