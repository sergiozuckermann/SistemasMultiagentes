#Sergio Zuckermann A01024831 
#Script para crear figuras en 3D usando el formato .obj
#Se calculan y crean coordenadas, vectores normales y caras de la figura
#Se usan tres variables iniciales manuales o automaticas: Lados, ancho, radio
import math
import sys

#Función para normalizar vectores
def normalize_vector(vector):
    magnitude = math.sqrt(sum(x**2 for x in vector))
    if magnitude != 0:
        normalized_vector = [x / magnitude for x in vector]
        return normalized_vector
    return vector

#Función para sacar el producto cruz
def cross(aprime, bprime):
    a = normalize_vector(aprime)
    b = normalize_vector(bprime)
    result = [
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0]
    ]
    return result


def shape():
    print("Choose manually (y) or automatic values (any key): ")
    option=str(input())
    if option=="y":
        print("Choose sides from 3 to 360: ")
        sides = float(input())

        print("Choose radius: ")
        radius = float(input())
        print("Choose width: ")
        width = float(input())
    else:
        sides=8.0
        radius=1.0
        width=.5
    #angulo de movimiento
    movement = 360 / sides
    #Posicionando la x en la coordenada inicial
    x= width / 2
    #Contador para insertar en orden los elementos
    counter = 0
    #Lista temporal
    temp=[]
    #Lista de coordenadas
    coord=[]

    #Coordenadas iniciales en el centro
    for j in range(2):
        temp.insert((0), x)
        temp.insert((1), 0.0)
        temp.insert((2), 0.0)
        counter += 1
        coord.insert((counter), temp)
        temp=[]
        x = (width / 2) * -1

    #Ciclo para sacar coordenadas cada uno de los lados
    for i in range(int(sides)):
        #Calculo de z, y
        z=round(radius * math.cos(math.radians(i * movement)), 4)
        y=round(radius * math.sin(math.radians(i * movement)), 4)
        #Ciclo para sacar la coordenada de z positiva y negativa con x, y calculados
        for j in range(2):
            #Lista temporal vacia
            temp=[]
            #Condición para posicionar z
            if j == 0:
                x = width / 2
            elif j == 1:
                x=((width / 2) * -1)
            #Insertar vectores a lista temporal
            temp.insert((1), x)
            temp.insert((2), y)
            temp.insert((3), z)
            #Aumentar contador para insertar correctamente la lista temporal
            counter += 1
            #Insertar lista temporal en lista de coordenadas
            coord.insert((counter), temp)
    #Lista de vectores normales
    normal=[]
    #Ciclo para sacar vectores normales en las caras centrales
    for i in range(2): 
        #Lista temporal vacia
        temp=[]
        #Condición en caso de que z sea positiva o negativa
        if i % 2 == 0:
            #Insertar en vecotr temporal las coordenadas de dos puntos de la cara
            temp.insert((0), coord[0])
            temp.insert((1), coord[2])
            #Función para sacar producto cruz entre ambas
            res = cross(temp[0],temp[1])
        elif i % 2 == 1:
            temp.insert((0), coord[1])
            temp.insert((1), coord[5])
            temp.insert((2), coord[3]) 
            res = cross(temp[0],temp[1])
        #Insertar resultado a lista de vectores normales
        normal.insert((i), res)
        
    #Contador es 2 porque ya se realizo 0,1 en el ciclo anterior
    counter = 2
    #Se repite el ciclo anterior en las caras laterales
    for i in range(int(sides)):
        temp = []
        if i % 2 == 0:
            temp.insert((0), coord[counter])
            counter += 3
            temp.insert((1), coord[counter])
            counter -= 1
            temp.insert((0), coord[counter])      
            res = cross(temp[0],temp[1])
            counter -= 2
            normal.insert((counter), res)
        elif  i % 2 == 1:
            temp.insert((0), coord[counter])
            counter += 1
            temp.insert((1), coord[counter])
            counter += 2
            temp.insert((0), coord[counter])
            res = cross(temp[0],temp[1])
            counter -= 2
            normal.insert((counter), res)        
            counter += 1
    #Lista de caras vacia
    faces=[]
    #Contador de cara actual
    countera=1
    #Contador de veces que ha pasado por el segundo ciclo
    counterb=1
    #Contador para insertar correctamente en la lista de caras
    counterc=0
    #Ciclo para crear caras centrales en z positiva y negativa
    for i in range(2):
        #Ciclo para cada uno de los lados
        for j in range(int(sides)-1):
            temp=[]
            #Si z es positiva se usa el vector normal 1 si no 2
            if i % 2 == 0:
                #Creación de caras
                append=str(countera)+"//1"
                temp.insert(0, append)
                countera= countera + (2 * counterb)
                append=str(countera)+"//1"
                temp.insert(1, append)
                countera +=2
                append=str(countera)+"//1"
                temp.insert(2, append)
                countera = 1
                counterb += 1
                faces.insert(counterc, temp)
                counterc += 1
            elif i % 2 == 1:
                append=str(countera)+"//2"
                temp.insert(0, append)
                countera= countera + (2 * counterb)
                append=str(countera)+"//2"
                temp.insert(1, append)
                countera +=2
                append=str(countera)+"//2"
                temp.insert(1, append)
                countera = 2
                counterb += 1
                faces.insert(counterc, temp)
                counterc += 1
        countera=2
        counterb=1
    
    #Creación de la ultima cara con las ultimas coordenas y las primeras
    temp=[]
    append="1//1"
    temp.insert(0, append)
    append=str((int(sides) * 2) + 1)+"//1"
    temp.insert(1, append)
    append="3//1"
    temp.insert(2, append)
    faces.insert(counterc, temp)
    counterc += 1
    temp=[]
    append="2//2"
    temp.insert(0, append)
    append="4//2"
    temp.insert(1, append)
    append=str((int(sides) * 2) + 2)+"//2"
    temp.insert(2, append)
    faces.insert(counterc, temp)
    counterc += 1
    #Posicionar countera en la primera coorenada lateral
    countera = 3
    #Counterb ahora va a definir el vector normal actual
    counterb = 3
    #Se repite el ciclo para caras laterales
    for j in range(int(sides) - 1):
        for i in range(2):
            temp=[]
            if i % 2 == 0:
                append=str(countera)+"//"+str(counterb)
                temp.insert(0, append)
                countera += 1
                append=str(countera)+"//"+str(counterb)
                temp.insert(1, append)
                countera += 2
                append=str(countera)+"//"+str(counterb)
                temp.insert(2, append)
                countera -= 3
                faces.insert(counterc, temp)
                counterc += 1
            elif i % 2 == 1:
                append=str(countera)+"//"+str(counterb)
                temp.insert(0, append)
                countera += 3
                append=str(countera)+"//"+str(counterb)
                temp.insert(1, append)
                countera -= 1
                append=str(countera)+"//"+str(counterb)
                temp.insert(2, append)
                faces.insert(counterc, temp)
                counterc += 1
        counterb += 1
    
    #Creación de últimas dos caras laterales con primeras y ultimas coordenadas
    temp=[]
    append="3//"+str(counterb)
    temp.insert(0, append)
    append=str((int(sides) * 2) + 1)+"//"+str(counterb)
    temp.insert(1, append)
    append=str((int(sides) * 2) + 2)+"//"+str(counterb)
    temp.insert(2, append)
    faces.insert(counterc, temp)
    counterc += 1
    temp=[]
    append="3//"+str(counterb)
    temp.insert(0, append)
    append=str((int(sides) * 2) + 2)+"//"+str(counterb)
    temp.insert(1, append)
    append="4//"+str(counterb)
    temp.insert(2, append)
    faces.insert(counterc, temp)
    counterc += 1

    #Creación de archivo output shape.obj con comentarios
    output_filename="shape.obj"
    with open(output_filename, 'w') as obj_file:
        obj_file.write(f"#Sergio Zuckermann A01024831: Output shape\n")
        obj_file.write(f"#vertices\n")
        for vertex in coord:
            obj_file.write(f"v {' '.join(map(str, vertex))}\n")
        obj_file.write(f"#normal vectors\n")
        for vector in normal:
            obj_file.write(f"vn {' '.join(map(str, vector))}\n")
        obj_file.write(f"#faces\n")
        for face in faces:
            obj_file.write(f"f {' '.join(map(str, face))}\n")
    #El archivo se creo correctamente
    print(f".obj file '{output_filename}' created successfully.")

if __name__ == "__main__":
         shape()