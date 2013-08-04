load-cms-data
=============

Simple Python scripts to parse and load the Centers for Medicare and Medicaid Services (CMS) [Medicare Provider Charge Data](http://www.cms.gov/Research-Statistics-Data-and-Systems/Statistics-Trends-and-Reports/Medicare-Provider-Charge-Data/) into a Sqlite3 database (easily adaptable for SQL-based database of your choosing). The data were released by CMS in XLS/CSV files and provide the average charges and Medicare payments for the top 100 inpatient services (by DRG code) and top 30 outpatient services (by APC code) for over 3000 care providers.

To use, simply run `python load_cms_data.py -d <DB_NAME.s3db>` (must have `create_cms_db.py` in the same folder).

Or just use the pre-made s3db in this repository.

Used for http://HealthCostNegotiator.com.
