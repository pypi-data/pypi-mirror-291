#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __coconut_hash__ = 0xaa3922e2

# Compiled with Coconut version 3.1.1-post_dev3

# Coconut Header: -------------------------------------------------------------

from __future__ import generator_stop, annotations
import sys as _coconut_sys
import os as _coconut_os
_coconut_header_info = ('3.1.1-post_dev3', '39', True)
_coconut_cached__coconut__ = _coconut_sys.modules.get('__coconut__')
_coconut_file_dir = _coconut_os.path.dirname(_coconut_os.path.abspath(__file__))
_coconut_pop_path = False
if _coconut_cached__coconut__ is None or getattr(_coconut_cached__coconut__, "_coconut_header_info", None) != _coconut_header_info and _coconut_os.path.dirname(_coconut_cached__coconut__.__file__ or "") != _coconut_file_dir:  # type: ignore
    if _coconut_cached__coconut__ is not None:
        _coconut_sys.modules['_coconut_cached__coconut__'] = _coconut_cached__coconut__
        del _coconut_sys.modules['__coconut__']
    _coconut_sys.path.insert(0, _coconut_file_dir)
    _coconut_pop_path = True
    _coconut_module_name = _coconut_os.path.splitext(_coconut_os.path.basename(_coconut_file_dir))[0]
    if _coconut_module_name and _coconut_module_name[0].isalpha() and all(c.isalpha() or c.isdigit() for c in _coconut_module_name) and "__init__.py" in _coconut_os.listdir(_coconut_file_dir):  # type: ignore
        _coconut_full_module_name = str(_coconut_module_name + ".__coconut__")  # type: ignore
        import __coconut__ as _coconut__coconut__
        _coconut__coconut__.__name__ = _coconut_full_module_name
        for _coconut_v in vars(_coconut__coconut__).values():  # type: ignore
            if getattr(_coconut_v, "__module__", None) == '__coconut__':  # type: ignore
                try:
                    _coconut_v.__module__ = _coconut_full_module_name
                except AttributeError:
                    _coconut_v_type = type(_coconut_v)  # type: ignore
                    if getattr(_coconut_v_type, "__module__", None) == '__coconut__':  # type: ignore
                        _coconut_v_type.__module__ = _coconut_full_module_name
        _coconut_sys.modules[_coconut_full_module_name] = _coconut__coconut__
from __coconut__ import *
from __coconut__ import _namedtuple_of, _coconut, _coconut_Expected, _coconut_MatchError, _coconut_SupportsAdd, _coconut_SupportsMinus, _coconut_SupportsMul, _coconut_SupportsPow, _coconut_SupportsTruediv, _coconut_SupportsFloordiv, _coconut_SupportsMod, _coconut_SupportsAnd, _coconut_SupportsXor, _coconut_SupportsOr, _coconut_SupportsLshift, _coconut_SupportsRshift, _coconut_SupportsMatmul, _coconut_SupportsInv, _coconut_iter_getitem, _coconut_base_compose, _coconut_forward_compose, _coconut_back_compose, _coconut_forward_star_compose, _coconut_back_star_compose, _coconut_forward_dubstar_compose, _coconut_back_dubstar_compose, _coconut_pipe, _coconut_star_pipe, _coconut_dubstar_pipe, _coconut_back_pipe, _coconut_back_star_pipe, _coconut_back_dubstar_pipe, _coconut_none_pipe, _coconut_none_star_pipe, _coconut_none_dubstar_pipe, _coconut_bool_and, _coconut_bool_or, _coconut_none_coalesce, _coconut_minus, _coconut_map, _coconut_partial, _coconut_complex_partial, _coconut_get_function_match_error, _coconut_base_pattern_func, _coconut_addpattern, _coconut_sentinel, _coconut_assert, _coconut_raise, _coconut_mark_as_match, _coconut_reiterable, _coconut_self_match_types, _coconut_dict_merge, _coconut_exec, _coconut_comma_op, _coconut_arr_concat_op, _coconut_mk_anon_namedtuple, _coconut_matmul, _coconut_py_str, _coconut_flatten, _coconut_multiset, _coconut_back_none_pipe, _coconut_back_none_star_pipe, _coconut_back_none_dubstar_pipe, _coconut_forward_none_compose, _coconut_back_none_compose, _coconut_forward_none_star_compose, _coconut_back_none_star_compose, _coconut_forward_none_dubstar_compose, _coconut_back_none_dubstar_compose, _coconut_call_or_coefficient, _coconut_in, _coconut_not_in, _coconut_attritemgetter, _coconut_if_op, _coconut_CoconutWarning
if _coconut_pop_path:
    _coconut_sys.path.pop(0)
