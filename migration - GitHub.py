import numpy as np
import networkx as nx
import math
from collections import deque

########################## Topology ##########################

numOfNode = 14
NSFNet = [[0,1,1,1,0,0,0,0,0,0,0,0,0,0],
          [1,0,1,0,0,0,0,1,0,0,0,0,0,0],
          [1,1,0,0,1,0,0,0,0,0,0,0,0,0],
          [1,0,0,0,0,1,0,0,0,0,1,0,0,0],
          [0,0,1,0,0,1,0,0,1,0,0,0,1,0],
          [0,0,0,1,1,0,1,0,0,0,0,0,0,0],
          [0,0,0,0,0,1,0,1,0,0,0,0,0,0],
          [0,1,0,0,0,0,1,0,0,1,0,0,0,0],
          [0,0,0,0,1,0,0,0,0,1,0,0,0,0],
          [0,0,0,0,0,0,0,1,1,0,0,1,0,1],
          [0,0,0,1,0,0,0,0,0,0,0,1,0,1],
          [0,0,0,0,0,0,0,0,0,1,1,0,1,0],
          [0,0,0,0,1,0,0,0,0,0,0,1,0,1],
          [0,0,0,0,0,0,0,0,0,1,1,0,1,0]]

linkDis = [[0,750,800,880,0,0,0,0,0,0,0,0,0,0],
           [750,0,1240,0, 0, 0,0,2200,0,0,0,0,0,0],
           [800,1240,0,0,1010,0,0,0,0,0,0,0,0,0],
           [880,0,0,0,0,630,0,0,0,0,2350,0,0,0],
           [0,0,1010,0,0,720,0,0,1620,0,0,0,2100,0],
           [0,0,0,630,720,0,700,0,0,0,0,0,0,0],
           [0,0,0,0,0,700,0,650,0,0,0,0,0,0],
           [0,2200, 0, 0, 0, 0, 650, 0, 0, 610, 0, 0, 0, 0],
           [0, 0, 0, 0, 1620, 0, 0, 0, 0, 1900, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 610, 1900, 0, 0, 1000, 0, 1320],
           [0, 0, 0, 2350, 0, 0, 0, 0, 0, 0, 0,740, 0, 700],
           [0, 0, 0, 0, 0, 0, 0, 0, 0, 1000,740, 0, 900, 0],
           [0, 0, 0, 0,2100, 0, 0, 0, 0, 0, 0, 900, 0, 830],
           [0, 0, 0, 0, 0, 0, 0, 0, 0, 1320, 700, 0, 830, 0]]

#per unit energy cost for each DCs in NSF net.
alpha=[9.09, 11.28, 12.57, 10.88, 12.12, 11.56, 10.60,
       12.50, 13.64, 11.58, 14.42, 18.54, 15.81, 12.99]

######################################### controller checkup ###########################################
NumOfReq = 450
def controller_checkup ():
    P_peak = 200  # watt
    P_idle = 100  # watt
    c_m = 100  # number of servers in each DC
    eta = 1.2
    a = 0.3 * P_peak * c_m * eta
    b = P_peak * c_m * eta

    # available RE resources at the beginning of the migration cycle
    RE_resources = []
    for dc in range(numOfNode):
        zeta_s = np.random.randint(a, b)
        RE_resources.append(zeta_s)
    print("available RE = ", RE_resources)


    # amount of workload in each DC
    Vec_Pdyna = []
    all_cpu_reqs = []
    for dc in range(numOfNode):
        cpu_req = list(np.random.randint(1, 3, size=NumOfReq))
        all_cpu_reqs.append(cpu_req)
        total_cpu = sum(cpu_req)
        U_mn = total_cpu / 1600
        numOfServer = math.ceil(total_cpu / 16)
        P_dynamic = (P_peak - P_idle) * U_mn * numOfServer #this dynamic power is for before migration
        Vec_Pdyna.append(P_dynamic)
    print("amount of P dynamic in each DC = ", Vec_Pdyna) #this vector has 14 elements. each for one DC.
    #print("CPU requests of each DCs in the topology : ", all_cpu_reqs)

    P_static = (P_idle + (eta - 1) * P_peak) * 100  # is equal to 140 watt and 100 server in total in a DC
    #print(P_static)
    P_dynamic1 = np.array(Vec_Pdyna)
    P_dc = list(P_static + P_dynamic1)
    print("workload (expressed in terms of power) in each DC before migration = ", P_dc)

    List_D = []
    for dc in range(numOfNode):
        if P_dc[dc] > RE_resources[dc]:
            List_D.append(dc)
    print("DC with insufficient RE = ", List_D)
    return List_D, P_dc, RE_resources, all_cpu_reqs, Vec_Pdyna

