import numpy as np

def simple_iter(A,b,N,x0,epsi = 1e-8):
    """
    简单迭代法
    """

    # 测试保证det(N)! = 0
    if np.linalg.det(N) == 0:
        print("矩阵N不可逆，无法进行简单迭代！")
        return None
    
    # 分解矩阵
    P = N - A
    G = np.linalg.inv(N)@P
    d = np.linalg.inv(N)@b

    print(G)
    print(d)

    # 测试迭代矩阵G是否收敛
    eig = np.linalg.eigvals(G)
    print("|lambda_i| = "+ str(abs(eig)) )
    rho = max(abs(eig))
    if rho >=1:
        print("迭代矩阵G谱半径大于一，无法收敛！")
        return None

    # 迭代求解
    xi = x0.copy()
    err = 999
    while err>=epsi:
        x_next = G @ xi + d
        err = max(abs(x_next-xi))
        xi = x_next
        # print(xi)
    
    print("求解得到了线性方程的解:")
    print(xi)

    return xi

def Jacobi_iter(A,b,x0,epsi = 1e-8):
    """
    雅可比迭代法
    """

    # 测试A是否为严格对角占优矩阵
    n = A.shape[0]
    for i in range(n):
        if abs(A[i,i]) <= sum(abs(A[i,:])) - abs(A[i,i]):
            print("矩阵A不是严格对角占优矩阵，可能无法收敛！")
            return None
        
    print("矩阵A是严格对角占优矩阵，可以保证收敛！")

    # 分解矩阵
    D = np.diag(np.diag(A))
    L = np.tril(A,-1)
    U = np.triu(A,1)

    D_inv = np.diag(1/D)
    G = -D_inv @ (L + U)
    d = D_inv @ b

    # 测试迭代矩阵G是否收敛
    eig = np.linalg.eigvals(G)
    print("|lambda_i| = "+ str(abs(eig)) )
    rho = max(abs(eig))
    if rho >=1:
        print("迭代矩阵G谱半径大于一，无法收敛！")
        return None
    
    # 迭代求解
    xi = x0.copy()
    err = 999
    while err>=epsi:
        x_next = G @ xi + d
        err = max(abs(x_next-xi))
        xi = x_next
        # print(xi)
    
    print("求解得到了线性方程的解:")
    print(xi)

    return xi

def GS_iter(A,b,x0,epsi = 1e-8):
    """
    Gauss-Seidel迭代法
    """
    # 测试A是否为正定矩阵
    if np.all(np.linalg.eigvals(A) > 0):
        print("矩阵A是正定矩阵，可以保证收敛！")
    
    D = np.diag(np.diag(A))
    L = np.tril(A,-1)
    U = np.triu(A,1)

    # 计算迭代矩阵
    DL = D + L
    DL_inv = np.linalg.inv(DL)
    G = -DL_inv @ U
    d = DL_inv @ b

    # 测试迭代矩阵G是否收敛
    eig = np.linalg.eigvals(G)
    print("|lambda_i| = "+ str(abs(eig)) )
    rho = max(abs(eig))
    if rho >=1:
        print("迭代矩阵G谱半径大于一，无法收敛！")
        return None
    
    # 迭代求解
    xi = x0.copy()
    err = 999
    count = 0
    while err>=epsi:
        x_next = G @ xi + d
        err = max(abs(x_next-xi))
        xi = x_next.copy()
        # print(xi)
        count += 1

    print(f"经过{count}次迭代")
    print("求解得到了线性方程的解:")
    print(xi)

    return xi

def SOR_iter(A,b,x0,omega = 1.5, epsi = 1e-8):
    """
    SOR迭代法
    """
    # 测试A是否为正定矩阵
    if np.all(np.linalg.eigvals(A) > 0):
        print("矩阵A是正定矩阵，可以保证收敛！")
    
    D = np.diag(np.diag(A))
    L = np.tril(A,-1)
    U = np.triu(A,1)

    # 计算迭代矩阵
    N = D/omega + L
    P = -((1-1/omega)*D + U)
    G = np.linalg.inv(N) @ P
    d = np.linalg.inv(N) @ b

    # 测试迭代矩阵G是否收敛
    eig = np.linalg.eigvals(G)
    print("|lambda_i| = "+ str(abs(eig)) )
    rho = max(abs(eig))
    if rho >=1:
        print("迭代矩阵G谱半径大于一，无法收敛！")
        return None
    
    # 迭代求解
    xi = x0.copy()
    err = 999
    count = 0
    while err>=epsi:
        x_next = G @ xi + d
        err = max(abs(x_next-xi))
        xi = x_next.copy()
        # print(xi)
        count += 1
    
    print(f"经过{count}次迭代")
    
    print("求解得到了线性方程的解:")
    print(xi)

    return xi

# 定义一组问题
A = np.array([[2, 5, 4],
              [1, 5, 3],
              [5, 3, 11]])
b = np.array([3, 15, 14]) # 注意这里的列矩阵的定义方式

# # 简单迭代法测试
# N = 100*np.identity(3)
# x0 = np.array([0,0,0])
# simple_iter(A,b,N,x0)

# # 雅可比迭代法测试
# x0 = np.array([0,0,0])
# Jacobi_iter(A,b,x0)


# Gauss-Seidel迭代法测试
x0 = np.array([1,2,3])
GS_iter(A,b,x0)

# SOR迭代法测试
x0 = np.array([1,2,3])
SOR_iter(A,b,x0,omega=1.25)

# 与numpy的对比
x = np.linalg.solve(A,b)
print(x)