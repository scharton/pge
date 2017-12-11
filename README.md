# pge
A processor and repository for consuming PG&E utility usage files.

Some parts of this early stage program are inflexible but will be made more configurable
as it evolves.

## Requirements
An online account with PG&E is necessary. Data files are accessible through the usage
link and "Green Button" download page.

## Files
Daily usage downloads are provided daily for gas and electric.

**Electric:** `pge_electric_interval_data_<account number>_YYYY-MM-DD_to_YYYY-MM-DD.csv`

**Gas:** `pge_gas_interval_data_<account number>_YYYY-MM-DD_to_YYYY-MM-DD.csv`

## Database
The program currently is designed to work with a SQLite 3 database specifically named
**energy.sqlite** and place it in the root of this project.

### Database Preparation
Until automated in the Python code, prepare your database with this one-time setup.
```sqlite-sql
CREATE TABLE elec
(
   elec_date     TEXT,
   elec_hr       TEXT,
   elec_datenum  INTEGER,
   usage         REAL,
   cost          REAL
);

CREATE TABLE gas
(
   gas_date     TEXT,
   gas_datenum  INTEGER,
   usage        REAL,
   cost         REAL
);

COMMIT;
```
### Staging Tables
Two staging tables created in the previous section `elec` and `gas` are loaded with 
the raw CSV data through the function sequence:
```python
if __name__ == '__main__':
    download_folder = '/Users/me/Downloads/'
    process_zip_file(download_folder)
    load_electric()
    load_gas()
```

### Summary Tables
Until rolled into the Python, summary tables area created by running the SQL files in a SQLite
client.

After loading the staging tables, run `load_electric.sql` and `load_gas.sql`. These are in the **sql** 
folder.