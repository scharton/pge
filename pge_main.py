#!/usr/local/bin/python3
import os
import csv
import sqlite3
import zipfile


# Steps to move file and prepare
# Copy "DailyUsagexxx" from Downloads to pge folder
# Unzip the file
# Copy from folder DailyUsage to pge (parent)
# Remove first 5 lines from each file (maybe do that before the copy)
# Delete the zip and temp folder

folderlocation = '.'

elecfile = 'pge_electric_interval_data'
gasfile = 'pge_gas_interval_data'
sample = 'pge_electric_interval_data_4575820864_2017-06-10_to_2017-07-09.csv'
eleccsv = 'electric.csv'

def build_electric_csv():

    header = 'TYPE,START DATE,END DATE,USAGE,UNITS,COST,NOTES'

    with open(eleccsv, 'w') as eleccsvinit:
        print('initialized new {}'.format(eleccsv))


    conn = sqlite3.connect('energy.sqlite')
    csr = conn.cursor()
    csr.execute('delete from elec')
    conn.commit()
    data = []

    for dir, subdir, files in os.walk('./'):
        for f in files:
            if f.startswith(elecfile):
                fullfile = dir + '/' + f
                with open(fullfile, 'r+') as pgefile:
                    reader = csv.reader(pgefile)
                    for row in reader:
                        # skip header/text
                        # if str.isalnum(row[0]):
                        #     # print('skipping {}'.format(row))
                        #     continue
                        if len(row) != 8 or str(row[0]).startswith('Electric') is False:
                            continue

                        elecdate = str('{}').format(row[1])

# datenum = str("{}{}{}").format(v[0:4], v[5:7], v[8:10])
                        elecdatenum = elecdate[0:4] + elecdate[5:7] + elecdate[8:10]
                        elechr = str('{} {}:00').format(elecdate, row[2])
                        usage = row[4]
                        cost = row[6].lstrip('$')
                        data.append((elecdate, elechr, elecdatenum, usage, cost))

                        rowtoelec = (elecdate, elecdatenum, elechr, usage, cost)
                        with open(eleccsv, 'a') as e:
                            writer = csv.writer(e)
                            writer.writerow(rowtoelec)


    csr.executemany('insert into elec values(?, ?, ?, ?, ?)', data)
    conn.commit()
    conn.close()

def build_gas_csv():

    conn = sqlite3.connect('energy.sqlite')
    csr = conn.cursor()
    csr.execute('delete from gas')
    data = []

    for dir, subdir, files in os.walk('./'):
        for f in files:
            if f.startswith(gasfile):
                fullfile = dir + '/' + f
                # print('writing {} to new csv'.format(fullfile))
                with open(fullfile, 'r+') as pgefile:
                    reader = csv.reader(pgefile)
                    for row in reader:
                        # skip header/text
                        # if str.isalnum(row[0]):
                        #     # print('skipping {}'.format(row))
                        #     continue

                        if len(row) != 6 or str(row[0]).startswith('Natural') is False:
                            continue

                        elecdate = str('{}').format(row[1])
                        elecdatenum = elecdate[0:4] + elecdate[5:7] + elecdate[8:10]
                        usage = row[2]
                        cost = row[4].lstrip('$')
                        data.append((elecdate, elecdatenum, usage, cost))
                        rowtogas = (elecdate, elecdatenum, usage, cost)
                        with open(eleccsv, 'a') as e:
                            writer = csv.writer(e)
                            writer.writerow(rowtogas)

    csr.executemany('insert into gas values(?, ?, ?, ?)', data)
    conn.commit()
    conn.close()
    # print(data)


def process_zip_file(folder):
    for dir, subdir, files in os.walk(folder):
        for f in files:
            if f.startswith('DailyUsageData'):
                zip_file = folder + f

                with zipfile.ZipFile(zip_file) as zip_pge:
                    pge_files = zip_pge.namelist()
                    for pge_file in pge_files:
                        # extraction will land in the pge folder because
                        # this is where the python script originates
                        zip_pge.extract(pge_file)


if __name__ == '__main__':

    download_folder = '/Users/dscharton/Downloads/'
    process_zip_file(download_folder)
    build_electric_csv()
    build_gas_csv()
    # write_to_db()
