close all
clear all

NumOfReq = [400, 440, 480, 520, 560,600, 640, 680];
c_before = [338612.662, 360735.45, 384823.185, 422858.22, 470530.75, 514626.157, 551831.752, 608295.03];
c_after = [111371.129, 150444.56, 176345.20, 217604.52, 248386.76, 317588.675, 371920.075, 443297.37];

imprv_percentage = [71.27, 62.41, 61.27, 55.930, 51.56, 44.903, 37.29, 34.037];

plot(NumOfReq, c_before,'-.r*','LineWidth',2,'MarkerSize',10)
hold on
plot(NumOfReq, c_after,'-bs','LineWidth',2,'MarkerSize',10)

grid on
xlabel('Number of Requests','fontweight','bold','fontsize',13, 'FontName','times')
ylabel('BE Consumption Cost of DCs (Cent)','fontweight','bold','fontsize',13,'FontName','times')
legend('Before Migration', 'After Migration Using SW-LCB','Location','northwest','FontName','times')
ylim([99000,610000])


%for 400 requests:
x1=[0.15 0.15];
y1=[0.44 0.16];
annotation('textarrow',x1,y1,'String',' 71% ','FontSize',10,'Linewidth',1)

%for 520 requests:
x2=[0.44 0.44];
y2=[0.56 0.33];
annotation('textarrow',x2,y2,'String',' 56% ','FontSize',10,'Linewidth',1)

%for 600 requests:
x3=[0.65 0.65];
y3=[0.71 0.48];
annotation('textarrow',x3,y3,'String',' 45% ','FontSize',10,'Linewidth',1)

%for 680 requests:
x4=[0.85 0.85];
y4=[0.87 0.68];
annotation('textarrow',x4,y4,'String',' 34% ','FontSize',10,'Linewidth',1)
