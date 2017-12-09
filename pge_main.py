import os
import csv
import sqlite3
import zipfile


csvdatafolder = './csvdata'

elecfile = 'pge_electric_interval_data'
gasfile = 'pge_gas_interval_data'
sample = 'pge_electric_interval_data_4575820864_2017-06-10_to_2017-07-09.csv'
eleccsv = 'electric.csv'

def load_electric():

    header = 'TYPE,START DATE,END DATE,USAGE,UNITS,COST,NOTES'

    conn = sqlite3.connect('energy.sqlite')
    csr = conn.cursor()
    csr.execute('delete from elec')
    conn.commit()
    data = []

    for dir, subdir, files in os.walk(csvdatafolder):
        for f in files:
            if f.startswith(elecfile):
                fullfile = dir + '/' + f
                with open(fullfile, 'r+') as pgefile:
                    reader = csv.reader(pgefile)
                    for row in reader:
                        # Each real record starts with "Electric" as the first item
                        if len(row) != 8 or str(row[0]).startswith('Electric') is False:
                            continue

                        elecdate = str('{}').format(row[1])

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

def load_gas():

    conn = sqlite3.connect('energy.sqlite')
    csr = conn.cursor()
    csr.execute('delete from gas')
    data = []

    for dir, subdir, files in os.walk(csvdatafolder):
        for f in files:
            if f.startswith(gasfile):
                fullfile = dir + '/' + f
                with open(fullfile, 'r+') as pgefile:
                    reader = csv.reader(pgefile)
                    for row in reader:
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
    """Look for any DailyUsageData files in the folder tree

    Files will look like pge_electric_interval...<date range>.csv
    or pge_gas_interval...<date range>.csv.


    """
    for dir, subdir, files in os.walk(folder):
        for f in files:
            if f.startswith('DailyUsageData'):
                zip_file = folder + f

                with zipfile.ZipFile(file=zip_file, mode='r') as zip_pge:
                    pge_files = zip_pge.namelist()
                    for pge_file in pge_files:
                        # extraction will land in the pge folder because
                        # this is where the python script originates
                        zip_pge.extract(member=pge_file, path=csvdatafolder)


if __name__ == '__main__':
    if False:
        print('hi')
    else:
        download_folder = '/Users/dscharton/Downloads/'
        process_zip_file(download_folder)
        load_electric()
        load_gas()
