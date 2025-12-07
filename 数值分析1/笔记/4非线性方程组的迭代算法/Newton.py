import numpy as np
import matplotlib.pyplot as plt

# 求解 f(x) = (x-5)^4 = 0

def f(x):
    # return (x-5)**4
    return np.tan(x)-x

def fdot(x):
    # return 4*(x-5)**3
    return 1/(np.cos(x)**2)-1

def fddot(x):
    return 12*(x-5)**2

def PlotF(ax,x):
    y = f(x)
    ax.plot(x,y,label = 'Function')
    return

def PlotX(ax,x):
    y = np.zeros_like(x)
    ax.plot(x,y,label = 'x-axis')
    return

# 牛顿法（切线法）
def Newton(x0,f,fdot,err):
    
    # 初始化
    x1 = x0 - f(x0)/fdot(x0)
    xseq = [x0,x1]
    yseq = [f(x0),f(x1)]
    
    # 计算误差（处理x1接近零的情况）
    if np.abs(x1) < 1e-12:
        Err = np.abs(x1 - x0)  # 用绝对误差
    else:
        Err = np.abs(x1 - x0)/np.abs(x1)  # 用相对误差

    while(Err>err):
        x0 = xseq[-1]

        # 迭代中检查除数（导数）
        if np.abs(fdot(x0)) < 1e-12:
            print("迭代中导数为零，终止计算")
            break
        
        x1 = x0 - f(x0)/fdot(x0)
        print(x1)
        xseq.append(x1)
        yseq.append(f(x1))

        if np.abs(x1) < 1e-12:
            Err = np.abs(x1 - x0)
        else:
            Err = np.abs(x1 - x0)/np.abs(x1)

    print("求解得到的根：")
    print(xseq[-1])

    return xseq,yseq

# 求重根牛顿法
def Newton_M(x0,f,fdot,fddot,err):
    
    # 初始化
    x1 = x0 - f(x0)*fdot(x0)/ (fdot(x0)**2-f(x0)*fddot(x0))
    xseq = [x0,x1]
    yseq = [f(x0),f(x1)]
    Err = np.abs(x1-x0)/np.abs(x1)

    # 计算误差（处理x1接近零的情况）
    if np.abs(x1) < 1e-12:
        Err = np.abs(x1 - x0)  # 用绝对误差
    else:
        Err = np.abs(x1 - x0)/np.abs(x1)  # 用相对误差

    while(Err>err):
        x0 = xseq[-1]
        
        # 迭代中检查除数（导数）
        if np.abs(fdot(x0)) < 1e-12:
            print("迭代中导数为零，终止计算")
            break

        x1 = x0 - f(x0)*fdot(x0)/ (fdot(x0)**2-f(x0)*fddot(x0))

        xseq.append(x1)
        yseq.append(f(x1))
        
        if np.abs(x1) < 1e-12:
            Err = np.abs(x1 - x0)
        else:
            Err = np.abs(x1 - x0)/np.abs(x1)

    print("求解得到的根：")
    print(xseq[-1])

    return xseq,yseq

# 绘图
plt.figure()
ax = plt.subplot(111)

a = 4
b = 5
x = np.linspace(a,b,1000)
PlotX(ax,x)
PlotF(ax,x)

# 求解
# xseq,fseq = Newton_M(x0=12,f=f,fdot=fdot,fddot=fddot,err=1e-5)
xseq,fseq = Newton(x0=4.5,f=f,fdot=fdot,err=1e-8)


ax.scatter(xseq,fseq,50,label = 'Points',zorder =3)
ax.scatter(xseq[-1],fseq[-1],100,marker='*',color='r',label = 'Solution',zorder =3)

plt.legend()
plt.grid('on')
plt.show()


