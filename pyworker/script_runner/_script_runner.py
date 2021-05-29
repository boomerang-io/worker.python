from abc import ABCMeta, abstractmethod


class ScriptRunner(metaclass=ABCMeta):
    def __init__(self):
        raise TypeError("This is an Abstract Class and it cannot be "
                        "instantiated!")

    @abstractmethod
    def run(self):
        # Run the script
        raise NotImplementedError(f"`run` method not implemented in class "
                                  f"{type(self).__name__}!")

    @property
    @abstractmethod
    def result(self) -> int:
        # Get script execution result
        raise NotImplementedError(f"`result` property not implemented in "
                                  f"class {type(self).__name__}!")

    @property
    @abstractmethod
    def output(self) -> int:
        # Get script execution output
        raise NotImplementedError(f"`output` property not implemented in "
                                  f"class {type(self).__name__}!")
