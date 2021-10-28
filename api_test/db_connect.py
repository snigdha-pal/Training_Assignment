# psycopg2 database adapter for postgreSQL
from psycopg2 import connect, Error
import configparser

config = configparser.ConfigParser()
config.readfp(open(r'configfile.txt'))
db_name = config.get('postgres_config', 'dbname')
user_name = config.get('postgres_config', 'user')
host_name = config.get('postgres_config', 'host')
pwd_name = config.get('postgres_config', 'password')
connect_count = config.get('postgres_config', 'connect_timeout')

try:
    # declare a new PostgreSQL connection object
    conn = connect(
            dbname = db_name,
            user = user_name,
            host = host_name,
            password = pwd_name,
            # attempt to connect for 3 seconds then raise exception
            connect_timeout = connect_count)
    cur = conn.cursor()
    print ("\ncreated cursor object:", cur)

except Exception as err:
    print("\n psycopg2 connect error:", err)
    conn = None
    cur = None
