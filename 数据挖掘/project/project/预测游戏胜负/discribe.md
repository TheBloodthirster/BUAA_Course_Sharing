# 预测游戏胜负

## 任务描述

《英雄联盟》（简称LOL）是由美国拳头游戏（Riot Games）开发、中国大陆地区腾讯游戏代理运营的英雄对战MOBA竞技网游。

英雄联盟的经典地图：召唤师峡谷，拥有三路，分为红蓝两方，红蓝双方各自拥有：主水晶、小水晶、防御塔等设施，主水晶会定时刷新三路小兵（Minions），召唤师峡谷也会在地图的特殊地区刷新中立生物（中立指不会主动攻击红蓝双方英雄，相对于小兵会攻击敌方），中立生物包含一般中立生物（三狼、F6、石头人及红蓝BUFF，还）以及远古史诗野怪（小龙Dragon，峡谷先锋Herald，大龙Baron）。召唤师（玩家）可以选择不同的英雄，红蓝双方各五名玩家，通过击杀敌方英雄、小兵、中立生物以及破坏敌方设施来获取金钱以购买装备（金钱越多，装备越好，英雄更加强力），最终以破坏敌方主水晶为目标，赢得比赛胜利。

召唤师峡谷变幻莫测，比赛中KFC上校的种种下饭预测也让观众肚子饱饱。这里，我们期望实现一个简单版的上校，通过游戏前10分钟的关键数据来预测最终的胜方。

## 数据集

我们收集了大约10000场高段位比赛，提取了红蓝双方前10分钟比赛里的关键数据，一共39个特征，其中包含：

| feature                    | column name                      | discribe |
| -------------------------- | -------------------------------- | -------- |
| 插眼数                     | blue/redWardsPlaced              | int      |
| 拆眼数                     | blue/redWardsDestroyed           | int      |
| 一血                       | blue/redFirstBlood               | binary   |
| 杀人数                     | blue/redKills                    | Int      |
| 死亡数                     | blue/redDeaths                   | int      |
| 助攻数                     | blue/redAssists                  | int      |
| 大师以上玩家数目           | blue/redEliteMonsters            | int      |
| 击杀小龙                   | blue/redDragons                  | binary   |
| 击杀峡谷先锋               | blue/redHeralds                  | binary   |
| 拆塔数                     | blue/redTowersDestroyed          | int      |
| 总金钱                     | blue/redTotalGold                | int      |
| 平均等级                   | blue/redAvgLevel                 | float    |
| 总经验                     | blue/redTotalExperience          | int      |
| 总击杀小兵数               | blue/redTotalMinionsKilled       | int      |
| 总击杀野怪数               | blue/redTotalJungleMinionsKilled | int      |
| 经济差                     | blue/redGoldDiff                 | int      |
| 经验差                     | blue/redExperienceDiff           | int      |
| 分均补刀数（分均击杀小兵） | blue/redCSPerMin                 | float    |
| 分均金钱                   | blue/redGoldPerMin               | float    |
| 蓝色方是否胜利             | blueWins                         | binary   |

注：由于游戏时间为10分钟，所以大龙不会被击杀，小龙和峡谷先锋也仅可能被击杀一次。

我们训练集和测试集的比例大约为7：3，即会提供给你约7000条数据以供训练。

**你需要根据红蓝双方一共38个特征来预测蓝色方是否获胜。**

## 评价

无标签的测试集会在本作业的截止日期发给你，对于测试集中的每个记录，你应该预测出每一场比赛蓝色方是否胜利，文件应该包含一个头，并具有以下格式：

----

文件名：组号_2，如8_2。连接符必须为下划线。

--------

id;blueWins

0;0

1;1

etc.

----

注：封号使用英文封号，不允许添加空格。

请各位同学严格遵守结果文件命名以及格式规范！



