close all
clear all

numOfReq = [400, 440, 480, 520, 560,600, 640, 680];
% with Tr cost = 22
c_MAB_noMig = [338612.662, 360735.45, 384823.185, 422858.22, 470530.75, 514626.157, 551831.752, 608295.03];
c_MAB =[111996.175, 151088.89, 176997.912, 218276.979, 249083.57, 318296.073, 372650.38, 444044.44];
c_kube =[120305.188, 160559.57, 191198.42, 225520.734, 266616.77, 332883.30, 397781.452, 465523.408 ];
c_greedy = [159413.938, 182425.200, 222158.248, 252664.684, 294853.963, 359207.801, 433763.105, 509218.67 ]; 
c_JRE = [209541.734, 222710.020, 269916.860, 281264.952, 349778.787, 415515.573, 488969.055, 545655.280];

%{
%plotting the bar chart:
figure(1)
cost =[c_MAB(:),c_noGrooming(:), c_greedy(:), c_greedy_noG(:),c_JRE(:), c_MAB_noMig(:)];
bar(numOfReq,cost,'grouped')
grid on
xlabel('Number of Requests','fontweight','bold','fontsize',12, 'FontName','times')
ylabel('Toatal Cost','fontweight','bold','fontsize',12, 'FontName','times')
legend('SW-LCB','SW-LCB Without OG', 'Epsilon-Greedy With OG','Epsilon-Greedy Without OG' , 'Anycast-JRE', 'No Migration' ,'Location','northwest')
%}

%{plotting the line graph:
figure(2)
plot(numOfReq, c_MAB_noMig, '-c+','LineWidth',2,'MarkerSize',7)
hold on
plot(numOfReq, c_JRE, '-.r^','LineWidth',2,'MarkerSize',7)
hold on 
plot(numOfReq, c_greedy,'-g*' ,'LineWidth',2,'MarkerSize',7)
hold on 
plot(numOfReq, c_kube,'-.k+' ,'LineWidth',2,'MarkerSize',7)
hold on
plot(numOfReq, c_MAB, '-bs','LineWidth',2,'MarkerSize',7)


grid on
xlabel('Number of Requests','fontweight','bold','fontsize',13, 'FontName','times')
ylabel('Total Cost (Cent)','fontweight','bold','fontsize',13, 'FontName','times')
legend('No Migration','Anycast-JRE','\epsilon-Greedy','KUBE','SW-LCB','Location','northwest')
xlim([400,680])
ylim([100000, 610000])
