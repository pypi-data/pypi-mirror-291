# !/usr/bin/env python3

__version__="0.1.3"

import argparse, os, json, csv, glob
import pandas as pd

def filter():
    keyword = input("Please provide a search keyword to perform this mass filter: ")
    output_file = input("Please give a name to the output file: ")

    if output_file != "":
        output = f'{output_file}.csv'
    else:
        output = 'output.csv'

    output_df = pd.DataFrame(columns=['Source_file', 'Column_y', 'Row_x'])

    ask = input("Scan sub-folder(s) as well (Y/n)? ")
    if  ask.lower() == 'y':
        csv_files = [file for file in glob.glob('**/*.csv', recursive=True) if os.path.basename(file) != output]
    else:
        csv_files = [file for file in glob.glob('*.csv') if file != output]

    for file in csv_files:
        df = pd.read_csv(file)
        for row_idx, row in df.iterrows():
            for col_idx, value in row.items():
                if isinstance(value, str) and keyword in value:
                    print(f"Matched record found: {file}, Row: {row_idx + 1}, Column: {df.columns.get_loc(col_idx) + 1}, Value: {value}")
                    new_row = {
                        'Source_file': file,
                        'Column_y': df.columns.get_loc(col_idx) + 1,
                        'Row_x': row_idx + 1
                    }
                    combined_row = {**new_row, **row}
                    output_df = output_df._append(combined_row, ignore_index=True)

    output_df.to_csv(output, index=False)
    print(f"Results of massive filtering saved to '{output}'")

def convertor():
    json_files = [file for file in os.listdir() if file.endswith('.json')]

    if json_files:
        print("JSON file(s) available. Select which one to convert:")
        
        for index, file_name in enumerate(json_files, start=1):
            print(f"{index}. {file_name}")

        choice = input(f"Enter your choice (1 to {len(json_files)}): ")
        choice_index=int(choice)-1
        selected_file=json_files[choice_index]
        print(f"File: {selected_file} is selected!")

        ask = input("Enter another file name as output (Y/n)? ")
        if  ask.lower() == 'y':
                given = input("Give a name to the output file: ")
                output=f'{given}.csv'
        else:
                output=f"{selected_file[:len(selected_file)-5]}.csv"
        
        try:
            with open(selected_file, encoding='utf-8-sig') as json_file:
                jsondata = json.load(json_file)

            data_file = open(output, 'w', newline='', encoding='utf-8-sig')
            csv_writer = csv.writer(data_file)

            count = 0
            for data in jsondata:
                if count == 0:
                    header = data.keys()
                    csv_writer.writerow(header)
                    count += 1
                csv_writer.writerow(data.values())

            data_file.close()

            print(f"Converted file saved to {output}")

        except (ValueError, IndexError):
            print("Invalid choice. Please enter a valid number.")
    else:
        print("No JSON files are available in the current directory.")

def reverser():
    csv_files = [file for file in os.listdir() if file.endswith('.csv')]

    if csv_files:
        print("CSV file(s) available. Select which one to convert:")
        
        for index, file_name in enumerate(csv_files, start=1):
            print(f"{index}. {file_name}")

        choice = input(f"Enter your choice (1 to {len(csv_files)}): ")
        choice_index=int(choice)-1
        selected_file=csv_files[choice_index]
        print(f"File: {selected_file} is selected!")

        ask = input("Enter another file name as output (Y/n)? ")
        if  ask.lower() == 'y':
                given = input("Give a name to the output file: ")
                output=f'{given}.json'
        else:
                output=f"{selected_file[:len(selected_file)-4]}.json"
        
        try:
            data = []
            with open(selected_file, mode='r', encoding='utf-8') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                for row in csv_reader:
                    data.append(dict(row))

            with open(output, mode='w', encoding='utf-8') as json_file:
                json.dump(data, json_file, ensure_ascii=False, indent=4)

            print(f"Converted file saved to {output}")

        except (ValueError, IndexError):
            print("Invalid choice. Please enter a valid number.")
    else:
        print("No CSV files are available in the current directory.")

def detector():
    csv_files = [file for file in os.listdir() if file.endswith('.csv')]

    if csv_files:
        print("CSV file(s) available. Select the 1st csv file:")
        
        for index, file_name in enumerate(csv_files, start=1):
            print(f"{index}. {file_name}")

        choice = input(f"Enter your choice (1 to {len(csv_files)}): ")
        choice_index=int(choice)-1
        input1=csv_files[choice_index]

        print("CSV file(s) available. Select the 2nd csv file:")
        
        for index, file_name in enumerate(csv_files, start=1):
            print(f"{index}. {file_name}")

        choice = input(f"Enter your choice (1 to {len(csv_files)}): ")
        choice_index=int(choice)-1
        input2=csv_files[choice_index]

        output = input("Give a name to the output file: ")
        
        try:
            file1 = pd.read_csv(input1)
            file2 = pd.read_csv(input2)

            columns_to_merge = list(file1.columns)
            merged = pd.merge(file1, file2, on=columns_to_merge, how='left', indicator=True)

            merged['Coexist'] = merged['_merge'].apply(lambda x: 1 if x == 'both' else '')
            merged = merged.drop(columns=['_merge'])
            merged.to_csv(f'{output}.csv', index=False)

            print(f"Results of coexist-record detection saved to {output}.csv")

        except (ValueError, IndexError):
            print("Invalid choice. Please enter a valid number.")
    else:
        print("No CSV files are available in the current directory.")

