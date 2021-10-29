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
Path_csvFile = 'output_csvfile.csv'

def create_table(cur):
    try:
        if cur != None:
            cur.execute("""CREATE TABLE persons (
                           id INTEGER, 
                           firstname VARCHAR(50), 
                           lastname VARCHAR(50), 
                           emails TEXT [],
                           profession VARCHAR(255), 
                           PRIMARY KEY (id))"""
                        )
    except Exception as err:
        print("\n execute_sql() error for create table:", err)

def insert_value(cur,Path_csvFile):
    try:
        if cur != None:
            with open(Path_csvFile, 'r') as csvf:
                reader = csv.reader(csvf,delimiter = '|')
                next(reader)
                for row in reader:
                    sq1="INSERT INTO persons VALUES ({0},'{1}','{2}', ARRAY{3},'{4}');".format(row[0],str(row[1]),str(row[2]),row[3],str(row[4]))
                    print(sq1)
                    cur.execute(sq1)
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
    conn.commit()
    insert_value(cur,Path_csvFile)
    conn.commit()

except Exception as err:
    print("\n psycopg2 connect error:", err)
    conn = None
    cur = None
