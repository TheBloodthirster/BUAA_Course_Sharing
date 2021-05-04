clc;
clear;
f = @(x,y) x.^2+y.^2;
g= @(x,y) (x-1).^3-y.^2;
fimplicit(g)
axis([-2 3 -2 2 ])
hold on
fcontour(f,'--','LineWidth',1)
plot(1,0,'ro');
legend('constraint','f contours','minimum');
hold off