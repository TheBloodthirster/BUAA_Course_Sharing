import numpy as np

A = np.array([[2,-1,7,11,-1],
             [3,7,3,4,1],
             [0,0,6,8,0],
             [0,0,0,1,-4],
             [0,0,0,2,3]])

eig,vec = np.linalg.eig(A)
print(eig)
print(vec)

# 幂法求解

def PowerMethod(A,iter):

    n = A.shape[0]
    u0= np.ones((1,n))
    y = u0/np.linalg.norm(u0)

    for i in range(iter):
        uk = A @ y.T
        y = uk.T/np.linalg.norm(uk)
        beta = (y @ A @ y.T) / (y @ y.T)

    print(beta)
    print(y)

    return beta,y

# 反幂法求解

def InversePowerMethod(A,iter):

    n = A.shape[0]
    u0= np.ones((1,n))
    y = u0/np.linalg.norm(u0)
    Ainv = np.linalg.inv(A)
    for i in range(iter):
        uk = Ainv @ y.T
        y = uk.T/np.linalg.norm(uk)
        beta = (y @ A @ y.T) / (y @ y.T)

    print(beta)
    print(y)
    return beta,y

# 反幂法求解，带有平移

def InversePowerMethod_Shift(A,p,iter):

    n = A.shape[0]
    u0= np.ones((1,n))
    y = u0/np.linalg.norm(u0)
    Ainv = np.linalg.inv(A-p*np.eye(n))
    for i in range(iter):
        uk = Ainv @ y.T
        y = uk.T/np.linalg.norm(uk)
        beta = (y @ A @ y.T) / (y @ y.T)

    print(beta)
    print(y)
    return beta,y


PowerMethod(A,100)
InversePowerMethod(A,100)
InversePowerMethod_Shift(A,14,100)