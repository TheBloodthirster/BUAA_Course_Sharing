/*
 * encoding: utf-8
 * */
#include <iostream>
#include <fstream>
#include <utility>
#include <vector>
#include <queue>
#include <cstring>

// 城市的数量、最大的花费、最大的距离
const int cityNum = 50, maxCost = 1500, maxLen = 9999;

// 定义边集，在其中搜索；其中reverseEdge是反向边集，用于dijkstra算法
struct Edge {
    int start;
    int end;
    int cost;
    int len;
} orderEdge[cityNum][cityNum], reverseEdge[cityNum][cityNum];

// 从点i有多少条边
int orderEdgeNum[cityNum], reverseEdgeNum[cityNum];

// 初始化，得到点i到终点的最短距离和最小花费
int minCost[cityNum], minLen[cityNum];

// 是否已经搜索过这个点
int visitPoint[cityNum];

// 记录当前花费、距离和路径
int curCost, curLen, curPath[cityNum + 1];

// 记录最优花费、距离和路径
int bestCost, bestLen, bestPath[cityNum + 1];

// 读取数据
void readData() {
    // 请注意，这里的路径是相对于可执行文件的路径
    std::ifstream fin1("./m1.txt");
    std::ifstream fin2("./m2.txt");
    int tmpLen, tmpCost;
    for (int i = 0; i < cityNum; i++) {
        for (int j = 0; j < cityNum; j++) {
            fin1 >> tmpLen;
            if (tmpLen < maxLen) {
                orderEdge[i][orderEdgeNum[i]].start = i;
                orderEdge[i][orderEdgeNum[i]].end = j;
                orderEdge[i][orderEdgeNum[i]].len = tmpLen;
                fin2 >> orderEdge[i][orderEdgeNum[i]].cost;
                reverseEdge[j][reverseEdgeNum[j]].start = j;
                reverseEdge[j][reverseEdgeNum[j]].end = i;
                reverseEdge[j][reverseEdgeNum[j]].len = tmpLen;
                reverseEdge[j][reverseEdgeNum[j]].cost = orderEdge[i][orderEdgeNum[i]].cost;
                orderEdgeNum[i]++;
                reverseEdgeNum[j]++;
            } else {
                fin2 >> tmpCost;
            }
        }
    }
    fin1.close();
    fin2.close();
}

// 初始化，获得每个点到终点的最短距离和最少花费
void dijstra_q(bool isLen = true) {
    typedef std::pair<int, int> PII;
    std::priority_queue<PII, std::vector<PII>, std::greater<>> q;
    q.emplace(0, cityNum - 1);
    minLen[cityNum - 1] = 0;
    minCost[cityNum - 1] = 0;
    if (isLen) {
        while (!q.empty()) {
            PII p = q.top();
            q.pop();
            int v = p.second;

            if (minLen[v] < p.first) {
                continue;
            }
            // 更新
            for (int i = 0; i < reverseEdgeNum[v]; i++) {
                Edge e = reverseEdge[v][i];
                if (minLen[e.end] > minLen[e.start] + e.len) {
                    minLen[e.end] = minLen[e.start] + e.len;
                    q.emplace(minLen[e.end], e.end);
                }
            }
        }
    } else {
        while (!q.empty()) {
            PII p = q.top();
            q.pop();
            int v = p.second;
            if (minCost[v] < p.first) {
                continue;
            }
            for (int i = 0; i < reverseEdgeNum[v]; i++) {
                Edge e = reverseEdge[v][i];
                if (minCost[e.end] > minCost[e.start] + e.cost) {
                    minCost[e.end] = minCost[e.start] + e.cost;
                    q.emplace(minCost[e.end], e.end);
                }
            }
        }
    }
}

// 初始化
void init() {
    memset(orderEdgeNum, 0, sizeof(orderEdgeNum));
    memset(reverseEdgeNum, 0, sizeof(reverseEdgeNum));
    memset(minCost, 0x7f, sizeof(minCost));
    memset(minLen, 0x7f, sizeof(minLen));
    memset(visitPoint, 0, sizeof(visitPoint));
    memset(curPath, 0, sizeof(curPath));
    curPath[0] = 1;
    memset(bestPath, 0, sizeof(bestPath));
    bestPath[0] = 1;
    curCost = 0;
    curLen = 0;
    bestCost = maxCost;
    bestLen = maxLen;

    readData();
    dijstra_q(true);
    dijstra_q(false);
}

// dfs搜索
void dfs(int curPoint) {
    // 到达终点
    if (curPoint == cityNum - 1) {
        if ((curLen < bestLen && curCost <= maxCost) || (curLen == bestLen && curCost < bestCost)) {
            bestCost = curCost;
            bestLen = curLen;
            memcpy(bestPath, curPath, sizeof(curPath));
        }
        return;
    }
    // 剪枝
    if (curCost + minCost[curPoint] > maxCost || curLen + minLen[curPoint] > bestLen) {
        return;
    }
    // 搜索
    for (int i = 0; i < orderEdgeNum[curPoint]; i++) {
        Edge e = orderEdge[curPoint][i];
        if (visitPoint[e.end] == 0 && curCost + e.cost <= maxCost && curLen + e.len <= bestLen) {
            visitPoint[e.end] = 1;
            curCost += e.cost;
            curLen += e.len;
            curPath[++curPath[0]] = e.end;
            dfs(e.end);
            visitPoint[e.end] = 0;
            curCost -= e.cost;
            curLen -= e.len;
            curPath[0]--;
        }
    }
}

// 打印结果
void printResult() {
    std::cout << "bestCost: " << bestCost << std::endl << "bestLen: " << bestLen << std::endl;
    std::cout << "bestPath: ";
    for (int i = 1; i <= bestPath[0]; i++) {
        std::cout << bestPath[i] + 1;
        if (i != bestPath[0]) {
            std::cout << "->";
        }
    }
    std::cout << std::endl;
}

int main() {
/*
    int num = 2000;
    clock_t startTime = clock();
    for (int i = 0; i < num; ++i) {
        init();
        dfs(0);
    }
    clock_t endTime = clock();
    std::cout << "time: " << (double) (endTime - startTime) / CLOCKS_PER_SEC * 1000 << "ms" << std::endl;
    std::cout << "time: " << (double) (endTime - startTime) << "clocks" << std::endl;
*/
    /* 重复2000次，所用时间（macos、1.4 GHz 四核Intel Core i5、release版本）
     * time: 2309.51ms
     * time: 2.30951e+06clocks
     * bestCost: 1448
     * bestLen: 464
     * bestPath: 1->3->8->11->15->21->23->26->32->37->39->45->47->50
     */

    init();
    dfs(0);
    printResult();

    return 0;
}
