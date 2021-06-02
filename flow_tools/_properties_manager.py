import os.path
import logging
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
    def shared(cls) -> "class":
        return cls()


class PropertiesManager(object, metaclass=_propertiesManagerSingleton):

    logger = logging.getLogger(__name__)

    def __init__(self):
        self._task_input_properties = None

    @property
    def task_input_properties(self):

        # Lazy instantiation if the property has not yet been created
        if self._task_input_properties is not None:
            return self._task_input_properties

        self.logger.debug("Lazy instantiate `task_input_properties`")

        # Default task input properties
        properties = {}

        # Get the first available file where task input properties are stored
        input_file_path = next((file_path
                                for file_path in constants.TASK_INPUT_FILES
                                if os.path.isfile(file_path)), None)

        # Read the properties if a file was found
        if input_file_path:
            properties = self.get_properties_from_file(input_file_path)

        # Set and return input properties
        self._task_input_properties = properties
        return self._task_input_properties

    @classmethod
    def get_properties_from_file(cls, file_path: str) -> dict:

        cls.logger.debug(f"Read properties from file: {file_path}")

        with open(file_path, "r", encoding="utf-8") as file:
            return {
                key: value
                for key, value in javaproperties.load(file).items()
                if key and value
            }
