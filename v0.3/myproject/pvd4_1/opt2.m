function a=opt2(xl,betas,b)
s=size(b,1);
N=size(xl,1);
n=size(xl,2);
a=zeros(N,s);
for i=1:N
    fx=@(x)norm(xl(i,:)-x*b,2)^2+betas*norm(x,1);%x=1×s
    options=optimoptions('fmincon', 'MaxFunctionEvaluations',5000);
    a(i,:)=fmincon(fx,a(i,:),[],[],[],[],[],[],[],options);
end
end

