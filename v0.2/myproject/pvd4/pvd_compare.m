clear all
close all
clc

flag1=0;%1-启用数据处理，0-取消数据处理
flag2=0;%1-启用st，0-取消st
flag3=0;%1-DRLR,0-LR
weight=0;%flag3-flag2-flag1:0-7间的数
%%%读取数据
data=readcell('sample_test(500).xlsx','Sheet','Sheet1');
G=cell2mat(data(2:end,[1]));
T=cell2mat(data(2:end,[2]));
V=cell2mat(data(2:end,[3]));
I=cell2mat(data(2:end,[4]));
P=V.*I;
%label=cell2mat(data(2:end,[5]));
num=size(V,1);
num_sample=num/20;
state=zeros(num_sample,1);
for i=1:num_sample
    state(i)=cell2mat(data(2+(i-1)*20,[5]));
end
% %用于对比的式样：label=4时需要手动设置一下label_PS：2-PS2；3-PS3
% label_PS=2;
% VSTC=zeros(num,1);
% ISTC=zeros(num,1);
% PSTC=zeros(num,1);
% for i=1:num
%     switch(label(i))
%         case 1
%             VSTC(i)=71.2035;ISTC(i)=13.3179;PSTC(i)=948.2844;
%         case 2
%             VSTC(i)=56.5038;ISTC(i)=13.3596;PSTC(i)=754.8650;
%         case 3
%             VSTC(i)=71.2030;ISTC(i)=8.8787;PSTC(i)=632.1895;
%         case 4
%             if label_PS==2
%                 VSTC(i)=71.5641;ISTC(i)=12.0103;PSTC(i)=859.5057;
%             else
%                 VSTC(i)=75.4898;ISTC(i)=9.7160;PSTC(i)=733.4612;
%             end
%     end
% end         
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
    x(:,1)=Istc;
    x(:,2)=Vstc;
    x(:,3)=Pstc;
end
% x_test=zeros(num_test,60);
%     for i=1:num_test
%         x_test(i,:)=[x(i:i+19,1)' x(i:i+19,2)' x(i:i+19,3)'];
%     end
%     XSTC=zeros(num_test,60);
%     for i=1:num_test
%         XSTC(i,:)=[ISTC(i:i+19)' VSTC(i:i+19)' PSTC(i:i+19)'];
%     end
x=reshape(x',[],num_sample);
x=x';
for i=1:num_sample
    x(i,:)=(reshape((reshape(x(i,:),3,[]))',[],1))';
end
y=state;
%划分训练/测试集
%取消了随机抽取
% id=zeros(4,num_sample/4);
% for i=1:4
%     id(i,:)=randperm(num_sample/4);
% end
num_test=500;%测试集数目
x_test=x;
y_test=y;
% r_tt=5/12;
% x_test=cat(1,x(id(1,1:num_sample/4*r_tt),:),x(id(2,1:num_sample/4*r_tt)+num_sample/4,:),x(id(3,1:num_sample/4*r_tt)+num_sample/4*2,:),x(id(4,1:num_sample/4*r_tt)+num_sample/4*3,:));
% y_test=cat(1,y(id(1,1:num_sample/4*r_tt),:),y(id(2,1:num_sample/4*r_tt)+num_sample/4,:),y(id(3,1:num_sample/4*r_tt)+num_sample/4*2,:),y(id(4,1:num_sample/4*r_tt)+num_sample/4*3,:));
% x_test=cat(1,x(1:num_test/4,:),x(num_test/4+1:num_test/4*2,:),x(num_test/4*2+1:num_test/4*3,:),x(num_test/4*3+1:num_test,:));
% y_test=cat(1,y(1:num_test/4,:),y(num_test/4+1:num_test/4*2,:),y(num_test/4*2+1:num_test/4*3,:),y(num_test/4*3+1:num_test,:));
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
figure
[mat,order]=confusionmat(y_test,y_pred);
cm = confusionchart(mat,order);
%%%计算指标
%占比
ratio=[sum(y_pred==1);sum(y_pred==2);sum(y_pred==3);sum(y_pred==4)]/size(y_pred,1);
%准确率
accuracy=[mat(1,1)+sum(mat(2:4,2:4),'all');...
    mat(2,2)+sum(mat([1 3:4],[1 3:4]),'all');...
    mat(3,3)+sum(mat([1:2 4],[1:2 4]),'all');...
    mat(4,4)+sum(mat(1:3,1:3),'all');]/size(y_test,1);
%精确率
precision=[mat(1,1)/sum(y_pred==1);mat(2,2)/sum(y_pred==2);mat(3,3)/sum(y_pred==3);mat(4,4)/sum(y_pred==4)];
%召回率
recall=[mat(1,1)/sum(y_test==1);mat(2,2)/sum(y_test==2);mat(3,3)/sum(y_test==3);mat(4,4)/sum(y_test==4)];
%F1-分数
F1=2*precision.*recall./(precision+recall);
