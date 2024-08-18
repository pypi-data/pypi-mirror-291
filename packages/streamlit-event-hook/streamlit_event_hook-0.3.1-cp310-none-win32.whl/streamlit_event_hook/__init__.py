import logging
import os
import threading
from typing import Callable

from .streamlit_event_hook import *

__doc__ = streamlit_event_hook.__doc__
if hasattr(streamlit_event_hook, "__all__"):
    __all__ = streamlit_event_hook.__all__


_render_interceptor = {}
_event_handler: Callable = None


def render_interceptor(stage):
    def decorator(func):
        _render_interceptor[stage] = func
        return func
    return decorator


def event_handler(func):
    def decorator():
        global _event_handler
        _event_handler = func
        return func

    return decorator()


def _before_render():
    if _render_interceptor.get("before"):
        try:
            _render_interceptor["before"]()
        except Exception as e:
            logging.error(e)


def _after_render():
    if _render_interceptor.get("after"):
        try:
            _render_interceptor["after"]()
        except Exception as e:
            logging.error(e)


def _my_event_handler(sender, event, forward_msg):
    if _event_handler is not None:
        try:
            _event_handler(sender, event, forward_msg)
        except Exception as e:
            logging.error(e)


def run_once(func):
    lock = threading.Lock()
    has_run = [False]

    def wrapper(*args, **kwargs):
        with lock:
            e_has_run = os.environ.get("streamlit_event_hook_has_run", "0")
            if not has_run[0] and e_has_run == "0":
                has_run[0] = True
                os.environ["streamlit_event_hook_has_run"] = "1"
                return func(*args, **kwargs)
    return wrapper


@run_once
def st_listen():
    streamlit_event_hook.hook(
        before_render=f"{_before_render.__module__}.{_before_render.__name__}",
        after_render=f"{_after_render.__module__}.{_after_render.__name__}",
        event_handler=f"{_my_event_handler.__module__}.{_my_event_handler.__name__}"
    )
