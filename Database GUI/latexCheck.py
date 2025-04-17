import re
from sympy.parsing.latex import parse_latex


def check_latex_validity(latex_string):
    """
    Checks if the LaTeX expression is valid in terms of both syntax and mathematics.
    """
    # Check for balanced delimiters (e.g., $...$, \(...\), etc.)
    delimiters = [r'\$', r'\$\$', r'\\\(', r'\\\[', r'\\begin\{.*?\\end\{.*?\}']
    combined_regex = '|'.join(delimiters)
    matches = re.findall(combined_regex, latex_string)
    if len(matches) % 2 != 0:
        return False, "Unbalanced LaTeX delimiters detected."

    latex_string = latex_string.strip('$$')

    # Check for unbalanced parentheses
    if latex_string.count('(') != latex_string.count(')'):
        return False, "Unbalanced parentheses detected."

    if latex_string.count('{') != latex_string.count('}'):
        return False, "Unbalanced curly brackets detected."

    if latex_string.count('[') != latex_string.count(']'):
        return False, "Unbalanced brackets detected."

    # Check for missing operands after operators (e.g., '2x + = 5')
    if re.search(r'\s*\+\s*=|\s*-\s*=|\s*\*\s*=|\s*\/\s*=', latex_string):
        return False, "Missing operand after operator."

    # Check for incorrect number of '=' signs in equations (like '2x + = 5')
    if '=' in latex_string and latex_string.count('=') != 1:
        return False, "Incorrect number of '=' signs in equation."

    try:
        # Attempt to parse the LaTeX string into a SymPy expression
        expr = parse_latex(latex_string)
        return True, expr  # Return True if valid, along with the parsed expression
    except Exception as e:
        return False, f"Error: {str(e)}"  # Return error message if parsing fails


# Example usage
# latex_string = r'\frac{1}{2 + (3x'
# latex_string = r'$'
# valid, result = check_latex_validity(latex_string)
#
# if valid:
#     print("LaTeX is valid.")
#     print(f"Parsed expression: {result}")
# else:
#     print(f"Error: {result}")
#     print("LaTeX is not valid.")
