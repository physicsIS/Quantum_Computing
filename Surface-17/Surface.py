import stim

def surface(distance, rounds):
    circuit = stim.Circuit()

    # Crear malla de qubits de datos
    qubits = [[x + distance * y for x in range(distance)] for y in range(distance)]

    circuit.append("R", list(range(distance * distance)))

    stabilizers = []
    ancilla_index = distance * distance  # Los ancillas van después de los qubits de datos

    for y in range(distance - 1):
        for x in range(distance - 1):
            plaqueta = [
                qubits[y][x],
                qubits[y][x+1],
                qubits[y+1][x],
                qubits[y+1][x+1]
            ]

            if (x + y) % 2 == 0:
                # Z estabilizador en esta plaqueta
                stabilizers.append({
                    "type": "Z",
                    "data": plaqueta,
                    "ancilla": ancilla_index
                })
            else:
                # X estabilizador en esta plaqueta
                stabilizers.append({
                    "type": "X",
                    "data": plaqueta,
                    "ancilla": ancilla_index
                })

            ancilla_index += 1

            for stab in stabilizers:
                if stab["type"] == "Z":
                    a = stab["ancilla"]
                    data_qubits = stab["data"]

                    # Reset ancilla
                    circuit.append("R", [a])

                    # Aplicar CNOT desde cada dato hacia el ancilla
                    for d in data_qubits:
                        circuit.append("CX", [d, a])

                    # Medir ancilla
                    circuit.append("M", [a])

    return circuit

prueba = surface(3,2)
print(prueba)



