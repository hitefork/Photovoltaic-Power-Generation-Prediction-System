clear all
close all
clc

%%%读取数据
data=readcell('data.xlsx','Sheet','Sheet11');
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
x(:,1)=Istc;
x(:,2)=Vstc;
x(:,3)=Pstc;
x=reshape(x',[],num_sample);
x=x';
num_r=randi([3,17],num_sample,1);
for i=1:num_sample
    da1=x(i,1:3);
    da2=x(i,31:33);
    da1=repmat(da1,1,num_r(i));
    da2=repmat(da2,1,20-num_r(i));
    x(i,:)=cat(2,da1,da2);
end
y=state;
numl=400;
numu=100;
xl=x(1:numl,:);
xu=x(numl+1:end,:);
yl=y(1:numl,:);
yu=y(numl+1:end,:);
%划分训练/测试集
id=zeros(5,numl/4);
for i=1:5
    id(i,:)=randperm(numl/4);
end
r_tt=0.5;%训练集占比
x_train=cat(1,xl(id(1,1:r_tt*numl/4),:),xl(id(2,1:r_tt*numl/4)+numl/4,:),xl(id(3,1:r_tt*numl/4)+numl/4*2,:),xl(id(4,1:r_tt*numl/4)+numl/4*3,:));
y_train=cat(1,yl(id(1,1:r_tt*numl/4),:),yl(id(2,1:r_tt*numl/4)+numl/4,:),yl(id(3,1:r_tt*numl/4)+numl/4*2,:),yl(id(4,1:r_tt*numl/4)+numl/4*3,:));
%x_test=cat(1,xl(id(1,r_tt*numl/4+1:end),:),xl(id(2,r_tt*numl/4+1:end)+numl/4,:),xl(id(3,r_tt*numl/4+1:end)+numl/4*2,:),xl(id(4,r_tt*numl/4+1:end)+numl/4*3,:),xu(id(5,0.8*numu+1:end),:));
%y_test=cat(1,yl(id(1,r_tt*numl/4+1:end),:),yl(id(2,r_tt*numl/4+1:end)+numl/4,:),yl(id(3,r_tt*numl/4+1:end)+numl/4*2,:),yl(id(4,r_tt*numl/4+1:end)+numl/4*3,:),yu(id(5,0.8*numu+1:end),:));
x_test=cat(1,xl(id(1,r_tt*numl/4+1:end),:),xl(id(2,r_tt*numl/4+1:end)+numl/4,:),xl(id(3,r_tt*numl/4+1:end)+numl/4*2,:),xl(id(4,r_tt*numl/4+1:end)+numl/4*3,:));
y_test=cat(1,yl(id(1,r_tt*numl/4+1:end),:),yl(id(2,r_tt*numl/4+1:end)+numl/4,:),yl(id(3,r_tt*numl/4+1:end)+numl/4*2,:),yl(id(4,r_tt*numl/4+1:end)+numl/4*3,:));
%x_unlabeled=xu(id(5,1:0.8*numu),:);
x_unlabeled=xu;
num_train=size(x_train,1);
num_test=size(x_test,1);

%%%self-taught learning
betas=0.3;%稀疏惩罚项权重
K=100;%迭代次数
s=300;%向量基维数
[a,b]=opt1(x_unlabeled,betas,K,s);
a_train=opt2(x_train,betas,b);

%%%模型训练
%Grid Search确定epsilon和kappa
epsilon=0.1:0.1:0.5;
kappa=1:2:10;
best_parameter=zeros(4,2);
best_performance=zeros(4,1);
best_theta=zeros(s,4);%改
fold=5;
F1_score=zeros(1,fold);
accuracy=zeros(1,fold);
best_parameter=[0.1 9;0.1 9;0.1 9;0.1 9];
for h=1:4
    xtrainset=a_train;%改
    ytrainset=y_train;
    ctp=10;
    ctn=10;%标签错误数
    for i=1:num_train
        if ytrainset(i)==h
            ytrainset(i)=1;
%             if ctp>0
%                 ytrainset(i)=-ytrainset(i);
%                 ctp=ctp-1;
%             end
        else
            ytrainset(i)=-1;
%             if ctn>0
%                 ytrainset(i)=-ytrainset(i);
%                 ctn=ctn-1;
%             end
        end
    end
%     %此处已加入标签错误
    id=randperm(size(ytrainset,1));
    xtrainset=xtrainset(id,:);
    ytrainset=ytrainset(id,:);
%     for i=1:size(epsilon,2)
%         for j=1:size(kappa,2)
%             %交叉验证
%             ind=crossvalind('Kfold',num_sample/5*4,fold);
%             for k=1:fold
%                 idtrain=(ind~=k);
%                 idtest=(ind==k);
%                 trainx=xtrainset(idtrain,:);
%                 trainy=ytrainset(idtrain,:);
%                 testx=xtrainset(idtest,:);
%                 testy=ytrainset(idtest,:);
%                 %求解优化问题
%                 theta=LP_ADMM(epsilon(i),kappa(j),300,trainx',trainy);
%                 %theta为1×60矩阵
%                 predy=(sigmf(theta'*testx',[1 0])>0.5)*2-1;
%                 %计算F1-score
%                 P=sum(testy==1);
%                 N=sum(testy==-1);
%                 PP=sum(predy'==1);
%                 TP=sum(predy'==1&testy==1);
%                 TN=sum(predy'==-1&testy==-1);
%                 accuracy(k)=(TP+TN)/(P+N);
%                 precision=TP/PP;
%                 if isnan(precision)
%                     precision=0;
%                 end
%                 recall=TP/P;
%                 if isnan(recall)
%                     recall=0;
%                 end
%                 F1_score(k)=2*precision*recall/(precision+recall);
%             end
%             F_mean=mean(F1_score,'omitnan');
%             %F_mean=mean(accuracy);
%             if F_mean>best_performance(h)
%                 best_performance(h)=F_mean;
%                 best_parameter(h,:)=[epsilon(i) kappa(j)];
%             end
%         end
%     end
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
