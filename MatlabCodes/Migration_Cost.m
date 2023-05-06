close all
clear all

numOfReq = [400, 440, 480, 520,560,600, 640, 680];


cmig_MAB = [620.219,642.765, 657.634, 663.532, 684.864, 709.931, 722.419, 776.470];
cmig_kube =[825.905, 837.905, 845.866, 867.306, 903.450, 943.589, 965.046, 1062.129];
cmig_greedy= [1180.360, 1238.21, 1312.003, 1424.276, 1561.450, 1603.640, 1755.074, 1825.623];

%plotting the bar chart:
cost =[cmig_MAB(:),cmig_kube(:), cmig_greedy(:)];
bar(numOfReq,cost,'grouped')
grid on
xlabel('Number of Requests','fontweight','bold','fontsize',13, 'FontName','times')
ylabel('Migration Cost (Cent)','fontweight','bold','fontsize',13, 'FontName','times')
legend('SW-LCB','KUBE', '\epsilon-Greedy','Location','northwest')
ylim([0, 1850]);




