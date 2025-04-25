import subprocess

# Correct way to check pip version
subprocess.run(["pip", "--version"])

# List all the Packages for the project
libraries = ["setuptools", "text2qti", "antlr4-python3-runtime==4.11", "sympy", "pyinstaller", "Pillow"]

for row in libraries:
    # Runs the text2qti form the command line to create a QTI file and solutions PDF
    subprocess.run(["pip", "install", row])


