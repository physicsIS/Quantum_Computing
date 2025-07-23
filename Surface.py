import stim 


def surface(distance, rounds):

		  circuit = stim.Circuit()

		  qubits = [[x + distance*y for x in range(distance)] for y in range(distance)]

		  circuit.append("R",list(range(distance *distance)))


		  

