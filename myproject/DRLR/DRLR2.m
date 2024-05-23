clear all
close all
clc
  
%%%读取数据
data=readcell('data.xlsx','Sheet','初始删LL2');
G=cell2mat(data(2:end,[2]));
T=cell2mat(data(2:end,[3]));
V=cell2mat(data(2:end,[9]));
I=cell2mat(data(2:end,[10]));
num=size(V,1);
num_sample=400;
state=[ones(num_sample/4,1);
       2*ones(num_sample/4,1);
       3*ones(num_sample/4,1);
       4*ones(num_sample/4,1);];

%%%数据处理
%定义参数
Gstc=1000;%STC下辐照度
Tstc=25;%STC下温度
alpha=0.00045;%短路电流温度系数,量纲1/℃
beta=-0.29376;%开路电压温度系数，量纲V/℃
Rs=0.83712;%串联电阻
k=0.05;%曲线修正系数
%数据处理
deltaI=alpha*(T-Tstc);
Istc=I./(1+deltaI)./(G/Gstc);
Vstc=V-beta*(Tstc-T)-deltaI*Rs-k*(Tstc-T).*Istc;
Pstc=Vstc.*Istc;
%归一化:a=0,b=1
M=[max(Istc);max(Vstc);max(Pstc)];
m=[min(Istc);min(Vstc);min(Pstc)];
Istc=(Istc-m(1))/(M(1)-m(1));
Vstc=(Vstc-m(2))/(M(2)-m(2));
Pstc=(Pstc-m(3))/(M(3)-m(3));
%生成完整数据集
X=zeros(num,3);
X(:,1)=Istc;
X(:,2)=Vstc;
X(:,3)=Pstc;
num_r=randi([3,17],num_sample,1);
x=zeros(num_sample,60);
for i=1:num_sample
    choice1=X(1:num_sample/4,:);
    switch(state(i))
        case 1
            choice2=X(1:num_sample/4,:);
        case 2
            choice2=X(num_sample/4+1:num_sample/4*2,:);
        case 3
            choice2=X(2*num_sample/4+1:num_sample/4*3,:);
        case 4
            choice21=X(3*num_sample/4+1:3*num_sample/4+20,:);%20=num_sample/4/5
            choice22=X(3*num_sample/4+21:3*num_sample/4+40,:);
            choice23=X(3*num_sample/4+41:3*num_sample/4+60,:);
            choice24=X(3*num_sample/4+61:3*num_sample/4+80,:);
            choice25=X(3*num_sample/4+81:end,:);
    end
    c1=choice1(randi(num_sample/4,[num_r(i),1]),:);
    c1=(reshape(c1',[],1))';
    if i>300&&i<=320
        c2=choice21(randi(num_sample/20,[20-num_r(i),1]),:);
    else
        if i>320&&i<=340
            c2=choice22(randi(num_sample/20,[20-num_r(i),1]),:);
        else
            if i>340&&i<=360
                c2=choice23(randi(num_sample/20,[20-num_r(i),1]),:);
            else
                if i>360&&i<=380
                    c2=choice24(randi(num_sample/20,[20-num_r(i),1]),:);
                else
                    if i>380
                        c2=choice25(randi(num_sample/20,[20-num_r(i),1]),:);
                    else
                        c2=choice2(randi(num_sample/4,[20-num_r(i),1]),:);
                    end
                end
            end
        end
    end
    c2=(reshape(c2',[],1))';
    x(i,:)=[c1 c2];
end
% for i=1:num_sample
%     x(i,:)=(reshape((reshape(x(i,:),3,[]))',[],1))';
% end
y=state;
%划分训练/测试集
id=zeros(4,num_sample/4);
for i=1:4
    id(i,:)=randperm(num_sample/4);
end
r_tt=0.5;%训练集占比
x_train=cat(1,x(id(1,1:r_tt*num_sample/4),:),x(id(2,1:r_tt*num_sample/4)+num_sample/4,:),x(id(3,1:r_tt*num_sample/4)+num_sample/4*2,:),x(id(4,1:r_tt*num_sample/4)+num_sample/4*3,:));
y_train=cat(1,y(id(1,1:r_tt*num_sample/4),:),y(id(2,1:r_tt*num_sample/4)+num_sample/4,:),y(id(3,1:r_tt*num_sample/4)+num_sample/4*2,:),y(id(4,1:r_tt*num_sample/4)+num_sample/4*3,:));
x_test=cat(1,x(id(1,r_tt*num_sample/4+1:end),:),x(id(2,r_tt*num_sample/4+1:end)+num_sample/4,:),x(id(3,r_tt*num_sample/4+1:end)+num_sample/4*2,:),x(id(4,r_tt*num_sample/4+1:end)+num_sample/4*3,:));
y_test=cat(1,y(id(1,r_tt*num_sample/4+1:end),:),y(id(2,r_tt*num_sample/4+1:end)+num_sample/4,:),y(id(3,r_tt*num_sample/4+1:end)+num_sample/4*2,:),y(id(4,r_tt*num_sample/4+1:end)+num_sample/4*3,:));
num_train=size(x_train,1);
num_test=size(x_test,1);

%%%模型训练
%Grid Search确定epsilon和kappa
epsilon=0.1:0.1:0.5;
kappa=9;
best_parameter=[0.1 9;0.1 9;0.4 9;0.1 9];
best_performance=zeros(4,1);
best_theta=zeros(60,4);
fold=5;
F1_score=zeros(1,fold);
accuracy=zeros(1,fold);
recall=zeros(1,fold);
precision=zeros(1,fold);
for h=1:4
    xtrainset=x_train;
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
    %此处已加入标签错误
    id=randperm(size(ytrainset,1));
    xtrainset=xtrainset(id,:);
    ytrainset=ytrainset(id,:);
%     if h>2
%     for i=1:size(epsilon,2)
% %         if h==3
% %             epsilon=0.8; 
% %         else
% %             epsilon=0.6;
% %         end
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
%                 theta=LP_ADMM(epsilon(i),kappa(j),500,trainx',trainy);
%                 %theta为1×60矩阵
%                 predy=(sigmf(theta'*testx',[1 0])>0.5)*2-1;
%                 %计算F1-score
%                 P=sum(testy==1);
%                 N=sum(testy==-1);
%                 PP=sum(predy'==1);
%                 TP=sum(predy'==1&testy==1);
%                 TN=sum(predy'==-1&testy==-1);
%                 accuracy(k)=(TP+TN)/(P+N);
%                 precision(k)=TP/PP;
%                 if isnan(precision(k))
%                     precision(k)=0;
%                 end
%                 recall(k)=TP/P;
%                 if isnan(recall(k))
%                     recall(k)=0;
%                 end
%                 F1_score(k)=2*precision(k)*recall(k)/(precision(k)+recall(k));
%             end
%             F_mean=mean(F1_score,'omitnan');
%             %F_mean=mean(accuracy);
%             if F_mean>best_performance(h)
%                 best_performance(h)=F_mean;
%                 best_parameter(h,:)=[epsilon(i) kappa(j)];
%             end
%         end
%     end
%     end
    best_theta(:,h)=LP_ADMM(best_parameter(h,1),best_parameter(h,2),700,xtrainset',ytrainset);
end
        
%%%测试
y_pred=zeros(num_test,1);
y_P=sigmf(best_theta'*x_test',[1 0]);
for i=1:num_test
    [maxn,maxp]=max(y_P(:,i));
    y_pred(i)=maxp;
end
figure
[mat,order]=confusionmat(y_test,y_pred);
cm = confusionchart(mat,order);