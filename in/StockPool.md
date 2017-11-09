title: 公司股票库优选
summary: 一、二、三级库有否价值
authors: yanfzhai
date: 2016-09-15
tags: 股票库划分
	  投资方法


# 公司股票库有没有利用价值？


![jjww](..\pics\perfect\dragen.png)

##公司股票库数据

**目前公司的股票库历史数据只有流水数据，缺乏截面数据**

- 使用0530的截面数据结合流水数据计算每一天的截面数据
- 跟0729的数据做对比
- 正向推导，成功！！！
- 反向推导，成功！！！！

**代码如下，此处可跳过不看**

```SQL
pool: update secucode:{`${reverse x til 6} reverse "000000", string x } each secucode from("DSSS";enlist",") 0: `:pool20160530.csv;
record: update secucode:{`${reverse x til 6} reverse "000000", string x } each secucode from("DTSSSS";enlist",") 0: `:record.csv;
record: update action:?[action=`$"增加到有效证券表";`in;`out]
 from {select from x where date>2016.05.30}update class:?[class=`$"一级库";`c1;?[class=`$"二级库";`c2;`c3]] from record;

mypool: pool;
cdate:2016.05.30+1+til 80;
// 正向推到，从历史某个截面，计算至当前可考的股票库

poolchg:{[pdate]
  temp:(select secucode,secuname,class from mypool where date=exec max date from mypool where date<pdate),
	select secucode,secuname,class from record where date=pdate,action=`in;
 `mypool upsert select date:pdate,secucode,secuname,class from
 {delete from x where action=`out}
 temp lj 2!select secucode,class,action from record where date=pdate,action=`out;
  };

poolchg each cdate;
pool0729: update secucode:{`${reverse x til 6} reverse "000000", string x } each secucode from 
  update class:?[class=`$"一级库";`c1;?[class=`$"二级库";`c2;`c3]] from ("DSS";enlist",") 0: `:class0729.csv;
// 可以匹配上
lj[;3! update cd:`now from pool0729]
select from mypool where date=2016.07.29
// 也可以匹配上
lj[pool0729;3!select date,secucode,class,secuname from mypool where date=2016.07.29]
// 因为liuchuxiao给的数据问题，我要尝试倒推股票库，即从现状倒推历史股票库
quota : hopen `:10.0.16.107:8001;
record2:select date:fdate,class,secucode,secuname,action from
lj[record;1!update fdate:prev date from quota "t4tradingday"]
mypool2:pool0729
cdate2:2016.07.29- 1+til 90
poolchg2:{[pdate;opoo;reco]
  temp:(select secucode,class from opoo where date=exec min date from opoo where date>pdate),
	select secucode,class from reco where date=pdate,action=`out;
 opoo upsert select date:pdate,secucode,class from
 {delete from x where action=`in}
 temp lj 2!select secucode,class,action from reco where date=pdate,action=`in;
  };
poolchg2[;`mypool2;record2] each cdate2
//对得上！！！
lj[;3!select date,secucode,class,secuname from pool]
select from mypool2 where date=2016.05.30
// 也对的上！！！
lj[select date,secucode,class,secuname from pool;3!update cd:`old from select from mypool2 where date=2016.05.30]
// 成功！！！
```

##因为09年的数据残缺不全，既有备选库还有优选库，没人弄得清楚到底哪个是股票库，只能逆向恢复数据

**从有一、二、三级库的字眼开始，日期始于2012年9月25日；恢复成功**

- 股票库全体数量的变化
  ![jjww](..\pics\stockpool\stockp_total.png)

- 一级库的数量
  ![jjww](..\pics\stockpool\c1.png)

- 二级库的数量
  ![jjww](..\pics\stockpool\c2.png)

- 三级库的数量
  ![jjww](..\pics\stockpool\c3.png)


##股票库质量

**光大保德信公司股票库由一、二、三级库组成，且互不重叠**

- 最新一期股票库数量，一级库1866只；二级库302只；三级库150只

- 由股票库中的股票等权重构成组合，每月月底按照最新的股票库调仓
  ![jjww](..\pics\stockpool\stockpoolperf.png)

- 三级库勉强跑赢基金指数，总体来说按表现计 一级库好于二级库，二级库好于三级库

- 分年度统计
  ![jjww](..\pics\stockpool\table4pool.png)

- 用总库指数除以基金指数，大致可以观察股票库有效和无效的时间段，并显示其区间回撤
  ![jjww](..\pics\stockpool\backword.png)

- 13年7月到15年7月的两年时间 是股票库相对非常有效的时间段；15年7月至今 总库指数相对基金同业表现为区间震荡，并没有明显优势

- 相同方法看一级库
  ![jjww](..\pics\stockpool\bkc1.png)
- 相同方法看二级库
  ![jjww](..\pics\stockpool\bkc2.png)
- 相同方法看三级库
  ![jjww](..\pics\stockpool\bkc3.png)

##结论
-  至少在当前阶段，使用公司股票库来选股并不具有优势

