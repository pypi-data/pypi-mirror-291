import ast
import numpy as np
from codefeedback.checks.global_variable_check import VariableVisitor


global_res_variables = {}
global_res_methods = {}
global_ans_variables = {}
global_ans_methods = {}


def set_global_var_dict(res_var_dict: dict, ans_var_dict):
    # TODO: different types of value should be formatted before save
    for key, value in res_var_dict.items():
        if isinstance(value, np.ndarray):
            set_global_variables(key, f"np.array({value.tolist()})", 'Response')
        elif isinstance(value, str):
            set_global_variables(key, f"'{value}'", 'Response')
        else:
            set_global_variables(key, value, 'Response')
    for key, value in ans_var_dict.items():
        if isinstance(value, np.ndarray):
            set_global_variables(key, f"np.array({value.tolist()})", 'Answer')
        elif isinstance(value, str):
            set_global_variables(key, f"'{value}'", 'Answer')
        else:
            set_global_variables(key, value, 'Answer')


def set_global_variables(variable_name, value, side):
    if side == 'Response':
        global_res_variables[variable_name] = value
    elif side == 'Answer':
        global_ans_variables[variable_name] = value


def set_global_method_dict(res_method_dict, ans_method_dict):
    for key, value in res_method_dict.items():
        set_global_methods(key, value, 'Response')
    for key, value in ans_method_dict.items():
        set_global_methods(key, value, 'Answer')


def get_global_variables(code_str, side):
    tree = ast.parse(code_str)
    visitor = VariableVisitor()
    visitor.visit(tree)
    variable_names = visitor.variables


    global_var_dict = {}
    global_method_dict = {}
    if side == 'Response':
        exist_var_set = global_res_variables.keys()
        exist_method_set = global_res_methods.keys()
        for var in variable_names:
            if var in exist_var_set:
                global_var_dict[var] = global_res_variables[var]
            if var in exist_method_set:
                global_method_dict[var] = global_res_methods[var]
        return global_var_dict, global_method_dict
    elif side == 'Answer':
        exist_var_set = global_ans_variables.keys()
        exist_method_set = global_ans_methods.keys()
        for var in variable_names:
            if var in exist_var_set:
                global_var_dict[var] = global_ans_variables[var]
            if var in exist_method_set:
                global_method_dict[var] = global_ans_methods[var]
        return global_var_dict, global_method_dict
    else:
        raise NameError("The type is wrong")

def set_global_methods(method_name, body, side):
    if side == 'Response':
        global_res_methods[method_name] = body
    elif side == 'Answer':
        global_ans_methods[method_name] = body
    else:
        raise NameError("The side is wrong")


if __name__ == '__main__':
    code_str = """
def f():
    pass
    
def g():
    pass
    
def h():
    pass
    

"""
