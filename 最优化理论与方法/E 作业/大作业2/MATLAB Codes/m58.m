%简单牛顿法
%For Problem 5.8  
%%
%用符号表达式定义目标函数
clc;
clear;
mu=1;
syms x1 x2;
X=[x1,x2];
f=-9*X(1)-10*X(2)-mu*(log(100-X(1)-X(2))+log(X(1))+log(X(2))+log(50-X(1)+X(2)));

F=eval(['@(x1,x2)',vectorize(f)]);
fx=diff(f,x1); %求f对x1偏导数
fy=diff(f,x2); %求f对x2偏导数
fxx=diff(fx,x1); %求二阶偏导数 对x1再对x1
fxy=diff(fx,x2); %求二阶偏导数 对x1再对x2
fyx=diff(fy,x1); %求二阶偏导数 对x2再对x1
fyy=diff(fy,x2); %求二阶偏导数 对x2再对x2
Gradient=[fx;fy];     %计算梯度表达式
Hesse=[fxx,fxy;fyx,fyy];

figure;
hold on;

xx =linspace(0,75,300);
yy = linspace(0,100,400);
[X,Y] = meshgrid(xx,yy);

Z=(X+Y<100).*(X-Y<50).*real(F(X,Y));

imagesc([0,75],[0,100],Z)
axis tight

colorbar
title('\mu=1 with linear seach')


%%
x=[8,90];        %定义初始点

N=100;     %总迭代次数
e=0.000001;
P=zeros(N,2);    %储存点的轨迹
OPT=zeros(N,2);     %储存最优值下降的轨迹
g=subs(Gradient,[x1 x2],[x(1) x(2)]);
step=1;
P(step,:)=x;
optim_fx=subs(f,[x1 x2],[x(1) x(2)]);
fprintf('Step[%d]:  x=[ %f %f ] optim_fx=%f\n',step,x(1),x(2),double(optim_fx));
OPT(step,:)=optim_fx;

