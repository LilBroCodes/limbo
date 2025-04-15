from typing import List, Optional
import re

from util import Function

def generate(file: str) -> List[Function]:
    # Match 'fun function_name(param1, param2) { ... }' with optional whitespace
    pattern = re.compile(
        r"fun\s+(\w+)\s*\(([^)]*)\)\s*{(.*?)}",
        re.DOTALL
    )

    functions = []

    with open(file, "r") as f:
        file_string = f.read()

    for match in pattern.finditer(file_string):
        name = match.group(1)
        body = match.group(3).strip()

        # Split the body into individual non-empty lines, stripping each
        commands = [line.strip() if not line.strip().endswith(";") else line.strip()[:-1] for line in body.splitlines() if line.strip()]
        functions.append(Function(name, commands))

    return functions
