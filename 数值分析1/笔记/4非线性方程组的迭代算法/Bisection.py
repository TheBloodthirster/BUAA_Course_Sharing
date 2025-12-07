import numpy as np
import matplotlib.pyplot as plt

# 求解 f(x)

def f(x):
    return x*x-x-1

def PlotF(ax,x):
    y = f(x)
    ax.plot(x,y,label = 'Function')
    return

def PlotX(ax,x):
    y = np.zeros_like(x)
    ax.plot(x,y,label = 'x-axis')
    return

# 二分法
def BisectionMethod(a,b,f,err):

    # 检测是否符合变号的条件
    if (f(a)*f(b)>=0):
        print("函数在a,b端未变号，无法使用二分法求解")
        return

    # 初始化第一个点
    mid = (a+b)/2
    fmid = f(mid)
    fa = f(a)
    xseq = [mid]
    fseq = [fmid]
    while(np.abs(fmid)>err):
        # 判断哪里发生了变号
        if (fa*fmid<0):
            b = mid
        else:
            a = mid
        # 迭代
        mid = (a+b)/2
        fmid = f(mid)
        print(mid)
        xseq.append(mid)
        fseq.append(fmid)
    
    print("求解得到的根：")
    print(mid)

    return xseq,fseq

# 绘图
plt.figure()
ax = plt.subplot(111)

x = np.linspace(1,10,100)
PlotX(ax,x)
PlotF(ax,x)

# 求解
xseq,fseq = BisectionMethod(0,10,f,err=1e-8)

ax.scatter(xseq,fseq,50,label = 'Points',zorder =3)
ax.scatter(xseq[-1],fseq[-1],100,marker='*',color='r',label = 'Solution',zorder =3)

plt.legend()
plt.grid('on')
plt.axis('equal')
plt.show()

