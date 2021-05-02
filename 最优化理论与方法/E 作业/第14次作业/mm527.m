clc;
clear;  %清理工作区变量
N=400;  %设定迭代次数
y=[-1,10];  %设定初始迭代值
d=[0.9427,0.8616,0.7384,0.5362,0.3739,0.3096];
t=[2000,5000,10000,20000,30000,50000];
P=zeros(1,N);%储存残差的下降情况

for step=1:N
    r=rk(y);
    P(step)=norm(r);
    A=d_r(y);
    s=-1*pinv(A'*A)*A'*r;
% 采用Armijo法则计算近似步长ak
%      ak=1;
%       rou=0.01;
%      r1=norm(rk(y+ak*s'));
%     r2=norm(r)+rou*ak*(r'*A*s);
%     while(r1> r2)
%         ak=0.5*ak;
%         r1=norm(rk(y+ak*s'));
%         r2=norm(r)+rou*ak*(r'*A*s);
%     end
    ak=0.05;
    y=y+ak*s';
end
disp('程序计算:')
y;
r=rk(y);
stv=sqrt(norm(r)/6)
x1=1/(y(2)*96.05)
x2=x1/y(1)

figure
subplot(2,1,1);
plot(P)
title('||r||_2^2','Color', 'r')
LP=log(P+1);
subplot(2,1,2);
plot(LP)
xlabel('n/迭代次数')
title('log(||r||_2^2+1)','Color', 'r')

[Y,resnorm] = lsqnonlin(@rk,[-0.5,1]);
disp('工具箱拟合:')
Y;
r_opt=rk(Y);
stv_opt=sqrt(norm(r_opt)/6)
x1_opt=1/(Y(2)*96.05)
x2_opt=x1/Y(1)

figure;
X=linspace(0,50000,50);
for i=1:50
y1(i)=phi(X(i),y);
y2(i)=phi(X(i),Y);
end
plot(X,y1,'b')
hold on;
plot(X,y2,'r--')
plot(t,d,'o')
legend('计算结果仿真','优化工具箱拟合','原始数据')



function A=d_r(y)
t=[2000,5000,10000,20000,30000,50000];
A=zeros(6,2);
for i=1:6
    A(i,1:2)=d_ri(t(i),y);
end
end

function dr=d_ri(t,y)
dr=[-1*t*(1-y(1)*t)^(y(2)-2),log(1-y(1)*t)*(1-y(1)*t)^(y(2)-1)];
end

function r=rk(y)
d=[0.9427,0.8616,0.7384,0.5362,0.3739,0.3096];
t=[2000,5000,10000,20000,30000,50000];
r=zeros(6,1);
for i=1:6
    r(i,1)=ri(t(i),y,d(i));
end
end

function r=ri(t,y,di)
r=phi(t,y)-di;
end

function z=phi(t,y)
z=(1-t*y(1))^(y(2)-1);
end