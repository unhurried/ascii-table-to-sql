import re
import argparse

# Extract table name from a SQL statement.
def extract_table_name(line):
    result = re.search('from ([a-zA-Z0-9_]+)', line);
    if result is None:
        return None
    else:
        return result.group(1)

# Extract a list of column names from a row.
def extract_column_list(line):
    if not line.startswith('|'):
        return None
    else:
        list = line.split('|')
        list = list[1:-1]
        list = map(str.strip, list)
        return ", ".join(list)

# Convert a data line to a INSERT statement.
def convert_to_sql(line):
    if not line.startswith('|'):
        return None
    else:
        list = line.split('|')
        list = list[1:-1]
        list = map(str.strip, list)
        list = map(convert_value, list)
        values = ', '.join(list)
        sql = 'INSERT INTO %s (%s) VALUES (%s);' % (table_name, column_list, values)
        return sql

# Convert a value to fit in a INSERT statement.
def convert_value(s):
    if len(s) == 0:
        return "''"
    elif s == 'NULL':
        return 'NULL'
    else:
        return "'%s'" % s

# Open input and output files in command line parameters.
parser = argparse.ArgumentParser()
parser.add_argument("input", help="input file", type=str)
parser.add_argument("output", help="output file", type=str)
args = parser.parse_args()

file_in = open(args.input)
file_out = open(args.output, 'w')

# Extract table name and column list, and generate INSERT statements.
table_name = None
column_list = None
for line in file_in:
    if table_name is None:
        table_name = extract_table_name(line)
    elif column_list is None:
        column_list = extract_column_list(line)
    else:
        sql = convert_to_sql(line)
        if sql is not None:
            file_out.write(sql + "\n")

file_in.close()
file_out.close()