######################################### MAB ###########################################

def MAB(numOfNode, List_D, P_dc,RE_resources, all_cpu_reqs, Vec_Pdyna):
    ListOfDC = list(range(numOfNode))
    ListOfArms= list(set(ListOfDC)-set(List_D))
    print("List of Arms : ", ListOfArms)
    beta = 0.001 #dollar

    fi_src=np.zeros(numOfNode)
    for i in List_D:
        fi_src[i]=P_dc[i]-RE_resources[i]


    fi_des=np.zeros(numOfNode)
    for j in ListOfArms:
        fi_des[j]= P_dc[j]-RE_resources[j]

    #exploration
    cost = np.zeros((numOfNode,numOfNode)) #src * des
    t = 100 # window size
    remain_wl = P_dc
    teta = 0
    reqNumVec = np.zeros((numOfNode, 1)) #number of migration in each DC
    bw_reqVec = np.zeros((numOfNode, NumOfReq))
    for dc in List_D:
        reqNumber=0
        bw_req = list(np.random.randint(2, 20, size=NumOfReq)) # Gbps
        for i in range(NumOfReq):
            bw_reqVec[dc][i]= bw_req[i]

        for arm in ListOfArms:
            T = OG(teta, dc, arm,bw_req[reqNumber]) #receiving the number of used transponders and amplifiers in the path
            Amp = routing(dc, arm)
            Total_c= (alpha[dc]* fi_src[dc]) + (beta * (bw_req[reqNumber] + T + Amp)) + (alpha[arm]* max(fi_des[arm],0))
            cost[dc][arm]= Total_c
            #print(cost)
            Migrated_P = P_calculation(dc, all_cpu_reqs, reqNumber)
            remain_wl[dc] = P_dc[dc] - Migrated_P
            reqNumber+=1
            teta +=1
        reqNumVec[dc][0] = reqNumber
    #print("cost after exploration = ", cost)
    print("remaining workload after exploration = ", remain_wl) # only dynamic power consumption has been considered for this term. as static term is always constatnt.
    print("teta after exploration = ", teta)
    #print("request number vector : ", reqNumVec)
    #print("vector request of BW: ", bw_reqVec)
    teta_explo = teta


    #explotation
    zi = 1
    for dc in List_D:

        Index_dic ={}
        reqNumber1 = int(reqNumVec[dc][0])
        bw_req1 = bw_reqVec[dc]
        cost_matrix = deque(maxlen= t)   # archive the cost matrix of the previous rounds
        while remain_wl[dc] >= RE_resources[dc]:
            teta += 1
            print("round number (teta) = ", teta)
            cost_matrix.append(cost)
            Index_vec = []
            for arm in ListOfArms:
                if max(fi_des[arm], 0) == 0 : #just to check that the destination DC won't get overloaded and swith to BE consumption
                    cMean = c_mean(dc, arm, cost_matrix)
                    E_term = math.sqrt((zi * math.log(min(teta, t)))/t)
                    i = cMean + E_term
                    Index_vec.append(i)
                    Index_dic[arm]= i
            print("index vector of DC ", dc, "is = ", Index_vec)
            print("index dictionary = ", Index_dic)

            index_min = min(Index_vec)
            arm1 = [k for k, v in Index_dic.items() if v == index_min][0]
            print("the arm related to DC", dc, " the minimum index = ", arm1)


            T = OG(teta, dc, arm1, bw_req1[reqNumber1])
            Amp = routing(dc, arm1)

            Total_c = (alpha[dc] * fi_src[dc]) + (beta * (bw_req1[reqNumber1] + T + Amp)) + (alpha[arm1] * max(fi_des[arm1], 0))
            cost[dc][arm1] = Total_c
            Migrated_P = P_calculation(dc, all_cpu_reqs, reqNumber1)
            remain_wl[dc] = P_dc[dc] - Migrated_P
            reqNumber1 +=1
        reqNumVec[dc][0] = reqNumber1

    #print("the cost matrix after MAB : ", cost)
    print("total round : ", teta)
    return cost


def c_mean(dc, arm, cost_matrix):
    n = 0
    d = len(cost_matrix)
    for k in range(d):
        n += cost_matrix[k][dc][arm]
    Mean = n/d

    return Mean


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


######################### ROUTING AND OPTICAL GROOMING ###############################

### number of EDFA amplifiers in each physical link :
EA = np.zeros((numOfNode, numOfNode))
for i in range(len(linkDis)):
    for j in range(len(linkDis)):
        if linkDis[i][j] != 0:
            temp = (linkDis[i][j] / 80) - 1
            EA[i][j] = math.floor(temp) + 2
#print(EA)


numOfSBVT = 10 # number of SBVT in each DC
SubTrans_MaxCap = 40 #Gbps (The maximum capacity of carrier)
SBVTCap = 400


