class CallCounter(object):
    "Decorator that keeps track of the number of times a function is called."

    __instances = {}  # type: ignore

    def __init__(self, f):
        self.__f = f
        self.__numcalls = 0
        CallCounter.__instances[f] = self

    def __call__(self, *args, **kwargs):
        self.__numcalls += 1
        return self.__f(*args, **kwargs)

    # @staticmethod
    def count_calls(self):
        "Return the number of times the function f was called."
        return CallCounter.__instances[self.__f].__numcalls

    @staticmethod
    def clear():
        for f in CallCounter.__instances:
            CallCounter.__instances[f].__numcalls = 0

    @staticmethod
    def counts():
        "Return a dict of {function: # of calls} for all registered functions."
        return dict(
            [
                (f.__name__, CallCounter.__instances[f].__numcalls)
                for f in CallCounter.__instances
            ]
        )
