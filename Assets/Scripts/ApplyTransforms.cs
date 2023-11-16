//Sergio Zuckermann A01024831
// Script para tranformar los vertices de un coche y sus ruedas

using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ApplyTransforms : MonoBehaviour
{
    //Objeto a instanciar
    [SerializeField] GameObject wheel;
    //Dirección de movimiento
    [SerializeField] Vector3 displacement;
    //Angulo inicial
    [SerializeField] float angle;
    //Angulo de rotación de la rueda
    [SerializeField] float anglew;
    //Ejes de rotación
    [SerializeField] AXIS rotationAxis;
    [SerializeField] AXIS rotationAxisw;
    //Posición original de las llantas
    [SerializeField]  Vector3 w1;
    [SerializeField]  Vector3 w2;
    [SerializeField]  Vector3 w3;
    [SerializeField]  Vector3 w4;
    //Escala a aplicar
    [SerializeField]  Vector3 scaler;

    //Meshes
    Mesh mesh;
    Mesh meshw1;
    Mesh meshw2;
    Mesh meshw3;
    Mesh meshw4;

    //Vertices base y nuevos para las transformaciones
    Vector3[] baseVertices;
    Vector3[] newVertices;
    Vector3[] baseVerticesw1;
    Vector3[] newVerticesw1;
    Vector3[] baseVerticesw2;
    Vector3[] newVerticesw2;
    Vector3[] baseVerticesw3;
    Vector3[] newVerticesw3;
    Vector3[] baseVerticesw4;
    Vector3[] newVerticesw4;

    //Declarar los objetos a iterar
    GameObject wheel1;
    GameObject wheel2;
    GameObject wheel3;
    GameObject wheel4;
    //Vector que contiene ceros para inicializar en el centro las ruedas
    Vector3 zeros;
    void Start(){
        zeros= new Vector3(0.0f,0.0f,0.0f);
        //Se instancian las ruedas y se guardan en variables GameObject
        wheel1= Instantiate(wheel, zeros, Quaternion.identity);
        wheel2= Instantiate(wheel, zeros, Quaternion.identity);
        wheel3= Instantiate(wheel, zeros, Quaternion.identity);
        wheel4= Instantiate(wheel, zeros, Quaternion.identity);
        //Se guardan las meshes de los componentes tomandolas de sus hijos
        mesh= GetComponentInChildren<MeshFilter>().mesh;
        meshw1= wheel1.GetComponentInChildren<MeshFilter>().mesh;
        meshw2= wheel2.GetComponentInChildren<MeshFilter>().mesh;
        meshw3= wheel3.GetComponentInChildren<MeshFilter>().mesh;
        meshw4= wheel4.GetComponentInChildren<MeshFilter>().mesh;
        //Se guardan los vertices de las meshes en los vertices base
        baseVertices = mesh.vertices;
        baseVerticesw1 = meshw1.vertices;
        baseVerticesw2 = meshw2.vertices;
        baseVerticesw3 = meshw3.vertices;
        baseVerticesw4 = meshw4.vertices;

        //Se inicializan los nuevos vertices con la longitud de los vertices base
        newVertices = new Vector3[baseVertices.Length];
        newVerticesw1 = new Vector3[baseVerticesw1.Length];
        newVerticesw2 = new Vector3[baseVerticesw2.Length];
        newVerticesw3 = new Vector3[baseVerticesw3.Length];
        newVerticesw4 = new Vector3[baseVerticesw4.Length];
        
        //Se generan los nuevos vertices tomando vertices base
        for (int i=0; i<baseVertices.Length; i++){
            newVertices[i]=baseVertices[i];
        }
        
        for (int i=0; i<baseVerticesw1.Length; i++){
            newVerticesw1[i]=baseVerticesw1[i];
        }

        for (int i=0; i<baseVerticesw2.Length; i++){
            newVerticesw2[i]=baseVerticesw2[i];
        }

        for (int i=0; i<baseVerticesw3.Length; i++){
            newVerticesw3[i]=baseVerticesw3[i];
        }

        for (int i=0; i<baseVerticesw4.Length; i++){
            newVerticesw4[i]=baseVerticesw4[i];
        }
    }   

    //Cada Frame se hace una transformación
    void Update(){
        DoTransform();
    }
    
    //Formula para actualizar el angulo segun el vector de desplazamiento
    float AngleCalculation(Vector3 initial){
        angle= Mathf.Atan2(initial.x, initial.z);
        angle=  Mathf.Rad2Deg * angle;
        return angle;
    }

    //Función de transformaciones
    void DoTransform(){
        //Se recalcula el angulo
        angle= AngleCalculation(displacement);

        //Se generan matrices para aplicar las transformacones del script HW_Transforms
        //Matrices base
        Matrix4x4 move= HW_Transforms.TranslationMat(displacement.x * Time.time, displacement.y * Time.time, displacement.z * Time.time);
        Matrix4x4 moveOrigin= HW_Transforms.TranslationMat(-displacement.x , -displacement.y, -displacement.z );
        Matrix4x4 moveObject= HW_Transforms.TranslationMat(displacement.x , displacement.y, displacement.z );
        Matrix4x4 scale= HW_Transforms.ScaleMat(scaler.x, scaler.y, scaler.z);
        Matrix4x4 rotate =HW_Transforms.RotateMat(angle, rotationAxis);
        //Matriz compuesta que sera el movimiento del coche
        Matrix4x4 composite= move*rotate;

        //Matriz de rotación con time para animar las ruedas sobre su eje
        Matrix4x4 rotatew =HW_Transforms.RotateMat(anglew*Time.time, rotationAxisw);

        //Matrices de traslación para acomodar las ruedas en su lugar
        Matrix4x4 trans1= HW_Transforms.TranslationMat(w1.x, w1.y, w1.z);
        Matrix4x4 trans2= HW_Transforms.TranslationMat(w2.x, w2.y, w2.z);
        Matrix4x4 trans3= HW_Transforms.TranslationMat(w3.x, w3.y, w3.z);
        Matrix4x4 trans4= HW_Transforms.TranslationMat(w4.x, w4.y, w4.z);
        
        //Matrices compuestas de las ruedas
        //Toman la compuesta del coche, la rotación de la llanta, la escala y la traslación
        Matrix4x4 compositew1= composite*trans1*scale*rotatew;
        Matrix4x4 compositew2= composite*trans2*scale*rotatew;
        Matrix4x4 compositew3= composite*trans3*scale*rotatew;
        Matrix4x4 compositew4= composite*trans4*scale*rotatew;

        //Se crean vectores temporales que guardan los vertices base y agregan un elemento 1 para que el vector tenga longitud de 4
        //Se aplican los cambios a los nuevos vertices multiplicando la compuesta adecuada por el vector temporal
        for(int i=0; i<newVertices.Length; i++){
            Vector4 temp = new Vector4(baseVertices[i].x, baseVertices[i].y, baseVertices[i].z, 1);
            newVertices[i] = composite * temp;
        }

        for(int i=0; i<newVerticesw1.Length; i++){
            Vector4 tempw1 = new Vector4(baseVerticesw1[i].x, baseVerticesw1[i].y, baseVerticesw1[i].z, 1);
            newVerticesw1[i] = compositew1* tempw1;
        }

        for(int i=0; i<newVerticesw2.Length; i++){
            Vector4 tempw2 = new Vector4(baseVerticesw2[i].x, baseVerticesw2[i].y, baseVerticesw2[i].z, 1);
            newVerticesw2[i] = compositew2 * tempw2;
        }

        for(int i=0; i<newVerticesw3.Length; i++){
            Vector4 tempw3 = new Vector4(baseVerticesw3[i].x, baseVerticesw3[i].y, baseVerticesw3[i].z, 1);
            newVerticesw3[i] = compositew3 * tempw3;
        }

        for(int i=0; i<newVerticesw1.Length; i++){
            Vector4 tempw4 = new Vector4(baseVerticesw4[i].x, baseVerticesw4[i].y, baseVerticesw4[i].z, 1);
            newVerticesw4[i] = compositew4 * tempw4;
        }

        //Se asignan los vertices a la mesh despues de transformalos
        //Se recalculan las normales
        mesh.vertices = newVertices;
        mesh.RecalculateNormals();
        meshw1.vertices = newVerticesw1;
        meshw1.RecalculateNormals();
        meshw2.vertices = newVerticesw2;
        meshw2.RecalculateNormals();
        meshw3.vertices = newVerticesw3;
        meshw3.RecalculateNormals();
        meshw4.vertices = newVerticesw4;
        meshw4.RecalculateNormals();
    }
}
