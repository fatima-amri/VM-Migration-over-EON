close all
clear all

numOfReq = [400, 440, 480, 520,560,600, 640, 680];

cnet_MAB = [62211.65, 73865.998, 74234.51, 84712.497, 88867.598, 97326.853, 109684.510, 112587.141];
cnet_noGrooming = [73086.036, 81644.474, 85410.116, 94512.86, 101005.459, 107090.506, 123338.612, 128075.53];

cnet_greedy= [79864.439, 84509.830, 89251.366, 99561.841, 105341.893, 111557.98, 128891.856,  136814.159  ];
cnet_greedy_noG = [83409.051, 88104.76, 95371.433, 106097.349, 112122.422, 119495.358, 135899.89, 144140.213 ];



%plotting the line graph:
plot(numOfReq, cnet_MAB, '-bs','LineWidth',2,'MarkerSize',10)
hold on 
plot(numOfReq, cnet_noGrooming,'-.ks' ,'LineWidth',2,'MarkerSize',10)
hold on 
plot(numOfReq, cnet_greedy,'-g*' ,'LineWidth',2,'MarkerSize',10)
hold on
plot(numOfReq, cnet_greedy_noG, '-.r*','LineWidth',2,'MarkerSize',10)


grid on
xlabel('Number of Requests','fontweight','bold','fontsize',13, 'FontName','times')
ylabel('Cost of Optical Network Elements (Cent)','fontweight','bold','fontsize',13, 'FontName','times')
legend('SW-LCB','SW-LCB Without Optical Grooming', '\epsilon-Greedy With Optical Grooming', '\epsilon-Greedy Without Optical Grooming','Location','northwest')
xlim([400,680])
ylim([60000, 145000]);
