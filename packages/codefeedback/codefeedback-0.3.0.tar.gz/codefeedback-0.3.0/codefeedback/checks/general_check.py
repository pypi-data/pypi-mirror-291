from codefeedback.mevars.globals import get_global_variables
from codefeedback.utils.method_utils import extract_method_names
# try:
from codefeedback.format.general_format import message_format, variable_format
# except ImportError:
#     from format import message_format, variable_format
import subprocess
import ast

def check_indents(code_str: str) -> bool:
    """
    This function checks the indentation correctness of the given Python code.
    Notice that indentation depends on student preference: (2 spaces or 4 spaces are acceptable)
    """
    formatted_code_lines = code_str.split('\n')
    indent_levels = []
    for line in formatted_code_lines:
        indent_level = len(line) - len(line.lstrip(' '))
        indent_levels.append(indent_level)

    # first line should not have any indents
    if indent_levels[0] != 0:
        return False

    # find the correctness indent: 2 or 4 spaces
    indent_difference = 0
    for indent_level in indent_levels:
        if indent_level > 0:
            indent_difference = indent_level
            break

    # zero indent only occur when they are no any syntax like (if, for)
    if indent_difference == 0:
        return all(indent_level == 0 for indent_level in indent_levels)

    # correct indents
    if indent_difference != 2 and indent_difference != 4:
        return False

    return all(indent_level % indent_difference == 0 for indent_level in indent_levels)


def check(code_string):
    if not check_indents(code_string):
        return f"Indent error, the indent should only be multiple of 2 or 4"
    # import necessary modules dynamically (not in use)
    # module_import(formatted_code_lines)
    is_syntax_correct, msg = check_syntax(code_string)
    if not is_syntax_correct:
        return f"Error occurs, please check the details below: \n{message_format(msg)}"

    return "General check passed!"


def check_syntax(code_string) -> (bool, str):
    try:
        result = subprocess.run(['python', '-c', code_string], capture_output=True)
        if result.returncode != 0:
            try:
                stderr = result.stderr.decode('utf-8')
            except UnicodeDecodeError:
                stderr = result.stderr.decode('utf-8', errors='replace')
            return False, stderr
        else:
            return True, result.stdout.decode('utf-8')
    except Exception:
        return False, "Exception occurs during execution"


def add_missing_global_variables(code_str, side):
    global_var_dict, global_method_dict = get_global_variables(code_str, side)
    var_str = variable_format(global_var_dict)

    exist_methods = extract_method_names(ast.parse(code_str))
    method_str = "\n".join(body for name, body in global_method_dict.items() if name not in exist_methods)
    return f"{var_str}\n{method_str}"

