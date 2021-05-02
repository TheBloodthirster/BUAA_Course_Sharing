clc;
clear;
global d;
N=20;
q = @(x) 21*x(1).^2+10*x(2).^2-2*x(1)-20*x(2)+11;
qq = @(x,y) 21*x.^2+10*y.^2-2*x-20*y+11;
fcontour(qq,[-1.5 1.5 -1.5 1.5])
hold on;
plot(1/21,1,'rd')
plot(0,0,'mo')
P=zeros(N+1,2);
x0=[0,0];
lb=[-10,-10];
ub=[10,10];
x2=1+(1/21)^2;
for i=1:N
    d=i/10;
    P(i+1,:) = fmincon(q,x0,[],[],[],[],lb,ub,@circlecon);
    if d^2<=x2
        fimplicit(@(x,y) x.^2+y.^2-d^2,'--')
    end
end
plot(P(:,1),P(:,2),'-x')
legend('q contours','minimum')

function [c,ceq] = circlecon(x)
global d;
c = x(1)^2+x(2)^2-d^2;
ceq = [];
end