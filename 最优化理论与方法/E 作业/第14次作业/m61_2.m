clc;
clear;
global d;
N=14;
size=1.5;
q = @(x) -9*x(1).^2+10*x(2).^2-2*x(1)+10*x(2)+3.5;
qq = @(x,y) -9*x.^2+10*y.^2-2*x+10*y+3.5;
fcontour(qq,[-size size -size size])
hold on;
plot(-1/9,-1/2,'rd')
plot(0,0,'mo')
P=zeros(N+1,2);
x0=[0,0];
lb=[-10,-10];
ub=[10,10];
x2=1/81+1/4;
for i=1:N
    d=i/10;
    P(i+1,:) = fmincon(q,x0,[],[],[],[],lb,ub,@circlecon);
    if d^2<=1
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