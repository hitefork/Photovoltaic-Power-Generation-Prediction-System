%green:[0.2 0.7 0.1]
%red:[0.95 0.2 0.1]
%blue:[0.1 0.1 0.9]
%yellow:[0.929 0.694 0.125]
%clear all;close all;clc;
data1=readcell('sample_test.xlsx','Sheet','OC');
G=cell2mat(data1(2:end,2));
T=cell2mat(data1(2:end,3));
V=cell2mat(data1(2:end,4));
I=cell2mat(data1(2:end,5));
P=V.*I;
label=cell2mat(data1(2:end,6));
%用于对比的式样：label=4时需要手动设置一下label_PS：2-PS2；3-PS3
label_PS=2;
VSTC=zeros(num,1);
ISTC=zeros(num,1);
PSTC=zeros(num,1);
for i=1:num
    switch(label(i))
        case 1
            VSTC(i)=71.2035;ISTC(i)=13.3179;PSTC(i)=948.2844;
        case 2
            VSTC(i)=56.5038;ISTC(i)=13.3596;PSTC(i)=754.8650;
        case 3
            VSTC(i)=71.2030;ISTC(i)=8.8787;PSTC(i)=632.1895;
        case 4
            if label_PS==2
                VSTC(i)=75.4898;ISTC(i)=9.7160;PSTC(i)=733.4612;
            else
                VSTC(i)=75.5123;ISTC(i)=9.7131;PSTC(i)=733.4596;
            end
    end
end
%数据处理
Gstc=1000;%STC下辐照度
Tstc=25;%STC下温度
alpha=0.00045;%短路电流温度系数,量纲1/℃
beta=-0.29376;%开路电压温度系数，量纲V/℃
gamma=-0.0031;%PV设备参数，量纲1/℃，gamma≈alpha+beta
delta=0.085;%PV设备参数，量纲1
Rs=0.83712;%串联电阻
k=0.04;%曲线修正系数
%转换
deltaI=alpha*(T-Tstc);
Istc=I./(1+deltaI)./(G/Gstc);
Vstc=V-beta*(Tstc-T)-deltaI*Rs-k*(Tstc-T).*Istc;
Pstc=Vstc.*Istc;
%%%测试数据出力图
% num_all=size(V,1);num_fault=26;
% t1=0:num_fault-1;t2=num_fault-1:num_all-1;
% plot(t1,P(1:num_fault),'LineStyle','-','LineWidth',2,'Color',[0.2 0.7 0.1]);hold on;
% plot(t2,P(num_fault:num_all),'LineStyle','-','LineWidth',2,'Color',[0.1 0.1 0.9]);hold on;
% xlabel('时间点','FontSize',25);ylabel('光伏出力/W','FontSize',25);
%%%训练数据出力图
% data2=readcell('训练数据展示画图用.xlsx','Sheet','ul');
% V=cell2mat(data2(2:end,4));
% I=cell2mat(data2(2:end,5));
% P=V.*I;
% label=cell2mat(data2(2:end,6));
% num_fault=sum(label==1);
% t1=0:num_fault-1;t2=num_fault-1:44;
% plot(t1,P(1:num_fault),'LineStyle','-','LineWidth',2,'Color',[0.2 0.7 0.1]);hold on;
% plot(t2,P(num_fault:45),'LineStyle','-','LineWidth',2,'Color',[0.929 0.694 0.125]);hold on;
% xlabel('时间点','FontSize',20);ylabel('光伏出力/W','FontSize',20);
%%%数据处理对比图
% num=size(V,1);t=0:num-1;
% figure;
% subplot(3,1,1);plot(t,V,'LineStyle','-','LineWidth',1);axis([0 45 70 75]);ylabel('真实电压/V');
% subplot(3,1,2);plot(t,I,'LineStyle','-','LineWidth',1);axis([0 45 7.5 13.5]);ylabel('真实电流/A');
% subplot(3,1,3);plot(t,P,'LineStyle','-','LineWidth',1);axis([0 45 500 1000]);ylabel('真实功率/W');
% xlabel('时间点');
% %normal:axis([0 45 70 72.3]);axis([0 45 5 15.5]);axis([0 45 480 1100])
% %LL:axis([0 45 54 71]);axis([0 45 5 15.2]);无
% %OC:axis([0 45 70.8 72.5]);axis([0 45 6.5 13.2]);无
% %PS2:axis([0 45 71 76]);axis([0 45 6.5 13.3]);无
% %PS3:axis([0 45 70 75]);axis([0 45 7.5 13.5]);axis([0 45 500 1000]);
% figure(2);
% subplot(3,1,1);plot(t,Vstc,'LineStyle','-','LineWidth',1);hold on;plot(t,VSTC,'LineStyle','-','LineWidth',1);axis([0 45 60 80]);ylabel('STC电压/V');
% subplot(3,1,2);plot(t,Istc,'LineStyle','-','LineWidth',1);hold on;plot(t,ISTC,'LineStyle','-','LineWidth',1);axis([0 45 9 14]);ylabel('STC电流/A');
% subplot(3,1,3);plot(t,Pstc,'LineStyle','-','LineWidth',1);hold on;plot(t,PSTC,'LineStyle','-','LineWidth',1);axis([0 45 600 1000]);ylabel('STC功率/W');
% xlabel('时间点');
% %normal:axis([0 45 70 72]);axis([0 45 13 13.5]);axis([0 45 920 960]);
% %LL:axis([0 45 55 72]);axis([0 45 12.5 13.5]);axis([0 45 740 960]);
% %OC:axis([0 45 60 75]);axis([0 45 8.4 13.8]);axis([0 45 600 980]);
% %PS2:axis([0 45 68 78]);axis([0 45 9.5 13.5]);axis([0 45 720 980]);
% %PS3:axis([0 45 60 80]);axis([0 45 9 14]);axis([0 45 600 1000]);
%%%饼图
% data = [22.4 26 22.6 29];
% labels = {'正常22.4%', '短路26%', '开路22.6%', '阴影29%'};
% p=pie(data, labels);
% %改字体大小
% p(2).FontSize=25;
% p(4).FontSize=25;
% p(6).FontSize=25;
% p(8).FontSize=25;
% %直接为每个扇区指定颜色
% colors = [[0.2 0.7 0.1];[0.95 0.2 0.1];[0.1 0.1 0.9];[0.929 0.8 0.125]];
% colormap(colors);
% hold on;
% %中间画白圆
% tt=linspace(0,2*pi,200);
% fill(cos(tt).*.5,sin(tt).*.5,'w');
%%%柱状图
% x={'正常','短路','开路','阴影'};
% y=[95.4 83.2;96.2 92.4;97.2 88.4;95.6 78];
% bar(y); 
% ylim([70,100]);
% set(gca, 'xticklabel', x,'FontSize',30);
% ylabel('准确率/%','FontSize',30);
%%%预测结果对比图
t=0:25;
plot(t,y_test,'LineStyle','-',...
                     'LineWidth',2,...
                     'Marker','v',...
                     'MarkerSize',3,...
                     'MarkerFaceColor','#0072BD');
axis([0 25 0 6]);grid on;hold on;
plot(t,y_pred,'LineStyle','-',...
                     'LineWidth',2,...
                     'Marker','^',...
                     'MarkerSize',3,...
                     'MarkerFaceColor','#D95319');
axis([0 25 0 6]);grid on;hold on;
set(gca, 'ytick',[1 2 3 4],'yticklabel',{'正常','短路','开路','阴影'},'FontSize',20);
xlabel('时间点','FontSize',20);
legend('真实结果','预测结果');