while (norm(g)>e  && step < N)       %当g的2-范数小于特定值时，或迭代次数到达上限时，停止迭代
    if(Check(x))
        break;
    end
    step=step+1;
    %计算目标函数点x(k)处一阶导数值
    g=subs(Gradient,[x1 x2],[x(1) x(2)]);
    %计算目标函数点x(k)处Hesse矩阵
    G=subs(Hesse,[x1 x2],[x(1) x(2)]);
    %计算目标函数点x(k)处搜索方向p
    p=-inv(G)*g;
    %p=-g;
    %点x(k)处的搜索步长
    %ak=Alpha(p,g,G);
    %ak=1;
    ak=1;
    xk=x+ak*double(p');
%    采用Armijo法则计算近似步长ak
%         while(F(xk(1),xk(2)) > (F(x(1),x(2))+0.01*double(p'*g)*ak)||Check(x+ak*double(p')))
%             ak=0.5*ak;
%             xk=x+ak*double(p');
%         end
    x=x+double(ak*p');
    %输出结果
    optim_fx=subs(f,[x1 x2],[x(1) x(2)]);
    fprintf('Step[%d]:  x=[ %f %f ] optim_fx=%f\n',step,x(1),x(2),double(optim_fx));
    P(step,:)=x;
    OPT(step,:)=optim_fx;
    g=subs(Gradient,[x1 x2],[x(1) x(2)]);
end
%输出结果
optim_fx=subs(f,[x1 x2],[x(1) x(2)]);
fprintf('\n牛顿Armijo回溯法,,共迭代 %d 步\n结果：\n  x=[ %d %d ] optim_fx=%f\n',step,x(1),x(2),double(optim_fx));
P(step+1:N,:)=[];      %删去P中的多余空间
OPT(step+1:N,:)=[];  


%figure;
plot(P(:,1),P(:,2),'-ro')
%axis equal tight
%figure;
%plot(OPT,'b')

%%
x=[1,40];        %定义初始点

N=100;     %总迭代次数
e=0.000001;
P=zeros(N,2);    %储存点的轨迹
OPT=zeros(N,2);     %储存最优值下降的轨迹
g=subs(Gradient,[x1 x2],[x(1) x(2)]);
step=1;
P(step,:)=x;
optim_fx=subs(f,[x1 x2],[x(1) x(2)]);
fprintf('Step[%d]:  x=[ %f %f ] optim_fx=%f\n',step,x(1),x(2),double(optim_fx));
OPT(step,:)=optim_fx;

while (norm(g)>e  && step < N)       %当g的2-范数小于特定值时，或迭代次数到达上限时，停止迭代
      if(Check(x))
        break;
    end
    step=step+1;
    %计算目标函数点x(k)处一阶导数值
    g=subs(Gradient,[x1 x2],[x(1) x(2)]);
    %计算目标函数点x(k)处Hesse矩阵
    G=subs(Hesse,[x1 x2],[x(1) x(2)]);
    %计算目标函数点x(k)处搜索方向p
    p=-inv(G)*g;
    %p=-g;
    %点x(k)处的搜索步长
    %ak=Alpha(p,g,G);
    %ak=1;
    ak=1;
    xk=x+ak*double(p');
%    采用Armijo法则计算近似步长ak
%         while(F(xk(1),xk(2)) > (F(x(1),x(2))+0.01*double(p'*g)*ak)||Check(x+ak*double(p')))
%             ak=0.5*ak;
%             xk=x+ak*double(p');
%         end
    x=x+double(ak*p');
    %输出结果
    optim_fx=subs(f,[x1 x2],[x(1) x(2)]);
    fprintf('Step[%d]:  x=[ %f %f ] optim_fx=%f\n',step,x(1),x(2),double(optim_fx));
    P(step,:)=x;
    OPT(step,:)=optim_fx;
    g=subs(Gradient,[x1 x2],[x(1) x(2)]);
end
%输出结果
optim_fx=subs(f,[x1 x2],[x(1) x(2)]);
fprintf('\n牛顿Armijo回溯法,,共迭代 %d 步\n结果：\n  x=[ %d %d ] optim_fx=%f\n',step,x(1),x(2),double(optim_fx));
P(step+1:N,:)=[];      %删去P中的多余空间
OPT(step+1:N,:)=[];  


%figure;
plot(P(:,1),P(:,2),'-black*')
%axis equal tight
%figure;
%plot(OPT,'b')
%%
x=[15,68.69];        %定义初始点

N=100;     %总迭代次数
e=0.000001;
P=zeros(N,2);    %储存点的轨迹
OPT=zeros(N,2);     %储存最优值下降的轨迹
g=subs(Gradient,[x1 x2],[x(1) x(2)]);
step=1;
P(step,:)=x;
optim_fx=subs(f,[x1 x2],[x(1) x(2)]);
fprintf('Step[%d]:  x=[ %f %f ] optim_fx=%f\n',step,x(1),x(2),double(optim_fx));
OPT(step,:)=optim_fx;

while (norm(g)>e  && step < N)       %当g的2-范数小于特定值时，或迭代次数到达上限时，停止迭代
      if(Check(x))
        break;
    end
    step=step+1;
    %计算目标函数点x(k)处一阶导数值
    g=subs(Gradient,[x1 x2],[x(1) x(2)]);
    %计算目标函数点x(k)处Hesse矩阵
    G=subs(Hesse,[x1 x2],[x(1) x(2)]);
    %计算目标函数点x(k)处搜索方向p
    p=-inv(G)*g;
    %p=-g;
    %点x(k)处的搜索步长
    %ak=Alpha(p,g,G);
    %ak=1;
    ak=1;
    xk=x+ak*double(p');
%    采用Armijo法则计算近似步长ak
%         while(F(xk(1),xk(2)) > (F(x(1),x(2))+0.01*double(p'*g)*ak)||Check(x+ak*double(p')))
%             ak=0.5*ak;
%             xk=x+ak*double(p');
%         end
    x=x+double(ak*p');
    %输出结果
    optim_fx=subs(f,[x1 x2],[x(1) x(2)]);
    fprintf('Step[%d]:  x=[ %f %f ] optim_fx=%f\n',step,x(1),x(2),double(optim_fx));
    P(step,:)=x;
    OPT(step,:)=optim_fx;
    g=subs(Gradient,[x1 x2],[x(1) x(2)]);
end
%输出结果
optim_fx=subs(f,[x1 x2],[x(1) x(2)]);
fprintf('\n牛顿Armijo回溯法,,共迭代 %d 步\n结果：\n  x=[ %d %d ] optim_fx=%f\n',step,x(1),x(2),double(optim_fx));
P(step+1:N,:)=[];      %删去P中的多余空间
OPT(step+1:N,:)=[];  


%figure;
plot(P(:,1),P(:,2),'-c>')
%axis equal tight
%figure;
%plot(OPT,'b')
%%
x=[10,20];        %定义初始点

N=100;     %总迭代次数
e=0.000001;
P=zeros(N,2);    %储存点的轨迹
OPT=zeros(N,2);     %储存最优值下降的轨迹
g=subs(Gradient,[x1 x2],[x(1) x(2)]);
step=1;
P(step,:)=x;
optim_fx=subs(f,[x1 x2],[x(1) x(2)]);
fprintf('Step[%d]:  x=[ %f %f ] optim_fx=%f\n',step,x(1),x(2),double(optim_fx));
OPT(step,:)=optim_fx;

while (norm(g)>e  && step < N)       %当g的2-范数小于特定值时，或迭代次数到达上限时，停止迭代
      if(Check(x))
        break;
    end
    step=step+1;
    %计算目标函数点x(k)处一阶导数值
    g=subs(Gradient,[x1 x2],[x(1) x(2)]);
    %计算目标函数点x(k)处Hesse矩阵
    G=subs(Hesse,[x1 x2],[x(1) x(2)]);
    %计算目标函数点x(k)处搜索方向p
    p=-inv(G)*g;
    %p=-g;
    %点x(k)处的搜索步长
    %ak=Alpha(p,g,G);
    %ak=1;
    ak=1;
    xk=x+ak*double(p');
%    采用Armijo法则计算近似步长ak
%         while(F(xk(1),xk(2)) > (F(x(1),x(2))+0.01*double(p'*g)*ak)||Check(x+ak*double(p')))
%             ak=0.5*ak;
%             xk=x+ak*double(p');
%         end
    x=x+double(ak*p');
    %输出结果
    optim_fx=subs(f,[x1 x2],[x(1) x(2)]);
    fprintf('Step[%d]:  x=[ %f %f ] optim_fx=%f\n',step,x(1),x(2),double(optim_fx));
    P(step,:)=x;
    OPT(step,:)=optim_fx;
    g=subs(Gradient,[x1 x2],[x(1) x(2)]);
end
%输出结果
optim_fx=subs(f,[x1 x2],[x(1) x(2)]);
fprintf('\n牛顿Armijo回溯法,,共迭代 %d 步\n结果：\n  x=[ %d %d ] optim_fx=%f\n',step,x(1),x(2),double(optim_fx));
P(step+1:N,:)=[];      %删去P中的多余空间
OPT(step+1:N,:)=[];  


%figure;
plot(P(:,1),P(:,2),'-ws')
%axis equal tight
%figure;
%plot(OPT,'b')
%%

% 计算精确步长ak
function a=Alpha(p,g,G)
a=-(p'*g)/(p'*G*p);
end

%采用Armijo法则计算近似步长ak
function a=Armijo(x,p,g)
a=1;
xk=x+a*double(p);
while(F(xk(1),xk(2)) > F(x(1),x(2))+0.01*doubel(p'*g)*a)
    a=0.9*a;
    xk=xk+a*double(p);
end
end

function bool=Check(x)
%判断点x是否越界
bool=1;
if (x(1)>0&& x(2)>0 && x(1)+x(2)<100&&x(1)-x(2)<50)
    bool=0;
end
end
