#include "stdafx.h"
#include<iostream>
#include<vector>
using namespace std;

const int N = 8; //八边形

//权值函数
vector<vector<int>> weight = {
	{ 0,14,25,27,10,11,24,16 },
	{ 14,0,18,15,27,28,16,14 },
	{ 25,18,0,19,14,19,16,10 },
	{ 27,15,19,0,22,23,15,14 },
	{ 10,27,14,22,0,14,13,20 },
	{ 11,28,19,23,14,0,15,18 },
	{ 24,16,16,15,13,15,0,27 },
	{ 16,14,10,14,20,18,27,0 }};

//初始化存储数组
vector<int> tempweight(N, 0);
vector<int> temppoint(N, -1);
// bestweight[i][j] 记录凸子多边形 {Vi, ..., Vj} 三角剖分的最优权值。
vector<vector<int>> bestweight(N, tempweight);
// bestpoint[i][j] 记录与 Vi、Vj 构成三角形第三个顶点 Vk 。
vector<vector<int>> bestpoint(N, temppoint);


//计算Vi,Vk,Vj组成的三角形的权重之和
int GetWeight(int i, int k, int j);

//自底向上动态规划计算n变形最优三角形的权值之和
int MinWeightTriangulation(int n);

//打印凸子多边形 {Vi, ..., Vj} 的最优三角剖分结果
void Traceback(int i, int j);

int main() {
	cout << "凸多边形权重矩阵为："  << endl;
	for (int i = 0; i < N; i++) {
		for (int j = 0; j < N; j++) {
			cout << weight[i][j] << " ";
		}
		cout << endl;
	}
	cout << endl;
	cout <<"动态规划算法计算结果：" << MinWeightTriangulation(N) << endl;
	cout << endl;
	cout << "最优三角剖分结构为：" << endl;
	Traceback(0, N - 1);
	cout << endl;

	cout << "bestPoint[i][j] 记录与 Vi、Vj 构成三角形第三个顶点 Vk 为："  << endl;
	for (int i = 0; i < N; i++) {
		for (int j = 0; j < N; j++) {
			cout << bestpoint[i][j] << "\t";
		}
		cout << endl;
	}

	system("pause");
	return 0;
}


int GetWeight(int i, int k, int j)
{
	return weight[i][k] + weight[k][j] + weight[i][j];
}

int MinWeightTriangulation(int n)
{
	//对动态规划数组初始化,这里初始化其实可以不做，前面已经初始化过了
	bestweight[n - 1][n - 1] = 0;//下面初始化会漏掉[n-1][n-1]点
	for (int i = 0; i < n - 1; i++) {
		bestweight[i][i] = bestweight[i][i + 1] = 0;
	}

	//scale代表子问题的规模大小，例如子问题{V0,V1,V2}的规模为2,子问题{V0,V1...V5}的规模为5
	for (int scale = 2; scale < n; scale++) {
		//求解子问题的最后一个为n-scale-1，例如scale=2，最后一个子问题为i=6,j+8,{V6,V7,V8}
		for (int i = 0; i < n - scale; i++) {
			// j 代表当前以 Vi 为起点的子问题的后边界 Vj
			int j = i + scale;

			//先处理 k = i+1的情况，这是为了有一开始的初值方便对比，这里也可以选择初始化最大值9999
			bestweight[i][j] = bestweight[i][i + 1] + bestweight[i + 1][j] + GetWeight(i, i + 1, j);
			bestpoint[i][j] = i + 1;

			//有了基准值之后，可以开始循环处理k=i+2的情况
			for (int k = i + 2; k < j; k++) {
				int temp = bestweight[i][k] + bestweight[k][j] + GetWeight(i, k, j);
				if (temp < bestweight[i][j]) {
					bestweight[i][j] = temp;
					bestpoint[i][j] = k;
				}
			}
		}
	}

	//返回右上角的最佳数值。
	return bestweight[0][n - 1];
}

void Traceback(int i, int j)
{
	//注意回溯查找的返回条件,i+1=j表示中间没有任何点存在，bestpoint[i][j]内部的值为出始化-1
	if (i+1 == j)
		return;
	Traceback(i,bestpoint[i][j]);
	cout << "V" << i << " -- V" << bestpoint[i][j] << " -- V" << j << " = " << GetWeight(i,bestpoint[i][j],j) << endl;
	Traceback(bestpoint[i][j],j);
}