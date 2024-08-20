import inspect


class ClassDefinitionError(Exception):
    """
    Base class for errors related to conflicts in the class definition when
    instantiating or using an object of a class.
    """

    def __init__(self, message: str):
        stack = inspect.stack()[1][0]
        frame_info = inspect.getframeinfo(stack)
        caller = f"{frame_info.function}:{frame_info.lineno}"
        if class_name := stack.f_locals.get("self", ""):
            caller = f"{class_name}.{caller}"
        self.caller = caller

        self.message = f"{message}\nOccurred in: {caller}"
        super().__init__(self.message)
