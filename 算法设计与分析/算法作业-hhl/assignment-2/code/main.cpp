/*
 * encoding: utf-8
 * */

#include <iostream>
#include <limits.h>

// 6 cities
const int n = 6;
const int m = 1 << (n - 1);
// 6x6 cost matrix
const int D[n][n] = {
        {0,  10, 20, 30, 40, 50},
        {12, 0,  18, 30, 25, 21},
        {23, 19, 0,  5,  10, 15},
        {34, 32, 4,  0,  8,  6},
        {45, 27, 11, 10, 0,  18},
        {56, 22, 16, 20, 12, 0}
};
// 表示从i出发经过j到城市1的距离
int dp[n][m];


void TSP() {
    // init 所有城市到城市1的距离
    for (int i = 0; i < n; i++) {
        dp[i][0] = D[i][0];
    }

    // dp
    for (int j = 1; j < m; j++) {
        for (int i = 0; i < n; i++) {
            dp[i][j] = INT_MAX;
            // if i is not in j 判断i是否在j中
            // j 是用二进制表示的，j的第i位为1表示i在j中
            if ((j >> (i - 1)) & 1) {
                continue;
            }
            // 遍历j中的每个城市k，找到最小的dp[i][j]
            for (int k = 1; k < n; k++) {
                if ((j >> (k - 1)) & 1) {
                    // j - {k} 表示j中除了k之外的城市
                    // 由于j中包含k，所以j - {k}中的城市数比j中的城市数少1
                    // 所以dp[k][j - {k}]已经在上一次循环中计算过了
                    dp[i][j] = std::min(dp[i][j], dp[k][j - (1 << (k - 1))] + D[i][k]);
                }
            }
        }
    }
}

void getPath() {
    // j = m - 1 表示所有城市都已经遍历过了
    // i = 0 表示从城市1开始
    int j = m - 1;
    int i = 0;
    while (j > 0) {
        // 从城市1开始，依次输出城市的编号
        std::cout << i + 1 << " -> ";
        for (int k = 1; k < n; k++) {
            if ((j >> (k - 1)) & 1) {
                // 如果dp[i][j] == dp[k][j - {k}] + D[i][k]
                // 说明从i出发经过j到城市1的距离等于从k出发经过j - {k}到城市1的距离加上i到k的距离
                // 所以i到k是最短路径的一部分
                // 所以下一次循环应该从k开始
                if (dp[i][j] == dp[k][j - (1 << (k - 1))] + D[i][k]) {
                    // j -= (1 << (k - 1)) 表示j中去掉k
                    j -= (1 << (k - 1));
                    i = k;
                    break;
                }
            }
        }
    }
    std::cout << i + 1 << " -> 1" << std::endl;
}

int main() {
    TSP();
    std::cout << "最短路径：";
    getPath();
    std::cout << "最短距离：";
    std::cout << dp[0][m - 1] << std::endl;
    return 0;
}
