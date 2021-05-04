%此程序为计算题5.7的牛顿法
clc;
clear;
N=10;
X=zeros(N,1);
P=zeros(N,1);
x=7.7;
step=1;
X(step)=x;
fun =@(x) 9*x-4*log(x-7);
%while (abs(g(x))>0.000001)
while (step<N+1)
    step=step+1;
    x=x-g(x)./G(x);
    X(step)=x;
    P(step)=f(x);
   %x=x-0.25*(x-7)*(9*x-67)
end
%plot(X)
%[s1,s2]= fminsearch(fun,7);
figure;
hold on
fplot(@(x) 9*x-4*log(x-7),[7.2,7.8])
plot(X,9*X-4*log(X-7))
function y=f(x)
y=9*x-4*log(x-7);
end

function y=g(x)
y=9-4./(x-7);
end 

function y=G(x)
y=4./(x-7).^2;
end
