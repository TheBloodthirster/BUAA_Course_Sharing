clc;
clear;
n=100;
X = sym('x', [2*n,1]) ; 
f=0;
for i=1:n
    f=f+(1-X(2*i-1))^2+10*(X(2*i)-X(2*i-1)^2)^2;  
end
x0=-500*ones(2*n,1);
F= matlabFunction(f,'Vars',{X});
grad=gradient(f,X); 
G=matlabFunction(grad,'Vars',{X});

%{
options=optimset('Display','iter','GradObj','on','Algorithm','trust-region');
[x,fval,exitflag,output]=fminunc({F,G},x0,options)
%}

options = optimoptions(@fminunc,'Display','iter','Algorithm','quasi-newton');
[x,fval,exitflag,output]=fminunc(F,x0,options)
