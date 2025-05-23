import stim

#Definiciónes la distancia para el código
d = 3

#Inicialización del Circuito cuantico
circuit = stim.Circuit()
qubits = [[x + d*y for x in range(d)] for y in range(d)] #Lista de indices de los qubits en la grilla
                                                         #Esta distribución es escribir una matriz de
                                                         #Forma continua en indices
                                                         
#Se definen lso qubits ancilar, los cuales se encargan de detectar si hubo algun bitflip(Error en X)
#O si ocurrio un faseflip(Error en Z). Detectan los sindromes
An_X = 9 #Numero de qubits del sistema donde son ancilares
An_Z = 10


#Se vería de esta manera
#   ↓ Detecta el X en las columnas
#  |q1|q2|q3|
#  |q4|q5|q6| ← Detecta el Z en las columnas
#  |q7|q8|q9|

for q in qubits:
    circuit.append("R",q) #Todos los cubits quedan incializados en |0>
    
#Se configuran los operadores x que se se aplican sobre las fila
#Esto se hace aplicando un CNOT a la columna con target el qubit ancilar para X
for coll in range(d):
    circuit.append("R",An_X)
    for row in range(d):
        circuit.append("CNOT", [qubits[row][coll],An_X])#Si se encuentra un flip el An_X se ve afectado
    circuit.append("M",An_X) #Se mide el qubit para ver el sindrome
         
#Se configuran los operadores Z que se se aplican sobre las columnas
#Esto se hace poniendo el primer qubit de las columnas como control y como objetivo los demas
#Con esto se le aplica a cada fila así si hay faseflip en el primero cambia la fila
for row in range(d):
    circuit.append("R",An_Z)
    circuit.append("H",An_Z) #Se le aplica un Hadamard para que los cubits no colaprsen al medir
    for coll in range(d):
        circuit.append("CZ", [qubits[row][coll],An_Z])#Si se encuentra un flip el An_Z se ve afectado
    circuit.append("H",An_Z) #Se reaplica Hadamard para obtener el sindrome
    circuit.append("M",An_Z) #Se mide el qubit para ver el sindrome 
        

#Resultados de la medición
sampler = circuit.compile_sampler()
samples = sampler.sample(shots=1000)  # 1000 repeticiones del experimento
print(samples.astype(int)) #Se spera imprima lso valores de lso qubits


#Existen bibliotecas como pymatching que puede decodificar el tipo de sindrome los cuales posee el qubit
#Tambien con stim se puede agregar errores en cubit específicos para poner aprueba la efectividad

        

