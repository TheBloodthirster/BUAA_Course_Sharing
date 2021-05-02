%   5.23:   精确步长的DFP法
clc;
clear;
N=200;
step=0;
x=[0.1,1]';
H=eye(2);
e=0.000001;
g=gg(x);
G=[20,0;0,2];
%%
while (norm(g)>e  && step < N) 
	step=step+1;
	p=-H*g;
	s=Alpha(p,g,G)*p;
	y=gg(x+s)-g;
	x=x+s;
	g=gg(x);
	H=H_update(H,s,y);
end
step
x
f(x)
H
%%
function y=f(x)
y=10*x(1)^2+x(2)^2;
end

function y=gg(x)
y=[20*x(1),2*x(2)]';
end

function h=H_update(H,s,y)
h=H+(s*s')/(s'*y)-(H*y*y'*H)/(y'*H*y);
end 

function a=Alpha(p,g,G)
a=-(p'*g)/(p'*G*p);
a=double(a);
end