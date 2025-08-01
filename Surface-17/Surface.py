import stim 

def surface(distance, rounds):
    circuit = stim.Circuit()

    # Crear malla de qubits de datos
    qubits = [[x + distance * y for x in range(distance)] for y in range(distance)]

    circuit.append("R", list(range(distance * distance))) #inicializar todos los qubits en 0

    stabilizers = []
    ancilla_index = distance * distance  # Los ancillas van después de los qubits de datos

    # Estabilizadores internos (plaquetas 2x2)
    for y in range(distance - 1):
        for x in range(distance - 1):
            plaqueta = [
                qubits[y][x],
                qubits[y][x+1],
                qubits[y+1][x],
                qubits[y+1][x+1]
            ]
            stab_type = "Z" if (x + y) % 2 == 0 else "X"
            stabilizers.append({
                "type": stab_type,
                "data": plaqueta,
                "ancilla": ancilla_index
            })
            ancilla_index += 1

    # Estabilizadores del borde superior e inferior

    for x in range(distance - 1):
        # Superior e inferior

        if x % 2 == 0:
            plaqueta_top = [qubits[distance-1][x], qubits[distance-1][x+1]]
            stab_type = "X"
            stabilizers.append({
                "type": stab_type,
                "data": plaqueta_top,
                "ancilla": ancilla_index
            })
            ancilla_index += 1



        if x % 2 != 0:
            plaqueta_bottom = [qubits[0][x], qubits[0][x+1]]
            stab_type = "X"
            stabilizers.append({
                "type": stab_type,
                "data": plaqueta_bottom,
                "ancilla": ancilla_index
            })
            ancilla_index += 1


    # Estabilizadores del borde izquierdo y derecho (vertical)
    for y in range(distance - 1):

        if y % 2 == 0:

            plaqueta_left = [qubits[y][0], qubits[y+1][0]]
            stab_type = "Z"
            stabilizers.append({
                "type": stab_type,
                "data": plaqueta_left,
                "ancilla": ancilla_index
            })
            ancilla_index += 1


        if y % 2 != 0:

            plaqueta_right = [qubits[y][distance-1], qubits[y+1][distance-1]]
            stab_type = "Z"
            stabilizers.append({
                "type": stab_type,
                "data": plaqueta_right,
                "ancilla": ancilla_index
            })
            ancilla_index += 1

    # Medición de estabilizadores (una sola ronda por ahora)
    for _ in range(rounds):
        for stab in stabilizers:
            a = stab["ancilla"]
            data_qubits = stab["data"]

            circuit.append("R", [a])

            if stab["type"] == "Z":
                for d in data_qubits:
                    circuit.append("CX", [d, a])
            else:  # tipo X
                circuit.append("H", [a])
                for d in data_qubits:
                    circuit.append("CX", [a, d])
                circuit.append("H", [a])

            circuit.append("M", [a])

    return circuit

# Ejemplo de prueba
prueba = surface(3, 1)
print(prueba)
