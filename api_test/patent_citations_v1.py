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
Path_csvFile = 'patent_citation.csv'

def create_table(cur,conn):
    try:
        if cur != None:
            cur.execute("""CREATE TABLE patent_citations(
                    id SERIAL PRIMARY KEY,
                    cited_patent_number VARCHAR(255),
                    patent_number VARCHAR(255),
                    CONSTRAINT fk_customer FOREIGN KEY(patent_number) REFERENCES patent(patent_number))"""
                )
            conn.commit()
    except Exception as err:
        print("\n execute_sql() error for create table:", err)

def insert_value(cur,conn,Path_csvFile):
    try:
        if cur != None:
           with open(Path_csvFile, 'r') as csvf:
                reader = csv.reader(csvf,delimiter = '|')
                next(reader)
                count = 1
                for row in reader:
                    sq1="INSERT INTO patent_citations VALUES ({0},'{1}','{2}');".format(count,str(row[0]),str(row[1]))
                    count = count + 1
                    cur.execute(sq1)
                    conn.commit()
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
    create_table(cur,conn)
    insert_value(cur,conn,Path_csvFile)
    conn.commit()

except Exception as err:
    print("\n psycopg2 connect error:", err)
    conn = None
    cur = None