def store(*values):
    store.values = values or store.values
    return store.values
store.values = ()


def checkTheRound(teta):
    if teta == 0:
        DC_active_SBVT = [0] * numOfNode
        SBVT_cap = np.ones((numOfNode, numOfSBVT)) * SBVTCap  # Gbps
        NumOfSubT = np.ones((numOfNode, numOfSBVT)) * 10
        preSelectedNodes = []
        store(preSelectedNodes, DC_active_SBVT, SBVT_cap, NumOfSubT)
    (a,b,c,d) = store()
    return a, b, c, d


def routing(src, des):
    ### finding shorting path
    graph = nx.from_numpy_matrix(np.matrix(linkDis), create_using=nx.DiGraph)
    path = nx.shortest_path(graph, source=src, target=des)
    # print(path)
    temp1 = 0
    for n in range(1, len(path)):
        #print(n)
        temp1 += EA[path[n - 1]][path[n]]
    NumAmp = temp1

    return NumAmp


def OG (teta, src, des, bw_req):
    # checking the round and getting the required values
    if teta == 0:
        (preSelectedNodes, DC_active_SBVT, SBVT_cap, NumOfSubT) = checkTheRound(teta)
    else:
        (preSelectedNodes, DC_active_SBVT, SBVT_cap, NumOfSubT) = store()

    # performing optical grooming:
    ## Operation 1:
    if src in preSelectedNodes and des in preSelectedNodes:
        #print("active SBVT in DCs = ", DC_active_SBVT)
        src_T_index = DC_active_SBVT[src]
        des_T_index = DC_active_SBVT[des]

        if SBVT_cap[src][src_T_index] <= SBVTCap and SBVT_cap[des][des_T_index] <= SBVTCap:
            #print(SBVT_cap)
            if NumOfSubT[src][src_T_index] > 0 and NumOfSubT[des][des_T_index] > 0:
                #print(NumOfSubT)
                NumOfSubT[src][src_T_index] -= 1
                NumOfSubT[des][des_T_index] -= 1
                SBVT_cap[src][src_T_index] = SBVT_cap[src][src_T_index] - bw_req
                SBVT_cap[des][des_T_index] = SBVT_cap[des][des_T_index] - bw_req
                NumTrans = 0
                store(preSelectedNodes, DC_active_SBVT, SBVT_cap, NumOfSubT)
            # end of Operation 1
            # if each of these if constraints get rejected, it will be Operation 2 or 1
            else:
                NumTrans = Operation2(src, des, bw_req, preSelectedNodes, DC_active_SBVT, SBVT_cap, NumOfSubT)

        else:
            NumTrans = Operation2_2(src, des, bw_req, preSelectedNodes, DC_active_SBVT, SBVT_cap, NumOfSubT)

    elif src in preSelectedNodes and des not in preSelectedNodes:
        preSelectedNodes.append(des)
        src_T_index = DC_active_SBVT[src]
        des_T_index = DC_active_SBVT[des]
        DC_active_SBVT[des] += 1
        NumOfSubT[des][des_T_index] -= 1
        SBVT_cap[des][des_T_index] = SBVT_cap[des][des_T_index] - bw_req
        NumTrans = 1

        if SBVT_cap[src][src_T_index] <= SBVTCap:
            if NumOfSubT[src][src_T_index] > 0:
                NumOfSubT[src][src_T_index] -= 1
                SBVT_cap[src][src_T_index] = SBVT_cap[src][src_T_index] - bw_req
                # so NumTrans remains 1
                store(preSelectedNodes, DC_active_SBVT, SBVT_cap, NumOfSubT)
            else:
                result = Operation2(src, des, bw_req, preSelectedNodes, DC_active_SBVT, SBVT_cap, NumOfSubT)
                NumTrans += result
        else:
            result1 = Operation2_2(rc, des, bw_req, preSelectedNodes, DC_active_SBVT, SBVT_cap, NumOfSubT)
            NumTrans += result1

    elif src not in preSelectedNodes and des in preSelectedNodes:
        preSelectedNodes.append(src)
        src_T_index = DC_active_SBVT[src]
        des_T_index = DC_active_SBVT[des]
        DC_active_SBVT[src] += 1
        NumOfSubT[src][src_T_index] -= 1
        SBVT_cap[src][src_T_index] = SBVT_cap[src][src_T_index] - bw_req
        NumTrans = 1

        if SBVT_cap[des][des_T_index] <= SBVTCap :
            if NumOfSubT[des][des_T_index] > 0:
                NumOfSubT[des][des_T_index] -= 1
                SBVT_cap[des][des_T_index] = SBVT_cap[des][des_T_index] - bw_req
                # so NumTrans remains 1
                store(preSelectedNodes, DC_active_SBVT, SBVT_cap, NumOfSubT)
            else:
                result = Operation2(src, des, bw_req, preSelectedNodes, DC_active_SBVT, SBVT_cap, NumOfSubT)
                NumTrans += result
        else:
            result1 = Operation2_2(rc, des, bw_req, preSelectedNodes, DC_active_SBVT, SBVT_cap, NumOfSubT)
            NumTrans += result1

    # Operation 3:
    else:
        preSelectedNodes.append(src)
        preSelectedNodes.append(des)
        NumTrans = Operation3(src, des, bw_req, preSelectedNodes, DC_active_SBVT, SBVT_cap, NumOfSubT)
        #store(preSelectedNodes, DC_active_SBVT, SBVT_cap, NumOfSubT)


    return NumTrans


