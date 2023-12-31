// TC2008B. Sistemas Multiagentes y Gráficas Computacionales
// C# client to interact with Python. Based on the code provided by Sergio Ruiz.
// Octavio Navarro. October 2023

// modified for the traffic simulation by Santiago Benitez and Sergio Zucckermann

using System;
using System.Collections;
using System.Collections.Generic;
using UnityEditor;
using UnityEngine;
using UnityEngine.Networking;

[Serializable]
public class AgentData
{
    /*
    The AgentData class is used to store the data of each agent.
    
    Attributes:
        id (string): The id of the agent.
        x (float): The x coordinate of the agent.
        y (float): The y coordinate of the agent.
        z (float): The z coordinate of the agent.
    */
    public string id, state, direction;
    public float x, y, z;
 

    public AgentData(string id, float x, float y, float z, string state, string direction)
    {
        this.id = id;
        this.x = x;
        this.y = y;
        this.z = z;
        this.state=state;
        this.direction = direction;
    }
}

[Serializable]

public class AgentsData
{
    /*
    The AgentsData class is used to store the data of all the agents.

    Attributes:
        positions (list): A list of AgentData objects.
    */
    public List<AgentData> positions;

    public AgentsData() => this.positions = new List<AgentData>();
}

public class AgentController : MonoBehaviour
{
    /*
    The AgentController class is used to control the agents in the simulation.

    Attributes:
        serverUrl (string): The url of the server.
        getAgentsEndpoint (string): The endpoint to get the agents data.
        getObstaclesEndpoint (string): The endpoint to get the obstacles data.
        sendConfigEndpoint (string): The endpoint to send the configuration.
        updateEndpoint (string): The endpoint to update the simulation.
        agentsData (AgentsData): The data of the agents.
        obstacleData (AgentsData): The data of the obstacles.
        agents (Dictionary<string, GameObject>): A dictionary of the agents.
        prevPositions (Dictionary<string, Vector3>): A dictionary of the previous positions of the agents.
        currPositions (Dictionary<string, Vector3>): A dictionary of the current positions of the agents.
        updated (bool): A boolean to know if the simulation has been updated.
        started (bool): A boolean to know if the simulation has started.
        agentPrefab (GameObject): The prefab of the agents.
        obstaclePrefab (GameObject): The prefab of the obstacles.
        floor (GameObject): The floor of the simulation.
        NAgents (int): The number of agents.
        width (int): The width of the simulation.
        height (int): The height of the simulation.
        timeToUpdate (float): The time to update the simulation.
        timer (float): The timer to update the simulation.
        dt (float): The delta time.
    */
    string serverUrl = "http://localhost:8585";
    string getAgentsEndpoint = "/getAgents";
    string getDestinationsUrl = "/getDestinations";
    string sendConfigEndpoint = "/init";
    string updateEndpoint = "/update";
    string getSemaphore = "/getSemaphore";
    
    // game objects
    public GameObject agentPrefab, obstaclePrefab, floor, semaphorePrefab; 

    AgentsData agentsData, destinationsData, semaphoreData; // Instances of AgentsData

    // Dictionaries
    Dictionary<string, GameObject> agents;
    Dictionary<string, Vector3> agentDestinations;
    Dictionary <string, Light> lights;

    // flags
    bool updated = false, started = false, starteds=false;

    // variables
    public int NAgents, width, height;
    public float timeToUpdate = 5.0f;
    private float timer, dt;

    void Start()
    {
        agentsData = new AgentsData();
        destinationsData = new AgentsData();
        agentDestinations = new Dictionary<string, Vector3>();
        semaphoreData= new AgentsData();
        lights = new Dictionary<string, Light>();
        agents = new Dictionary<string, GameObject>();
        floor.transform.localScale = new Vector3((float)width / 10, 1, (float)height / 10);
        floor.transform.localPosition = new Vector3((float)width / 2 - 0.5f, 1, (float)height / 2 - 0.5f);

        timer = timeToUpdate;

        // Launches a couroutine to send the configuration to the server.
        StartCoroutine(SendConfiguration());
    }

    private void Update()
    {
        if (timer < 0) // determine when to update the simulation
        {
            timer = timeToUpdate;
            updated = false;
            StartCoroutine(UpdateSimulation());
        }
        
        if (updated)
        {
            timer -= Time.deltaTime;
        }
    }

    IEnumerator UpdateSimulation()
    {
        UnityWebRequest www = UnityWebRequest.Get(serverUrl + updateEndpoint);
        yield return www.SendWebRequest();

        if (www.result != UnityWebRequest.Result.Success)
            Debug.Log(www.error);
        else
        {
            StartCoroutine(GetAgentsData());
            StartCoroutine(GetDestinationsData());
            StartCoroutine(GetSemaphoreData());
        }
    }

    IEnumerator SendConfiguration()
    {
        /*
        The SendConfiguration method is used to send the configuration to the server.

        It uses a WWWForm to send the data to the server, and then it uses a UnityWebRequest to send the form.
        */
        WWWForm form = new WWWForm();

        form.AddField("NAgents", NAgents.ToString());
        form.AddField("width", width.ToString());
        form.AddField("height", height.ToString());

        UnityWebRequest www = UnityWebRequest.Post(serverUrl + sendConfigEndpoint, form);
        www.SetRequestHeader("Content-Type", "application/x-www-form-urlencoded");

        yield return www.SendWebRequest();

        if (www.result != UnityWebRequest.Result.Success)
        {
            Debug.Log(www.error);
        }
        else
        {
            Debug.Log("Configuration upload complete!");
            Debug.Log("Getting Agents positions");

            // Once the configuration has been sent, it launches a coroutine to get the agents data.
            StartCoroutine(GetAgentsData());
            StartCoroutine(GetDestinationsData());
            StartCoroutine(GetSemaphoreData());

        }
    }

