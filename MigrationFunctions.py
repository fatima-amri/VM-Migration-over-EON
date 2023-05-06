import numpy as np
import networkx as nx
import math
from collections import deque


######################################### controller checkup Function ##########################################

NumOfReq = "You Need to Enter the Number Of Requests Here"

alpha= np.random.uniform(9,15,size=numOfNode)

def controller_checkup ():
    P_peak = 200  # watt
    P_idle = 100  # watt
    c_m = 100  # number of servers in each DC
    eta = 1.2
    a = 0.3 * P_peak * c_m * eta # 7200 watt
    b = P_peak * c_m * eta # 24000 watt

    # available RE resources at the beginning of the migration cycle
    RE_resources = []
    for dc in range(numOfNode):
        zeta_s = np.random.randint(a, b)
        RE_resources.append(zeta_s)
    #print("available RE = ", RE_resources)


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
    #print("amount of P dynamic in each DC = ", Vec_Pdyna) #this vector has 14 elements. each for one DC.
    #print("CPU requests of each DCs in the topology : ", all_cpu_reqs)

    P_static = (P_idle + (eta - 1) * P_peak) * 100  # is equal to 140 watt and 100 server in total in a DC
    #print(P_static)
    P_dynamic1 = np.array(Vec_Pdyna)
    P_dc = list(P_static + P_dynamic1)
    #print("workload (expressed in terms of power) in each DC before migration = ", P_dc)

    List_D = []
    for dc in range(numOfNode):
        if P_dc[dc] > RE_resources[dc]:
            List_D.append(dc)
    print("DC with insufficient RE = ", List_D)

    #initial BE cost calculation (before migration):
    fi_src = np.zeros(numOfNode)
    initial_cost = np.zeros(numOfNode)
    for i in range(numOfNode):
        fi_src[i] = P_dc[i] - RE_resources[i]
        initial_cost [i] = alpha[i] * fi_src[i]
    #print("Initial cost before migration = ", initial_cost)
    return List_D, P_dc, RE_resources, all_cpu_reqs, initial_cost


######################################### MAB Function ###########################################

