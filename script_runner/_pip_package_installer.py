import logging
import tempfile
import threading
import subprocess

from ._script_runner import ScriptRunner


class PipPackageInstaller(ScriptRunner):

    logger = logging.getLogger(__name__)

    def __init__(self, packages: str = ""):
        self.__packages = packages
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
                raise InterruptedError("Pip packages already installed!")

            # Set status in progress
            self.__status = 1

        try:
            # Create a temporary file for storing pip packages
            with tempfile.NamedTemporaryFile("r+") as tmp_file:

                self.logger.debug(f"Temporary file created at: "
                                  f"{tmp_file.name}")

                # Write pip packages inside the temporary file
                tmp_file.write(self.__packages)
                tmp_file.flush()

                self.logger.debug(f"Pip packages have been written to the "
                                  f"temporary file successfully!")

                exec_cmd = f"pip install -r {tmp_file.name}"

                self.logger.debug(f"Run pip package installer with command: "
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
