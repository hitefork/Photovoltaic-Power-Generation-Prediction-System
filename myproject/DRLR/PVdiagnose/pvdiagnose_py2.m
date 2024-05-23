clear all
close all
clc

%%%读取数据
data=readcell('data2.xlsx','Sheet','test');
G=cell2mat(data(2:end,[2]));
T=cell2mat(data(2:end,[3]));
V=cell2mat(data(2:end,[4]));
I=cell2mat(data(2:end,[5]));
num=size(V,1);
num_sample=num-19;
state=zeros(num_sample,1);
for i=1:num_sample
    state(i)=cell2mat(data(i+19,[7]));
end

%%%数据处理
%定义参数
Gstc=1000;%STC下辐照度
Tstc=25;%STC下温度
alpha=0.00045;%短路电流温度系数,量纲1/℃
beta=-0.29376;%开路电压温度系数，量纲V/℃
gamma=-0.0031;%PV设备参数，量纲1/℃，gamma≈alpha+beta
delta=0.04;%PV设备参数，量纲1
Rs=0.83712;%串联电阻
k=0.05;%曲线修正系数
%数据处理
deltaI=alpha*(T-Tstc);
%deltaV=beta*(T-Tstc);
Istc=I./(1+deltaI)./(G/Gstc);
Vstc=V-beta*(Tstc-T)-deltaI*Rs-k*(Tstc-T).*Istc;
%Vstc=V./(1+deltaV)./(1+delta*log(G/Gstc));
%Pstc=I.*V*Gstc./(G.*(1+gamma*(T-Tstc)).*(1+delta*log(G/Gstc)));
Pstc=Vstc.*Istc;
%归一化:a=0,b=1
% M=[max(Istc);max(Vstc);max(Pstc)];
% m=[min(Istc);min(Vstc);min(Pstc)];
% M=[13.4292;74.3368;957.0184];
% m=[8.8461;53.4116;517.6447];
M=[13.5711;76.4276;948.1973];
m=[8.7813;53.7115;530.6448];
Istc=(Istc-m(1))/(M(1)-m(1));
Vstc=(Vstc-m(2))/(M(2)-m(2));
Pstc=(Pstc-m(3))/(M(3)-m(3));
%生成完整数据集
x=zeros(num,3);
x(:,1)=Istc;
x(:,2)=Vstc;
x(:,3)=Pstc;
x_test=zeros(num_sample,60);
for i=1:num_sample
    x_test(i,:)=[x(i,:),x(i+1,:),x(i+2,:),x(i+3,:),x(i+4,:),x(i+5,:),x(i+6,:),x(i+7,:),x(i+8,:),x(i+9,:),...
                 x(i+10,:),x(i+11,:),x(i+12,:),x(i+13,:),x(i+14,:),x(i+15,:),x(i+16,:),x(i+17,:),x(i+18,:),x(i+19,:)];
end
% betas=0.3;
% data_b=readcell('weight.xlsx','Sheet','b');
% b=cell2mat(data_b);
% x_test=opt2(x_test,betas,b);
y_test=state;
%%%测试
theta=readcell('weight.xlsx','Sheet','Sheet3');
best_theta=cell2mat(theta(2:end,[1:4]));
y_pred=zeros(num_sample,1);
y_P=sigmf(best_theta'*x_test',[1 0]);
for i=1:num_sample
    [maxn,maxp]=max(y_P(:,i));
    y_pred(i)=maxp;
end
figure
[mat,order]=confusionmat(y_test,y_pred);
cm = confusionchart(mat,order);