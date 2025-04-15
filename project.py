import re
from typing import List, Dict, Optional

class Output:
    def __init__(self, namespace: str, target_path: str):
        self.namespace = namespace
        self.target_path = target_path

class Predicate:
    def __init__(self, name: str, path: str):
        self.name = name
        self.path = path


class LimboProject:
    def __init__(self):
        self.name: Optional[str] = None
        self.version: Optional[str] = None
        self.minecraft_version: Optional[str] = None
        self.description: Optional[str] = None
        self.output: Optional[Output] = None
        self.author: Optional[str] = None
        self.pack_icon: Optional[str] = None
        self.tags: Dict[str, List[str]] = {}
        self.predicates: List[Predicate] = []

    def __repr__(self):
        return f"<LimboProject name={self.name} version={self.version}>"


def from_file(filename: str) -> LimboProject:
    project = LimboProject()
    current_section = None
    current_subsection = None
    current_predicate: Optional[Dict[str, str]] = None

    with open(filename, "r", encoding="utf-8") as file:
        lines = file.readlines()

    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue  # Skip empty and comment lines

        # Section like "output:" or "tags:"
        if re.match(r"^[\w_]+:$", line):
            current_section = line[:-1]
            current_subsection = None
            continue

        # Subsection like "blocks:"
        if re.match(r"^[\w_]+:\s*$", line):
            current_subsection = line[:-1]
            if current_section == "tags":
                project.tags[current_subsection] = []
            continue

        # List item (tags or predicates)
        if line.startswith("- "):
            item = line[2:].strip().strip("\"")
            if current_section == "tags" and current_subsection:
                project.tags[current_subsection].append(item)
            elif current_section == "predicates":
                # New predicate item starting
                if current_predicate:
                    # Save the previous one if complete
                    if "name" in current_predicate and "path" in current_predicate:
                        project.predicates.append(Predicate(**current_predicate))
                current_predicate = {}

        # Key-value pair
        if re.match(r"^[\w_]+:\s*\".*\"$", line):
            key, val = line.split(":", 1)
            key = key.strip()
            val = val.strip().strip("\"")

            if current_section == "output":
                if not project.output:
                    project.output = Output(namespace="", target_path="")
                if hasattr(project.output, key):
                    setattr(project.output, key, val)
            elif current_section == "predicates":
                if current_predicate is None:
                    current_predicate = {}
                current_predicate[key] = val
            elif hasattr(project, key):
                setattr(project, key, val)

        # Handle inline predicate
        if current_section == "predicates" and "," in line:
            parts = line.split(",")
            predicate_data = {}
            for part in parts:
                key, val = part.split(":", 1)
                predicate_data[key.strip()] = val.strip().strip("\"")
            if "name" in predicate_data and "path" in predicate_data:
                project.predicates.append(Predicate(**predicate_data))

    # Add last parsed predicate if it's complete
    if current_predicate and "name" in current_predicate and "path" in current_predicate:
        project.predicates.append(Predicate(**current_predicate))

    return project
