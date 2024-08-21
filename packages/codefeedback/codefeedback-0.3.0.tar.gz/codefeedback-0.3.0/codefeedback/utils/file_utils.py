import ast

import pandas as pd


def get_variables_from_pyscript(file_path):
    with open(file_path, 'r') as file:
        script_content = file.read()
    variables = {}
    exec(script_content, globals(), variables)
    return variables


def get_variables_from_csv(file_path):
    df = pd.read_csv(file_path, header=None)
    result = {}
    for index, row in df.iterrows():
        key = row[0].strip()
        values = ast.literal_eval(row[1])
        category = row[2].strip()

        result[key] = (values, category)

    return result