try:
    __file__ = _coconut_os.path.abspath(__file__) if __file__ else __file__
except NameError:
    pass
else:
    if __file__ and '__coconut_cache__' in __file__:
        _coconut_file_comps = []
        while __file__:
            __file__, _coconut_file_comp = _coconut_os.path.split(__file__)
            if not _coconut_file_comp:
                _coconut_file_comps.append(__file__)
                break
            if _coconut_file_comp != '__coconut_cache__':
                _coconut_file_comps.append(_coconut_file_comp)
        __file__ = _coconut_os.path.join(*reversed(_coconut_file_comps))

# Compiled Coconut: -----------------------------------------------------------

import sys  #1 (line in Coconut source)

from claude_here.debugger import collect_stack_info  #3 (line in Coconut source)
from claude_here.debugger import collect_exc_info  #3 (line in Coconut source)
from claude_here.launcher import launch_claude  #4 (line in Coconut source)


BASE_HOOKS = {"breakpointhook": sys.__breakpointhook__, "excepthook": sys.__excepthook__}  #7 (line in Coconut source)


def breakpointhook(msg=None, just_gather_info=False, base_debugger=None, **kwargs):  #13 (line in Coconut source)
    """Claude breakpoint handler."""  #14 (line in Coconut source)
    extra_info = {}  #15 (line in Coconut source)
    if msg is not None:  #16 (line in Coconut source)
        extra_info["user_message"] = msg  #17 (line in Coconut source)
    collect_stack_info(stack_level=2, extra_info=extra_info)  #18 (line in Coconut source)
    if not just_gather_info:  #19 (line in Coconut source)
        launch_claude(**kwargs)  #20 (line in Coconut source)
        ((lambda _coconut_x: BASE_HOOKS["breakpointhook"] if _coconut_x is None else _coconut_x)(base_debugger))()  #21 (line in Coconut source)



EXTRA_RECURSION_LIMIT = 100  #24 (line in Coconut source)
IGNORE_EXCEPTIONS_FROM = {"pdb", "bdb"}  #25 (line in Coconut source)


def excepthook(exc_type, exc_val, exc_tb):  #28 (line in Coconut source)
    """Claude exception handler."""  #29 (line in Coconut source)
# if we're recovering from a RecursionError, we'll need some extra stack
    sys.setrecursionlimit(sys.getrecursionlimit() + EXTRA_RECURSION_LIMIT)  #31 (line in Coconut source)
    try:  #32 (line in Coconut source)
        BASE_HOOKS["excepthook"](exc_type, exc_val, exc_tb)  #33 (line in Coconut source)
    finally:  #34 (line in Coconut source)
        if getattr(exc_type, "__module__", "") not in IGNORE_EXCEPTIONS_FROM:  #35 (line in Coconut source)
            collect_exc_info(exc_type, exc_val, exc_tb)  #36 (line in Coconut source)
            launch_claude()  #37 (line in Coconut source)



def set_claude_here_breakpoint(on=True):  #40 (line in Coconut source)
    """Set breakpoint() to collect info and launch Claude."""  #41 (line in Coconut source)
    if on:  #42 (line in Coconut source)
        if sys.breakpointhook is not breakpointhook:  #43 (line in Coconut source)
            BASE_HOOKS["breakpointhook"], sys.breakpointhook = sys.breakpointhook, breakpointhook  #44 (line in Coconut source)
    else:  #45 (line in Coconut source)
        sys.breakpointhook = BASE_HOOKS["breakpointhook"]  #46 (line in Coconut source)



def set_claude_here_excepthook(on=True):  #49 (line in Coconut source)
    """Configure uncaught exceptions to launch Claude."""  #50 (line in Coconut source)
    if on:  #51 (line in Coconut source)
        if sys.excepthook is not excepthook:  #52 (line in Coconut source)
            BASE_HOOKS["excepthook"], sys.excepthook = sys.excepthook, excepthook  #53 (line in Coconut source)
    else:  #54 (line in Coconut source)
        sys.excepthook = BASE_HOOKS["excepthook"]  #55 (line in Coconut source)
