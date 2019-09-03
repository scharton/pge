sample = 'pge_electric_interval_data_4575820864_2019-08-13_to_2019-09-11.csv'

print(sample)

s = sample.split('_')
print(s)

last = s[-1]
print(last)

end_date = last.split('.')[0]
print(end_date)

# elecdatenum = elecdate[0:4] + elecdate[5:7] + elecdate[8:10]

end_datenum = end_date[0:4] + end_date[5:7] + end_date[8:10]
print(end_datenum)