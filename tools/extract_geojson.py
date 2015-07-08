import csv
import json
import argparse

  
def csvfile_to_dict_list(filename, delimiter=';'):
    row_list = []
    with open(filename, 'rb') as csvfile:
        reader = csv.DictReader(csvfile, delimiter = delimiter)
        for row in reader:
            row_list.append(row)
    return row_list
    
def dict_list_to_jsonfile(dict_list, filename):
    with open(filename, 'wb') as jsonfile:
        json.dump(dict_list, jsonfile)   
    


def main():
    parser = argparse.ArgumentParser(
        description="Extract geoJSON field from the csv file" + \
                    "that contains data about CABA's 'comunas'")
    
    parser.add_argument('csvfile', help = 'Input file')
    parser.add_argument('jsonfile', help = 'Output file')
    parser.add_argument('delimiter', help = 'Delimiter')

    args = parser.parse_args()
    
    rows_as_dicts = csvfile_to_dict_list(args.csvfile, args.delimiter)    

    dict_list_to_jsonfile(rows_as_dicts, args.jsonfile)


if __name__ == "__main__":
    main()
