clear all
close all
clc

%%%读取数据
data=readcell('sample_l.xlsx','Sheet','Sheet1');
G=cell2mat(data(2:end,[1]));
T=cell2mat(data(2:end,[2]));
V=cell2mat(data(2:end,[3]));
I=cell2mat(data(2:end,[4]));
num=size(V,1);
num_sample=num/20;
state=zeros(num_sample,1);
for i=1:num_sample
    state(i)=cell2mat(data(2+(i-1)*20,[5]));
end
%无标签数据
datau1=readcell('sample_u.xlsx','Sheet','normal');
datau2=readcell('sample_u.xlsx','Sheet','LL');
datau3=readcell('sample_u.xlsx','Sheet','OC');
datau4=readcell('sample_u.xlsx','Sheet','PS');
datau5=readcell('sample_u.xlsx','Sheet','PS_new');
G=[G;cell2mat(datau1(2:end,[1]));cell2mat(datau2(2:end,[1]));cell2mat(datau3(2:end,[1]));cell2mat(datau4(2:end,[1]));cell2mat(datau5(2:end,[1]))];
T=[T;cell2mat(datau1(2:end,[2]));cell2mat(datau2(2:end,[2]));cell2mat(datau3(2:end,[2]));cell2mat(datau4(2:end,[2]));cell2mat(datau5(2:end,[2]))];
V=[V;cell2mat(datau1(2:end,[3]));cell2mat(datau2(2:end,[3]));cell2mat(datau3(2:end,[3]));cell2mat(datau4(2:end,[3]));cell2mat(datau5(2:end,[3]))];
I=[I;cell2mat(datau1(2:end,[4]));cell2mat(datau2(2:end,[4]));cell2mat(datau3(2:end,[4]));cell2mat(datau4(2:end,[4]));cell2mat(datau5(2:end,[4]))];
%%%数据处理
%定义参数
Gstc=1000;%STC下辐照度
Tstc=25;%STC下温度
alpha=0.00045;%短路电流温度系数,量纲1/℃
beta=-0.29376;%开路电压温度系数，量纲V/℃
gamma=-0.0031;%PV设备参数，量纲1/℃，gamma≈alpha+beta
delta=0.085;%PV设备参数，量纲1
Rs=0.83712;%串联电阻
k=0.04;%曲线修正系数
%数据处理
deltaI=alpha*(T-Tstc);
Istc=I./(1+deltaI)./(G/Gstc);
Vstc=V-beta*(Tstc-T)-deltaI*Rs-k*(Tstc-T).*Istc;
%Pstc=I.*V*Gstc./(G.*(1+gamma*(T-Tstc)).*(1+delta*log(G/Gstc)));
Pstc=Vstc.*Istc;
%归一化:a=0,b=1
M=[max(Istc);max(Vstc);max(Pstc)];
m=[min(Istc);min(Vstc);min(Pstc)];
Istc=(Istc-m(1))/(M(1)-m(1));
Vstc=(Vstc-m(2))/(M(2)-m(2));
Pstc=(Pstc-m(3))/(M(3)-m(3));
%生成完整数据集
x=zeros(num,3);
x(:,1)=Istc(1:num);
x(:,2)=Vstc(1:num);
x(:,3)=Pstc(1:num);
x=reshape(x',[],num_sample);
x=x';
for i=1:num_sample
    x(i,:)=(reshape((reshape(x(i,:),3,[]))',[],1))';
end
y=state;
%划分训练/测试集
id=zeros(4,num_sample/4);
for i=1:4
    id(i,:)=randperm(num_sample/4);
end
r_tt=1/6;%训练集占比
num_yz=500;%验证集数目
x_train=cat(1,x(id(1,1:r_tt*num_sample/4),:),x(id(2,1:r_tt*num_sample/4)+num_sample/4,:),x(id(3,1:r_tt*num_sample/4)+num_sample/4*2,:),x(id(4,1:r_tt*num_sample/4)+num_sample/4*3,:));
y_train=cat(1,y(id(1,1:r_tt*num_sample/4),:),y(id(2,1:r_tt*num_sample/4)+num_sample/4,:),y(id(3,1:r_tt*num_sample/4)+num_sample/4*2,:),y(id(4,1:r_tt*num_sample/4)+num_sample/4*3,:));
x_test=cat(1,x(id(1,r_tt*num_sample/4+1:r_tt*num_sample/4+num_yz/4),:),x(id(2,r_tt*num_sample/4+1:r_tt*num_sample/4+num_yz/4)+num_sample/4,:),x(id(3,r_tt*num_sample/4+1:r_tt*num_sample/4+num_yz/4)+num_sample/4*2,:),x(id(4,r_tt*num_sample/4+1:r_tt*num_sample/4+num_yz/4)+num_sample/4*3,:));
y_test=cat(1,y(id(1,r_tt*num_sample/4+1:r_tt*num_sample/4+num_yz/4),:),y(id(2,r_tt*num_sample/4+1:r_tt*num_sample/4+num_yz/4)+num_sample/4,:),y(id(3,r_tt*num_sample/4+1:r_tt*num_sample/4+num_yz/4)+num_sample/4*2,:),y(id(4,r_tt*num_sample/4+1:r_tt*num_sample/4+num_yz/4)+num_sample/4*3,:));
num_train=size(x_train,1);
num_test=size(x_test,1);
%处理无标签数据
xu=zeros(100000,3);
xu(:,1)=Istc(num+1:end);
xu(:,2)=Vstc(num+1:end);
xu(:,3)=Pstc(num+1:end);
xu=reshape(xu',[],5000);
xu=xu';
for i=1:num_sample
    xu(i,:)=(reshape((reshape(xu(i,:),3,[]))',[],1))';
end
xu1=xu([1:150 1001:1150 2001:2150 3001:3150 4001:5000],:);
x_unlabeled=xu1(randperm(1600,200),:); 

%%%self-taught learning
betas=0.3;%稀疏惩罚项权重
K=100;%迭代次数
s=300;%向量基维数
%[a,b]=opt1(x_unlabeled,betas,K,s);
weight=readcell('weight.xlsx','Sheet','Sheet1');
b=cell2mat(weight);
a_train=opt2(x_train,betas,b);

%%%模型训练
%Grid Search确定epsilon和kappa
epsilon=0.1:0.1:0.8;
kappa=9;
best_parameter=[0.1 9;0.1 9;0.8 9;0.6 9];
best_performance=zeros(4,1);
best_theta=zeros(s,4);%改
fold=5;
F1_score=zeros(1,fold);
accuracy=zeros(1,fold);
for h=1:4
    xtrainset=a_train;%改
    ytrainset=y_train;
    ctp=4;
    ctn=4;%标签错误数
    for i=1:num_train
        if ytrainset(i)==h
            ytrainset(i)=1;
            if ctp>0
                ytrainset(i)=-ytrainset(i);
                ctp=ctp-1;
            end
        else
            ytrainset(i)=-1;
            if ctn>0
                ytrainset(i)=-ytrainset(i);
                ctn=ctn-1;
            end
        end
    end
    %此处已加入标签错误
    id=randperm(size(ytrainset,1));
    xtrainset=xtrainset(id,:);
    ytrainset=ytrainset(id,:);
    for i=1:size(epsilon,2)
        for j=1:size(kappa,2)
            %交叉验证
            ind=crossvalind('Kfold',num_train/5*4,fold);
            for k=1:fold
                idtrain=(ind~=k);
                idtest=(ind==k);
                trainx=xtrainset(idtrain,:);
                trainy=ytrainset(idtrain,:);
                testx=xtrainset(idtest,:);
                testy=ytrainset(idtest,:);
                %求解优化问题
                theta=LP_ADMM(epsilon(i),kappa(j),300,trainx',trainy);
                %theta为1×60矩阵
                predy=(sigmf(theta'*testx',[1 0])>0.5)*2-1;
                %计算F1-score
                P=sum(testy==1);
                N=sum(testy==-1);
                PP=sum(predy'==1);
                TP=sum(predy'==1&testy==1);
                TN=sum(predy'==-1&testy==-1);
                accuracy(k)=(TP+TN)/(P+N);
                precision=TP/PP;
                if isnan(precision)
                    precision=0;
                end
                recall=TP/P;
                if isnan(recall)
                    recall=0;
                end
                F1_score(k)=2*precision*recall/(precision+recall);
            end
            F_mean=mean(F1_score,'omitnan');
            %F_mean=mean(accuracy);
            if F_mean>best_performance(h)
                best_performance(h)=F_mean;
                best_parameter(h,:)=[epsilon(i) kappa(j)];
            end
        end
    end
    best_theta(:,h)=LP_ADMM(best_parameter(h,1),best_parameter(h,2),700,xtrainset',ytrainset);
end

%%%测试
y_pred=zeros(num_test,1);
x_test=opt2(x_test,betas,b);
y_P=sigmf(best_theta'*x_test',[1 0]);
for i=1:num_test
    [maxn,maxp]=max(y_P(:,i));
    y_pred(i)=maxp;
end
figure
[mat,order]=confusionmat(y_test,y_pred);
cm = confusionchart(mat,order);
% %%%计算指标
% %占比
% ratio=[sum(y_pred==1);sum(y_pred==2);sum(y_pred==3);sum(y_pred==4)]/size(y_pred,1);
% %准确率
% accuracy=[mat(1,1)+sum(mat(2:4,2:4),'all');...
%           mat(2,2)+sum(mat([1 3:4],[1 3:4]),'all');...
%           mat(3,3)+sum(mat([1:2 4],[1:2 4]),'all');...
%           mat(4,4)+sum(mat(1:3,1:3),'all');]/size(y_test,1);
% %精确率
% precision=[mat(1,1)/sum(y_pred==1);mat(2,2)/sum(y_pred==2);mat(3,3)/sum(y_pred==3);mat(4,4)/sum(y_pred==4)];
% %召回率
% recall=[mat(1,1)/sum(y_test==1);mat(2,2)/sum(y_test==2);mat(3,3)/sum(y_test==3);mat(4,4)/sum(y_test==4)];