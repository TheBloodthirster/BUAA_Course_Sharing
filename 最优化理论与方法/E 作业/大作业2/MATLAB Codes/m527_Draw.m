%绘制题5.27误差函数图形
clc;
clear;

x=[-2:0.01:1/50000];  
y=[-3:0.01:3];
[X,Y]=meshgrid(x,y);  
[row,col]=size(X);  


for l=1:col  
    for h=1:row  
        z(h,l)=log(norm(rk([X(h,l),Y(h,l)])));  
    end  
end  

figure(1);
hold on;
surf(X,Y,z);
contour(X,Y,z,30)
colorbar
shading interp  
hold off;
%print('-f1','-r1200','-dpng','4_1');




function r=rk(y)
    d=[0.9427,0.8616,0.7384,0.5362,0.3739,0.3096];
    t=[2000,5000,10000,20000,30000,50000];
    r=zeros(6,1);
    for i=1:6
        r(i)=ri(t(i),y,d(i));
    end
end

function r=ri(t,y,di)
    r=phi(t,y)-di;
end

function z=phi(t,y)
    z=(1-t*y(1))^(y(2)-1);
end
