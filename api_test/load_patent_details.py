# Import python library
import requests,json,sys

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

def load_data(URL):
    response = requests.get(URL)
    result = json.dumps(response.json(),sort_keys=True, indent=4)
    json_result = json.loads(result)
    return json_result["patents"]

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

if cur != None:
    try:
        patent_URL = 'https://api.patentsview.org/patents/query?q={"_gte":{"patent_date":"2020-06-01"}}&f=["patent_number","patent_date","patent_title"]'
        patent_details = load_data(patent_URL)

        columns = []
        sql_string = ''
        table_name = "patent"
        if type(patent_details) == list:
            first_record = patent_details[0]
            columns = list(first_record.keys())
            print("\n Column Names:",columns)
        for i, patent_dict in enumerate(patent_details):
            # iterate over the values of each record dict object
            values = []
            for col_names, val in patent_dict.items():
                # Postgres strings must be enclosed with single quotes
                if type(val) == str:
                    # escape apostrophies with two single quotations
                    val = val.replace("'", "''")
                    val = "'" + val + "'"
                values += [ str(val) ]
            sql_string = 'INSERT INTO {} '.format( table_name )
            sql_string += "(" + ', '.join(columns) + ")\nVALUES "
            sql_string += "(" + ', '.join(values) + "),\n"
            sql_string = sql_string[:-2] + ";"
            print(sql_string)
            cur.execute( sql_string )
            conn.commit()
    except Exception as error:
        print("\nexecute_sql() error:", error)

