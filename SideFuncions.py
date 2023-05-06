# Calculates the BE cost of a DC
def c_calculation(alpha, remain_wl):
    fi = np.zeros(numOfNode)
    final_cost = np.zeros((numOfNode,1))
    for i in range(numOfNode):
        fi[i] = remain_wl[i] - RE_resources[i]
        final_cost[i] = alpha[i] * fi[i]

    return final_cost

# Calculates the average of delays
def t_mean(dc, arm, cost_matrix):
    n = 0
    d = len(cost_matrix)
    for k in range(d):
        n += cost_matrix[k][dc][arm]
    Mean = n/d

    return Mean

# Calculates the power consumption related to migrated workloads
def P_calculation(dc, all_cpu_reqs, reqNumber):
    P_peak = 200  # watt
    P_idle = 100  # watt
    eta = 1.2
    cpu_req = all_cpu_reqs[dc]
    P_wl = cpu_req[reqNumber] / 1600
    P_dyna = (P_peak - P_idle) * P_wl
    P_static = P_idle + (eta - 1) * P_peak
    remain_wl = P_dyna + P_static
    return remain_wl

# A store function to store some variables' values
def store(*values):
    store.values = values or store.values
    return store.values
store.values = ()

# This function checks the round number through migration process
def checkTheRound(teta):
    if teta == 0:
        DC_active_SBVT = [0] * numOfNode
        SBVT_cap = np.ones((numOfNode, numOfSBVT)) * SBVTCap  # Gbps
        NumOfSubT = np.ones((numOfNode, numOfSBVT)) * 10
        preSelectedNodes = []
        store(preSelectedNodes, DC_active_SBVT, SBVT_cap, NumOfSubT)
    (a,b,c,d) = store()
    return a, b, c, d

# Finding shorting path from source to destination
def routing(src, des):
    graph = nx.from_numpy_matrix(np.matrix(linkDis), create_using=nx.DiGraph)
    path = nx.shortest_path(graph, source=src, target=des)
    # print(path)
    temp1 = 0
    for n in range(1, len(path)):
        temp1 += linkDis[path[n - 1]][path[n]]
    #print(temp1)
    delay = temp1 / (2 * (10 ** 5)) * 1000

    temp2 = 0
    for n in range(1, len(path)):
        #print(n)
        temp2 += EA[path[n - 1]][path[n]]
    NumAmp = temp1

    return delay


# Calulating the average of a list
def average(lst):
    return sum(lst)/len(lst)
