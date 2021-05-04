clc;
clear;
f = @(x,y) x.*y;
g= @(x,y) x.^2+y.^2-1;
fimplicit(g)
axis([-2 2 -2 2 ])
hold on
fcontour(f,'--','LineWidth',1)
axis equal
plot(1/2^0.5,-1/2^0.5,'ro');
plot(-1/2^0.5,1/2^0.5,'ro');
legend('constraint','f contours','minimum');
hold off