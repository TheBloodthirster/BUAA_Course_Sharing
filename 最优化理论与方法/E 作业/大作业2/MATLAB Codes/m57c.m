clc;
clear;
N=8;
X=zeros(N,1);
P=zeros(N,1);
step=0;
hold on
for i=0:0.25:N
    step=step+1;
    X(step)=5+i;
    x=X(step);
    for j=1:100
        x=x-0.25*(x-7)*(9*x-67);
    end
    P(step)=x;
end
hold on
plot(P)
%[s1,s2]= fminsearch(fun,7);

function y=f(x)
y=9*x-4*log(x-7);
end

function y=g(x)
y=9-4./(x-7);
end 

function y=G(x)
y=4./(x-7).^2;
end
