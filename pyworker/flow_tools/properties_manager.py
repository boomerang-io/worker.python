import os.path
import javaproperties

from . import _constants as constants


class _propertiesManagerSingleton(type):

    __shared = None

    def __call__(cls, *args, **kwargs):
        if cls.__shared is None:
            cls.__shared = super(_propertiesManagerSingleton,
                                 cls).__call__(*args, **kwargs)
        return cls.__shared

    @property
    def shared(cls):
        return cls()


class PropertiesManager(object, metaclass=_propertiesManagerSingleton):
    def __init__(self):
        self._task_input_properties = None

    @property
    def task_input_properties(self):

        # Lazy instantiation
        if self._task_input_properties is not None:
            return self._task_input_properties

        # Default task input properties
        properties = {}

        # Get the first available file where task input properties are stored
        input_file_path = next((file_path
                                for file_path in constants.TASK_INPUT_FILES
                                if os.path.isfile(file_path)), None)

        # Read the properties if a file was found
        if input_file_path:
            properties = self.propertiesFromFile(input_file_path)

        # Set and return input properties
        self._task_input_properties = properties
        return self._task_input_properties

    @staticmethod
    def propertiesFromFile(file_path: str) -> dict:
        with open(file_path, "r", encoding="utf-8") as file:
            return {
                key: value
                for key, value in javaproperties.load(file).items()
                if key and value
            }
