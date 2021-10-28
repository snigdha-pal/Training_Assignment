# Import csv and json library
import csv, json

# Define path of csv and json file
print("Define input and output file path.\n")
Path_csvFile = 'input_csvfile.csv'
Path_jsonFile = 'output_jsonfile.json'

# Create a jsonArray
jsonArray = []

# Open csv file 
print("Read Input CSV File and Covert to Json.\n")
with open(Path_csvFile, encoding='utf-8') as csvFile:
     # Use csv library's dictionary reader 
     reader = csv.DictReader(csvFile)

     # Convert each csv row into python dict and append them to jsonArray
     for row in reader:
         jsonArray.append(row)

# Open json file for Write
with open(Path_jsonFile,'w', encoding='utf-8') as jsonFile:

    # Convert python jsonArray to JSON String and write them to file
    jsonString = json.dumps(jsonArray)
    print("Json Output:\n",jsonString)
    print("\n Store Output in a JSON file.")
    jsonFile.write(jsonString)



