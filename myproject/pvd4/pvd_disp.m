clear all
close all
clc

flag1=0;%1-启用数据处理，0-取消数据处理
flag2=0;%1-启用st，0-取消st
flag3=0;%1-DRLR,0-LR
weight=0;%flag3-flag2-flag1:0-7间的数
%%%读取数据
data=readcell('sample_test.xlsx','Sheet','normal');
G=cell2mat(data(2:end,[2]));
T=cell2mat(data(2:end,[3]));
V=cell2mat(data(2:end,[4]));
I=cell2mat(data(2:end,[5]));
P=V.*I;
label=cell2mat(data(2:end,[6]));
num=size(V,1);
num_test=num-19;
state=zeros(num_test,1);
for i=1:num_test
    state(i)=label(i+19);
end
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
                VSTC(i)=71.5641;ISTC(i)=12.0103;PSTC(i)=859.5057;
            else
                VSTC(i)=75.4898;ISTC(i)=9.7160;PSTC(i)=733.4612;
            end
    end
end         
%%%数据处理
if flag1==0
    %取消
    %归一化的上下限
    if flag2==0
        M=[18.1166;72.5121;1244.5318];
        m=[4.5317;52.2542;309.4458];
    else
        M=[18.1166;77.6295;1244.5318];
        m=[2.7813;34.0915;213.0236];
    end
    I=(I-m(1))/(M(1)-m(1));
    V=(V-m(2))/(M(2)-m(2));
    P=(P-m(3))/(M(3)-m(3));
    x=zeros(num,3);
    x(:,1)=I;
    x(:,2)=V;
    x(:,3)=P; 
else
    %启用
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
    %归一化的上下限
    if flag2==0
        M=[13.4236;74.3335;958.8557];
        m=[8.8388;54.1935;524.6652];
    else
        M=[13.4335;78.4134;959.8794];
        m=[5.4542;33.1011;385.5465];
    end
    Istc=(Istc-m(1))/(M(1)-m(1));
    Vstc=(Vstc-m(2))/(M(2)-m(2));
    Pstc=(Pstc-m(3))/(M(3)-m(3));
    x=zeros(num,3);
    x(:,1)=Istc(1:num);
    x(:,2)=Vstc(1:num);
    x(:,3)=Pstc(1:num);
end
x_test=zeros(num_test,60);
for i=1:num_test
    x_test(i,:)=[x(i:i+19,1)' x(i:i+19,2)' x(i:i+19,3)'];
end
XSTC=zeros(num_test,60);
for i=1:num_test
    XSTC(i,:)=[ISTC(i:i+19)' VSTC(i:i+19)' PSTC(i:i+19)'];
end
y=state;
%%%重构特征向量
if flag2==1
    %启用
    betas=0.3;
    if flag1==0
        if flag3==0
            data_b=readcell('weight.xlsx','Sheet','b1');%LR+无处理
        else
            data_b=readcell('weight.xlsx','Sheet','b2');%DRLR+无处理
        end
    else
        if flag3==0
            data_b=readcell('weight.xlsx','Sheet','b3');%LR+处理
        else
            data_b=readcell('weight.xlsx','Sheet','b4');%DRLR+处理
        end
    end
    b=cell2mat(data_b);
    x_test=opt2(x_test,betas,b);
end
%%%算法选择
data_theta=readcell('weight.xlsx','Sheet',num2str(weight));
theta=cell2mat(data_theta(2:end,[1:4]));
y_pred=zeros(num_test,1);
if flag3==1
    y_P=sigmf(theta'*x_test',[1 0]);
else
    y_P=sigmf(theta(2:end,:)'*x_test'+theta(1,:)',[1 0]);
end
for i=1:num_test
    [maxn,maxp]=max(y_P(:,i));
    y_pred(i)=maxp;
end
    