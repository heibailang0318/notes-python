-- 第1行:['o_m_lnktbl2', '', 'partition_dt', 'incr']
-- 表：o_m_lnktbl2
-- 处理方式：增量
-- 主键字段：['']
-- 增量字段：partition_dt
-- 拉链字段：('a', 'b', 'c', 'd')
-------------------------------生成语句：-------------------------------
-- 创建拉链表：
CREATE TABLE o_m_lnktbl2_his (a varchar(20) COMMENT '', b varchar(20) COMMENT '', c varchar(20) COMMENT '', d varchar(20) COMMENT '', start_date varchar(10) COMMENT '拉链起始日期', end_date varchar(10) COMMENT '拉链最新日期' ) ROW FORMAT DELIMITED FIELDS TERMINATED BY '\001' STORED AS TEXTFILE;
-- 初始化拉链表：
INSERT OVERWRITE TABLE o_m_lnktbl2_his SELECT distinct t1.a, t1.b, t1.c, t1.d, '2000-01-01' as start_date, '2099-01-01' as end_date FROM o_m_lnktbl2;
----- 每日拉链ETL逻辑：-----
-- 1.存储增量数据：
CREATE TABLE o_m_lnktbl2_tmp as SELECT distinct t1.a, t1.b, t1.c, t1.d FROM o_m_lnktbl2 WHERE partition_dt = date_add(CURRENT_DATE,-1);
-- 2.拉链逻辑：
INSERT OVERWRITE TABLE o_m_lnktbl2_his 
SELECT t1.a, t1.b, t1.c, t1.d, t1.start_date
, 
case when t1.end_date='2099-01-01' 
and t2.a,'_',t2.b,'_',t2.c,'_',t2.d is not null 
then date_add(CURRENT_DATE,-2) 
else t1.end_date end as end_date 
FROM o_m_lnktbl2_his t1 
left join o_m_lnktbl2_tmp t2 
on concat(t1.) = concat(t1.) 

union all 

select t1.a, t1.b, t1.c, t1.d, date_add(CURRENT_DATE,-1) as start_date, '2099-01-01' as end_date 
from o_m_lnktbl2_tmp t1;

-- 第2行:['o_m_lnktbl2', 'a,b', 'partition_dt', 'full']
---- 表：o_m_lnktbl2
-- 处理方式：全量
-- 主键字段：['a', 'b']
-- 拉链字段：('c', 'd')
-------------------------------生成语句：-------------------------------
-- 创建拉链表：
CREATE TABLE o_m_lnktbl2_his (a varchar(20) COMMENT '', b varchar(20) COMMENT '', c varchar(20) COMMENT '', d varchar(20) COMMENT '', start_date varchar(10) COMMENT '拉链起始日期', end_date varchar(10) COMMENT '拉链最新日期' ) ROW FORMAT DELIMITED FIELDS TERMINATED BY '\001' STORED AS TEXTFILE;
-- 初始化拉链表：
INSERT OVERWRITE TABLE o_m_lnktbl2_his SELECT distinct t1.a, t1.b, t1.c, t1.d, '2000-01-01' as start_date, '2099-01-01' as end_date FROM o_m_lnktbl2;
----- 每日拉链ETL逻辑：-----
-- 1.存储增量数据：
CREATE TABLE o_m_lnktbl2_tmp as 
SELECT * from (
select case when concat(t1.a,'_',t1.b) is not null 
and concat(t2.a,'_',t2.b) is null 
then 'I' 
when concat(t1.a,'_',t1.b) is null 
and concat(t2.a,'_',t2.b) is not null then 'D' 
when concat(t1.a,'_',t1.b) is not null 
and concat(t2.a,'_',t2.b) is not null 
and concat(t1.a,'_',t1.b) <> concat(t2.a,'_',t2.b) 
then 'U' else 'N' end as dtype
, t1.a, t1.b, t1.c, t1.d
, concat(t1.a,'_',t1.b) as t1_pkcol, concat(t2.a,'_',t2.b) as t1_pkcol from (
select distinct * from o_m_lnktbl2 
where partition_dt=date_add(CURRENT_DATE,-1)
) t1 full join (
select distinct * from o_m_lnktbl2 
where partition_dt=date_add(CURRENT_DATE,-2)
) t2 
on concat(t1.a,'_',t1.b)=concat(t2.a,'_',t2.b)) t where dtype<>'N';
-- 2.拉链逻辑：
INSERT OVERWRITE TABLE o_m_lnktbl2_his SELECT t1.a, t1.b, t1.c, t1.d, t1.start_date, case when t1.end_date='2099-01-01' and concat(t2.a,'_',t2.b)) is not null then date_add(CURRENT_DATE,-2) else t1.end_date end as end_date FROM o_m_lnktbl2_his t1 left join o_m_lnktbl2_tmp t2 on concat(t1.a,'_',t1.b) = concat(t2.a,'_',t2.b) union all select t1.a, t1.b, t1.c, t1.d, date_add(CURRENT_DATE,-1) as start_date, '2099-01-01' as end_date from o_m_lnktbl2_tmp t1 where dtype <> 'D';

-- 第3行table列有误: [' ', '', '', '']
-- 第4行type列有误: ['a', '', '', 'aa']
