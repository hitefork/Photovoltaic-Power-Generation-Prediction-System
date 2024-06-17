function [my_V,my_I,my_state,M,ratio,accuracy,precision,recall] = test1()

  %%%读取数据
  data=readcell('data.xlsx','Sheet','Sheet1');
  G=cell2mat(data(2:end,[1]));
  T=cell2mat(data(2:end,[2]));
  V=cell2mat(data(2:end,[3]));
  I=cell2mat(data(2:end,[4]));
  my_state=cell2mat(data(2:end,[5]));

  my_V=V;
  my_I=I;
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
  %Istc=I+deltaI;
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

  num_r=randi([3,17],400,1);
  for i=1:400
    da1=x(i,1:3);
    da2=x(i,31:33);
    da1=repmat(da1,1,num_r(i));
    da2=repmat(da2,1,20-num_r(i));
    x(i,:)=cat(2,da1,da2);
  end
  y=state;
  %划分训练/测试集
  id=zeros(4,num_sample/4);
  for i=1:4
    id(i,:)=randperm(num_sample/4);
  end
  x_train=cat(1,x(id(1,1:0.8*num_sample/4),:),x(id(2,1:0.8*num_sample/4)+num_sample/4,:),x(id(3,1:0.8*num_sample/4)+num_sample/4*2,:),x(id(4,1:0.8*num_sample/4)+num_sample/4*3,:));
  y_train=cat(1,y(id(1,1:0.8*num_sample/4),:),y(id(2,1:0.8*num_sample/4)+num_sample/4,:),y(id(3,1:0.8*num_sample/4)+num_sample/4*2,:),y(id(4,1:0.8*num_sample/4)+num_sample/4*3,:));
  x_test=cat(1,x(id(1,0.8*num_sample/4+1:end),:),x(id(2,0.8*num_sample/4+1:end)+num_sample/4,:),x(id(3,0.8*num_sample/4+1:end)+num_sample/4*2,:),x(id(4,0.8*num_sample/4+1:end)+num_sample/4*3,:));
  y_test=cat(1,y(id(1,0.8*num_sample/4+1:end),:),y(id(2,0.8*num_sample/4+1:end)+num_sample/4,:),y(id(3,0.8*num_sample/4+1:end)+num_sample/4*2,:),y(id(4,0.8*num_sample/4+1:end)+num_sample/4*3,:));
  %%%测试
  theta=readcell('weight.xlsx','Sheet','Sheet1');
  best_theta=cell2mat(theta(2:end,[1:4]));
  y_pred=zeros(num_sample/5,1);
  y_P=sigmf(best_theta'*x_test',[1 0]);
  for i=1:num_sample/5
    [maxn,maxp]=max(y_P(:,i));
    y_pred(i)=maxp;
  end
  [mat,order]=confusionmat(y_test,y_pred);
  M=confusionmat(y_test,y_pred);
  %cm = confusionchart(mat,order);
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

end
