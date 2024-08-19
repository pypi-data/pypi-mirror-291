import os, glob
import pandas as pd

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