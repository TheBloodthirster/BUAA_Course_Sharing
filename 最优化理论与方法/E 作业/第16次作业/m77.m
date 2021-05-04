clc;
clear;
f = @(x,y) x.^2+y.^2-1;
g= @(x,y) (x-1).^3-y;
gg= @(x,y) y-0;
hold on
fimplicit(f)
fimplicit(g)
fimplicit(gg,'black')
axis([-2 3 -2 2 ])

plot(1,0,'ro');
legend('c1','c2','x-axis');
hold off