def MAB(numOfNode, List_D, P_dc,RE_resources, all_cpu_reqs):
    ListOfDC = list(range(numOfNode))
    ListOfArms= list(set(ListOfDC)-set(List_D))
    print("List of Arms : ", ListOfArms)
    rho = 0.1
    beta_T = 22 
    c_ROADM = [163.02, 163.02, 163.02, 163.02, 163.02, 150.54, 150.54, 163.02, 150.54,175.5,163.02,163.02,163.02,163.02] #As this cost is fix, we have pre-calculate thhis.
    


    #Exploration
    cost = np.zeros((numOfNode,numOfNode)) # migration cost matrix  #src * des
    costNet = np.zeros((numOfNode,numOfNode)) # optical network costs   (src * des)
    lnk_d_mat = np.zeros((numOfNode,numOfNode)) #(src * des) a matrix to get the delay of the link
    t = 30 # window size
    remain_wl = P_dc # or we can say remaining power
    teta = 0
    reqNumVec = np.zeros((numOfNode, 1)) #number of migration in each DC
    bw_reqVec = np.zeros((numOfNode, NumOfReq))

    reg_vec =[]
    reg_dc_mat = np.zeros((numOfNode))
    arm_counter = [0] * numOfNode

    for dc in List_D:
        reg_dc = []
        reqNumber=0
        bw_req = list(np.random.randint(2, 20, size=NumOfReq)) # Gbps
        for i in range(NumOfReq):
            bw_reqVec[dc][i]= bw_req[i]

        for arm in ListOfArms:
            arm_counter[arm] += 1
            T = OG(teta, dc, arm,bw_req[reqNumber])
            link_delay = np.random.uniform(10,200) #milisec
            lnk_d_mat[dc][arm]= link_delay
            mig_cost = (rho * link_delay)

            net_cost = (beta_T * T) + (c_ROADM[dc]+c_ROADM[arm])

            cost[dc][arm] = mig_cost
            costNet[dc][arm] += net_cost
            Migrated_P = P_calculation(dc, all_cpu_reqs, reqNumber)
            remain_wl[dc] = P_dc[dc] - Migrated_P
            remain_wl[arm] = P_dc[arm] + Migrated_P

            cMig_opt = (beta_T * 0) +(rho * 105)  # millisec
            regret = np.abs(mig_cost + (beta_T * T) - cMig_opt)
            #print("reg = ",regret)
            reg_vec.append(regret)
            reg_dc.append(regret)

            reqNumber+=1
            teta +=1
        reqNumVec[dc][0] = reqNumber
        #print("for dc",dc, "the reg vec after exploration is ",reg_dc)
        #print(len(reg_dc))
        #reg_dc_mat[dc][0] = reg_dc
    #print("cost after exploration = ", cost)
    #print("remaining workload after exploration = ", remain_wl) # only dynamic power consumption has been considered for this term. as static term is always constatnt.
    #print("teta after exploration = ", teta)
    #print("request number vector : ", reqNumVec)
    #print("vector request of BW: ", bw_reqVec)



    #Explotation
    zi = 0.55
    for dc in List_D:
        regret2 =[]
        Index_dic = {}
        reqNumber1 = int(reqNumVec[dc][0])
        bw_req1 = bw_reqVec[dc]
        time_matrix = deque(maxlen= t)   # archive the delay matrix of the previous rounds
        while remain_wl[dc] >= RE_resources[dc]:
            teta += 1
            time_matrix.append(lnk_d_mat)
            Index_vec = []

            for arm in ListOfArms:
                arm_counter[arm] += 1
                tMean = t_mean(dc, arm, time_matrix)
                E_term = math.sqrt((zi * math.log(min(teta, t)))/arm_counter[arm])
                i = tMean - E_term  # this i is the estimated data transmission time
                mig_cost1 = (rho * i)
                Index_vec.append(mig_cost1)
                Index_dic[arm]= mig_cost1
            #print("index vector of DC ", dc, "is = ", Index_vec)
            #print("index dictionary = ", Index_dic)

            index_min = min(Index_vec)
            arm1 = [k for k, v in Index_dic.items() if v == index_min][0]
            #print("the arm related to DC", dc, " the minimum index = ", arm1)

            # Do the migration
            T = OG(teta, dc, arm1, bw_req1[reqNumber1])
            link_delay = np.random.uniform(10, 200)  # millisecond
            lnk_d_mat[dc][arm1] = link_delay
            Migrated_P = P_calculation(dc, all_cpu_reqs, reqNumber1)
            remain_wl[dc] = P_dc[dc] - Migrated_P
            remain_wl[arm1] = P_dc[arm1] + Migrated_P
            mig_cost2 = (rho * index_min)

            net_cost1 = (beta_T * T) + (c_ROADM[dc]+c_ROADM[arm1])

            cost[dc][arm1] += mig_cost2
            costNet[dc][arm1] += net_cost1

            cMig_opt1 = (beta_T * 0) + (rho * 105)
            regret1 = np.abs((mig_cost2 + (beta_T * T)) - cMig_opt1)
            reg_vec.append(regret1)
            regret2.append(regret1)

            reqNumber1 +=1
        reqNumVec[dc][0] = reqNumber1
        #regret3 = list(np.cumsum(regret2))
        #print("for dc ", dc, "the cum sum is ", regret3)
        #print("for dc ",dc," the reg vec after exploitation is ",regret2)
        #print(len(regret2))
    #print("reg_vec after explotation = ", reg_vec)

    #print("remaining workload after explotation = ", remain_wl)

    #print("total round : ", teta)

    BEcostOfDC = c_calculation(alpha, remain_wl) #this is the cost of DCs after finishing migration (IT IS NOT ABOUT MIGRATION COST)

    return cost, BEcostOfDC, reg_vec, teta, costNet


######################### Optical Grooming Function ###############################

numOfSBVT = 55 # We assume no limit in the numbers.
SubTrans_MaxCap = 40 # Gbps (The maximum capacity of carrier)
SBVTCap = 400 # Gbps (the total capacity of one SBVT)

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
            result1 = Operation2_2(src, des, bw_req, preSelectedNodes, DC_active_SBVT, SBVT_cap, NumOfSubT)
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
            result1 = Operation2_2(src, des, bw_req, preSelectedNodes, DC_active_SBVT, SBVT_cap, NumOfSubT)
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
