clc;
clear;
N=20;
A = hilb(N);
b=ones(N,1);
for i=1:N
    dD(i)=1/(2*i-1);
end
D=diag(dD);
[x0,fl0,rr0,it0,rv0] = pcg(A,b,1e-3,10000);
[x1,fl1,rr1,it1,rv1] = pcg(A,b,1e-3,10000,D);
figure;
semilogy(0:it0,rv0/norm(b),'b.');
hold on;
semilogy(0:it1,rv1/norm(b),'r.');
legend('No Preconditioner','Preconditioner');
xlabel('iteration number');
ylabel('relative residual');
hold off;