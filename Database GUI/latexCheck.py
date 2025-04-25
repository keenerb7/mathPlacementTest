import re
from sympy.parsing.latex import parse_latex
import subprocess
import tempfile
import os


def check_latex_validity(latex_snippet):
    # Template for a minimal LaTeX document
    tex_template = r"""
    \documentclass{article}
    \usepackage{amsmath}
    \usepackage{amssymb}
    \begin{document}
    %s
    \end{document}
        """ % latex_snippet

    # Create a temporary directory to store the LaTeX file and compilation artifacts
    with tempfile.TemporaryDirectory() as tmpdir:
        # Path to the temporary LaTeX file
        tex_file = os.path.join(tmpdir, "temp.tex")

        # Write the LaTeX snippet into the temporary file
        with open(tex_file, "w") as f:
            f.write(tex_template)

        try:
            # Compile the LaTeX file using pdflatex
            subprocess.run(
                ["pdflatex", "-interaction=nonstopmode", "temp.tex"],
                cwd=tmpdir, # Set the working directory to the temporary directory
                stdout=subprocess.PIPE, # Capture standard output
                stderr=subprocess.PIPE,  # Capture standard error
                check=True  # Raise an exception if the command fails
            )
            return True, ""
        
        except subprocess.CalledProcessError as e:
            error_output = e.stdout.decode('utf-8', errors='ignore')
            # Try to extract relevant error lines (optional, for clarity)
            lines = error_output.splitlines()
            error_lines = [line for line in lines if "!" in line or "l." in line]
            short_error = "\n".join(error_lines[:6])  # Limit number of lines
            
            return False, short_error or "Unknown LaTeX error"
