%本实验采用最速下降法，步长为精确步长
%%
%用符号表达式定义目标函数
clc;
clear;
syms x1 x2;
X=[x1,x2];
f=(10*X(1)^2-18*X(1)*X(2)+10*X(2)^2)/2+4*X(1)-15*X(2)+13;
F=eval(['@(x1,x2)',vectorize(f)]);
fx=diff(f,x1); %求f对x1偏导数
fy=diff(f,x2); %求f对x2偏导数
fxx=diff(fx,x1); %求二阶偏导数 对x1再对x1
fxy=diff(fx,x2); %求二阶偏导数 对x1再对x2
fyx=diff(fy,x1); %求二阶偏导数 对x2再对x1
fyy=diff(fy,x2); %求二阶偏导数 对x2再对x2
Gradient=[fx;fy];     %计算梯度表达式
Hesse=[fxx,fxy;fyx,fyy];
x=[-0.4,0];        %定义初始点

%%
N=20;     %总迭代次数
e=0.000001;
P=zeros(N,2);    %储存点的轨迹

%OPT=zeros(N,2);    
g=subs(Gradient,[x1 x2],[x(1) x(2)]);
step=1;
P(step,:)=x;
optim_fx=double(subs(f,[x1 x2],[x(1) x(2)]));
fprintf('Step[%d]:  x=[ %f %f ] optim_fx=%f\n',step,x(1),x(2),double(optim_fx));
OPT(step,:)=optim_fx;   %储存最优值下降的轨迹
%%
while (norm(g)>e  && step < N)       %当g的2-范数小于特定值时，或迭代次数到达上限时，停止迭代
    step=step+1;
    %计算目标函数点x(k)处一阶导数值
    g=subs(Gradient,[x1 x2],[x(1) x(2)]);
    %计算目标函数点x(k)处Hesse矩阵
    G=subs(Hesse,[x1 x2],[x(1) x(2)]);
    %计算目标函数点x(k)处搜索方向p
    %p=-G\g';
    p=-g;
    %点x(k)处的搜索步长
   
    ak=1;
    ak=Alpha(p,g,G);
%     xk=x+ak*double(p');
%     %采用Armijo法则计算近似步长ak
%     while(F(xk(1),xk(2)) > (F(x(1),x(2))+0.1*double(p'*g)*ak))
%         ak=0.5*ak;
%         xk=x+ak*double(p');
%     end
    x=x+double(ak*p');
    %输出结果
    optim_fx=double(subs(f,[x1 x2],[x(1) x(2)]));
    P(step,:)=x;
    OPT(step,:)=optim_fx;
    kk(step-1)=(optim_fx+22)/(OPT(step-1,:)+22);
    fprintf('Step[%d]:  x=[ %f %f ] optim_fx=%f,kk=%f \n',step,x(1),x(2),double(optim_fx),kk(step-1));
    g=subs(Gradient,[x1 x2],[x(1) x(2)]);
end
%输出结果
optim_fx=subs(f,[x1 x2],[x(1) x(2)]);
fprintf('\n最速下降法,共迭代 %d 步\n结果：\n  x=[ %d %d ] optim_fx=%f\n',step,x(1),x(2),double(optim_fx));
P(step+1:N,:)=[];      %删去P中的多余空间\
figure;
plot(P(:,1),P(:,2))
hold on;
xx =linspace(-1,12);
yy = linspace(-1,7);
[X,Y] = meshgrid(xx,yy);
Z=F(X,Y);

contour(X,Y,Z,50)
plot(5,6,'rd')

% fplot(@(x) (9/10)*(x-5)+6)
% fplot(@(x) (10/9)*(x-5)+6)
legend('Iteration','q contours','minimum','L_1','L_2')
figure;
plot(OPT)
xlabel('n/迭代次数')
ylabel('q(x)')
title('函数值的下降过程')
figure;
plot(kk,'*-')
title('函数值收敛速度')
%%
% 最速下降法子程序，计算精确步长ak
function a=Alpha(p,g,G)
a=-(p'*g)/(p'*G*p);
a=double(a);
end