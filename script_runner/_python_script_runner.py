import os
import logging
import tempfile

from pathlib import Path
from threading import Thread
from types import SimpleNamespace
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
        self.__executed = False

    def run(self):

        # Sanity check
        if self.__executed:
            raise InterruptedError("The script cannot be executed multiple "
                                   "times!")

        # First, create the named pipe for python script
        fifo_path = Path(tempfile.mkdtemp(), "__py_fifo")
        fifo_path.unlink(missing_ok=True)
        os.mkfifo(fifo_path)

        self.logger.debug(f"Named pipe created: {fifo_path}")

        # Create the output attributes for script writer and executor threads
        writer_attributes = SimpleNamespace(result=None, output=None)
        executer_attributes = SimpleNamespace(result=None, output=None)

        # Create script writer and executor threads and start their activity
        script_writer_thread = Thread(target=self.__script_writer,
                                      args=(fifo_path, self.__script,
                                            writer_attributes))
        script_executor_thread = Thread(target=self.__script_executer,
                                        args=(fifo_path, self.__py_version,
                                              self.__cmd_args,
                                              executer_attributes))
        script_writer_thread.start()
        script_executor_thread.start()

        # Wait until threads finish their execution
        script_writer_thread.join()
        script_executor_thread.join()

        # Delete the named pipe file
        fifo_path.unlink()

        self.logger.debug(f"Named pipe deleted: {fifo_path}")

        # Update script output, result and execution
        attributes = (writer_attributes if writer_attributes.result != 0 else
                      executer_attributes)

        self.__result = attributes.result
        self.__output = attributes.output
        self.__executed = True

    @property
    def result(self) -> int:

        # Sanity check
        if not self.__executed:
            raise InterruptedError("The result is available once the script "
                                   "execution is completed!")
        return self.__result

    @property
    def output(self) -> str:

        # Sanity check
        if not self.__executed:
            raise InterruptedError("The output is available once the script "
                                   "execution is completed!")
        return self.__output

    @classmethod
    def __script_writer(cls, file_path: Path, script: str,
                        out_attributes: SimpleNamespace):

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

        out_attributes.result = 0
        out_attributes.output = "ha ha!"

    @classmethod
    def __script_executer(cls, file_path: Path, python_version: PythonVersion,
                          cmd_args: str, out_attributes: SimpleNamespace):
        out_attributes.result = 0
        out_attributes.output = "ha ha!"
