import re
from sympy.parsing.latex import parse_latex
import subprocess
import tempfile
import os


def check_latex_validity(latex_snippet):
    tex_template = r"""
    \documentclass{article}
    \usepackage{amsmath}
    \usepackage{amssymb}
    \begin{document}
    %s
    \end{document}
        """ % latex_snippet

    with tempfile.TemporaryDirectory() as tmpdir:
        tex_file = os.path.join(tmpdir, "temp.tex")
        with open(tex_file, "w") as f:
            f.write(tex_template)

        try:
            subprocess.run(
                ["pdflatex", "-interaction=nonstopmode", "temp.tex"],
                cwd=tmpdir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True
            )
            return True, ""
        except subprocess.CalledProcessError as e:
            error_output = e.stdout.decode('utf-8', errors='ignore')
            # Try to extract relevant error lines (optional, for clarity)
            lines = error_output.splitlines()
            error_lines = [line for line in lines if "!" in line or "l." in line]
            short_error = "\n".join(error_lines[:6])  # Limit number of lines
            return False, short_error or "Unknown LaTeX error"
