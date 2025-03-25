import subprocess

# Correct way to check pip version
subprocess.run(["pip", "--version"])

# List all the Packages for the project
libraries = ["mysql", "setuptools", "text2qti"]

for row in libraries:
    # Runs the text2qti form the command line to create a QTI file and solutions PDF
    subprocess.run(["pip", "install", row])


