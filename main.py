import os.path
import argparse
import logging
import shutil

import mcfunc
import project as proj
import mcmeta

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def generate(project_file: str, verbose: bool, delete: bool):
    logging.info("Starting the generation process.")

    # Load project
    project = proj.from_file(project_file)
    logging.info(f"Loaded project from {project_file}")

    if verbose:
        logging.debug(f"Project object: {project}")

    # Define all relevant paths
    project_path = os.path.dirname(project_file)
    target_path = project.output.target_path
    data_path = os.path.join(target_path, "data")
    namespace_path = os.path.join(data_path, project.output.namespace)
    functions_path = os.path.join(namespace_path, "functions")

    # Handle target deletion
    if delete and os.path.exists(target_path):
        logging.info(f"Deleting existing target directory: {target_path}")
        shutil.rmtree(target_path)

    # Create necessary directories
    for path in [target_path, namespace_path]:
        if not os.path.exists(path):
            logging.info(f"Creating directory: {path}")
            os.makedirs(path)
        elif verbose:
            logging.debug(f"Directory already exists: {path}")

    # Write pack.mcmeta
    meta = mcmeta.mcmeta_from_lmproj(project)
    meta_path = os.path.join(target_path, "pack.mcmeta")
    with open(meta_path, "w", encoding="utf-8") as file:
        file.write(meta)
    logging.info(f"Wrote 'pack.mcmeta' to {meta_path}")

    if verbose:
        logging.debug(f"pack.mcmeta content:\n{meta}")

    # Find and parse .lm source files
    limbo_sources = [file for file in os.listdir(project_path) if file.endswith(".lm")]
    logging.info(f"Found {len(limbo_sources)} .lm file(s).")

    if limbo_sources and not os.path.exists(functions_path):
        logging.info(f"Creating functions directory: {functions_path}")
        os.makedirs(functions_path)

    for file in limbo_sources:
        file_path = os.path.join(project_path, file)
        if verbose:
            logging.debug(f"Processing source file: {file_path}")

        minecraft_functions = mcfunc.generate(file_path)
        logging.info(f"{file}: {len(minecraft_functions)} function(s) generated.")

        for func in minecraft_functions:
            func_file_path = os.path.join(functions_path, f"{func.name}.mcfunction")
            with open(func_file_path, "w") as f:
                f.write("\n".join(func.commands))

            if verbose:
                logging.debug(f"Wrote function '{func.name}' to {func_file_path}")

    logging.info("Generation process complete.")

def main():
    parser = argparse.ArgumentParser(description="Generate pack.mcmeta from a project file.")
    parser.add_argument("project_file", help="Path to the .lmproj project file")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose logging")
    parser.add_argument("-d", "--delete", action="store_true", help="Delete already built project")

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        logging.debug("Verbose mode enabled.")

    generate(args.project_file, args.verbose, args.delete)


if __name__ == "__main__":
    main()
