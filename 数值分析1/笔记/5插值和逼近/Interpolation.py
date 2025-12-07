import numpy as np
import matplotlib.pyplot as plt

# 问题定义: 假设某个复杂函数 f(x)，给定有限个点，需要找出一条连续函数Pn进行插值

x = np.linspace(1,5,10)
y1 = np.sin(x) + np.log(x)
X = np.linspace(1,5,1000)
y2 = np.sin(X) + np.log(X)

plt.figure(figsize=(10,10))
plt.grid()
plt.plot(X,y2,linewidth = 5, linestyle = '--')
plt.plot(x,y1,'.',markersize = 30)

# 课上推倒过采用范德蒙矩阵方法，Pn=a0+a1x+...anx^n为n阶多项式函数
def Vandermonde_Method(X,Y):

    # 几个点就是几次多项式
    n = len(X)

    # 构建矩阵A
    A = np.ones((n,n))
    for i in range(0,n):
        for j in range(0,n):
            A[i,j]= X[i]**j

    # 构建矩阵B
    B = np.array([Y]).T
    # 求解系数矩阵
    a = np.linalg.solve(A,B)
    # 构建多项式函数
    x = np.linspace(X[0],X[-1],100)
    Pn = 0
    for i in range(0,n):
        Pn = Pn + a[i]*x**i

    return x,Pn

# 拉格朗日插值方法，比较简单的计算比范德蒙矩阵方法少的方法
def Lagrange_Method(X,Y):

    n = len(X)

    x = np.linspace(X[0],X[-1],100)

    # 第k个拉格朗日基函数L_k
    def Lagrange_base(k,x,X):
        n = len(X)
        Lk = 1
        for i in range(0,n):
            if i != k:
                Lk = Lk * (x - X[i])/(X[k]-X[i])
        return Lk
    
    # 求解n个基函数，并将其对齐到对应的Y：
    Li = []
    Pn = 0
    for i in range(0,n):
        L = Y[i]*Lagrange_base(i,x,X)
        Pn += L
        Li.append(L)

    return  x, Pn, Li

# 牛顿插值方法，比拉格朗日方法更优，可以处理额外增加一个值而不需要重新计算的情况
def Newton_Method(X,Y):

    def DiffTable(X,Y):
        # 构建差商表，以获取牛顿法插值的系数，获取这里先初始化
        n = len(X)
        A = np.zeros((n,n))
        A[:,0] = Y
        # 对于n个点，需要计算n-1次差商
        for j in range(1,n): #列
            for i in range(j,n): #行
                A[i,j] = (A[i,j-1]-A[i-1,j-1])/(X[i]-X[i-j]) # 计算差商
        param = np.diag(A)
        return param

    def Newton_Bases(k,x,X):
        # 牛顿基函数
        if k ==0:
            return np.ones_like(x)
        
        wi = 1.0
        for i in range(0,k):
            wi *= (x-X[i])
        
        return wi
    
    x = np.linspace(X[0],X[-1],100)
    param = DiffTable(X,Y)

    Wi = []
    Pn = 0
    for i in range(0,len(X)):
        w = param[i]*Newton_Bases(i,x,X)
        Pn += w
        Wi.append(w)
    return x, Pn, Wi

# # 范德蒙矩阵求解
# X,Pn = Vandermonde_Method(x,y1)
# plt.plot(X,Pn,label = 'InterpolationCurve',linewidth = 2)

# # 拉格朗日插值法
# X,Pn,Li = Lagrange_Method(x,y1)

# plt.plot(X,Pn,label = 'InterpolationCurve',linewidth = 5)
# for i in range(0,len(Li)):
#     plt.plot(X,Li[i],alpha = 0.5, label = ('Lagrange Bases' + str(i)))

# # 牛顿插值法
# X,Pn,Wi = Newton_Method(x,y1)
# plt.plot(X,Pn,label = 'InterpolationCurve',linewidth = 5)
# for i in range(0,len(Wi)):
#     plt.plot(X,Wi[i],alpha = 0.5, label = ('Newton Bases' + str(i)))


plt.legend()
plt.show()