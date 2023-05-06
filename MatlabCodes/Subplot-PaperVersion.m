close all
clear all

NumOfReq = [400, 440, 480, 520, 560,600, 640, 680];
c_before = [338612.662, 360735.45, 384823.185, 422858.22, 470530.75, 514626.157, 551831.752, 608295.03];
c_after = [111371.129, 150444.56, 176345.20, 217604.52, 248386.76, 317588.675, 371920.075, 443297.37];
imprv_percentage = [71.27, 62.41, 61.27, 55.930, 51.56, 44.903, 37.29, 34.037];


numOfReq = [400, 440, 480, 520,560,600, 640, 680];

cmig_MAB = [620.219,642.765, 657.634, 663.532, 684.864, 709.931, 722.419, 776.470];
cmig_kube =[825.905, 837.905, 845.866, 867.306, 903.450, 943.589, 965.046, 1062.129];
cmig_greedy= [1180.360, 1238.21, 1312.003, 1424.276, 1561.450, 1603.640, 1755.074, 1825.623];


%1
subplot(2,1,1)
comp = [c_before(:),c_after(:)];
bar(NumOfReq, comp, 'grouped')
grid on
xlabel(['Number of Requests',newline,'(a)'],'fontweight','bold','fontsize',10, 'FontName','times')
ylabel('BE Consumption Cost of DCs','fontweight','bold','fontsize',10,'FontName','times')
lgnd1 = legend('Before Migration', 'After Migration Using SW-LCB','Location','northwest','FontName','times')
set(lgnd1,'color','none', 'EdgeColor', 'none');

%2
subplot(2,1,2)
cost =[cmig_MAB(:),cmig_kube(:), cmig_greedy(:)];
bar(numOfReq,cost,'grouped')
grid on
xlabel(['Number of Requests',newline,'(b)'],'fontweight','bold','fontsize',10, 'FontName','times')
ylabel('Migration Cost','fontweight','bold','fontsize',10, 'FontName','times')
lgnd2 = legend('SW-LCB','KUBE', '\epsilon-Greedy','Location','northwest')
set(lgnd2,'color','none', 'EdgeColor', 'none');



%%
  
  
numOfReq = [400, 440, 480, 520,560,600, 640, 680];
cnet_MAB = [62211.65, 73865.998, 74234.51, 84712.497, 88867.598, 97326.853, 109684.510, 112587.141];
cnet_noGrooming = [73086.036, 81644.474, 85410.116, 94512.86, 101005.459, 107090.506, 123338.612, 128075.53];
cnet_greedy= [79864.439, 84509.830, 89251.366, 99561.841, 105341.893, 111557.98, 128891.856,  136814.159  ];
cnet_greedy_noG = [83409.051, 88104.76, 95371.433, 106097.349, 112122.422, 119495.358, 135899.89, 144140.213 ];


c_MAB_noMig = [338612.662, 360735.45, 384823.185, 422858.22, 470530.75, 514626.157, 551831.752, 608295.03];
c_MAB =[111996.175, 151088.89, 176997.912, 218276.979, 249083.57, 318296.073, 372650.38, 444044.44];
c_kube =[120305.188, 160559.57, 191198.42, 225520.734, 266616.77, 332883.30, 397781.452, 465523.408 ];
c_greedy = [159413.938, 182425.200, 222158.248, 252664.684, 294853.963, 359207.801, 433763.105, 509218.67 ];

%1
subplot(2,1,1)
netcost = [cnet_greedy_noG(:),cnet_greedy(:),cnet_noGrooming(:), cnet_MAB(:)];
bar(numOfReq,netcost,'grouped')
grid on
xlabel(['Number of Requests',newline,'(a)'],'fontweight','bold','fontsize',10, 'FontName','times')
ylabel('Cost of Optical Network Devices','fontweight','bold','fontsize',10, 'FontName','times')
lgnd3 = legend('\epsilon-Greedy Without Optical Grooming','\epsilon-Greedy With Optical Grooming','SW-LCB Without Optical Grooming','SW-LCB', 'Location','northwest');
set(lgnd3,'color','none', 'EdgeColor', 'none');

%2
subplot(2,1,2)
total = [c_MAB(:),c_kube(:), c_greedy(:), c_MAB_noMig(:)];
bar(numOfReq,total,'grouped')
grid on
xlabel(['Number of Requests',newline,'(b)'],'fontweight','bold','fontsize',10, 'FontName','times')
ylabel('Total Cost','fontweight','bold','fontsize',10, 'FontName','times')
lgnd4 = legend('SW-LCB','KUBE','\epsilon-Greedy','No Migration','Location','northwest')
set(lgnd4,'color','none', 'EdgeColor', 'none');
