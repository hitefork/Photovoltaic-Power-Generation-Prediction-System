%green:[0.2 0.7 0.1]
%red:[0.95 0.2 0.1]
%blue:[0.1 0.1 0.9]
%yellow:[0.929 0.694 0.125]
%clear all;close all;clc;
data1=readcell('sample_test.xlsx','Sheet','LL');
G=cell2mat(data1(2:end,2));
T=cell2mat(data1(2:end,3));
V=cell2mat(data1(2:end,4));
I=cell2mat(data1(2:end,5));
P=V.*I;
num=size(V,1);
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
% xlabel('时间点/5min','FontSize',25);ylabel('光伏出力/W','FontSize',25);
%%%训练数据出力图
% data2=readcell('训练数据展示画图用.xlsx','Sheet','LL');
% V=cell2mat(data2(2:end,4));
% I=cell2mat(data2(2:end,5));
% P=V.*I;
% label=cell2mat(data2(2:end,6));
% num_fault=sum(label==1);
% time=data2(2:end,1);
% t=zeros(1,size(time,1));
% for i=1:size(time,1)
%     t(i)=datenum(time{i,1});
% end
% t1=t(1:num_fault);t2=t(num_fault:end);
% plot(t1,P(1:num_fault),'LineStyle','-','LineWidth',2,'Color',[0.2 0.7 0.1]);hold on;
% plot(t2,P(num_fault:45),'LineStyle','-','LineWidth',2,'Color',[0.95 0.2 0.1]);hold on;
% datetick('x',15);
% xlabel('时间','FontSize',20);ylabel('光伏出力/W','FontSize',20);
% axis([min(t) inf -inf inf]);
%%%数据处理对比图
num=size(V,1);
time=data1(2:end,1);
t=zeros(1,size(time,1));
for i=1:size(time,1)
    t(i)=datenum(time{i,1});
