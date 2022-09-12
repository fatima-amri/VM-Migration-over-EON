import numpy as np
import math

########################## NSF Topology ##########################

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
NumOfReq=100
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

    P_static = (P_idle + (eta - 1) * P_peak) * 100  # is equal to 140 watt and 100 server in total in a DC
    #print(P_static)
    P_dynamic1 = np.array(Vec_Pdyna)
    P_dc = list(P_static + P_dynamic1)
    print("workload in each DC before migration= ", P_dc)

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
    beta = 0.001 #dollar

    fi_src=np.zeros(numOfNode)
    for i in List_D:
        fi_src[i]=P_dc[i]-RE_resources[i]

    fi_des=np.zeros(numOfNode)
    for j in ListOfArms:
        fi_des[j]= P_dc[j]-RE_resources[j]

    #exploration
    cost = np.zeros((len(List_D),len(ListOfArms)))
    remain_wl = Vec_Pdyna
    for dc in List_D:
        reqNumber=0
        bw = list(np.random.randint(2, 20, size=NumOfReq)) # Gbps
        for arm in ListOfArms:
            (T, Amp)= R_OG(dc, arm) #receiving the number of used transponders and amplifiers in the path
            Total_c= (alpha[dc]* fi_src[dc]) + (beta * (bw[reqNumber] + T + Amp)) + (alpha[arm]* max(fi_des[arm],0))
            cost[dc][arm]= Total_c
            Migrated_P = P_dynamic_calculation(dc, all_cpu_reqs, reqNumber)
            remain_wl[dc] = Vec_Pdyna[dc] - Migrated_P
            reqNumber+=1
    print("cost after exploration = ", cost)
    print("remaining workload after exploration = ", remain_wl)

    return cost

def P_dynamic_calculation(dc, all_cpu_reqs, reqNumber):
    P_peak = 200  # watt
    P_idle = 100  # watt
    cpu_req = all_cpu_reqs[dc]
    P_wl = cpu_req[reqNumber] / 1600
    P_dyna = (P_peak - P_idle) * P_wl
    return P_dyna

######################### ROUTING AND OPTICAL GROOMING ###############################

#number of EDFA amplifiers in each physical link :
EA=np.zeros((numOfNode, numOfNode))
for i in range(len(linkDis)):
    for j in range(len(linkDis)):
        if linkDis[i][j] != 0:
            temp = (linkDis[i][j] / 80) - 1
            EA[i][j] = math.floor(temp) + 2
#print(EA)


def R_OG (src, des):


    return
