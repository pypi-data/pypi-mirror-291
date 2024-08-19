### rjj (read-joint-jet) [![Static Badge](https://img.shields.io/badge/ver-0.1.3-black?logo=github)](https://github.com/calcuis/rjj/releases)
rjj is a simple cmd-based data transforming/analysis tool 🛠⚙
#### install it via pip/pip3
```
pip install rjj
```
#### update rjj
```
pip install rjj --upgrade
```
#### check current version
```
rjj -v
```
#### read user manual
```
rjj -h
```
#### convertor
convert json to csv; select a json file in the current directory, choose to enter another file name (don't need the extension) for output or not (Y/n); if not, the converted csv will be saved with the same name as the json♻
```
rjj c
```
#### reversor
reverse csv back to json; select a csv file in the current directory, choose to enter another file name for output or not (Y/n); if not, the converted json file will be saved with the same name; 🌀support any data type, even emoji🐷
```
rjj r
```
#### filter
locate the input `Keyword` among all csv files in the current directory👁‍🗨 (and could opt to expand to its all sub-folder files; cool right?🔍); give your searching keyword first, apply to all sub-folder(s) or just the files in the current directory (Y/n), then give a name for the output file (if not, the output file will be named as output.csv); source file (location info) will be indicated in a newly created first column `Source_file`; the exact coordinate (x,y) will be given in the newly created second and third columns, named `Column_y` and `Row_x`; and the full record will be pasted behind for simplifying your auditing work📑
```
rjj k
```
#### detector
detect the co-existing record(s) between two csv files🔍; select two csv files to execute the detection process, then give a name for the output file; co-existing record(s) will be indicated in a newly created column `Coexist`
```
rjj d
```
### jointer and splitter
joint or split your data file(s)
#### jointer
joint all csv files in the current directory together; all file names will be stored in the first field of the newly created column `File`; when you execute the command you will be asked for assigning a name for the output file🖇
```
rjj j
```
#### splitter
split the selected csv file to different csv files and name it according to the value in the first field of that selected file📑
```
rjj s
```
#### xplit
split the selected excel (.xls or .xlsx) to pieces and name it according to the value in the first field of that selected excel
```
rjj x
```
#### joint
joint all excels (.xls and .xlsx) in the current directory together*; all file names will be stored in the first field of the newly created column `File`; when you execute the command you might be asked for assigning a name for the output file
```
rjj t
```
**differ from csv jointer, since both .xls and .xlsx is accepted, and the file extention will not be taken, it will be merged while two of them share the same file name (cannot be split by the command above); understand this condition, make good use of it!*