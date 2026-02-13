import inspect
from typing import List


class RunnableFunctionInfo:
    def __init__(self, func, text, path_from_cwd):
        self.func = func
        self.text = text
        self.path_from_cwd = path_from_cwd

    def get_func_name(self):
        return self.func.__name__

    def get_module(self):
        return inspect.getmodule(self.func)

    def get_func_module_name(self):
        return inspect.getmodulename(inspect.getfile(self.func))

    def get_func_doc(self):
        return self.get_module().__doc__


runnable_funcs_registry: List[RunnableFunctionInfo] = []
