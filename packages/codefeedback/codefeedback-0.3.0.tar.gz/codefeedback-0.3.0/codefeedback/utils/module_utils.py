import ast
import types


def get_specific_module_alias(code_str, module_name):
    tree = ast.parse(code_str)
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name == module_name and alias.asname:
                    return alias.asname
        elif isinstance(node, ast.ImportFrom):
            if node.module == module_name:
                for alias in node.names:
                    if alias.asname:
                        return alias.asname
    return None


def extract_modules(var_dict):
    modules = []
    for var_name, module_part in var_dict.items():
        if isinstance(module_part, types.ModuleType):
            modules.append((var_name, module_part.__name__))
    for var_name, _ in modules:
        del var_dict[var_name]
    return modules, var_dict
