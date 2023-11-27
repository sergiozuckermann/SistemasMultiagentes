
// script that controls the movement of the car
// Santiago Benitez - A01782813

using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class MoveCar : MonoBehaviour
{
    // displacement vector where the car will move
    [SerializeField] Vector3 displacement;
    
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
    //Vector3 w1Pos = new Vector3(1.279f, -0.37f, -1.88f);
    //Vector3 w2Pos = new Vector3(1.279f, -0.37f, 1.98f);
    //Vector3 w3Pos = new Vector3(-1.26f, -0.37f, 1.98f);
    //Vector3 w4Pos = new Vector3(-1.26f, -0.37f, -1.892f);

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
        }

        // copy vertices of the wheels
        for (int i = 0; i < 4; i++)
        {
            wheelNewVertices[i] = new Vector3[wheelBaseVertices[i].Length];
            for(int j = 0; j < 4; j++)
            {   
                wheelNewVertices[i][j] = wheelBaseVertices[i][j];
            }
        }
    }

    // Update is called once per frame
    void Update()
    {
        DoTransform();
    }

    void DoTransform()
    {
        // get angle in the direction of the displacement
        angle = Mathf.Atan2(displacement.x, displacement.z) * Mathf.Rad2Deg;

        // move matrix for the car
        Matrix4x4 move = HW_Transforms.TranslationMat(displacement.x * Time.time, displacement.y * Time.time, displacement.z * Time.time);

        // rotate matrix for the car
        Matrix4x4 rotate = HW_Transforms.RotateMat(angle, AXIS.Y);

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

        // rotate matrix for the wheels
        Matrix4x4 rotateW = HW_Transforms.RotateMat(angleW * Time.time, AXIS.X);

        // scale matrix for the wheels
        Matrix4x4 scaleTransform = HW_Transforms.ScaleMat(1.5f, 1.5f, 1.5f);

        for(int i = 0; i < 4; i++)
        {

            // transformation matrix for the wheels
            Matrix4x4 wheelTransform = HW_Transforms.TranslationMat(wheelPositions[i].x, wheelPositions[i].y, wheelPositions[i].z);

            // composite matrix fro the wheels
            Matrix4x4 wheelComposite = carComposite * wheelTransform * rotateW * scaleTransform;
            for (int j = 0; j < wheelNewVertices[i].Length; j++)
            {
                Vector4 temp = new Vector4(wheelBaseVertices[i][j].x, wheelBaseVertices[i][j].y, wheelBaseVertices[i][j].z, 1);
                wheelNewVertices[i][j] = wheelComposite * temp;
            }

            // Assign the new vertices to the current wheel mesh
            wheelMeshes[i].vertices = wheelNewVertices[i];

            // Recalculate normals of the current wheel mesh
            wheelMeshes[i].RecalculateNormals();


        }
     
    }
}
