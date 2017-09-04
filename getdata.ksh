#!/bin/ksh
cp ~/Downloads/DailyUsageData-2017-09-09.zip .
rm pge_gas_interval_data_4575820121_2017-08-11_to_2017-09-09.csv
rm pge_electric_interval_data_4575820864_2017-08-11_to_2017-09-09.csv
unzip DailyUsageData-2017-09-09.zip
rm DailyUsageData-2017-09-09.zip
sed 1,5d pge_gas_interval_data_4575820121_2017-08-11_to_2017-09-09.csv > pge_gas_interval_data_4575820121_2017-08-11_to_2017-09-09.csv.new
rm pge_gas_interval_data_4575820121_2017-08-11_to_2017-09-09.csv
mv pge_gas_interval_data_4575820121_2017-08-11_to_2017-09-09.csv.new pge_gas_interval_data_4575820121_2017-08-11_to_2017-09-09.csv
sed 1,5d pge_electric_interval_data_4575820864_2017-08-11_to_2017-09-09.csv > pge_electric_interval_data_4575820864_2017-08-11_to_2017-09-09.csv.new
rm pge_electric_interval_data_4575820864_2017-08-11_to_2017-09-09.csv
mv pge_electric_interval_data_4575820864_2017-08-11_to_2017-09-09.csv.new pge_electric_interval_data_4575820864_2017-08-11_to_2017-09-09.csv
rm ~/Downloads/DailyUsageData-2017-09-09.zip
