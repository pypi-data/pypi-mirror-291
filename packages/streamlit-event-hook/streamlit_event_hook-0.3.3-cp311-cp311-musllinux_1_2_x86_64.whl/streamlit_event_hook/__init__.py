import logging
import os
import threading
import time
from typing import Callable

import streamlit as st
from .streamlit_event_hook import *

__doc__ = streamlit_event_hook.__doc__
if hasattr(streamlit_event_hook, "__all__"):
    __all__ = streamlit_event_hook.__all__


_render_interceptor = {}
_event_handler_run_obj: Callable = None


def render_interceptor(stage):
    def decorator(func):
        _render_interceptor[stage] = func
        return func
    return decorator


def event_handler(func):
    def decorator():
        global _event_handler_run_obj
        _event_handler_run_obj = func
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


def _event_handler(sender, event, forward_msg):
    if _event_handler_run_obj is not None:
        try:
            _event_handler_run_obj(sender, event, forward_msg)
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
    logging.info("streamlit_event_hook is initializing..")
    streamlit_event_hook.hook_streamlit()
    time.sleep(0.2)
    logging.info("streamlit_event_hook initialization complete, restarting now.")
    st.rerun()
