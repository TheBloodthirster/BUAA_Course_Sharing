import numpy as np
import matplotlib.pyplot as plt

# 求解 f(x) = x-lnx-2 = 0

def f(x):
    return x-np.log(x)-2

def PlotF(ax,x):
    y = f(x)
    ax.plot(x,y,label = 'Function')
    return

def PlotX(ax,x):
    y = np.zeros_like(x)
    ax.plot(x,y,label = 'x-axis')
    return

# 割线法
def Secant(x0,x1,f,err):
    
    # 初始化
    x2 = x1 - f(x1)*(x1-x0)/(f(x1)-f(x0))
    xseq = [x0,x1,x2]
    yseq = [f(x0),f(x1),f(x2)]
    
    Err = np.abs(x2 - x1)/np.abs(x2)

    while(Err>err):
        x0 = xseq[-2] #注意，这里仅一行差异
        x1 = xseq[-1]
        if np.abs(f(x1) - f(x0)) < 1e-12:
            print("分母为零，终止迭代")
            break
        x2 = x1 - f(x1)*(x1-x0)/(f(x1)-f(x0))

        xseq.append(x2)
        yseq.append(f(x2))

        Err = np.abs(x2 - x1)/np.abs(x2)

    print("求解得到的根：")
    print(xseq[-1])

    return xseq,yseq

# 单点割线法
def Secant_Fix(x0,x1,f,err):
    
    # 初始化
    x2 = x1 - f(x1)*(x1-x0)/(f(x1)-f(x0))
    xseq = [x0,x1,x2]
    yseq = [f(x0),f(x1),f(x2)]
    
    Err = np.abs(x2 - x1)/np.abs(x2)

    while(Err>err):
        x1 = xseq[-1]
        if np.abs(f(x1) - f(x0)) < 1e-12:
            print("分母为零，终止迭代")
            break
        x2 = x1 - f(x1)*(x1-x0)/(f(x1)-f(x0))

        xseq.append(x2)
        yseq.append(f(x2))

        Err = np.abs(x2 - x1)/np.abs(x2)

    print("求解得到的根：")
    print(xseq[-1])

    return xseq,yseq

# 绘图
plt.figure()
ax = plt.subplot(111)

a = 2
b = 5
x = np.linspace(a,b,100)
PlotX(ax,x)
PlotF(ax,x)

# 求解
xseq,fseq = Secant_Fix(x0=2,x1=5,f=f,err=1e-5)


ax.scatter(xseq,fseq,50,label = 'Points',zorder =3)
ax.scatter(xseq[-1],fseq[-1],100,marker='*',color='r',label = 'Solution',zorder =3)

plt.legend()
plt.grid('on')
plt.show()


