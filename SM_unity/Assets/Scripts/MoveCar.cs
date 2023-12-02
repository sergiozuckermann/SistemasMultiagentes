
// script that controls the movement of the car
// Santiago Benitez - A01782813

using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class MoveCar : MonoBehaviour
{


    // displacement vector where the car will move
    Vector3 displacement;
    
    // wheel game object
    [SerializeField] GameObject wheel;

    // angle value for the rotation matrix of the wheels
    [SerializeField] float angleW = 40;

    // Rotation angle of the car
    float angle;

    // car mesh
    Mesh mesh;

    // array for vertices and base vertices of the car
    Vector3[] newVertices;
    Vector3[] baseVertices;

    // wheel meshes
    Mesh[] wheelMeshes = new Mesh[4];

    // wheel vertices
    Vector3[][] wheelBaseVertices = new Vector3[4][];
    Vector3[][] wheelNewVertices = new Vector3[4][];
    
    // wheel game objects
    GameObject[] wheels = new GameObject[4];

    // wheel positions
    [SerializeField] Vector3[] wheelPositions;

    // control variables for interpolation
    float elapsedTime = 0f, prevAngle = 0f, t;
    public float moveTime;

    // boolean flags
    public bool starting = true, hasReachedDestination = false;

    Vector3 startPos, finalPos;

    // Start is called before the first frame update
    void Start()
    {

        // instantiate wheels in origin 
        for(int i = 0; i < wheels.Length; i++)
        {
            wheels[i] = Instantiate(wheel, Vector3.zero, Quaternion.identity);
        }

        // get mesh of the car
        mesh = GetComponentInChildren<MeshFilter>().mesh;

        // base Vertices of the car
        baseVertices = mesh.vertices;

        // copy the vertices of the car
        newVertices = new Vector3[baseVertices.Length];
        for (int i = 0; i < baseVertices.Length; i++)
        {
            newVertices[i] = baseVertices[i];
        }

        // Get meshes and vertices for the wheels
        for (int i = 0; i < 4; i++)
        {
            wheelMeshes[i] = wheels[i].GetComponentInChildren<MeshFilter>().mesh;
            wheelBaseVertices[i] = wheelMeshes[i].vertices;
            wheelNewVertices[i] = new Vector3 [wheelBaseVertices[i].Length];
        }

        // copy vertices of the wheels
        for (int i = 0; i < 4; i++)
        {

            for(int j = 0; j < wheelBaseVertices[i].Length; j++)
            {   
                wheelNewVertices[i][j] = wheelBaseVertices[i][j];
            }
        }
    }

    // Update is called once per frame
    void Update()
    {
            if(elapsedTime < moveTime) // check when to move from one point to the other
        {
            DoTransform();
        }
            elapsedTime += Time.deltaTime;

    }

    public void DoTransform()
    {
         
        t = elapsedTime / moveTime; // time

        displacement = startPos + (finalPos - startPos) * t; // interpolation

        float angle = getAngle(); // find angle

        // move matrix for the car
        Matrix4x4 move = HW_Transforms.TranslationMat(displacement.x, displacement.y, displacement.z);

        // rotate matrix for the car
        Matrix4x4 rotate = HW_Transforms.RotateMat(angle + 180, AXIS.Y);

        // scale matrix for the car
        Matrix4x4 carScale = HW_Transforms.ScaleMat(.05f, .05f, .05f);

        // composite matrix for the car
        Matrix4x4 carComposite = move * rotate;
        for (int i = 0; i < newVertices.Length; i++)
        {
            Vector4 temp = new Vector4(baseVertices[i].x, baseVertices[i].y, baseVertices[i].z, 1);
            newVertices[i] = carComposite * temp;

        }

        // Assign the new vertices to the car mesh
        mesh.vertices = newVertices;

        // recalculate normals of the car mesh
        mesh.RecalculateNormals();
        mesh.RecalculateBounds();

        // rotate matrix for the wheels
        Matrix4x4 rotateW = HW_Transforms.RotateMat(angleW * Time.time, AXIS.X);

        // scale matrix for the wheels
        Matrix4x4 scaleTransform = HW_Transforms.ScaleMat(0.5f, 0.5f, 0.5f);

        for(int i = 0; i < 4; i++)
        {

            // transformation matrix for the wheels
            Matrix4x4 wheelTransform = HW_Transforms.TranslationMat(wheelPositions[i].x, wheelPositions[i].y, wheelPositions[i].z);

            // composite matrix for the wheels
            Matrix4x4 wheelComposite = carComposite * wheelTransform; //rotateW
            for (int j = 0; j < wheelNewVertices[i].Length; j++)
            {
                Vector4 temp = new Vector4(wheelBaseVertices[i][j].x, wheelBaseVertices[i][j].y, wheelBaseVertices[i][j].z, 1);
                wheelNewVertices[i][j] = wheelComposite * temp;
            }

            // Assign the new vertices to the current wheel mesh
            wheelMeshes[i].vertices = wheelNewVertices[i];

            // Recalculate normals of the current wheel mesh
            wheelMeshes[i].RecalculateNormals();
            wheelMeshes[i].RecalculateBounds();


        }
     
    }

    public float getAngle()
    {
        // check if car agent has reached its destination to keep the rotation angle
        if(displacement == finalPos)
        {
            angle = prevAngle;
        } 
        // get angle in the direction of the displacement
        else
        {
        Vector3 direction = finalPos - startPos;
        angle = Mathf.Atan2(direction.x, direction.z) * Mathf.Rad2Deg;
        prevAngle = angle;
        }

        return angle;
    }

    public void setNextPosition(Vector3 newPos)   
    {
        // if it is moving to the first destination
        if(starting)
        {
            starting = false;
            startPos = newPos;
            finalPos = newPos;
        }

        // set the final pos as the start pos and update the final pos to newPos
        startPos = finalPos;
        finalPos = newPos;
        elapsedTime = 0f;


    }

    public void setMoveTime(float time)
    {
        moveTime = time;
    }

    // method to destroy the instance of the game object and the wheel
    public void DestroyAll()
    {
        Debug.Log("destroyed called");
        for(int i = 0; i < wheels.Length; i++)
        {
            Destroy(wheels[i]); // destroy wheels
        }
        Destroy(gameObject); // destroy car
      
    }

}