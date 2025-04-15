import json
import os.path
from util import Logging, MapType, Mapping, Mappings
logger = Logging.change_log_format("Build Maps")

def from_lmap(path: str, verbose: bool = False) -> Mappings:
    mappings = []
    current_owner = None
    in_block = False

    logger.info(f"Loading mapping file: {path}")

    with open(os.path.join(path), 'r', encoding='utf-8') as f:
        for lineno, raw_line in enumerate(f, start=1):
            line = raw_line.strip()
            if not line or line.startswith("#"):
                if verbose:
                    logger.debug(f"[Line {lineno}] Skipping empty/comment line.")
                continue

            # Detect block start
            if line.endswith("{"):
                owner_key = line[:-1].strip()
                try:
                    current_owner = MapType[owner_key]
                    in_block = True
                    logger.info(f"[Line {lineno}] Entered block for owner: {current_owner.name}")
                except KeyError:
                    logger.warning(f"[Line {lineno}] Unknown MapType '{owner_key}' — skipping block.")
                    current_owner = None
                    in_block = False
                continue

            # Detect block end
            if line == "}":
                if verbose:
                    logger.debug(f"[Line {lineno}] Closed block for owner: {current_owner.name if current_owner else 'None'}")
                in_block = False
                current_owner = None
                continue

            if in_block and current_owner:
                if line.startswith("METHOD"):
                    line = line[len("METHOD"):].strip()
                    if '|' not in line:
                        logger.warning(f"[Line {lineno}] Malformed METHOD line (missing '|'): {line}")
                        continue
                    subcommand, translatable = line.split('|', 1)
                    subcommand = subcommand.strip()
                    translatable = translatable.strip()
                    mapping = Mapping(current_owner, subcommand, translatable)
                    mappings.append(mapping)
                    logger.info(f"[Line {lineno}] Registered mapping '{subcommand}' for {current_owner.name}")
                    if verbose:
                        logger.debug(f"[Line {lineno}] Mapping object: owner={current_owner}, subcommand={subcommand}, translatable={translatable}")
                else:
                    if verbose:
                        logger.debug(f"[Line {lineno}] Ignored non-METHOD line inside block: {line}")

    logger.info(f"Finished loading {len(mappings)} mapping(s).")
    return Mappings(mappings)

def compile_mappings(mappings_folder: str):
    overrides = {
        "1.20.2": "1.20.1",
    }

    versions = ["1.20.1", "1.20.2"]
    versions.sort()

    mappings = {}

    for version in versions:
        version_string = overrides.get(version) if version in overrides.keys() else version
        if version_string in mappings.keys():
            mappings[version] = mappings.get(version_string)
        else:
            mappings[version] = from_lmap(os.path.join(mappings_folder, f"{version}.lmap")).to_dict()

    maps = json.dumps(mappings, indent=1)
    code = f"mappings = {maps}"
    with open("../mappings.py", "w") as out_file:
        out_file.write(code)

if __name__ == '__main__':
    compile_mappings("mappings")
