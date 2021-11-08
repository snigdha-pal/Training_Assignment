# Import python library
import json, configparser, requests
# psycopg2 database adapter for postgreSQL
from psycopg2 import connect, Error

config = configparser.ConfigParser()
config.readfp(open(r'configfile.txt'))

# dp configuration of Database Connection
db_name = config.get('postgres_config', 'dbname')
user_name = config.get('postgres_config', 'user')
host_name = config.get('postgres_config', 'host')
pwd_name = config.get('postgres_config', 'password')
connect_count = config.get('postgres_config', 'connect_timeout')
table_name = config.get('postgres_config', 'table_name')

# do configuration of SOLR Connection
solr_host = config.get('solr_config', 'host_ip')
solr_port = config.get('solr_config', 'port_number')
solr_collection = config.get('solr_config','collection_name')

def fetch_table_data(cur,conn):
    try:
        if cur != None:
            result = []
            sql = "select * from {0};".format(table_name)
            cur.execute(sql)
            for row in cur.fetchall():
                key = []
                value = []
                for i, val in enumerate(row):
                    key.append(cur.description[i][0])
                    value.append(val)
                row_data = dict(zip(key,value))
                result.append(row_data)
            conn.commit()
            return result
    except Exception as err:
        print("\n execute_sql() error to fetch data from table:", err)

def commit_to_solr(result):
    url = "http://{0}:{1}/solr/{2}/update?commit=true".format(solr_host,solr_port,solr_collection)
    header = {"Content-type":"application/json"}
    payload = json.dumps(result)
    res = requests.post(url, data=payload, headers=header)
    pastebin_url = res.text
    print(pastebin_url)


try:
    # declare a new PostgreSQL connection object
    conn = connect(
            dbname = db_name,
            user = user_name,
            host = host_name,
            password = pwd_name,
            connect_timeout = connect_count)
    cur = conn.cursor()
    result = fetch_table_data(cur,conn)
    conn.commit()
    commit_to_solr(result)
    conn.commit()

except Exception as err:
    print("\n psycopg2 connect error:", err)
    conn = None
    cur = None
