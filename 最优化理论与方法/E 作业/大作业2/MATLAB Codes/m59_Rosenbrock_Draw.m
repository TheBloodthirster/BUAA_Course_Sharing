%绘制Rosenbrock函数图形
clc;
clear;

x=[-1.5:0.01:1.5];  
y=[-0.5:0.01:1.5];  
[X,Y]=meshgrid(x,y);  
[row,col]=size(X);  
for l=1:col  
    for h=1:row  
        z(h,l)=Rosenbrock([X(h,l),Y(h,l)]);  
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
%print('-f1','-r1200','-dpng','4_2');

figure(2);
contour3(X,Y,z,30)
colorbar
shading interp  
%print('-f3','-r1200','-dpdf','4_3');

figure(3);
contour(X,Y,z,30)
colorbar
shading interp  
%print('-f3','-r1200','-dpdf','4_3');

function result=Rosenbrock(x)  
%Rosenbrock 函数    
[row,col]=size(x);  
if row>1  
    error('输入的参数错误');  
end  
result=100*(x(1,2)-x(1,1)^2)^2+(x(1,1)-1)^2;  
%result=L(result);  
result=L(L(result)); 
end

function y=L(x)
y=log(x+1);
end