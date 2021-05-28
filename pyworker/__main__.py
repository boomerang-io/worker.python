import logging
import argparse

from .flow_tools import PropertiesManager

# Constants
DEV_INPUT_FILE_PATH = "./dev.input"
DEV_OUTPUT_FILE_PATH = "./dev.output"

INPUT_VERSION_KEY = "pythonVersion"
INPUT_PACKAGES_KEY = "pythonPackages"
INPUT_SCRIPT_KEY = "pythonScript"
INPUT_ARGUMENTS_KEY = "pythonArguments"


def main():
    # Configure logger
    logging.basicConfig()
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.WARNING)

    # Create command line argument parser and add program supported arguments
    parser = argparse.ArgumentParser()

    # Add development mode positional argument
    parser.add_argument("--dev",
                        action="store_true",
                        help="enable development mode",
                        dest="dev_enabled")

    # Parse the arguments
    args = parser.parse_args()

    # Update logger level if development mode is enabled
    if args.dev_enabled:
        logger.setLevel(logging.DEBUG)

    # Read flow task input properties
    input_props = None

    if args.dev_enabled:
        input_props = PropertiesManager.shared.propertiesFromFile(
            DEV_INPUT_FILE_PATH)
    else:
        input_props = PropertiesManager.shared.task_input_properties

    logger.info("Input properties:")
    logger.info(f"Python Version: {input_props.get(INPUT_VERSION_KEY)}")
    logger.info(f"Python Packages:\n{input_props.get(INPUT_PACKAGES_KEY)}")
    logger.info(f"Python Arguments: {input_props.get(INPUT_ARGUMENTS_KEY)}")
    logger.info(f"Python Script:\n{input_props.get(INPUT_SCRIPT_KEY)}")

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


if __name__ == "__main__":
    main()
