import numpy as np
import matplotlib.pyplot as plt

# 求解 f(x) = x-lnx-2 = 0

def f(x):
    return x-np.log(x)-2

def phi(x):
    return np.log(x)+2
    # return x-(1/2/np.sqrt(3))*(x*x-3)

def PlotF(ax,x):
    y = f(x)
    ax.plot(x,y,label = 'Function')
    return

def PlotX(ax,x):
    y = np.zeros_like(x)
    ax.plot(x,y,label = 'x-axis')
    return

def PlotBox(ax,a,b):
    x = np.linspace(a,b,10)
    ones = np.ones_like(x)
    ax.plot(x,a*ones,color = 'k')
    ax.plot(x,b*ones,color = 'k')
    ax.plot(a*ones,x,color = 'k')
    ax.plot(b*ones,x,color = 'k')

# 简单迭代法
def SimpleIter(x0,phi,f,err):
    
    # 初始化
    x1 = phi(x0)
    xseq = [x0,x1]
    yseq = [f(x0),f(x1)]
    Err = np.abs(x1-x0)/np.abs(x1)
    k = 0
    while(Err>err):
        x0 = xseq[-1]
        x1 = phi(x0)
        xseq.append(x1)
        yseq.append(f(x1))
        k = k+1
        print(k)
        print(x1)
        Err = np.abs(x1-x0)/np.abs(x1)

    print("求解得到的根：")
    print(xseq[-1])

    return xseq,yseq
    # return xseq

# 绘图
plt.figure()
ax = plt.subplot(111)

a = 1
b = 10
x = np.linspace(a,b,100)
PlotX(ax,x)
PlotF(ax,x)

# 求解
xseq,fseq = SimpleIter(x0=1,phi=phi,f=f,err=1e-5)
# xseq = SimpleIter(x0=1,phi=phi,f=f,err=1e-5)

ax.scatter(xseq,fseq,50,label = 'Points',zorder =3)
ax.scatter(xseq[-1],fseq[-1],100,marker='*',color='r',label = 'Solution',zorder =3)

plt.legend()
plt.grid('on')
plt.axis('equal')
plt.show()

# 绘制收敛信息图像

plt.figure()
ax = plt.subplot(1,2,1)
PlotBox(ax,a,b)
ax.plot(x,phi(x),label = r'$\phi(x)$')
ax.legend()
ax.grid('on')
ax.axis('equal')

ax = plt.subplot(1,2,2)
ax.plot(x[0:-1],np.abs(np.diff(phi(x)) / (x[1]-x[0])),label = r"$|\phi(x)'|$")
ax.set_xlim((a,b))
ax.set_ylim((0,1))
ax.legend()
ax.grid('on')

plt.show()


