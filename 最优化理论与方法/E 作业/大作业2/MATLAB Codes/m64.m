%Steihaug共轭梯度法 for Problem 6.8
clc;
clear;
ns=0.25;
nv=0.75;
ri=2;
rd=0.5;
n=10;
delta=1;
c1=0;
c2=0;
c3=0;
xx=5*ones(2*n,1);
X = sym('x', [2*n,1]) ;  %符号表达式定义x1,x2,...x2n
f=0; 

for i=1:n
    f=f+(1-X(2*i-1))^2+10*(X(2*i)-X(2*i-1)^2)^2;    %符号表达式定义f(x)
end

grad=gradient(f,X);  %计算梯度向量的表达式
Hess=hessian(f,X);    %计算hessian阵的表达式

g=double(subs(grad,X,xx));
global  step
step=0;
global op;
op=0;
fprintf('Iteration:0\nf(x)=%f      radius:%f      g(x)=%f\n\n',double(subs(f,X,xx)),delta,norm(g))
A(1,:)=[0,double(subs(f,X,xx)),delta,0,norm(g),0,0];
while (norm(g)>10e-6)
    step=step+1;
    fun=double(subs(f,X,xx));
    g=double(subs(grad,X,xx));
    B=double(subs(Hess,X,xx));
    s=Steihaug(g,B,n,delta);
    p=-1*(double(subs(f,X,xx))-double(subs(f,X,(xx+s))))/(s'*g+0.5*s'*B*s );
    if(norm(s)<10e-14)
         p=1;
    end
    fprintf('Iteration:%d	   ',step)
    if(p>=nv)
        delta=delta*ri;
        fprintf('Very successful\n')
        c1=c1+1;
    elseif(p>ns)
        delta=delta;
        fprintf('Successful\n')
        c2=c2+1;
    else
        delta=delta*rd;
        fprintf('Unsuccessful\n')
        c3=c3+1;
    end
    if(p<=0)
        xx=xx;
    else
        xx=xx+s;
    end
    fprintf('f(x)= %f     radius: %f     p= %f\ng(x)=%f        stepsize= %f     CG-iterations:  %d \n\n',fun,delta,norm(p),norm(s),p,op)
    A(step+1,:)=[step,fun,delta,norm(s),norm(g),p,op];
end

fprintf('\n最优值为%f\n求解子问题%d次\n',fun,step)
fprintf('\n[Very successful]:%d\n[Successful]:%d\n[Unsuccessful]:%d\n\n',c1,c2,c3)

fprintf('  Iteration     f(x)   radius    stepsize        g	      p	    CG-iterations \n')
disp(A)
%%
%Steihaug共轭梯度法
function s=Steihaug(g,B,n,delta)
    global op
    op=0;
    eps=10e-6;
    x=zeros(2*n,1);
    r=g;
    r0=r;
    p=-r;
    s=x;
    if(norm(r)<=eps)
            fprintf('满足条件\n')
            return 
    end
    while (1)
        op=op+1;
    	if(p'*B*p<=0)
            t=find(x,p,delta);
            s=x+double(t)*p;
            fprintf('曲率非正\n')
            return 
        end
        d=B*p;
        a=(r'*r)/(p'*d);
        if(norm(x+a*p)>=delta)
            t=find(x,p,delta);
            s=x+double(t)*p;
            fprintf('抵达信赖域边界\n')
            return 
        end
        x=x+a*p;
        r1=r+a*d;
        if(norm(r1)<eps*norm(r0))
             s=x;
             fprintf('满足条件\n')
             return
        end
        b=(r1'*r1)/(r'*r);
        r=r1;
        p=-r+b*p;
    end
end


function t=find(x,p,delta)
    syms a;
    eqn = (x'+a*p')*(x+a*p)== delta*delta;
    t=vpasolve (eqn,a,[0,delta/norm(p)*2+1]);
end


