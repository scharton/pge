--
-- Build gas_summary table from elec staging table.
-- Gas data is expected as 1 row per day.
-- Update the case when a new month file is discovered
--
drop table gas_summary;
create table gas_summary as
select
	case
		when gas_datenum >= 20171109 then 20171208
		when gas_datenum >= 20171011 then 20171108
		when gas_datenum >= 20170912 then 20171010
		when gas_datenum >= 20170811 then 20170911
	 	when gas_datenum >= 20170712 then 20170810
		when gas_datenum >= 20170608 then 20170711
		when gas_datenum >= 20170509 then 20170609
		when gas_datenum >= 20170409 then 20170510
		when gas_datenum >= 20170309 then 20170410
		when gas_datenum >= 20170207 then 20170310
		when gas_datenum >= 20170108 then 20170208
		when gas_datenum >= 20161207 then 20170109
		when gas_datenum >= 20161107 then 20161208
		when gas_datenum >= 20161009 then 20161108
		when gas_datenum >= 20160908 then 20161010
		when gas_datenum >= 20160809 then 20160909
		when gas_datenum >= 20160710 then 20160810
		when gas_datenum >= 20160608 then 20160711
		when gas_datenum >= 20160509 then 20160609
		when gas_datenum >= 20160407 then 20160510
		when gas_datenum >= 20160309 then 20160408
	else 20160310
	end as end_date,
	sum(cost) cost,
	sum(usage) usage,
	max(gas_datenum) last_day,
	count(*) days,
	(sum(usage))/(count(*)) usage_per_day,
	case
		when count(*) >= 29 then sum(cost)
		else  ( 30.0 / (count(*)) ) * sum(cost)
	end as cost_projection
from gas e
group by end_date
order by end_date desc
;
