# Import python library
import csv, configparser

# psycopg2 database adapter for postgreSQL
from psycopg2 import connect, Error

# do configuration of Database Connection
config = configparser.ConfigParser()
config.readfp(open(r'configfile.txt'))
db_name = config.get('postgres_config', 'dbname')
user_name = config.get('postgres_config', 'user')
host_name = config.get('postgres_config', 'host')
pwd_name = config.get('postgres_config', 'password')
connect_count = config.get('postgres_config', 'connect_timeout')

# Define CSV File Path
Path_csvFile = 'patent.csv'

def create_table(cur):
    try:
        if cur != None:
            cur.execute("""CREATE TABLE patent (
                patent_date DATE NOT NULL,
                patent_number VARCHAR(255) PRIMARY KEY,
                patent_title VARCHAR
                )"""
                )
    except Exception as err:
        print("\n execute_sql() error for create table:", err)

def insert_value(cur,Path_csvFile):
    try:
        if cur != None:
            with open(Path_csvFile, 'r') as csvf:
                next(csvf)
                cur.copy_from(csvf, 'patent', sep = '|')
    except Exception as err:
        print("\n execute_sql() error for insert value in table:", err)

try:
    # declare a new PostgreSQL connection object
    conn = connect(
            dbname = db_name,
            user = user_name,
            host = host_name,
            password = pwd_name,
            connect_timeout = connect_count)
    cur = conn.cursor()
    create_table(cur)
    insert_value(cur,Path_csvFile)
    conn.commit()

except Exception as err:
    print("\n psycopg2 connect error:", err)
    conn = None
    cur = None
