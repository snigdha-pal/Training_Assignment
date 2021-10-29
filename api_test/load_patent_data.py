# Import python library
import requests,json,csv


def load_data(URL):
    response = requests.get(URL)
    result = json.dumps(response.json(),sort_keys=True, indent=4)
    json_result = json.loads(result)
    return json_result["patents"]

def write_json(result,Path_jsonFile):
    with open(Path_jsonFile,'w', encoding='utf-8') as jsonFile:
        result_json = json.dumps(result, sort_keys=True, indent=4)
        jsonFile.write(result_json)

def write_csv(result,Path_csvFile):
    data_file = open(Path_csvFile, 'w')
    csv_writer = csv.writer(data_file, delimiter = '|')
    count = 0
    for patent in result:
        if count == 0 :
            column_name = patent.keys()
            csv_writer.writerow(column_name)
            count += 1

        csv_writer.writerow(patent.values())

Patent_URL = 'https://api.patentsview.org/patents/query?q={"_gte":{"patent_date":"2020-06-01"}}&f=["patent_number","patent_date","patent_title"]'
Path_jsonFile = 'patent.json' 
Path_csvFile = 'patent.csv'

patent_details=load_data(Patent_URL)
write_json(patent_details,Path_jsonFile)
write_csv(patent_details,Path_csvFile)