def Operation2(src, des, bw_req, preSelectedNodes, DC_active_SBVT, SBVT_cap, NumOfSubT):
    src_T_index = DC_active_SBVT[src]
    des_T_index = DC_active_SBVT[des]

    if NumOfSubT[src][src_T_index] == 0 and NumOfSubT[des][des_T_index] > 0:
        DC_active_SBVT[src] += 1
        src_T_index = DC_active_SBVT[src]
        NumOfSubT[src][src_T_index] -= 1
        SBVT_cap[src][src_T_index] = SBVT_cap[src][src_T_index] - bw_req
        NumTrans = 1
        store(preSelectedNodes, DC_active_SBVT, SBVT_cap, NumOfSubT)

    elif NumOfSubT[des][des_T_index] == 0 and NumOfSubT[src][src_T_index] > 0:
        DC_active_SBVT[des] += 1
        des_T_index = DC_active_SBVT[des]
        NumOfSubT[des][des_T_index] -= 1
        SBVT_cap[des][des_T_index] = SBVT_cap[des][des_T_index] - bw_req
        NumTrans = 1
        store(preSelectedNodes, DC_active_SBVT, SBVT_cap, NumOfSubT)

    else:
        NumTrans = Operation3(src, des, bw_req, preSelectedNodes, DC_active_SBVT, SBVT_cap, NumOfSubT)

    return NumTrans


def Operation2_2(src, des, bw_req, preSelectedNodes, DC_active_SBVT, SBVT_cap, NumOfSubT):
    src_T_index = DC_active_SBVT[src]
    des_T_index = DC_active_SBVT[des]

    if SBVT_cap[src][src_T_index] > SBVTCap and SBVT_cap[des][des_T_index] <= SBVTCap:
        DC_active_SBVT[src] += 1
        src_T_index = DC_active_SBVT[src]
        NumOfSubT[src][src_T_index] -= 1
        SBVT_cap[src][src_T_index] = SBVT_cap[src][src_T_index] - bw_req
        NumTrans = 1
        store(preSelectedNodes, DC_active_SBVT, SBVT_cap, NumOfSubT)

    elif SBVT_cap[src][src_T_index] <= SBVTCap and SBVT_cap[des][des_T_index] > SBVTCap:
        DC_active_SBVT[des] += 1
        des_T_index = DC_active_SBVT[des]
        NumOfSubT[des][des_T_index] -= 1
        SBVT_cap[des][des_T_index] = SBVT_cap[des][des_T_index] - bw_req
        NumTrans = 1
        store(preSelectedNodes, DC_active_SBVT, SBVT_cap, NumOfSubT)

    else:
        NumTrans = Operation3(src, des, bw_req, preSelectedNodes, DC_active_SBVT, SBVT_cap, NumOfSubT)

    return NumTrans


def Operation3(src, des, bw_req, preSelectedNodes, DC_active_SBVT, SBVT_cap, NumOfSubT):

    DC_active_SBVT[src] += 1
    src_T_index = DC_active_SBVT[src]
    NumOfSubT[src][src_T_index] -= 1
    SBVT_cap[src][src_T_index] = SBVT_cap[src][src_T_index] - bw_req

    DC_active_SBVT[des] += 1
    des_T_index = DC_active_SBVT[des]
    NumOfSubT[des][des_T_index] -= 1
    SBVT_cap[des][des_T_index] = SBVT_cap[des][des_T_index] - bw_req

    NumTrans = 2
    store(preSelectedNodes, DC_active_SBVT, SBVT_cap, NumOfSubT)
    return NumTrans


###################################### MAIN ########################################

(List_D, P_dc, RE_resources, all_cpu_reqs, Vec_Pdyna) = controller_checkup()
COST = MAB(numOfNode, List_D, P_dc, RE_resources, all_cpu_reqs, Vec_Pdyna)
print("Final cost matrix = ", COST)
