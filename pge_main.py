import os
import csv
import shutil
import sqlite3
import zipfile
import configparser


csvdatafolder = './csvdata'

elecfile = 'pge_electric_interval_data'
gasfile = 'pge_gas_interval_data'
eleccsv = 'electric.csv'

def get_bill_end_datenum(filename):
    # split by underscore
    # get last element
    # split by dot
    # get first element
    # remove dashes
    filename_csv = filename.split('_')[-1]
    end_date = filename_csv.split('.')[0]
    end_datenum = end_date[0:4] + end_date[5:7] + end_date[8:10]
    return str(end_datenum)


def load_electric():

    print("load_electric")

    header = 'TYPE,START DATE,END DATE,USAGE,UNITS,COST,NOTES'

    conn = sqlite3.connect('energy.sqlite')
    csr = conn.cursor()
    csr.execute('delete from elec')
    conn.commit()
    data = []

    for dir, subdir, files in os.walk(csvdatafolder):
        for f in files:
            if f.startswith(elecfile):
                bill_end_datenum = get_bill_end_datenum(f)
                print(bill_end_datenum)
                fullfile = dir + '/' + f
                with open(fullfile, 'r+', encoding='utf-8') as pgefile:
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
                        data.append((elecdate, elechr, elecdatenum, bill_end_datenum, usage, cost))

                        rowtoelec = (elecdate, elecdatenum, bill_end_datenum, elechr, usage, cost)
                        with open(eleccsv, 'a') as e:
                            writer = csv.writer(e)
                            writer.writerow(rowtoelec)


    csr.executemany('insert into elec values(?, ?, ?, ?, ?, ?)', data)
    conn.commit()
    conn.close()


def build_electric_summary():
    """Create the elec_summary table based on the raw data in elec"""

    # Read each electric file in the csv folder

    print("build_electric_summary")
    conn = sqlite3.connect('energy.sqlite')
    csr = conn.cursor()
    csr.execute('drop table if exists elec_summary')
    conn.commit()
    elec_summary_sql = """
        create table elec_summary as
        select
            case
        """
    date_sql = []
    for dir, subdir, files in os.walk(csvdatafolder):
        for f in files:
            if f.endswith('.csv') is False:
                continue
            file_parts = f.split('_')

            date_start = file_parts[5].split('-')
            date_start = "".join(date_start)
            date_end = file_parts[7].split('.')[0].split('-')
            date_end = "".join(date_end)
            date_sql.append((date_start, date_end))

    date_sql = date_sql[::-1]
    case_sql = ''
    for sql in date_sql:
        case_sql = "{} when elec_datenum >= {} then {}\n".format(case_sql, sql[0], sql[1])

    case_sql = "{} end as end_date,".format(case_sql)
    elec_summary_sql = "{} {}".format(elec_summary_sql, case_sql)
    elec_summary_sql = """{}
            sum(cost) cost,
            sum(usage) usage,
            max(elec_datenum) last_day,
            count(*)/24 days,
            (sum(usage))/(count(*)/24) usage_per_day,
            case 
                when count(*)/24 >= 29 then sum(cost)
                else  ( 30.0 / (count(*)/24.0) ) * sum(cost)
                --else ( 30 / (count(*)/24) ) * sum(cost)
            end as cost_projection
        from elec e
        group by end_date
        order by end_date desc
        ;

    """.format(elec_summary_sql)
    # print(elec_summary_sql)

    csr.execute(elec_summary_sql)
    conn.commit()
    conn.close()


def build_gas_summary():
    """Create the gas_summary table based on the raw data in gas"""

    print("build_gas_summary")
    conn = sqlite3.connect('energy.sqlite')
    csr = conn.cursor()
    csr.execute('drop table if exists gas_summary')
    conn.commit()
    gas_summary_sql = """
        create table gas_summary as
        select
            case
        """
    date_sql = []
    for dir, subdir, files in os.walk(csvdatafolder):
        for f in files:
            if f.endswith('.csv') is False:
                continue
            file_parts = f.split('_')

            date_start = file_parts[5].split('-')
            date_start = "".join(date_start)
            date_end = file_parts[7].split('.')[0].split('-')
            date_end = "".join(date_end)
            date_sql.append((date_start, date_end))

    date_sql = date_sql[::-1]
    case_sql = ''
    for sql in date_sql:
        case_sql = "{} when gas_datenum >= {} then {}\n".format(case_sql, sql[0], sql[1])

    case_sql = "{} end as end_date,".format(case_sql)
    gas_summary_sql = "{} {}".format(gas_summary_sql, case_sql)
    gas_summary_sql = """{}
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

    """.format(gas_summary_sql)
    # print(gas_summary_sql)

    csr.execute(gas_summary_sql)
    conn.commit()
    conn.close()


def load_gas():

    print("load_gas")
    conn = sqlite3.connect('energy.sqlite')
    csr = conn.cursor()
    csr.execute('delete from gas')
    data = []

    for dir, subdir, files in os.walk(csvdatafolder):
        for f in files:
            if f.startswith(gasfile):
                fullfile = dir + '/' + f
                with open(fullfile, 'r+', encoding='utf-8') as pgefile:
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
    print("Checking folder {}".format(folder))
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
                        print(pge_file)


def copy_download_to_csvdata():
    download_folder = cp.get('default', 'download_folder')
    print(download_folder)
    print(csvdatafolder)

    for dir, subdir, files in os.walk(download_folder):
        for f in files:
            if f.startswith('pge_'):
                fp = os.path.join(dir, f)
                shutil.copy(fp, csvdatafolder)


if __name__ == '__main__':
    cp = configparser.ConfigParser()
    cp.read('pge.cfg')

    # Get the results from the downloads
    download_folder = cp.get('default', 'download_folder')
    process_zip_file(download_folder)
    
    copy_download_to_csvdata()

    load_electric()
    load_gas()
    build_electric_summary()
    build_gas_summary()
