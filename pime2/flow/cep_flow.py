# pylint: disable=anomalous-backslash-in-string
# pylint: disable=eval-used
import logging
import re
import json

expression_regex = "([0-9<>=!()+\-*/. ]|(and)|(or)|(True)|(False))*"
variable_regex = "^[uvwxyz]{1}$"

# TODO: maybe only the keyword sensor_result_x with x = number of the result
keywords = ["result", "gpio_1_result", "gpio_2_result"]

def cep_executer(expression, variables, payload) :
    """
    Checks if the cep result is True or False
    """
    final_expression = cep_validator(expression=expression, variables=variables, payload=payload)
    if final_expression:
        try:
            return eval(final_expression)
        except Exception as ex:
            logging.error("Invalid CEP expression!: %s", ex)
    return False


def cep_validator(expression, variables, payload):
    """
    Makes sure that eval evaluates only allowed expressions
    """
    # check for correct expression
    try:
        # substitute variables
        expression = substitute_variables(expression, variables, payload)
        if not re.fullmatch(expression_regex, expression):
            raise ValueError("Invalid CEP expression!")
        return expression
    except (ValueError, SyntaxError):
        logging.debug("Invalid CEP expression!: %s", expression)
        return False

def substitute_variables(expression, variables, payload):
    """
    Substitutes the variables inside the expression
    """
    for key, value in variables.items():
        if is_keyword(value):
            value = json.loads(payload)[value]
        elif not is_allowed_variable(key):
            raise ValueError("Invalid CEP variable!")

        expression = re.sub(key, str(value), expression)

    expression = re.sub("true", "True", expression)
    expression = re.sub("false", "False", expression)

    return expression

def is_keyword(value):
    """
    Checks if the value is a keyword from the keyword list
    """
    return value in keywords

def is_allowed_variable(variable):
    """
    Checks if the variable is allowed
    """
    return re.fullmatch(variable_regex, variable)
