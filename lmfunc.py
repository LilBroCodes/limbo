import re
from typing import List
from mcfunc import Function

def generate(filename: str) -> List[Function]:
    functions = []
    file_string = ""
    with open(filename, "r") as file:
        file_string = file.read()
        
    pattern = re.compile(
        r"def\s+(\w+)\s*\(([^)]*)\)\s*{(.*?)}",
        re.DOTALL
    )
    
    for match in pattern.finditer(file_string):
        name = match.group(1)
        param_str = match.group(2).strip()
        body = match.group(3).strip()

        # Extract parameters (comma-separated)
        params = [p.strip() for p in param_str.split(",") if p.strip()] if param_str else []

        # Split the body into individual non-empty lines, stripping each
        commands = [line.strip() if not line.strip().endswith(";") else line.strip()[:-1] for line in body.splitlines() if line.strip()]
        functions.append(Function(name, params, commands))
    return functions