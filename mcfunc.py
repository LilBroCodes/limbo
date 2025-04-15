from typing import List, Optional
import re

class Function:
    def __init__(self, name: str, params: Optional[List[str]], commands: List[str]):
        self.name = name
        self.params = params or []
        self.commands = commands

    def __repr__(self):
        return f"Function(name={self.name!r}, params={self.params!r}, commands={self.commands!r})"

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
        param_str = match.group(2).strip()
        body = match.group(3).strip()

        # Extract parameters (comma-separated)
        params = [p.strip() for p in param_str.split(",") if p.strip()] if param_str else []

        # Split the body into individual non-empty lines, stripping each
        commands = [line.strip() for line in body.splitlines() if line.strip()]
        functions.append(Function(name, params, commands))

    return functions
