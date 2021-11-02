import json
import requests

Path_jsonFile = 'employee.json'
jsonDict = []

with open(Path_jsonFile,'r', encoding='utf-8') as jsonFile:
        jsonDict = json.load(jsonFile)

url = "http://172.31.6.101:8983/solr/employees/update?commit=true"
header = {"Content-type":"application/json"}
payload = jsonDict
res = requests.post(url, data=open("employee.json", "rb").read(), headers=header)
pastebin_url = res.text
print(pastebin_url)
