clc;
clear;
N=8;
for i=0:0.05:0.8
    X=zeros(1,N);
    x=7+i;
    step=1;
    X(step)=x;
    while (step<N+1)
        step=step+1;
        x=x-0.25*(x-7)*(9*x-67);
        X(step)=x;
    end
    hold on
    plot(X)
end