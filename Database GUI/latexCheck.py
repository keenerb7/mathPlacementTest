import re


def check_latex_validity(latex_snippet):
    # Step 1: Ignore escaped \$ for counting unescaped math delimiters
    snippet_no_escaped_dollars = re.sub(r'\\\$', '', latex_snippet)

    # Step 2: Check unmatched math mode delimiters
    if len(re.findall(r'(?<!\\)\$', snippet_no_escaped_dollars)) % 2 != 0:
        return False, "Unmatched $ in inline math mode. If you want a $, use $\\$$"
    if latex_snippet.count(r'\[') != latex_snippet.count(r'\]'):
        return False, "Unmatched \\[ or \\] in display math mode."
    if latex_snippet.count(r'\(') != latex_snippet.count(r'\)'):
        return False, "Unmatched \\( or \\) in inline math mode."
    if latex_snippet.count('$$') % 2 != 0:
        return False, "Unmatched $$ in display math mode."

    # Step 3: Replace full math environments with placeholders
    placeholder = "<<MATH>>"
    latex = re.sub(r'\$\$.*?\$\$', placeholder, latex_snippet, flags=re.DOTALL)
    latex = re.sub(r'\\\[.*?\\\]', placeholder, latex, flags=re.DOTALL)
    latex = re.sub(r'\\\(.*?\\\)', placeholder, latex, flags=re.DOTALL)

    # Step 4: Handle valid inline math $...$
    inline_math_regex = r'(?<!\\)\$(.+?)(?<!\\)\$'
    inline_math_matches = list(re.finditer(inline_math_regex, latex_snippet))
    for match in inline_math_matches:
        math_content = match.group(1)
        if not math_content.strip():
            return False, "Empty inline math expression."
    latex = re.sub(inline_math_regex, placeholder, latex)

    # Step 5: Handle literal dollar sign uses like "$5 for a donut"
    latex = re.sub(r'(?<!\\)\$(\d+(\.\d+)?|\w+)', r"<<DOLLAR>>\1", latex)

    # Step 6: Check for balanced curly braces
    if latex_snippet.count('{') != latex_snippet.count('}'):
        return False, "Unbalanced curly braces."

    # Step 7: Optional - Check for LaTeX command typos
    known_commands = {'frac', 'sqrt', 'sum', 'int', 'lim', 'log', 'sin', 'cos', 'tan', 'left', 'right'}
    for cmd in re.findall(r'\\([a-zA-Z]+)', latex_snippet):
        if cmd not in known_commands and cmd not in ('[', ']', '(', ')'):
            return False, f"Unknown or unsupported LaTeX command: \\{cmd}"

    return True, ""
