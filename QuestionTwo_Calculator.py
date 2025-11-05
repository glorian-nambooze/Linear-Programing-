# Nkumba University Basic Calculator
# This program helps students perform basic arithmetic and additional mathematical operations.
# Author: Gloria Nalubega Nambooze
# Date: 05-Nov-2025
# ---------------------------------------------

import math  

def calculator():
    """
    Interactive calculator for performing basic arithmetic operations (+, -, *, /, %),
    exponentiation (^), and square roots. The program continuously prompts for input
    until the user types 'exit'. Includes error handling for invalid input and division by zero.
    """
    
    print("\t\t\tWELCOME TO THE NKUMBA UNIVERSITY CALCULATOR!!!\n ")
    print("\t\t\tAvailable operations: +, -, *, /, %, ^ for power, or 'sqrt' for square root.\n")
    print("\t\t\tExample input: 10 * 5 or sqrt 81\n")
    print("\t\t\tType 'exit' to quit the calculator.\n")

    while True:
        # Prompt user for input
        user_input = input("\t\t\tEnter your calculation: ")

        # Exit condition
        if user_input.lower() == "exit":
            print("\t\t\tCalculator session ended. Goodbye!")
            break

        try:
            # Handle square root operation
            if "sqrt" in user_input:
                # Extract numeric value from input and compute square root
                num_str = user_input.replace("sqrt", "").strip()
                num = float(num_str)
                result = math.sqrt(num)

            # Handle exponentiation operation
            elif "^" in user_input:
                # Split input by '^' to separate base and exponent
                base_str, exp_str = user_input.split("^")
                result = float(base_str) ** float(exp_str)

            else:
                # Evaluate basic arithmetic expressions
                result = eval(user_input)

            # Display result
            print(f"\t\t\tResult: {result}\n")

        except ZeroDivisionError:
            # Catch division by zero attempts
            print("\t\t\tError: Division by zero is not allowed.\n")

        except ValueError:
            # Catch invalid numeric inputs
            print("\t\t\tError: Please enter a valid number.\n")

        except Exception as e:
            # Catch any other unexpected errors
            print(f"\t\t\tUnexpected error: {e}\n")

# Execute the calculator function
calculator()
