
class _task_utils_meta(type):

    def __init__(cls, *args, **kwargs):
        cls._input_properties = None

    @property
    def input_properties(cls):

        # Lazy instantiation
        if cls._input_properties is not None:
            return cls._input_properties

        cls._input_properties = {}

        return cls._input_properties

    # @input_properties.setter
    # def input_properties(cls, value: dict):
    #     cls._input_properties = value


class TaskUtils(metaclass=_task_utils_meta):
    pass
