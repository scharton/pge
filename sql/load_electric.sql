--
-- Build elec_summary table from elec staging table.
-- Electric data is expected as 1 row per hour which is why the
-- division by 24 is necessary.
-- Update the case when a new month file is discovered
--
drop table elec_summary
;
create table elec_summary as
select
	case
		when elec_datenum >= 20171109 then 20171208
		when elec_datenum >= 20171011 then 20171108
		when elec_datenum >= 20170912 then 20171010
		when elec_datenum >= 20170811 then 20170911
	 	when elec_datenum >= 20170712 then 20170810
		when elec_datenum >= 20170608 then 20170711
		when elec_datenum >= 20170509 then 20170609
		when elec_datenum >= 20170409 then 20170510
		when elec_datenum >= 20170309 then 20170410
		when elec_datenum >= 20170207 then 20170310
		when elec_datenum >= 20170108 then 20170208
		when elec_datenum >= 20161207 then 20170109
		when elec_datenum >= 20161107 then 20161208
		when elec_datenum >= 20161009 then 20161108
		when elec_datenum >= 20160908 then 20161010
		when elec_datenum >= 20160809 then 20160909
		when elec_datenum >= 20160710 then 20160810
		when elec_datenum >= 20160608 then 20160711
		when elec_datenum >= 20160509 then 20160609
		when elec_datenum >= 20160407 then 20160510
		when elec_datenum >= 20160309 then 20160408
	else 20160310
	end as end_date,
	sum(cost) cost,
	sum(usage) usage,
	max(elec_datenum) last_day,
	count(*)/24 days,
	(sum(usage))/(count(*)/24) usage_per_day,
	case
		when count(*)/24 >= 29 then sum(cost)
		else  ( 30.0 / (count(*)/24.0) ) * sum(cost)
	end as cost_projection
from elec e
group by end_date
order by end_date desc
;
