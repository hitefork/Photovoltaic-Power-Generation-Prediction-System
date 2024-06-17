function [theta,q]=ADMM(lambda,kappa,circle,trainx,trainy)
N=size(trainx,2);%样本数
n=size(trainx,1);%特征向量维数
%初始化
gamma=1.05;%gamma>=1，参考文献DRLR
rho=0.001;%参考文献DRLR
theta=ones(n,1);
w=ones(N,1);
mu=zeros(N,1);
Z=zeros(N,n);
for i=1:N
    mu(i,:)=trainy(i)*theta'*trainx(:,i);
end
for i=1:N
    Z(i,:)=trainy(i)*trainx(:,i)';
end
%迭代求解
A=zeros(1,n);
B=zeros(1,N);
for i=1:circle
    %theta-update
    fx=@(x)rho/2*(norm(Z*x-mu-w/rho,2))^2+(sum(svd(x))<=lambda);
    theta=fmincon(fx,theta,A,0);
    %mu-update
    fy=@(y)rho/2*(norm(y-(Z*theta-(w+1/2/N-exp(-y)./(1+exp(-y)))/rho),2))^2+1/2/N*sum(abs(y-lambda*kappa));
    mu=fmincon(fy,mu,B,0);
    %other-update
    w=w-rho*(Z*theta-mu);
    rho=gamma*rho;
end
%计算结果
g=sum(svd(theta))<=lambda;
f=1/N*sum(log(1+exp(-mu))+0.5*(mu-lambda*kappa));
P=1/2/N*sum(abs(mu-lambda*kappa));
q=f+P+g;
end