end
figure;
subplot(3,1,1);plot(t,V,'LineStyle','-','LineWidth',1);ylabel('真实电压/V');datetick('x',15);axis([min(t) inf 54 71]);
subplot(3,1,2);plot(t,I,'LineStyle','-','LineWidth',1);ylabel('真实电流/A');datetick('x',15);axis([min(t) inf 5 15.2]);
subplot(3,1,3);plot(t,P,'LineStyle','-','LineWidth',1);ylabel('真实功率/W');datetick('x',15);axis([min(t) inf 400 1000]);
xlabel('时间');
%normal:axis([0 45 70 72.3]);axis([0 45 5 15.5]);axis([0 45 480 1100])
%LL:axis([0 45 54 71]);axis([0 45 5 15.2]);axis([0 45 400 1000])
%OC:axis([0 45 70.8 72.5]);axis([0 45 6.5 13.2]);axis([0 45 400 1000])
%PS2:axis([0 45 71 76]);axis([0 45 6.5 13.3]);axis([0 45 400 1000])
%PS3:axis([0 45 70 75]);axis([0 45 7.5 13.5]);axis([0 45 500 1000])
figure(2);
subplot(3,1,1);plot(t,Vstc,'LineStyle','-','LineWidth',1);hold on;plot(t,VSTC,'LineStyle','-','LineWidth',1);ylabel('STC电压/V');datetick('x',15);axis([min(t) inf 55 72]);legend('实际','式样');
subplot(3,1,2);plot(t,Istc,'LineStyle','-','LineWidth',1);hold on;plot(t,ISTC,'LineStyle','-','LineWidth',1);ylabel('STC电流/A');datetick('x',15);axis([min(t) inf 12.5 13.5]);
subplot(3,1,3);plot(t,Pstc,'LineStyle','-','LineWidth',1);hold on;plot(t,PSTC,'LineStyle','-','LineWidth',1);ylabel('STC功率/W');datetick('x',15);axis([min(t) inf 740 960]);
% subplot(3,1,1);plot(t,Vstc,'LineStyle','-','LineWidth',1);ylabel('STC电压/V');datetick('x',15);axis([min(t) inf 55 72]);
% subplot(3,1,2);plot(t,Istc,'LineStyle','-','LineWidth',1);ylabel('STC电流/A');datetick('x',15);axis([min(t) inf 12.5 13.5]);
% subplot(3,1,3);plot(t,Pstc,'LineStyle','-','LineWidth',1);ylabel('STC功率/W');datetick('x',15);axis([min(t) inf 740 960]);
xlabel('时间');
%normal:axis([0 45 70 72]);axis([0 45 13 13.5]);axis([0 45 920 960]);
%LL:axis([0 45 55 72]);axis([0 45 12.5 13.5]);axis([0 45 740 960]);
%OC:axis([0 45 60 75]);axis([0 45 8.4 13.8]);axis([0 45 600 980]);
%PS2:axis([0 45 68 78]);axis([0 45 9.5 13.5]);axis([0 45 720 980]);
%PS3:axis([0 45 60 80]);axis([0 45 9 14]);axis([0 45 600 1000]);
%%%饼图
% data = [26 24.8 24 25.2];
% %data = [25 25 25 25];
% labels = {'正常26%', '短路24.8%', '开路24%', '阴影25.2%'};
% %labels = {'正常25%', '短路25%', '开路25%', '阴影25%'};
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
% time=data(21:end,1);
% t=zeros(1,size(time,1));
% for i=1:size(time,1)
%     t(i)=datenum(time{i,1});
% end
% plot(t,y_test,'LineStyle','-',...
%                      'LineWidth',2,...
%                      'Marker','v',...
%                      'MarkerSize',3,...
%                      'MarkerFaceColor','#0072BD');
% datetick('x',15);
% axis([-inf inf 0 6]);grid on;hold on;
% plot(t,y_pred,'LineStyle','-',...
%                      'LineWidth',2,...
%                      'Marker','^',...
%                      'MarkerSize',3,...
%                      'MarkerFaceColor','#D95319');
% datetick('x',15);
% axis([-inf inf 0 6]);grid on;hold on;
% set(gca,'xtick',t([1 6 11 16 21 26]),'FontSize',15);
% set(gca,'ytick',[1 2 3 4],'yticklabel',{'正常','短路','开路','阴影'},'FontSize',15);
% xlabel('时间','FontSize',15);
% legend('真实结果','预测结果');
%%%训练数据组成图
% x={'带标签数据','无标签数据'};
% y=[50 50 50 50 0;20 20 20 20 120];
% b=bar(y); 
% b(1).FaceColor=[0.2 0.7 0.1];
% b(2).FaceColor=[0.95 0.2 0.1];
% b(3).FaceColor=[0.1 0.1 0.9];
% b(4).FaceColor=[0.929 0.8 0.125];
% b(5).FaceColor=[1 0.5 1];
% xtips1=b(1).XEndPoints;xtips2=b(2).XEndPoints;xtips3=b(3).XEndPoints;xtips4=b(4).XEndPoints;xtips5=b(5).XEndPoints;
% ytips1=b(1).YEndPoints;ytips2=b(2).YEndPoints;ytips3=b(3).YEndPoints;ytips4=b(4).YEndPoints;ytips5=b(5).YEndPoints;
% labels1=string(b(1).YData);labels2=string(b(2).YData);labels3=string(b(3).YData);labels4=string(b(4).YData);labels5=string(b(5).YData);
% text(xtips1,ytips1,labels1,'HorizontalAlignment','center','VerticalAlignment','bottom');
% text(xtips2,ytips2,labels2,'HorizontalAlignment','center','VerticalAlignment','bottom');
% text(xtips3,ytips3,labels3,'HorizontalAlignment','center','VerticalAlignment','bottom');
% text(xtips4,ytips4,labels4,'HorizontalAlignment','center','VerticalAlignment','bottom');
% text(xtips5,ytips5,labels5,'HorizontalAlignment','center','VerticalAlignment','bottom');
% ylim([0,150]);
% set(gca, 'xticklabel', x,'FontSize',20);
% ylabel('样本数量','FontSize',20);
% legend('正常','短路','开路','阴影','其它阴影','FontSize',15,'Location','NorthWest');
%%%辐照度图
data3=readcell('辐照度图.xlsx','Sheet','测试数据');
time=data3(2:end,1);
t=zeros(size(time,1),1);
for i=1:size(time,1)
    t(i)=datenum(time{i,1});
end
G=cell2mat(data3(2:end,2));
T=cell2mat(data3(2:end,3));
num_all=size(G,1);
plot(t,G,'LineStyle','-','LineWidth',1);
datetick('x',25,'keepticks');
set(gca,'FontSize',5);
axis([min(t) max(t) -inf inf]);
xlabel('时间','FontSize',20);ylabel('辐照度（W/㎡）','FontSize',20);