def jointer(output_file):
    output = f'{output_file}.csv'
    csv_files = [f for f in os.listdir() if f.endswith('.csv') and f != output]
    dataframes = []

    if csv_files:
        for file in csv_files:
            file_name = os.path.splitext(file)[0]
            df = pd.read_csv(file)
            df['File'] = file_name
            dataframes.append(df)

        combined_df = pd.concat(dataframes, ignore_index=True)
        combined_df = combined_df[['File'] + [col for col in combined_df.columns if col != 'File']]
        combined_df.to_csv(output, index=False)

        print(f"Combined CSV file saved as {output}")
    else:
        print(f"No CSV files are available in the current directory; the output file {output} was dropped.")

def spliter():
    csv_files = [file for file in os.listdir() if file.endswith('.csv')]

    if csv_files:
        print("CSV file(s) available. Select which one to split:")
        
        for index, file_name in enumerate(csv_files, start=1):
            print(f"{index}. {file_name}")

        choice = input(f"Enter your choice (1 to {len(csv_files)}): ")
        
        try:
            choice_index=int(choice)-1
            selected_file=csv_files[choice_index]
            print(f"File: {selected_file} is selected!")
            
            df = pd.read_csv(selected_file)
            reference_field = df.columns[0]
            groups = df.groupby(reference_field)

            for file_id, group in groups:
                group = group.drop(columns=[reference_field]) 
                output_file = f'{file_id}.csv'
                group.to_csv(output_file, index=False)

            print("CSV files have been split and saved successfully.")

        except (ValueError, IndexError):
            print("Invalid choice. Please enter a valid number.")
    else:
        print("No CSV files are available in the current directory.")

def xplit():
    excel_files = [file for file in os.listdir() if file.endswith('.xls') or file.endswith('.xlsx')]

    if excel_files:
        print("Excel file(s) available. Select which one to split:")
        
        for index, file_name in enumerate(excel_files, start=1):
            print(f"{index}. {file_name}")

        choice = input(f"Enter your choice (1 to {len(excel_files)}): ")
        
        try:
            choice_index=int(choice)-1
            selected_file=excel_files[choice_index]
            print(f"File: {selected_file} is selected!")
            
            df = pd.read_excel(selected_file)
            reference_field = df.columns[0]
            groups = df.groupby(reference_field)

            for file_id, group in groups:
                group = group.drop(columns=[reference_field]) 
                output_file = f'{file_id}.xlsx'
                group.to_excel(output_file, index=False)

            print("Excel files have been split and saved successfully.")

        except (ValueError, IndexError):
            print("Invalid choice. Please enter a valid number.")
    else:
        print("No excel files are available in the current directory.")

def joint():
    excel_files = [f for f in os.listdir() if f.endswith('.xls') or f.endswith('.xlsx') and f != output]
    dataframes = []

    if excel_files:
        for file in excel_files:
            file_name = os.path.splitext(file)[0]
            df = pd.read_excel(file)
            df['File'] = file_name
            dataframes.append(df)

        output_file = input("Give a name to the output file: ")
        output = f'{output_file}.xlsx'

        combined_df = pd.concat(dataframes, ignore_index=True)
        combined_df = combined_df[['File'] + [col for col in combined_df.columns if col != 'File']]
        combined_df.to_excel(output, index=False)

        print(f"Combined excel file saved as {output}")
    else:
        print(f"No excel files are available in the current directory.")

def __init__():
    parser = argparse.ArgumentParser(description="rjj will execute different functions based on command-line arguments")
    parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + __version__)

    subparsers = parser.add_subparsers(title="subcommands", dest="subcommand", help="choose a subcommand:")
    subparsers.add_parser('c', help='convert json to csv')
    subparsers.add_parser('r', help='convert csv to json')
    subparsers.add_parser('k', help='keyword filter for csv data')
    subparsers.add_parser('d', help='detect co-existing record(s)')
    subparsers.add_parser('j', help='joint all csv(s) together')
    subparsers.add_parser('s', help='split csv to piece(s)')
    subparsers.add_parser('t', help='joint all excel(s) into one')
    subparsers.add_parser('x', help='split excel to piece(s)')

    args = parser.parse_args()
    if args.subcommand == 'j':
        output_file = input("Give a name to the output file: ")
        jointer(output_file)
    elif args.subcommand == 's':
        spliter()
    elif args.subcommand == 'k':
        filter()
    elif args.subcommand == 'd':
        detector()
    elif args.subcommand == 'c':
        convertor()
    elif args.subcommand == 'r':
        reverser()
    elif args.subcommand == 'x':
        xplit()
    elif args.subcommand == 't':
        joint()