import ast
import astor
from codefeedback.utils.method_utils import extract_method_attr
from codefeedback.utils.module_utils import get_specific_module_alias

COMMON_PLOT_METHODS = ["plot", "scatter", "bar", "hist", "show"]


def is_image_exist(code_str):
    method_attr_set = extract_method_attr(code_str)
    return any(name in COMMON_PLOT_METHODS for name in method_attr_set)


def hide_images(code_str, modules):
    """
    Delete all codes related to matplotlib.pyplot:
    TODO: there exist other plot methods like ax.plot(), which should be detected
    """
    alias = get_abbr(modules)

    class MatplotlibRemover(ast.NodeTransformer):
        def visit_Import(self, node):
            node.names = [n for n in node.names if not (n.name == 'matplotlib.pyplot')]
            return node if node.names else None

        def visit_Expr(self, node):
            if isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Attribute):
                if isinstance(node.value.func.value, ast.Name) and node.value.func.value.id == alias:
                    return None
            return node

        def visit_Assign(self, node):
            node.value = self.visit(node.value)
            return node if node.value is not None else None

        def visit_Call(self, node):
            if isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name):
                if node.func.value.id == alias:
                    return None
            return node

    remover = MatplotlibRemover()
    tree = ast.parse(code_str)
    cleaned_tree = remover.visit(tree)
    return astor.to_source(cleaned_tree)


def get_abbr(modules_str):
    module_name = "matplotlib.pyplot"
    alias = get_specific_module_alias(modules_str, module_name)
    if alias:
        return alias
    else:
        return module_name
