import os
import logging
import argparse

from typing import Tuple
from utils import configure_logging, constants
from flow_tools import PropertyManager
from script_runner import PythonVersion
from script_runner import PythonScriptRunner, PipPackageInstaller

logger = logging.getLogger(__name__)


def main():
    # Configure the logger
    configure_logging()

    # Create command line argument parser and add program supported arguments
    parser = argparse.ArgumentParser(prog="PyWorker")

    # Add development mode positional argument
    parser.add_argument("--dev",
                        action="store_true",
                        help="enable development mode",
                        dest="dev_enabled")

    # Add custom provided input properties file argument
    parser.add_argument("-in",
                        "--input-properties",
                        default=None,
                        type=argparse.FileType("r"),
                        help=("override program input properties with the "
                              "properties from the provided %(metavar)s"),
                        metavar="FILE",
                        dest="input_properties_file")

    # Parse the arguments
    args = parser.parse_args()

    # Update root logger logging level if development mode is enabled
    if args.dev_enabled:
        logging.getLogger().setLevel(logging.DEBUG)

    # Read flow task input properties
    input_props = None

    if args.input_properties_file:
        input_props = PropertyManager.shared.get_properties_from_file(
            args.input_properties_file.name)
    else:
        input_props = PropertyManager.shared.task_input_properties

    # Convert python version from string to python version enum
    python_version = (PythonVersion.PYTHON_2_7 if "python 2"
                      in input_props.get(constants.INPUT_VERSION_KEY,
                                         "") else PythonVersion.PYTHON_3_9)

    # Check required task input properties
    if not input_props.get(constants.INPUT_SCRIPT_KEY):
        raise ValueError("Python script not provided or empty!")

    # Run the script
    result, output = run_script_job(
        python_version=python_version,
        additional_packages=input_props.get(constants.INPUT_PACKAGES_KEY, ""),
        script=input_props.get(constants.INPUT_SCRIPT_KEY, ""),
        cmd_args=input_props.get(constants.INPUT_ARGUMENTS_KEY, ""),
        development=args.dev_enabled)

    # Temporary: subject to be changed to a more generic form
    # Limit the file size to 4096 bytes
    output_file_path = input_props.get(constants.INPUT_OUTPUT_FILE_PATH_KEY,
                                       "").strip()

    # In case output file path was not provided
    if not output_file_path:
        output_file_path = "/tekton/results/output"

    # Create folder hierarchy
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

    logger.debug(f"Creating output file at: {output_file_path}")

    try:
        # Write output content to file
        with open(output_file_path, "w") as file:
            file.write(output)

            logger.debug(f"Script output successfully written at: "
                         f"{output_file_path}")
    except Exception as error:

        logger.error(f"Could not write output to file: {output_file_path}")
        logger.error(error, exc_info=True)

    # Program execution result from script job
    exit(result)


def run_script_job(python_version: PythonVersion,
                   additional_packages: str,
                   script: str,
                   cmd_args: str,
                   development: bool = False) -> Tuple[int, str]:

    logger.info("Input properties:")
    logger.info(f"🔢Python Version: {python_version}")
    logger.info(f"📦Python Packages:\n{additional_packages}")
    logger.info(f"📣Python Arguments: {cmd_args}")
    logger.info(f"🐍Python Script:\n{script}")

    # Create a new pip package installer instance and execute it
    pip_package_installer = PipPackageInstaller(packages=additional_packages)

    logger.debug("📥Start pip package installer activity...")

    pip_package_installer.run()

    logger.info(
        f"🗳Pip package installer result: {pip_package_installer.result}")
    logger.info(
        f"📝Pip package installer output:\n{pip_package_installer.output}")

    # If pip package installation has failed, exit the function prematurely
    if pip_package_installer.result != 0:
        return (pip_package_installer.result, pip_package_installer.output)

    # Create a new python script runner and execute the script
    python_script_runner = PythonScriptRunner(python_version=python_version,
                                              script=script,
                                              cmd_args=cmd_args)

    logger.debug("🐍Start python script runner activity...")

    python_script_runner.run()

    logger.info(f"🗳Python script runner result: {python_script_runner.result}")
    logger.info(
        f"📝Python script runner output:\n{python_script_runner.output}")

    return (python_script_runner.result, python_script_runner.output)


if __name__ == "__main__":
    main()
