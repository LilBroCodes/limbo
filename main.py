import os.path
import argparse
import shutil

import lmfunc
import mcfunc
import project as proj
import mcmeta
import util
import mappings as maps

logger = util.Logging.change_log_format("Build Limbo")

def generate(project_file: str, verbose: bool, delete: bool):
    logger.info("Starting the generation process.")

    # Load project
    project = proj.from_file(project_file)
    logger.info(f"Loaded project from {project_file}")

    if verbose:
        logger.debug(f"Project object: {project}")

    # Define all relevant paths
    project_path = os.path.dirname(project_file)
    target_path = project.output.target_path
    data_path = os.path.join(target_path, "data")
    namespace_path = os.path.join(data_path, project.output.namespace)
    functions_path = os.path.join(namespace_path, "functions")
    icon_path = os.path.join(project_path, project.pack_icon if project.pack_icon is not None else "icon.png")

    # Handle target deletion
    if delete and os.path.exists(target_path):
        logger.info(f"Deleting existing target directory: {target_path}")
        shutil.rmtree(target_path)

    # Create necessary directories
    for path in [target_path, namespace_path]:
        if not os.path.exists(path):
            logger.info(f"Creating directory: {path}")
            os.makedirs(path)
        elif verbose:
            logger.debug(f"Directory already exists: {path}")

    # Write pack.mcmeta
    meta = mcmeta.mcmeta_from_lmproj(project)
    meta_path = os.path.join(target_path, "pack.mcmeta")
    with open(meta_path, "w", encoding="utf-8") as file:
        file.write(meta)
    logger.info(f"Wrote 'pack.mcmeta' to {meta_path}")
    
    if verbose:
        logger.debug("Attempting to copy icon into generated datapack")
    if os.path.exists(icon_path):
        try:
            with open(icon_path, "rb") as original:
                data = original.read()
                with open(os.path.join(target_path, "pack.png"), "wb") as file:
                    file.write(data)
                    logger.info(f"Copied icon to {os.path.join(target_path, 'pack.png')}")
        except Exception as e:
            logger.error("Failed to copy icon!" + (" Use verbose mode for more details" if not verbose else ""))
            if verbose:
                logger.debug(f"Icon move failed with exception: {e}")
    else:
        logger.warning("Icon file doesn't exist!" if not verbose else f"Icon file {icon_path} doesn't exist!")

    if verbose:
        logger.debug(f"pack.mcmeta content:\n{meta}")

    # Find and parse .lm source files
    limbo_sources = [file for file in os.listdir(project_path) if file.endswith(".lm")]
    logger.info(f"Found {len(limbo_sources)} .lm file(s).")

    if limbo_sources and not os.path.exists(functions_path):
        logger.info(f"Creating functions directory: {functions_path}")
        os.makedirs(functions_path)

    for file in limbo_sources:
        file_path = os.path.join(project_path, file)
        if verbose:
            logger.debug(f"Processing source file: {file_path}")

        minecraft_functions = mcfunc.generate(file_path) + lmfunc.generate(file_path, maps.mappings[project.minecraft_version]["mappings"])
        logger.info(f"{file}: {len(minecraft_functions)} function(s) generated.")

        for func in minecraft_functions:
            func_file_path = os.path.join(functions_path, f"{func.name}.mcfunction")
            with open(func_file_path, "w") as f:
                f.write("\n".join(func.commands))

            if verbose:
                logger.debug(f"Wrote {'generated function' if func.limbo else 'function'} '{func.name}' to {func_file_path}")

    logger.info("Generation process complete.")

def main():
    parser = argparse.ArgumentParser(description="Generate pack.mcmeta from a project file.")
    parser.add_argument("project_file", help="Path to the .lmproj project file")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose logging")
    parser.add_argument("-d", "--delete", action="store_true", help="Delete already built project")

    args = parser.parse_args()

    if args.verbose:
        logger.debug("Verbose mode enabled.")

    generate(args.project_file, args.verbose, args.delete)


if __name__ == "__main__":
    main()
