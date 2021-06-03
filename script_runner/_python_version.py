from ordered_enum import OrderedEnum
from packaging.version import Version


class PythonVersion(OrderedEnum):
    PYTHON_0_9 = Version("0.9")
    PYTHON_1_0 = Version("1.0")
    PYTHON_1_1 = Version("1.1")
    PYTHON_1_2 = Version("1.2")
    PYTHON_1_3 = Version("1.3")
    PYTHON_1_4 = Version("1.4")
    PYTHON_1_5 = Version("1.5")
    PYTHON_1_6 = Version("1.6")
    PYTHON_2_0 = Version("2.0")
    PYTHON_2_1 = Version("2.1")
    PYTHON_2_2 = Version("2.2")
    PYTHON_2_3 = Version("2.3")
    PYTHON_2_4 = Version("2.4")
    PYTHON_2_5 = Version("2.5")
    PYTHON_2_6 = Version("2.6")
    PYTHON_2_7 = Version("2.7")
    PYTHON_3_0 = Version("3.0")
    PYTHON_3_1 = Version("3.1")
    PYTHON_3_2 = Version("3.2")
    PYTHON_3_3 = Version("3.3")
    PYTHON_3_4 = Version("3.4")
    PYTHON_3_5 = Version("3.5")
    PYTHON_3_6 = Version("3.6")
    PYTHON_3_7 = Version("3.7")
    PYTHON_3_8 = Version("3.8")
    PYTHON_3_9 = Version("3.9")
    PYTHON_3_10 = Version("3.10")

    def python_executable(self) -> str:

        if self.value.minor:
            return f"python{self.value.major}.{self.value.minor}"

        return f"python{self.value.major}"

    def __str__(self):
        return f"Python {self.value}"
