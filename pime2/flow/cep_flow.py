import logging
import re

expression_regex = "([0-9<>=!()+\-*/. ]|(and)|(or))*"
variable_regex = "^[uvwxyz]*$"

# TODO: maybe only the keyword sensor_result_x with x = number of the result
keywords = ["result", "gpio_1_result", "gpio_2_result"]

def cep_executer(expression, variables, payload) :
    """
    Checks if the cep result is True or False
    """
    final_expression = cep_validator(expression=expression, variables=variables, payload=payload)
    if(final_expression):
        try: 
            return eval(final_expression)
        except SyntaxError as ex:
            logging.error("Invalid CEP expression!", ex)
    return False
    


def cep_validator(expression, variables, payload):
    """
    Makes sure that eval evaluates only allowed expressions
    """
    
    # check for correct expression
    try:
        # substitute variables
        expression = substitute_variables(expression, variables, payload)
        # expression = expression.replace(" ", "")
        if re.fullmatch(expression_regex, expression):
            return expression
        else:
            raise ValueError("Invalid CEP expression!")
    except (ValueError, SyntaxError):
        #logging.info("Invalid CEP expression!: %s", expression)
        return False

def substitute_variables(expression, variables, payload):
    for key, value in variables.items():
        if (is_keyword(value)):
            value = payload[value]

        elif (not is_allowed_variable(key)):
            raise ValueError("Invalid CEP variable!")

        expression = re.sub(key, str(value), expression)
    return expression

def is_keyword(value):
    return value in keywords

def is_allowed_variable(variable):
    return re.fullmatch(variable_regex, variable)





