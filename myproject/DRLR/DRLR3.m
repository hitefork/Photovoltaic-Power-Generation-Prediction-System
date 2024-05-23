
function [accuracy,precision,recall,F1_score]=DRLR()  
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

    %%%数据处理
    %定义参数
    Gstc=1000;%STC下辐照度
    Tstc=25;%STC下温度
    alpha=0.00045;%短路电流温度系数,量纲1/℃
    beta=-0.29376;%开路电压温度系数，量纲V/℃
    gamma=-0.0031;%PV设备参数，量纲1/℃，gamma≈alpha+beta
    delta=0.085;%PV设备参数，量纲1
    Rs=0.83712;%串联电阻
    k=0.05;%曲线修正系数
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
    for i=1:num_sample
        x(i,:)=(reshape((reshape(x(i,:),3,[]))',[],1))';
    end
    y=state;
    %划分训练/测试集
    id=zeros(4,num_sample/4);
    for i=1:4
        id(i,:)=randperm(num_sample/4);
    end
    r_tt=1/20;%训练集占比
    num_yz=500;%验证集数目
    x_train=cat(1,x(id(1,1:r_tt*num_sample/4),:),x(id(2,1:r_tt*num_sample/4)+num_sample/4,:),x(id(3,1:r_tt*num_sample/4)+num_sample/4*2,:),x(id(4,1:r_tt*num_sample/4)+num_sample/4*3,:));
    y_train=cat(1,y(id(1,1:r_tt*num_sample/4),:),y(id(2,1:r_tt*num_sample/4)+num_sample/4,:),y(id(3,1:r_tt*num_sample/4)+num_sample/4*2,:),y(id(4,1:r_tt*num_sample/4)+num_sample/4*3,:));
    x_test=cat(1,x(id(1,r_tt*num_sample/4+1:r_tt*num_sample/4+num_yz/4),:),x(id(2,r_tt*num_sample/4+1:r_tt*num_sample/4+num_yz/4)+num_sample/4,:),x(id(3,r_tt*num_sample/4+1:r_tt*num_sample/4+num_yz/4)+num_sample/4*2,:),x(id(4,r_tt*num_sample/4+1:r_tt*num_sample/4+num_yz/4)+num_sample/4*3,:));
    y_test=cat(1,y(id(1,r_tt*num_sample/4+1:r_tt*num_sample/4+num_yz/4),:),y(id(2,r_tt*num_sample/4+1:r_tt*num_sample/4+num_yz/4)+num_sample/4,:),y(id(3,r_tt*num_sample/4+1:r_tt*num_sample/4+num_yz/4)+num_sample/4*2,:),y(id(4,r_tt*num_sample/4+1:r_tt*num_sample/4+num_yz/4)+num_sample/4*3,:));
    num_train=size(x_train,1);
    num_test=size(x_test,1);

    %%%模型训练
    %Grid Search确定epsilon和kappa
    epsilon=0;
    kappa=[9 50 200 500 900];
    best_parameter=[0.1 9;0.1 9;0.1 9;0.1 9];
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
            else
                ytrainset(i)=-1;

            end
        end
        %此处已加入标签错误
        id=randperm(size(ytrainset,1));
        xtrainset=xtrainset(id,:);
        ytrainset=ytrainset(id,:);

        best_theta(:,h)=LP_ADMM(best_parameter(h,1),best_parameter(h,2),700,xtrainset',ytrainset);
    end
            
    %%%测试
    y_pred=zeros(num_test,1);
    y_P=sigmf(best_theta'*x_test',[1 0]);
    for i=1:num_test
        [maxn,maxp]=max(y_P(:,i));
        y_pred(i)=maxp;
    end
    [mat,order]=confusionmat(y_test,y_pred);
    cm = confusionchart(mat,order);

end