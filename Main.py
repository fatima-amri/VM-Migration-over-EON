from datetime import datetime

start = datetime.now()

vec_c_before = []
vec_c_after = []
improvement_lst = []
mig_mat =[]
mig_vec =[]
reg = []
teta_vec =[]
costNet_vec =[]

# As we used some random variables, we repeat the simulation 100 times, and consider the average.
for r in range(100): 
    (List_D, P_dc, RE_resources, all_cpu_reqs, initial_cost) = controller_checkup()
    (COST, BEcostOfDC, reg_vec, teta, costNet) = MAB(numOfNode, List_D, P_dc, RE_resources, all_cpu_reqs)

    teta_vec.append(teta)

    costNetsum = np.sum(costNet)
    costNet_vec.append(costNetsum)

    reg1 = list(np.cumsum(reg_vec))
    reg.append(reg1)


    total_BEc_before = cost_cal(initial_cost)
    vec_c_before.append(total_BEc_before)

    total_BEc_after = cost_cal(BEcostOfDC)
    vec_c_after.append(total_BEc_after)

    Topo_migCost = np.sum(COST)
    mig_vec.append(Topo_migCost)

    if total_BEc_after < total_BEc_before:
        print("successful")
        p = (100 - ((total_BEc_after / total_BEc_before) * 100))
        improvement_lst.append(p)



for m in range(1):
    l = len(reg[m])
    if round(mean_teta)-2 <= l <= round(mean_teta)+2:
        print(reg[m])


mean_before = average(vec_c_before)
mean_after = average(vec_c_after)
print("cost avg before migration = ", mean_before)
print("cost avg after migration =  ", mean_after)

mean_percentage = average(improvement_lst)
print("in average the improvement is ", mean_percentage, " percent")

mean_migCost = average(mig_vec)
print("avg of migration cost = ", mean_migCost)

mean_netCost = average(costNet_vec)
print("avg of network elements' cost = ", mean_netCost)

Total_cost = mean_after + mean_migCost
print("Final Total Cost = ",Total_cost)


print("time = ", datetime.now()-start)
