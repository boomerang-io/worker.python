import logging
import tempfile
import threading
import subprocess

from ._script_runner import ScriptRunner
from ._python_version import PythonVersion


class PythonScriptRunner(ScriptRunner):

    logger = logging.getLogger(__name__)

    def __init__(self,
                 python_version: PythonVersion = PythonVersion.PYTHON_3_9,
                 script: str = "",
                 cmd_args: str = ""):
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

    def run(self) -> None:

        # Sanity check
        with self.__lock:
            if self.__status > 0:
                raise InterruptedError("The script cannot be executed "
                                       "multiple times!")
            # Set status in progress
            self.__status = 1

        try:
            # Create a temporary file for storing the script
            with tempfile.NamedTemporaryFile("r+") as tmp_file:

                self.logger.debug("Temporary file created at: "
                                  f"{tmp_file.name}")

                # Write the script inside the temporary file
                tmp_file.write(self.__script)
                tmp_file.flush()

                self.logger.debug("Script has been written to the temporary "
                                  "file successfully!")

                exec_cmd = (f"{self.__py_version.python_executable()} "
                            f"{tmp_file.name} "
                            f"{self.__cmd_args}")

                self.logger.debug(f"Executing python script with command: "
                                  f"{exec_cmd}")

                result = subprocess.run(exec_cmd,
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.STDOUT,
                                        shell=True,
                                        text=True)

                self.logger.debug(f"Sub-process run result:\n{result}")

                # Update script output, result and execution
                self.__result = result.returncode
                self.__output = result.stdout

        except Exception as error:

            # An exception has occurred, update the result and output
            self.__result = 1
            self.__output = str(error)

        finally:

            # Set status to completed
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
