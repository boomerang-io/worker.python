import os.path

from . import _constants as constants


class _task_utils_meta(type):
    def __init__(cls, *args, **kwargs):
        cls._input_properties = None

    @property
    def input_properties(cls):

        # Lazy instantiation
        if cls._input_properties is not None:
            return cls._input_properties

        # Get the first available file where task input properties are stored
        input_file_path = next((file_path
                                for file_path in constants.TASK_INPUT_FILES
                                if os.path.isfile(file_path)), None)

        print(input_file_path)

        cls._input_properties = {}

        return cls._input_properties

    # @input_properties.setter
    # def input_properties(cls, value: dict):
    #     cls._input_properties = value


class TaskUtils(metaclass=_task_utils_meta):
    pass
