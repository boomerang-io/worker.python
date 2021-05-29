from ._script_runner import ScriptRunner
from ._python_version import PythonVersion


class PythonScriptRunner(ScriptRunner):
    def __init__(self,
                 python_version: PythonVersion = PythonVersion.PYTHON_3_9,
                 script: str = "",
                 cmd_args: str = ""):
        self.__py_version = python_version
        self.__script = script
        self.__cmd_args = cmd_args
        self.__executed = False

    def run(self):

        # Sanity check
        if self.__executed:
            raise InterruptedError("The script cannot be executed multiple "
                                   "times!")

        self.__executed = True

    @property
    def result(self) -> int:

        # Sanity check
        if not self.__executed:
            raise InterruptedError("The result is available once the script "
                                   "execution is completed!")

    @property
    def output(self) -> int:

        # Sanity check
        if not self.__executed:
            raise InterruptedError("The output is available once the script "
                                   "execution is completed!")
