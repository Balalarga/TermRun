import inspect
import logging
import os
from pathlib import Path

import invoke

from .runnable_function_info import runnable_funcs_registry, RunnableFunctionInfo


def __make_runnable_func(func, title):
    pwd = Path(os.getcwd())
    module_path = Path(inspect.getfile(func))
    if not module_path.is_relative_to(pwd):
        raise Exception(f"Path to module {module_path} is somehow not relative to working dir {pwd}")

    func_sign = inspect.signature(func)
    params = func_sign.parameters
    if len(params) != 1:
        raise Exception(f"'{func.__name__}' signature should be func(invoke_ctx)")

    for k in params:
        param = params[k]
        if param.kind is not inspect.Parameter.POSITIONAL_OR_KEYWORD:
            raise Exception(f"'{func.__name__}' signature should be func(invoke_ctx)")

        if param.annotation is not inspect.Parameter.empty and param.annotation != invoke.Context:
            raise Exception(
                f"'{func.__name__}' parameter type missmatch should be: {invoke.Context} but is {param.annotation}")

    if len(title) == 0:
        title = func.__name__

    return RunnableFunctionInfo(func, title, module_path.relative_to(pwd).parent)


def term_runnable(title="", os_filter: str = None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        if os_filter is not None and os_filter is not os.name:
            logging.info(f"Skip function. Incompatible os: '{os_filter}'")
            return wrapper

        runnable_funcs_registry.append(__make_runnable_func(func, title))
        return wrapper

    return decorator
