import numpy as np

A = np.array([[3, 2, -4],
              [1, 3, 3],
              [5, -3, 1]])

b = np.array([3, 15, 14]) # 注意这里的列矩阵的定义方式
print(b.T)

def test_decomposition(A):
    """
    测试是否能够进行LU分解
    """

    n = A.shape[0]
    
    for i in range(n):
        if np.linalg.det(A[0:i+1, 0:i+1]) == 0:
            print("测试：矩阵A的前"+str(i+1)+"阶主子式行列式为0，不能进行LU分解")
            return False
    print("测试：矩阵A的所有主子式行列式均不为0，可以进行LU分解")
    return True

def LU_decomposition_Doolittle(A):
    """
    Doolittle方法进行LU分解
    """

    # 初始化LU矩阵
    n = A.shape[0]
    L = np.identity(n)
    U = np.zeros([n,n])

    # 使用Doolittle分解公式

    for k in range(0,n):
        for j in range (k,n):
            U[k,j] = A[k,j]-sum(L[k,0:k]*U[0:k,j])
        for i in range(k+1,n):
            L[i,k] = (A[i,k]-sum(L[i,0:k]*U[0:k,k]))/U[k,k]
        print("第"+str(k+1)+"步分解结果：")
        print("L=\n",np.round(L,3))
        print("U=\n",np.round(U,3))

    # 测试
    print("测试：LU=\n",np.dot(L,U))
    print("测试：A=\n",A)

    return L, U

def LU_decomposition_Crout(A):
    """
    Crout方法进行LU分解
    """

    # 初始化LU矩阵
    n = A.shape[0]
    U = np.identity(n)
    L = np.zeros([n,n])

    # 使用Crout分解公式

    for k in range(0,n):
        for i in range (k,n):
            L[i,k] = A[i,k]-sum(L[i,0:k]*U[0:k,k])
        for j in range(k+1,n):
            U[k,j] = (A[k,j]-sum(L[k,0:k]*U[0:k,j]))/L[k,k]
        print("第"+str(k+1)+"步分解结果：")
        print("L=\n",np.round(L,3))
        print("U=\n",np.round(U,3))

    # 测试
    print("测试：LU=\n",np.dot(L,U))
    print("测试：A=\n",A)

    return L, U

def Doolittle_Solve(A,b):
    """
    使用Doolittle分解法求解Ax=b
    """
    test_decomposition(A)
    L, U = LU_decomposition_Doolittle(A)

    # 求解Ly=b
    n = A.shape[0]
    y = np.zeros(b.shape)
    x = np.zeros(b.shape)

    y[0]=b[0]
    for i in range(1,n):
        y[i] = b[i]-sum(L[i,0:i]*y[0:i])

    x[n-1] = y[n-1]/U[n-1,n-1]
    for i in range(n-2,-1,-1):
        x[i] = (y[i]-sum(U[i,i+1:n]*x[i+1:n]))/U[i,i]

    print("Doolittle分解法求解结果：\n",x)

    return x

def Crout_Solve(A,b):
    """
    使用Crout分解法求解Ax=b
    """
    test_decomposition(A)
    L, U = LU_decomposition_Crout(A)

    # 求解Ly=b
    n = A.shape[0]
    y = np.zeros(b.shape)
    x = np.zeros(b.shape)

    y[0]=b[0]/L[0,0]
    for i in range(1,n):
        y[i] = (b[i]-sum(L[i,0:i]*y[0:i]))/L[i,i]

    x[n-1] = y[n-1]
    for i in range(n-2,-1,-1):
        x[i] = y[i]-sum(U[i,i+1:n]*x[i+1:n])

    print("Crout分解法求解结果：\n",x)

    return x

# test_decomposition(A)

# LU_decomposition_Doolittle(A)
# LU_decomposition_Crout(A)

Doolittle_Solve(A,b)
Crout_Solve(A,b)

# 验证结果
x = np.linalg.solve(A,b) 
print("Numpy求解结果：\n",x)