    IEnumerator GetAgentsData()
    {
        // The GetAgentsData method is used to get the agents data from the server.

        UnityWebRequest www = UnityWebRequest.Get(serverUrl + getAgentsEndpoint);
        yield return www.SendWebRequest();

        if (www.result != UnityWebRequest.Result.Success)
            Debug.Log(www.error);
        else
        {
            // Once the data has been received, it is stored in the agentsData variable.
            // Then, it iterates over the agentsData.positions list to update the agents positions.
            agentsData = JsonUtility.FromJson<AgentsData>(www.downloadHandler.text);

            Vector3 destinationPos;
            foreach (AgentData agent in agentsData.positions)
            {
                Vector3 newAgentPosition = new Vector3(agent.x, agent.y, agent.z);
                Vector3 zeroes = new Vector3(0, 0, 0);
                GameObject car;
                if (!started)
                {
                    // if the simulation is starting create the gameobject
                    agents[agent.id] = Instantiate(agentPrefab, zeroes, Quaternion.identity);
                    car = agents[agent.id];

                    // set the position where the agent should move and the move time
                    car.GetComponent<MoveCar>().setNextPosition(newAgentPosition);
                    car.GetComponent<MoveCar>().setMoveTime(timeToUpdate);
                }
                else
                {
                    // after starting
                    if (agents.TryGetValue(agent.id, out car))
                    {
                        // if the car exists update the position where it should move
                        car.GetComponent<MoveCar>().setNextPosition(newAgentPosition);
                    }

                    else
                    {
                        // if it does not exist create it and set the position where it should move
                        agents[agent.id] = Instantiate(agentPrefab, zeroes, Quaternion.identity);
                        car = agents[agent.id];
                        car.GetComponent<MoveCar>().setNextPosition(newAgentPosition);
                        car.GetComponent<MoveCar>().setMoveTime(timeToUpdate);

                    }

                }

                // check if next destination is the car agent's destination                
                if(agentDestinations.TryGetValue(agent.id, out destinationPos))
                {
                    if(destinationPos == newAgentPosition) { 
                        // delete the car and the wheels if they reach the destination
                        agents[agent.id].GetComponent<MoveCar>().DestroyAll();
                    }
                
                }

                updated = true;
                if (!started) started = true;
            }
        }
    }


    IEnumerator GetSemaphoreData() 
    {
        // The GetSemaphoreData method is used to get the semaphores data.
        UnityWebRequest www = UnityWebRequest.Get(serverUrl + getSemaphore);
        yield return www.SendWebRequest();

        if (www.result != UnityWebRequest.Result.Success)
            Debug.Log(www.error);
        else 
        {
            // Once the data has been received, it is stored in the agentsData variable.
            // Then, it iterates over the agentsData.positions list to update the agents positions.
            semaphoreData = JsonUtility.FromJson<AgentsData>(www.downloadHandler.text);
            foreach(AgentData semaphore in semaphoreData.positions)
            {
                // semaphore positions
                Vector3 newAgentPosition = new Vector3(semaphore.x, semaphore.y, semaphore.z);
                    if(!starteds)
                    {
                        // Instantiate semaphore gameobjects with proper rotation based on the direction of the road
                        if(semaphore.direction == "right"){
                            agents[semaphore.id] = Instantiate(semaphorePrefab, newAgentPosition, Quaternion.identity);
                        }
                        else if(semaphore.direction == "left"){
                            agents[semaphore.id] = Instantiate(semaphorePrefab, newAgentPosition, Quaternion.Euler(0, 180, 0));
                        }
                        else if(semaphore.direction == "up"){
                            agents[semaphore.id] = Instantiate(semaphorePrefab, newAgentPosition, Quaternion.Euler(0, 270, 0));
                        }
                        else if(semaphore.direction == "down"){
                            agents[semaphore.id] = Instantiate(semaphorePrefab, newAgentPosition, Quaternion.Euler(0, 90, 0));   
                        }
                    
                        // add the gameobject to the lights dictionary based on the semaphore id
                        lights[semaphore.id] = agents[semaphore.id].GetComponentInChildren<Light>();

                    }
                    else
                    {
                        // Check the state of the semaphore and update the color of the light accordingly
                        if (semaphore.state == "True"){
                            lights[semaphore.id].color= Color.green;
                        }
                        else if (semaphore.state == "False"){
                            lights[semaphore.id].color= Color.red;
                        }
                    }
            }

            updated = true;
            if(!starteds) starteds = true;
        }
    }
        
        IEnumerator GetDestinationsData()
        {
        // The GetDestinationsData method is used to get the destinatio position of the agents

        UnityWebRequest www = UnityWebRequest.Get(serverUrl + getDestinationsUrl);
            yield return www.SendWebRequest();

            if (www.result != UnityWebRequest.Result.Success)
                Debug.Log(www.error);
            else
            {
                // Once the data has been received, it is stored in the agentsData variable.
                // Then, it iterates over the agentsData.positions list to update the destination positions.
                destinationsData = JsonUtility.FromJson<AgentsData>(www.downloadHandler.text);

                Vector3 v;
                foreach (AgentData agentDestination in destinationsData.positions)
                {
                    Vector3 destinationPosition = new Vector3(agentDestination.x, agentDestination.y, agentDestination.z);

                    // add destination of agent if id is not in the dictionary
                    if (agentDestinations.TryGetValue(agentDestination.id, out v) == false)
                     {
                        
                        agentDestinations[agentDestination.id] = destinationPosition;
                     }
                }

            }
        }

    }