import logging
import argparse

from utils import configureLogging
from flow_tools import PropertiesManager
from script_runner import PythonVersion, PythonScriptRunner

# Constants
# DEV_INPUT_FILE_PATH = "./tests/input_props_test1.txt"
DEV_INPUT_FILE_PATH = "./io_properties/dev_input.properties"
DEV_OUTPUT_FILE_PATH = "./io_properties/dev_output.properties"

INPUT_VERSION_KEY = "pythonVersion"
INPUT_PACKAGES_KEY = "pythonPackages"
INPUT_SCRIPT_KEY = "pythonScript"
INPUT_ARGUMENTS_KEY = "pythonArguments"


def main():
    # Configure and get the logger for this module
    configureLogging()
    logger = logging.getLogger(__name__)

    # Create command line argument parser and add program supported arguments
    parser = argparse.ArgumentParser()

    # Add development mode positional argument
    parser.add_argument("--dev",
                        action="store_true",
                        help="enable development mode",
                        dest="dev_enabled")

    # Parse the arguments
    args = parser.parse_args()

    # Update root logger logging level if development mode is enabled
    if args.dev_enabled:
        logging.getLogger().setLevel(logging.DEBUG)

    # Read flow task input properties
    input_props = None

    if args.dev_enabled:
        input_props = PropertiesManager.shared.get_properties_from_file(
            DEV_INPUT_FILE_PATH)
    else:
        input_props = PropertiesManager.shared.task_input_properties

    logger.info("Input properties:")
    logger.info(f"🔢Python Version: {input_props.get(INPUT_VERSION_KEY)}")
    logger.info(f"📦Python Packages:\n{input_props.get(INPUT_PACKAGES_KEY)}")
    logger.info(f"📣Python Arguments: {input_props.get(INPUT_ARGUMENTS_KEY)}")
    logger.info(f"🚀Python Script:\n{input_props.get(INPUT_SCRIPT_KEY)}")

    # Check required task input properties
    if not input_props.get(INPUT_SCRIPT_KEY):
        raise ValueError("Python script not provided or empty!")

    # Create a new python script runner and execute the script
    python_version = (PythonVersion.PYTHON_3_9
                      if "python 2" in input_props.get(INPUT_VERSION_KEY, "")
                      else PythonVersion.PYTHON_2_7)
    python_script_runner = PythonScriptRunner(
        python_version=python_version,
        script=input_props.get(INPUT_SCRIPT_KEY, ""),
        cmd_args=input_props.get(INPUT_ARGUMENTS_KEY, ""))

    logger.debug("Start python script runner activity...")

    python_script_runner.run()

    logger.info(f"🗳Python script runner result: {python_script_runner.result}")
    logger.info(
        f"📝Python script runner output:\n{python_script_runner.output}")

    # print(os.system("echo $PATH"))

    # print(PropertiesManager())
    # print(PropertiesManager.shared_instance)
    # print(PropertiesManager.shared_instance.task_input_properties)
    # print(PropertiesManager.shared_instance.task_input_properties)
    # print(PropertiesManager.shared_instance.task_input_properties)
    # print(PropertiesManager.shared_instance.task_input_properties)
    # print(f"fere")

    # py_script_str = ("print(\"Hello World2\")\n"
    #                  "x = 3\n"
    #                  "y = 7\n"
    #                  "result = (x + y) ** 2\n"
    #                  "print(result)\n")

    # fifo_path = "fifo_file"

    # print(os.path.exists(fifo_path))

    # # if stat.S_ISFIFO(os.stat(fifo_path).st_mode):
    # if not os.path.exists(fifo_path):
    #     os.mkfifo(fifo_path)

    # with open(fifo_path, "w", encoding="utf-8") as fifo:
    #     fifo.write(py_script_str)

    # Program execution successful
    exit(0)


def run_script():
    pass


if __name__ == "__main__":
    main()
