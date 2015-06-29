
SELECT c.`name`,
  CASE WHEN v.`type` = 20 THEN '楼口小店'
    WHEN v.`type` = 10 THEN '便利店'
    WHEN v.`type` = 40 THEN '全城送'
  END AS `type`,
  COUNT( DISTINCT CASE WHEN o.`add_time` >= UNIX_TIMESTAMP('VAR_START') AND o.`add_time` < UNIX_TIMESTAMP('VAR_END') AND o.`buyer_id` <> 0 THEN o.`buyer_id` ELSE NULL END) AS lastdayusercnt,
  COUNT( DISTINCT CASE WHEN o.`add_time` >= UNIX_TIMESTAMP('VAR_EARLY') AND o.`add_time` < UNIX_TIMESTAMP('VAR_START') AND o.`buyer_id` <> 0 THEN o.`buyer_id` ELSE NULL END) AS last7dayusercnt,
  COUNT( DISTINCT CASE WHEN o.`add_time` >= UNIX_TIMESTAMP('VAR_EARLY') AND o.`add_time` < UNIX_TIMESTAMP('VAR_END') AND o.`buyer_id` <> 0 THEN o.`buyer_id` ELSE NULL END) AS last8dayusercnt,
  '0' AS placeholder1,
  '0' AS placeholder2,
  '0' AS placeholder3,
  SUM(CASE WHEN o.`add_time` >= UNIX_TIMESTAMP('VAR_START') AND o.`add_time` < UNIX_TIMESTAMP('VAR_END') THEN o.`goods_amount` ELSE 0 END) AS goodsamount,
  SUM(CASE WHEN o.`add_time` >= UNIX_TIMESTAMP('VAR_START') AND o.`add_time` < UNIX_TIMESTAMP('VAR_END') THEN 1 ELSE 0 END) AS ordercnt,
  '0' AS placeholder4
FROM mall.`tcz_order` o, cvs.`cvs_info` v, cvs.`city_info` c
WHERE o.`shipping_id` = v.`id`
AND o.`source` = 50
AND o.`add_time` >= UNIX_TIMESTAMP('VAR_EARLY') AND o.`add_time` < UNIX_TIMESTAMP('VAR_END')
AND o.`status` IN (3, 13, 15)
AND v.`city_id` = c.`id`
GROUP BY v.`city_id`, c.`name`, v.`type`
UNION
SELECT c.`name`,
  CASE WHEN v.`type` = 20 THEN '楼口小店'
    WHEN v.`type` = 10 THEN '便利店'
    WHEN v.`type` = 40 THEN '全城送'
  END AS `type`,  
  COUNT( DISTINCT CASE WHEN o.`add_time` >= UNIX_TIMESTAMP('VAR_START') AND o.`add_time` < UNIX_TIMESTAMP('VAR_END') AND o.`buyer_id` <> 0 THEN o.`buyer_id` ELSE NULL END) AS lastdayusercnt,
  COUNT( DISTINCT CASE WHEN o.`add_time` >= UNIX_TIMESTAMP('VAR_EARLY') AND o.`add_time` < UNIX_TIMESTAMP('VAR_START') AND o.`buyer_id` <> 0 THEN o.`buyer_id` ELSE NULL END) AS last7dayusercnt,
  COUNT( DISTINCT CASE WHEN o.`add_time` >= UNIX_TIMESTAMP('VAR_EARLY') AND o.`add_time` < UNIX_TIMESTAMP('VAR_END') AND o.`buyer_id` <> 0 THEN o.`buyer_id` ELSE NULL END) AS last8dayusercnt,
  '0' AS placeholder1,
  '0' AS placeholder2,
  '0' AS placeholder3,
  SUM(CASE WHEN o.`add_time` >= UNIX_TIMESTAMP('VAR_START') AND o.`add_time` < UNIX_TIMESTAMP('VAR_END') THEN o.`goods_amount` ELSE 0 END) AS goodsamount,
  SUM(CASE WHEN o.`add_time` >= UNIX_TIMESTAMP('VAR_START') AND o.`add_time` < UNIX_TIMESTAMP('VAR_END') THEN 1 ELSE 0 END) AS ordercnt,
  '0' AS placeholder4
FROM mall.`tcz_order` o, cvs.`cvs_info` v, cvs.`city_info` c
WHERE o.`seller_id` = v.`store_id`
AND o.`source` IN (20,21,30) 
AND o.`add_time` >= UNIX_TIMESTAMP('VAR_EARLY') AND o.`add_time` < UNIX_TIMESTAMP('VAR_END')
AND o.`status` IN (3, 13, 15)
AND v.`store_id` <> 0 
AND v.`city_id` = c.`id`
GROUP BY v.`city_id`, c.`name`, v.`type`;

