title: 模型对比--从最大回撤的角度来看
summary: 对比算法
authors: yanfzhai
date: 2015-12-15
tags: 模型构建
	    多层对比

# 模型对比--从最大回撤的角度来看

![jjww](..\pics\perfect\read-1564105_960_720.jpg)
[TOC]
##小盘价值模型 Vs 现在使用模型
- 小盘价值模型：市值因子、PB、分析师预期、动态PE
- 小盘价值模型，选股数量300只
- 现在使用的模型：小盘价值模型+交易因子，选股数量50只
- 考虑调仓交易费用，剔除新股效应、ST股票和停牌股票



##对比算法

- 分别计算两个策略模型的每日收益率

- 计算两者每日收益率之差，把这个收益率之差累乘起来

- 这相当于用原小盘价值模型 对冲 现在的模型持仓，且每日再平衡
  ![jjww](..\pics\AboutBack\allyears.png)

- 对应的最大回撤情况
  ![jjww](..\pics\AboutBack\allyears_MB.png)


- 2013年
  ![jjww](..\pics\AboutBack\f_2013.png)
  ![jjww](..\pics\AboutBack\mb_2013.png)
  ​
- 2014年
  ![jjww](..\pics\AboutBack\f_2014.png)
  ![jjww](..\pics\AboutBack\mb_2014.png)
  ​
- 2015年
  ![jjww](..\pics\AboutBack\f_2015.png)
  ![jjww](..\pics\AboutBack\mb_2016.png)
  ​
- 2016年
  ![jjww](..\pics\AboutBack\f_2016.png)
  ![jjww](..\pics\AboutBack\mb_2016.png)
  ​

##结论
-  历史最大回撤在5.5%左右
-  持仓数量减少 本身也会导致相较原来模型更大的震荡，引致回撤发生

