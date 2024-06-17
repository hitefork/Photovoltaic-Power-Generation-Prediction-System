function theta=LP_ADMM(epsilon,kappa,circle,trainx,trainy)
lambda1=0;
lambda2=0;
lambda3=1;
lambda4=0.2785/epsilon;
r=0.618;
q2=100;
q3=0;
while (abs(q2-q3)>1)&&(abs(lambda2-lambda3)>0.0001)
   lambda2=r*lambda1+(1-r)*lambda4;
   lambda3=(1-r)*lambda1+r*lambda4;
   %[theta1,q1]=ADMM(lambda1,kappa,circle,trainx,trainy);
   [theta2,q2]=ADMM(lambda2,kappa,circle,trainx,trainy);
   [theta3,q3]=ADMM(lambda3,kappa,circle,trainx,trainy);
   %[theta4,q4]=ADMM(lambda4,kappa,circle,trainx,trainy);
   if q2<q3
       lambda4=lambda3;theta=theta2;
   else
       lambda1=lambda2;theta=theta3;
   end
end           
end