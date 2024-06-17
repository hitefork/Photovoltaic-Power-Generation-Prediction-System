function [a,b]=opt1(xu,betas,K,s)
n=size(xu,2);
N=size(xu,1);
b=ones(s,n)/100;
a=zeros(N,s);
for i=1:K
    for j=1:N
        fx=@(x)norm(xu(j,:)-x*b,2)^2+betas*norm(x,1);
        a(j,:)=fmincon(fx,a(j,:),[],[]);
    end
    for j=1:n
        fy=@(y)sum(vecnorm(xu(:,j)-a*y,2,2).^2);
        b(:,j)=fmincon(fy,b(:,j),[],[],[],[],[],[],@mycon);
    end
%     fy=@(y)sum(vecnorm(a*y,2,2));
%     options=optimoptions('fmincon', 'MaxFunctionEvaluations',30000);
%     b=fmincon(fy,b,[],[],[],[],[],[],[],options);
%     fx=@(x)sum(vecnorm(xu'-b'*x',2,1).^2+betas*vecnorm(x',1,1));
%     a=fmincon(fx,a,[],[]);
%     fy=@(y)sum(vecnorm(xu'-y'*a',2,1).^2+betas*vecnorm(a',1,1));
%     b=fmincon(fy,b,[],[],[],[],[],[],@mycon);
end
end