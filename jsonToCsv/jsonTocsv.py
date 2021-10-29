# Import csv and json library
import csv, json

# Define path of csv and json file
print("Define input and output file path.\n")
Path_csvFile = 'output_csvfile.csv'
Path_jsonFile = 'input_jsonfile.json'

# Create a jsonArray
jsonDict = []

# Open json file for Read
with open(Path_jsonFile,'r', encoding='utf-8') as jsonFile:
    jsonDict = json.load(jsonFile)
    print("Json Output:\n",jsonDict)

# Open csv file 
print("Write CSV File.\n")
with open(Path_csvFile, 'w', encoding='utf-8') as csvFile:
     # Use csv library's dictionary reader
     columns = []
     row_value = []
     csv_writer = csv.writer(csvFile, delimiter = '|')
     count = 0
     for person in jsonDict:
         row_value = []
         emails = []
         id_value = ''
         first_name = ''
         last_name = ''
         profession = ''
         if count == 0:
             columns = list(person.keys())
             columns.remove('email2')
             csv_writer.writerow(columns)
             count += 1
         for key in list(person.keys()):
             if key == 'email2' or key == 'email':
                emails.append(person[key])
             if key == 'id':
                id_value = person[key]
             if key == 'firstname':
                first_name = person[key]
             if key == 'lastname':
                last_name = person[key]
             if key == 'profession':
                profession = person[key]
         row_value = [id_value,first_name,last_name,emails,profession]
         csv_writer.writerow(row_value)
