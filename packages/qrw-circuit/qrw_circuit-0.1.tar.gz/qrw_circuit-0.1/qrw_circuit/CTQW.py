import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit, transpile, Aer, execute
from qiskit.quantum_info import Operator
from qiskit.visualization import plot_histogram
from scipy.linalg import expm






def circular_graph(num_nodes):
    G = nx.Graph()
    for i in range(num_nodes):
        G.add_node(i)
    for i in range(num_nodes):
        G.add_edge(i, (i + 1) % num_nodes)
    return G

def adjacency_matrix(G):
    adj_matrix = nx.adjacency_matrix(G)
    return adj_matrix.todense()

def create_hamiltonian(adj_matrix):
    # Create Hamiltonian as a 2^n x 2^n matrix
    n = adj_matrix.shape[0]
    N = 2**n
    H = np.zeros((N, N), dtype=complex)
    
    for i in range(n):
        for j in range(n):
            if adj_matrix[i, j] != 0:
                # Apply X gate to transition between connected nodes
                H[2**i, 2**j] = H[2**j, 2**i] = 1
    
    return H

def continuous_time_quantum_walk(hamiltonian, steps, time_step):
    num_qubits = int(np.log2(hamiltonian.shape[0]))
    
    # Create quantum circuit
    qc = QuantumCircuit(num_qubits)
    
    # Initialize the state at the first position
    qc.x(0)
    
    # Calculate the time evolution operator U
    U = expm(-1j * hamiltonian *time_step * steps)
    
    # Ensure U is unitary
    U = U / np.linalg.norm(U, ord=2)
    
    # Convert U to a valid quantum operator
    U_operator = Operator(U)
    
    for _ in range(steps):
        qc.unitary(U_operator, list(range(num_qubits)), label="QWalk")

    # Add measurement
    qc.measure_all()

    # Execute the quantum circuit
    backend = Aer.get_backend('qasm_simulator')
    job = execute(qc, backend, shots=1024)
    result = job.result()
    counts = result.get_counts(qc)
    
    return counts




# %%
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

def circular_graph(num_nodes):
    G = nx.Graph()
    for i in range(num_nodes):
        G.add_node(i)
    for i in range(num_nodes):
        G.add_edge(i, (i + 1) % num_nodes)
    return G

def adjacency_matrix(G):
    adj_matrix = nx.adjacency_matrix(G)
    return adj_matrix.todense()

def draw_circular_graph(G):
    pos = nx.circular_layout(G)
    nx.draw(G, pos, with_labels=True, node_color='skyblue', edge_color='gray')
    plt.show()




def adjacency_matrix(num_nodes,structure):
    if structure == 'circular':
        
        G = circular_graph(num_nodes)
        adj_matrix = nx.adjacency_matrix(G)
        return adj_matrix.todense()
    else:
        raise ValueError("Invalid structure. Not implement.")

def draw_graph(num_nodes, structure):
    if structure == 'circular':
        G = circular_graph(num_nodes)
        draw_circular_graph(G)
    else:
        raise ValueError("Invalid structure. Not implement.")

# %%
def M0(num_nodes,p,time_step,H):
    L_sum = np.zeros((num_nodes,num_nodes))
    L_sum = np.asmatrix(L_sum)
    for i in range(num_nodes):
        for j in range(num_nodes):
            bracket_i = np.zeros(int(num_nodes))
            bracket_i[i] = 1
            # i_state = np.binary_repr(i, width=int(num_nodes*(1/2)))
            # for k in range(int(num_nodes*(1/2))):
            #     bracket_i[k] = int(i_state[k])
            bracket_j = np.zeros(int(num_nodes))
            bracket_j[j] = 1
            # j_state = np.binary_repr(j, width=int(num_nodes*(1/2)))
            # for k in range(int(num_nodes*(1/2))):
            #     bracket_j[k] = int(j_state[k])
            L = H[i,j]/sum(H[i])*np.tensordot(bracket_i.T,bracket_j,axes=0)
            L = np.asmatrix(L)
            # L_sum += p**2*L.getH()*L
            L_sum += p*L.getH()*L
    L_sum = 1/2*L_sum
    k0  = np.identity(num_nodes) - time_step*(1j*H*(1-p) + (1/2)*L_sum)
    return k0 

def Mk(num_nodes,p,time_step,H,k):
    if k < num_nodes:
        bracket_i = np.zeros(int(num_nodes))
        if k+1 == num_nodes:
            bracket_i[0] = 1
        else:
            bracket_i[k+1] = 1
        bracket_j = np.zeros(int(num_nodes))
        bracket_j[k] = 1
        # print("bracket_i:" ,bracket_i)
        # print("bracket_j:" ,bracket_j)
        if k+1 == num_nodes:
            L_k = H[k,0]/sum(H[k])*np.tensordot(bracket_i.T,bracket_j,axes=0)
        else:
            L_k = H[k,k+1]/sum(H[k])*np.tensordot(bracket_i.T,bracket_j,axes=0)
        L_k = np.asmatrix(L_k)
        L_k = p**(1/2)*L_k
    else:
        k = k - num_nodes
        bracket_j = np.zeros(int(num_nodes))
        if k+1 == num_nodes:
            bracket_j[0] = 1
        else:
            bracket_j[k+1] = 1
        bracket_i = np.zeros(int(num_nodes))
        bracket_i[k] = 1
        # print("bracket_i:" ,bracket_i)
        # print("bracket_j:" ,bracket_j)
        if k+1 == num_nodes:
            L_k = H[0,k]/sum(H[0])*np.tensordot(bracket_i.T,bracket_j,axes=0)
        else:
            L_k = H[k+1,k]/sum(H[k+1])*np.tensordot(bracket_i.T,bracket_j,axes=0)
        L_k = np.asmatrix(L_k)
        L_k = p**(1/2)*L_k
    return time_step**(1/2)*L_k


from qiskit.quantum_info import Choi, Kraus
def kraus_to_choi(kraus):
    choi = Choi(Kraus(kraus))
    return choi

def optimize_kraus(choi):
    optimized_kraus = Kraus(choi)
    return optimized_kraus


def U_operator(adj_matrix, p, time_step):
    num_nodes = adj_matrix.shape[0]
    m0 = M0(num_nodes,p = p,time_step=time_step ,H=adj_matrix)
    kraus = [m0]
    for i in range(num_nodes*2):
        kraus.append(Mk(num_nodes,p = p,time_step=time_step ,H=adj_matrix,k=i))
    output = optimize_kraus(kraus_to_choi(kraus))
    V = []
    for i in range(len(output.data)):
        V.append(output.data[i])
    V = np.array(V)

    V = np.reshape(V,(V.shape[0]*V.shape[1],V.shape[2]),order='A')
    Q, R = np.linalg.qr(V, mode='complete')
    signs = np.sign(np.diag(R[:V.shape[1],:V.shape[1]]))
    Q[:, :V.shape[1]] = Q[:, :V.shape[1]] * signs
    R[:V.shape[1], :] = R[:V.shape[1], :] * signs[:, np.newaxis]
    check =np.dot(Q[:,:V.shape[1]],R[:V.shape[1],:])
    U = Q

    dim = 1
    while True:
        dim = dim*2
        if dim >= U.shape[0]:
            break
    new_U = np.eye(dim, dtype=U.dtype)
    new_U[:U.shape[0], :U.shape[1]] = U
    from qiskit.quantum_info import Operator
    op_U = Operator(new_U)
    import math
    dim = math.ceil(math.log(dim,2))
    return op_U , dim





