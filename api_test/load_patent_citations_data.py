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
    columns = []
    if type(patent_details) == list:
        first_record = patent_details[0]
        for column in list(first_record.keys()):
            if type(first_record[column]) == list:
                columns = list(first_record[column][0].keys())
            else:
                columns.append(column)
    csv_writer.writerow(columns)
    for i, patent_dict in enumerate(patent_details):
        patent_number = ''
        citation_number = []
        row_value = []
        for col_names, val in patent_dict.items():
            if type(val) == str:
                patent_number = val
            if type(val) == list:
                for count in val:
                    for count_value in list(count.values()):
                        citation_number.append(count_value)
        for citation in citation_number:
            row_value = []
            row_value.append(citation)
            row_value.append(patent_number)
            csv_writer.writerow(row_value)

Patent_URL = 'https://api.patentsview.org/patents/query?q={"_gte":{"patent_date":"2020-06-01"}}&f=["patent_number","cited_patent_number"]'
Path_jsonFile = 'patent_citation.json' 
Path_csvFile = 'patent_citation.csv'

patent_details=load_data(Patent_URL)
write_json(patent_details,Path_jsonFile)
write_csv(patent_details,Path_csvFile)
