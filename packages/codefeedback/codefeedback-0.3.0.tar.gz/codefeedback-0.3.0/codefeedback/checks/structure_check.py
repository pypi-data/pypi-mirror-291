import ast

from codefeedback.mevars.configs import get_config


def extract_definitions(node, parent=None):
    definitions = []
    for child in ast.iter_child_nodes(node):

        if isinstance(child, ast.FunctionDef):
            if parent is None:
                definitions.append((child.name, "2"))
            else:
                definitions.append((child.name, parent))
            definitions.extend(extract_definitions(child, parent=child.name))
        elif isinstance(child, ast.ClassDef):
            if parent is None:
                definitions.append((child.name, "2"))
            else:
                definitions.append((child.name, parent))
            definitions.extend(extract_definitions(child, parent=child.name))
    return definitions


def split_structure(code_str):
    tree = ast.parse(code_str)
    hierarchy = extract_definitions(tree)
    # guarantee the root of the tree is unique
    hierarchy.append(("2", "1"))
    return hierarchy


def check_structure(response, answer):
    return set(split_structure(response)) == set(split_structure(answer))


def check_loops(response, answer):
    class LoopDetector(ast.NodeVisitor):
        def __init__(self):
            self.has_for = False
            self.has_while = False

        def visit_For(self, node):
            self.has_for = True
            self.generic_visit(node)

        def visit_While(self, node):
            self.has_while = True
            self.generic_visit(node)

    tree = ast.parse(response)
    detector = LoopDetector()
    detector.visit(tree)
    has_res_for, has_res_while = detector.has_for, detector.has_while
    tree = ast.parse(answer)
    detector = LoopDetector()
    detector.visit(tree)
    has_ans_for, has_ans_while = detector.has_for, detector.has_while
    CONFIG = get_config()
    if CONFIG['check_for'] and has_ans_for:
        if not has_res_for:
            if has_res_while:
                return False, "We detect the while loop, but the codes require the for loop only"
            else:
                return False, "For loop statement is lacking"
    elif CONFIG['check_while'] and has_ans_while:
        if not has_res_while:
            if has_res_for:
                return False, "We detect the for loop, but the codes require the while loop only"
            else:
                return False, "while loop statement is lacking"
    elif CONFIG['check_loop']:
        if has_ans_for or has_ans_while:
            if not (has_res_for or has_res_while):
                return False, "The answer has loop, but your response seems not have the correct loop"
    else:
        return True, ""
    return True, "NotDefined"
