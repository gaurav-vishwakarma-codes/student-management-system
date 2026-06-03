# VALIDATED STRING INPUT
def get_valid_input(message,validation_function):

    while True:

        value = input(message).strip()

        if validation_function(value):

            return value