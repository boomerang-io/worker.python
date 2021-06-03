import logging
import tempfile
import threading
import subprocess

from pathlib import Path
from ._script_runner import ScriptRunner
from ._python_version import PythonVersion


class PythonScriptRunner(ScriptRunner):

    logger = logging.getLogger(__name__)

    def __init__(self,
                 python_version: PythonVersion = PythonVersion.PYTHON_3_9,
                 script: str = "",
                 cmd_args: str = "",
                 development: bool = False):
        self.__py_version = python_version
        self.__script = script
        self.__cmd_args = cmd_args

        self.__result = None
        self.__output = None

        # Status states:
        # 0 - Not started
        # 1 - Started, in progress
        # 2 - Completed
        self.__status = 0
        self.__lock = threading.Lock()
        self.__development = development

    def run(self) -> None:

        # Sanity check
        with self.__lock:
            if self.__status > 0:
                raise InterruptedError("The script cannot be executed "
                                       "multiple times!")
            # Set status in progress
            self.__status = 1

        # Create the temporary file for the script
        tmp_file_path = Path([tempfile.mkdtemp(), "./"][self.__development],
                             "__py_script")
        tmp_file_path.unlink(missing_ok=True)
        tmp_file_path.touch()

        self.logger.debug(f"Temporary file created at: {tmp_file_path}")

        # Write the script inside the temporary file
        try:
            with open(tmp_file_path, "w") as file:
                file.write(self.__script)

        except Exception as error:

            # An exception has occurred, update result, output and exit
            # prematurely
            self.__result = 1
            self.__output = str(error)

            with self.__lock:
                self.__status = 2

            return

        self.logger.debug(f"Script has been written to the temporary file "
                          f"successfully!")

        exec_cmd = (f"{self.__py_version.python_executable()} "
                    f"{tmp_file_path} "
                    f"{self.__cmd_args}")

        self.logger.debug(f"Executing python script with command: {exec_cmd}")

        result = subprocess.run(exec_cmd,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT,
                                shell=True)

        self.logger.debug(f"Sub-process run result:\n{result}")

        # Delete the temporary file
        tmp_file_path.unlink()

        self.logger.debug(f"Temporary file deleted from: {tmp_file_path}")

        # Update script output, result and execution
        self.__result = result.returncode
        self.__output = result.stdout

        with self.__lock:
            self.__status = 2

    @property
    def result(self) -> int:

        # Sanity check
        if self.__status < 2:
            raise InterruptedError("The result is available once the script "
                                   "execution is completed!")
        return self.__result

    @property
    def output(self) -> str:

        # Sanity check
        if self.__status < 2:
            raise InterruptedError("The output is available once the script "
                                   "execution is completed!")
        return self.__output
