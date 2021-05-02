%Conjugate Gradient method for Problem 5.19
clc;
clear;
N=20;
step=1;
G=hilb(N);
for i=1:N
    dD(i)=(2*i-1);
end
D=diag(dD);
B=ones(N,1);
x=zeros(N,1);
P=zeros(N,1);
g = G*x-B;
y=D*g;
x0=G\B;
P(step)=f(x,x0,G);
p = -y;
while(norm(g)/norm(B)>1e-7)
    step = step + 1;
    d=G*p;
    a=(g'*y)/(p'*d);
    x = x+a*p;
    g1=g+a*d;
    y1=D*g1;
    b=(g1'*y1)/(g'*y);
    g=g1;
    y=y1;
    P(step)=f(x,x0,G);
    p=-y+b*p;
end
X=linspace(0,step-1,step);
figure
subplot(2,1,1);
hold on
plot(X,log(P))
ylabel('log(||x-x*||_G^2)','Color', 'black')
title(['PCG:N=',num2str(N)])
subplot(2,1,2);
Eig=eig(D*G);
plot(Eig','-*')
title([num2str(N),'阶Hilbert矩阵预处理后特征值的分布'])

hold off
% y0=norm(G*x0-B)
% y=norm(G*x-B)
% xx=invhilb(N)*B;
% yy=norm(G*xx-B)

% norm(G*inv(G)-eye(N),'fro')
% norm(G*pinv(G)-eye(N),'fro')
% norm(G*invhilb(N)-eye(N),'fro')

%norm(hilb(N)*invhilb(N)-eye(N),'fro')
function z=f(x,x0,G)
    dx=x-x0;
    z=dx'*G*dx;
end