import numpy as np
import matplotlib.pyplot as plt

plt.rcParams["font.family"] = ["Microsoft YaHei"]
plt.rcParams['axes.unicode_minus'] = False

# 求解一个模型问题 y' = f = Lt，这里简化了，没有额外的状态，只依赖时间
L = -2

def f(t):    
    return L*t

# 精确解
# y = L/2 t^2 + y0
def acc_y(y0,t):
    return y0 + L*t*t/2

# 欧拉方法
# yn+1 = yn+hf(x)
def Euler(f,h,Time,y0):
    y = [y0]
    for t in Time:
        y.append(y[-1]+h*f(t))
    return y[0:-1]

# RK4方法
def RK4(f,h,Time,y0):
    y = [y0]
    for t in Time:
        k1 = f(t)
        k2 = f(t+0.5*h)
        k3 = f(t+0.5*h)
        k4 = f(t+h)
        y.append(y[-1]+h/6*(k1+2*k2+2*k3+k4))
    return y[0:-1]

# 定义运算区间
T = 2 #总时长
n = 10 #总区间
Time = np.linspace(0,T,n+1)
h = T/n #步长
y0 = 0 #初始条件

#精确解
y_acc = acc_y(y0,Time)
#欧拉方法
y_euler = Euler(f,h,Time,y0)
#RK4方法
y_RK4 = RK4(f,h,Time,y0)

plt.figure()
plt.grid('on')
plt.plot(Time,y_acc,label = '精确解',linewidth=5,linestyle ='--')
plt.plot(Time,y_RK4,label = 'RK4方法')
plt.plot(Time,y_euler,label = '欧拉方法')
plt.xlabel('Time')
plt.ylabel('y')
plt.legend()
plt.show()


