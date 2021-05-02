f = @(x) 0.5*(0.5*x.^2-14).^2-x.^2+3*x;
g= @(x) 0.5*x.^3-16*x+3;
X=linspace(-8,8,10000);
XX=linspace(-6,6,100000);
Y1=f(X);
Y2=zeros(1,10000);
Y4=zeros(1,100000);
Y3=g(XX);
figure
subplot(2,1,1);
plot(X,Y1)
hold on
plot(X,Y2,'black')
legend('f(x)')

subplot(2,1,2);
plot(XX,Y3)
hold on
plot(XX,Y4,'black')
legend("f'(x)")
