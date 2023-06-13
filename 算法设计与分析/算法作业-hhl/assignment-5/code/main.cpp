#include <iostream>
#include <random>
#include <cstring>

// ZY2206117 黄海浪
const double initTemperature = 6117;
// 是否打印过程日志
bool isLog = true;
// 6 cities
const int n = 6;
// 6x6 cost matrix
const int D[n][n] = {
        {0,  10, 20, 30, 40, 50},
        {12, 0,  18, 30, 25, 21},
        {23, 19, 0,  5,  10, 15},
        {34, 32, 4,  0,  8,  16},
        {45, 27, 11, 10, 0,  18},
        {56, 22, 16, 20, 12, 0}
};
// 解的编码（顺序编码） 下面为初始解
int ans[n] = {0, 3, 5, 1, 2, 4};

// 领域动作产生的解
int gAns[n];

// 计算路径长度
int getLength(const int *path) {
    int length = 0;
    for (int i = 0; i < n - 1; ++i) {
        length += D[path[i]][path[i + 1]];
    }
    length += D[path[n - 1]][path[0]];
    return length;
}

// 领域动作，换任意两个城市(V1 不参与交换)
void getNeighbor(const int *path) {
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<> dis(1, n - 1);
    int i = dis(gen);
    int j = dis(gen);
    while (i == j) {
        j = dis(gen);
    }
    memcpy(gAns, path, sizeof(int) * n);
    std::swap(gAns[i], gAns[j]);
}

void logData(int i, int j, double t, const std::string &info) {
    std::cout << "第" << i << "次迭代，第" << j << "次动作，温度：" << t << "，" << info << std::endl;
    std::cout << "当前解长度：" << getLength(ans) << std::endl;
    std::cout << "当前解：";
    for (int an: ans) {
        std::cout << an + 1 << " ";
    }
    std::cout << std::endl;
    std::cout << "产生解长度：" << getLength(gAns) << std::endl;
    std::cout << "产生解：";
    for (int an: gAns) {
        std::cout << an + 1 << " ";
    }
    std::cout << std::endl << std::endl;
}

int main() {
    double t = initTemperature;

    for (int i = 0; i < 4; ++i) {
        for (int j = 0; j < 4; ++j) {
            getNeighbor(ans);
            int ansLength = getLength(ans);
            int gAnsLength = getLength(gAns);
            if (ansLength > gAnsLength) {
                if (isLog) {
                    logData(i + 1, j + 1, t, "优于当前解，直接接受");
                }
                // 优于当前解，直接接受
                memcpy(ans, gAns, sizeof(int) * n);
            } else {
                // 以一定概率接受
                std::random_device rd;
                std::mt19937 gen(rd());
                std::uniform_real_distribution<> dis(0.5, 1);
                // 由于用学号后4位作为温度，直接用目标函数值作为概率不行，因此放大100倍
                double p = exp((ansLength - gAnsLength) * 100 / t);
                // 越到后面，越容易被接受
                double sigma = dis(gen) * (1 - 0.10 * j);
                std::string logParam = "p：" + std::to_string(p) + "，sigma：" + std::to_string(sigma);
                if (p > sigma) {
                    if (isLog) {
                        logData(i + 1, j + 1, t, logParam + "，不优于当前解，以一定概率接受");
                    }
                    memcpy(ans, gAns, sizeof(int) * n);
                } else {
                    if (isLog) {
                        logData(i + 1, j + 1, t, logParam + "，不优于当前解，以一定概率拒绝");
                    }
                }

            }
        }
        // 降温
        t *= 0.6;
    }
    std::cout << std::endl << std::endl;
    std::cout << "最短路径长度：" << getLength(ans) << std::endl;
    std::cout << "最短路径：";
    for (int an: ans) {
        std::cout << an + 1 << " ";
    }
    std::cout << std::endl;
    return 0;
}
