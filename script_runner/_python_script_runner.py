import logging

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

        # Create script handler thread attributes for the job
        attributes = SimpleNamespace()
        attributes.python_version = self.__py_version
        attributes.script = self.__script
        attributes.cmd_args = self.__cmd_args
        attributes.result = None
        attributes.output = None

        # Create script handler thread itself and start its activity
        script_handler_thread = Thread(target=self.__script_handler,
                                       args=(attributes, ))
        script_handler_thread.start()

        # Wait until script handler finishes its execution
        script_handler_thread.join()

        # Update script output, result and execution
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
    def __script_handler(cls, attributes: SimpleNamespace):
        attributes.result = 0
        attributes.output = "ha ha!"

    @classmethod
    def __script_executer(cls):
        pass
