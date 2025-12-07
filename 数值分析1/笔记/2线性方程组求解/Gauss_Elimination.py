import numpy as np

A = np.array([[0.001,2,3], 
              [-1,3.716,4.810], 
              [-2,1.116,5.712]])
b = np.array([1, 2, 3])

x = np.linalg.solve(A, b)

print("Python直接解法的结果为：", x)

## ---------------------------------------------------------

def gauss_elimination(A, b):
    '''
    顺次高斯消元法
    '''
    # 1. 建立增广矩阵
    C = np.column_stack((A,b))
    print("原始增广矩阵:")
    print(C)

    # 2. 迭代的方式顺序消元，形成上三角
    n = len(b)
    for i in range(0,n):
        # 提取主元素
        major_element = C[i,i]
        
        # 对当前行的主元素进行归一化
        for j in range (0,n+1):
            C[i,j] /= major_element

        # 对剩余行进行消元
        for k in range (i+1,n):
            row_element = C[k,i]
            for j in range(0,n+1):
                C[k,j] -= row_element*C[i,j]
        
        # 打印当前情况:
        print("第"+str(i+1)+"次消元后矩阵情况：")
        print(C)

    # 3. 从后往前顺次迭代解(反向消元)，将系数矩阵变为单位矩阵
    for k in range(n-1, 0, -1):  # 从最后一行向上处理
        print(f"\n第{k}行反向消元")
        
        # 处理当前行上方的所有行
        for i in range(k-1, -1, -1):
            factor = C[i, k]  # 要消除的元素
            # 整行相减，消除当前列上方的元素
            for j in range(k, n+1):  # 从当前列开始到最后一列
                C[i, j] -= factor * C[k, j]
            print("当前矩阵状态：")
            print(C)
        
    # 提取最后一列作为解
    x = C[:, -1]
    print("求解得到的解："+str(x))

    return x

def gauss_elimination_column(A, b):
    '''
    列主元素高斯消元法
    '''
    # 1. 建立增广矩阵
    C = np.column_stack((A,b))
    print("原始增广矩阵:")
    print(C)

    # 2. 迭代的方式顺序消元，形成上三角
    n = len(b)
    for i in range(0,n):
        # 寻找最大主元素
        max_row = np.argmax(np.abs(C[i:,i])) + i

        # 换行
        if max_row!=i:
            # 这种方式交换
            C[[i, max_row]] = C[[max_row, i]]
            print(f"\n第{i+1}步交换行 {i+1} 和 {max_row+1} 后：")
            print(C)

        # 提取主元素
        major_element = C[i,i]
        
        # 对当前行的主元素进行归一化
        for j in range (0,n+1):
            C[i,j] /= major_element

        # 对剩余行进行消元
        for k in range (i+1,n):
            row_element = C[k,i]
            for j in range(0,n+1):
                C[k,j] -= row_element*C[i,j]
        
        # 打印当前情况:
        print("第"+str(i+1)+"次消元后矩阵情况：")
        print(C)

    # 3. 从后往前顺次迭代解(反向消元)，将系数矩阵变为单位矩阵
    for k in range(n-1, 0, -1):  # 从最后一行向上处理
        print(f"\n第{k}行反向消元")
        
        # 处理当前行上方的所有行
        for i in range(k-1, -1, -1):
            factor = C[i, k]  # 要消除的元素
            # 整行相减，消除当前列上方的元素
            for j in range(k, n+1):  # 从当前列开始到最后一列
                C[i, j] -= factor * C[k, j]
            print("当前矩阵状态：")
            print(C)
        
    # 提取最后一列作为解
    x = C[:, -1]
    print("求解得到的解："+str(x))

    return x

# gauss_elimination(A,b)

gauss_elimination_column(A,b)