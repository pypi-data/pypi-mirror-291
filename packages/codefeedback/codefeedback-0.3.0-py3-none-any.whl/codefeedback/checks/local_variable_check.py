"""
The script is used only the Teacher forgets to input the check_list, or lacking of global variables
"""
import sys
import itertools

from codefeedback.utils.module_utils import extract_modules
from codefeedback.checks.global_variable_check import variable_content, check_global_variable_content
from codefeedback.format.general_format import local_missing_modules_and_variables_format
from codefeedback.utils.param_utils import param_generator, guess_param_type
from codefeedback.checks.same_variable_content_check import check_same_content_with_different_variable
from codefeedback.utils.method_utils import extract_params_and_body



# code = """
# def example_function(x):
#     return x ** 2 + 1
# """
# print(extract_params_and_body(code))

def check_local_variable_content(response, answer, check_list: list):
    """
    TODO The checklist will be randomly generated when the checklist is empty (it's teachers' input)
    otherwise, the local variable will be checked

    """
    answer_method_params_and_body_list = extract_params_and_body(answer)
    response_method_params_and_body_list = extract_params_and_body(response)

    # only the same function name will be checked
    method_names = answer_method_params_and_body_list.keys() & response_method_params_and_body_list.keys()

    remaining_check_list = check_list
    feedback = ""

    # it still needs to check the global variable content at first
    response_var_dict = variable_content(response)
    answer_var_dict = variable_content(answer)

    for method_name in method_names:
        # add sys to the dict, it changes locally but not globally
        response_var_dict['sys'] = sys
        answer_var_dict['sys'] = sys
        response_arg_list, response_body = response_method_params_and_body_list[method_name]
        answer_arg_list, answer_body = answer_method_params_and_body_list[method_name]

        # add all variables globally to the local variables
        response_modules, response_var_dict = extract_modules(response_var_dict)
        answer_modules, answer_var_dict = extract_modules(answer_var_dict)

        global_response_variable_content = local_missing_modules_and_variables_format(
            response_modules, response_var_dict)
        global_answer_variable_content = local_missing_modules_and_variables_format(
            answer_modules, answer_var_dict)

        # If the input parameter is not given, we need to generate some of them
        if 0 < len(answer_arg_list) == len(response_arg_list):

            # get the params dict with name and possible types
            answer_params_dict = {param: guess_param_type(param, answer_body) for param in answer_arg_list}
            response_params_dict = {param: guess_param_type(param, response_body) for param in response_arg_list}
            response_body, response_params_dict = check_same_content_with_different_variable(
                response_body, response_params_dict, answer_params_dict, [], mode='param')

            if response_params_dict != answer_params_dict:
                if method_name in remaining_check_list:
                    return False, f"The arguments of the method {method_name} are not correct: check inputs and types of the params"
                return True, "NotDefined"
            param_result_dict = param_generator(answer_arg_list, answer_body)
            # There are tiny probability that the generated answer is false positive
            correct_count = 0
            false_count = 0
            not_defined_count = 0
            is_next = False

            for _ in range(5):

                for choice in permutation(param_result_dict):
                    if is_next:
                        break
                    response_params_msg = "\n".join(f"{key}={value}" for key, value in choice.items())
                    answer_params_msg = "\n".join(f"{key}={value}" for key, value in choice.items())
                    response_body = f"{global_response_variable_content}\n{response_params_msg}\n{response_body}"
                    answer_body = f"{global_answer_variable_content}\n{answer_params_msg}\n{answer_body}"
                    remaining_check_list.append("TMP")
                    is_correct, feedback, remaining_check_list, response_body = \
                        check_global_variable_content(response_body, answer_body, remaining_check_list)

                    response_var_dict = variable_content(response_body)
                    answer_var_dict = variable_content(answer_body)
                    response_var_dict = {k: v for k, v in response_var_dict.items() if
                                         k not in list(response_params_dict.keys()) and k != "TMP"}
                    answer_var_dict = {k: v for k, v in answer_var_dict.items() if
                                       k not in answer_arg_list and k != "TMP"}

                    # only correct when there is no execution err (WellDefined), no remaining check list, and correct
                    if is_correct and feedback != "NotDefined":
                        if correct_count > 1:
                            if method_name in remaining_check_list:
                                remaining_check_list.remove(method_name)
                            if len(remaining_check_list) == 0:
                                return True, ""
                            else:
                                is_next = True
                        correct_count += 1
                    elif not is_correct and feedback != "NameError":
                        false_count += 1
                    elif feedback == "NotDefined":
                        not_defined_count += 1

                    if false_count > 1:
                        if feedback != "NameError" and method_name in remaining_check_list:
                            return False, f"The method {method_name} is not correct: {feedback}"
                    if not_defined_count > 1:
                        return True, "NotDefined"


        else:
            response_body = f"{global_response_variable_content}\n{response_body}"
            answer_body = f"{global_answer_variable_content}\n{answer_body}"

            remaining_check_list.append("TMP")

            response_var_dict.update(variable_content(response_body))
            answer_var_dict.update(variable_content(answer_body))
            response_var_dict.pop('TMP', 'NA')
            answer_var_dict.pop('TMP', 'NA')

            is_correct, feedback, remaining_check_list, response_body = check_global_variable_content(response_body,
                                                                                                      answer_body,
                                                                                                      remaining_check_list)
            # response might have different argument input and execution error
            if feedback == "NameError":
                return False, f"The arguments of the method {method_name} are not correct: check inputs and types of the params"
            if feedback == "NotDefined":
                return True, feedback
            if not is_correct:
                return False, feedback
            else:
                if method_name in remaining_check_list:
                    remaining_check_list.remove(method_name)

    if len(remaining_check_list) == 0:
        return (True, "") if feedback != "NotDefined" else (True, feedback)
    else:
        if len(remaining_check_list) == 1:
            return False, f"The variable of {remaining_check_list[0]} is not defined"
        else:
            return False, f"""The variable of '{"', '".join(remaining_check_list)}' is not defined"""





def permutation(param_dict):
    filtered_params = [p for p in param_dict.values() if p]
    empty_params_dict = {k: [] for k, v in param_dict.items() if not v}

    permutations = itertools.product(*filtered_params)
    keys = [k for k, v in param_dict.items() if v]
    perm_dict_list = [{**dict(zip(keys, permutation)), **empty_params_dict} for permutation in permutations]
    return perm_dict_list
