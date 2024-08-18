#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __coconut_hash__ = 0x9eba8dca

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

import os  #1 (line in Coconut source)

from claude_here.util import DEFAULT_VERBOSITY  #3 (line in Coconut source)
from claude_here.util import get_verbosity  #3 (line in Coconut source)
from claude_here.util import in_stdlib  #3 (line in Coconut source)


# META PROMPT:
# The task is for Claude to act as an assistant in debugging Python code. The application will automatically collect information about the currently running environment and send that to Claude to help debug upon encountering an exception or breakpoint. The information available is:
# * The raw source code of the file(s) being debugged.
# * A list of debug contexts, each containing information about a particular called breakpoint or caught exception. The contained information is: the filename, the function being called, the line on which the error occurred, and one of:
#     - The traceback if it's from an exception.
#     - The locals and globals if it's from a breakpoint.

BASE_PROMPT = """Your task is to follow the attached instructions, which should involve analyzing the attached Python code, breakpoint contexts, and/or unhandled exceptions to identify issues and provide helpful debugging suggestions. Remember to be thorough in your analysis, clear in your explanations, helpful in your suggestions, and to use Markdown to format your response."""  #17 (line in Coconut source)

POSTAMBLE = """Make sure to carefully examine the above source code, breakpoint contexts, and/or unhandled exceptions. Try to identify the root cause of any errors or issues and suggest solutions to fix them. Follow these steps:

1. Analyze the source code:
- Look for syntax errors, logical errors, or potential issues in the code structure.
- Pay attention to common Python pitfalls.

2. Examine the breakpoint contexts and/or unhandled exceptions provided:
- For each context, note the filename, function, and code context where the error occurred or breakpoint was reached.
- If it's an exception, carefully review the traceback to understand the error type and message.
- If it's a breakpoint, analyze the local and global variables to identify any unexpected values or states.

3. Identify the root cause:
- Cross-reference the provided context with the source code to pinpoint the exact location of the issue.
- Determine if the error is caused by the code itself or if it's related to external factors (e.g., missing dependencies, environment issues).

4. Develop debugging suggestions:
- Propose clear and concise solutions to fix any identified issues.
- If applicable, suggest alternative approaches or best practices to improve the code.
- Provide explanations for your suggestions to help the user understand the reasoning behind them.
- If there is anything you're not sure you understand from the provided context, you can ask the user for more information, but you should still give your best attempt at debugging given only the context provided.

5. Present your findings and suggestions:
- Summarize the identified issues and their locations in the code.
- List your debugging suggestions in a clear and organized manner.
- If relevant, include small code snippets to illustrate your suggestions.
- Format your response using Markdown."""  #44 (line in Coconut source)

README_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "README.md")  #46 (line in Coconut source)


class Markdown(_coconut.collections.namedtuple("Markdown", ('code',))):  #49 (line in Coconut source)
    __slots__ = ()  #49 (line in Coconut source)
    _coconut_is_data = True  #49 (line in Coconut source)
    __match_args__ = ('code',)  #49 (line in Coconut source)
    def __add__(self, other): return _coconut.NotImplemented  #49 (line in Coconut source)
    def __mul__(self, other): return _coconut.NotImplemented  #49 (line in Coconut source)
    def __rmul__(self, other): return _coconut.NotImplemented  #49 (line in Coconut source)
    __ne__ = _coconut.object.__ne__  #49 (line in Coconut source)
    def __eq__(self, other):  #49 (line in Coconut source)
        return self.__class__ is other.__class__ and _coconut.tuple.__eq__(self, other)  #49 (line in Coconut source)
    def __hash__(self):  #49 (line in Coconut source)
        return _coconut.tuple.__hash__(self) ^ _coconut.hash(self.__class__)  #49 (line in Coconut source)
    def __new__(_coconut_cls, _coconut_match_first_arg=_coconut_sentinel, *_coconut_match_args, **_coconut_match_kwargs):  #49 (line in Coconut source)
        _coconut_match_check_0 = False  #49 (line in Coconut source)
        _coconut_FunctionMatchError = _coconut_get_function_match_error()  #49 (line in Coconut source)
        if _coconut_match_first_arg is not _coconut_sentinel:  #49 (line in Coconut source)
            _coconut_match_args = (_coconut_match_first_arg,) + _coconut_match_args  #49 (line in Coconut source)
        if (_coconut.len(_coconut_match_args) <= 1) and (_coconut.sum((_coconut.len(_coconut_match_args) > 0, "code" in _coconut_match_kwargs)) == 1):  #49 (line in Coconut source)
            _coconut_match_temp_0 = _coconut_match_args[0] if _coconut.len(_coconut_match_args) > 0 else _coconut_match_kwargs.pop("code")  #49 (line in Coconut source)
            _coconut_match_temp_1 = _coconut.getattr(str, "_coconut_is_data", False) or _coconut.isinstance(str, _coconut.tuple) and _coconut.all(_coconut.getattr(_coconut_x, "_coconut_is_data", False) for _coconut_x in str)  # type: ignore  #49 (line in Coconut source)
            if not _coconut_match_kwargs:  #49 (line in Coconut source)
                _coconut_match_check_0 = True  #49 (line in Coconut source)
        if _coconut_match_check_0:  #49 (line in Coconut source)
            _coconut_match_check_0 = False  #49 (line in Coconut source)
            if not _coconut_match_check_0:  #49 (line in Coconut source)
                _coconut_match_set_name_code = _coconut_sentinel  #49 (line in Coconut source)
                if (_coconut_match_temp_1) and (_coconut.isinstance(_coconut_match_temp_0, str)) and (_coconut.len(_coconut_match_temp_0) >= 1):  #49 (line in Coconut source)
                    _coconut_match_set_name_code = _coconut_match_temp_0[0]  #49 (line in Coconut source)
                    _coconut_match_temp_2 = _coconut.len(_coconut_match_temp_0) <= _coconut.max(1, _coconut.len(_coconut_match_temp_0.__match_args__)) and _coconut.all(i in _coconut.getattr(_coconut_match_temp_0, "_coconut_data_defaults", {}) and _coconut_match_temp_0[i] == _coconut.getattr(_coconut_match_temp_0, "_coconut_data_defaults", {})[i] for i in _coconut.range(1, _coconut.len(_coconut_match_temp_0.__match_args__))) if _coconut.hasattr(_coconut_match_temp_0, "__match_args__") else _coconut.len(_coconut_match_temp_0) == 1  # type: ignore  #49 (line in Coconut source)
                    if _coconut_match_temp_2:  #49 (line in Coconut source)
                        _coconut_match_check_0 = True  #49 (line in Coconut source)
                if _coconut_match_check_0:  #49 (line in Coconut source)
                    if _coconut_match_set_name_code is not _coconut_sentinel:  #49 (line in Coconut source)
                        code = _coconut_match_set_name_code  #49 (line in Coconut source)

            if not _coconut_match_check_0:  #49 (line in Coconut source)
                if (not _coconut_match_temp_1) and (_coconut.isinstance(_coconut_match_temp_0, str)):  #49 (line in Coconut source)
                    _coconut_match_check_0 = True  #49 (line in Coconut source)
                if _coconut_match_check_0:  #49 (line in Coconut source)
                    _coconut_match_check_0 = False  #49 (line in Coconut source)
                    if not _coconut_match_check_0:  #49 (line in Coconut source)
                        _coconut_match_set_name_code = _coconut_sentinel  #49 (line in Coconut source)
                        if _coconut.type(_coconut_match_temp_0) in _coconut_self_match_types:  #49 (line in Coconut source)
                            _coconut_match_set_name_code = _coconut_match_temp_0  #49 (line in Coconut source)
                            _coconut_match_check_0 = True  #49 (line in Coconut source)
                        if _coconut_match_check_0:  #49 (line in Coconut source)
                            if _coconut_match_set_name_code is not _coconut_sentinel:  #49 (line in Coconut source)
                                code = _coconut_match_set_name_code  #49 (line in Coconut source)

                    if not _coconut_match_check_0:  #49 (line in Coconut source)
                        _coconut_match_set_name_code = _coconut_sentinel  #49 (line in Coconut source)
                        if not _coconut.type(_coconut_match_temp_0) in _coconut_self_match_types:  #49 (line in Coconut source)
                            _coconut_match_temp_3 = _coconut.getattr(str, '__match_args__', ())  # type: _coconut.typing.Any  # type: ignore  #49 (line in Coconut source)
                            if not _coconut.isinstance(_coconut_match_temp_3, _coconut.tuple):  #49 (line in Coconut source)
                                raise _coconut.TypeError("str.__match_args__ must be a tuple")  #49 (line in Coconut source)
                            if _coconut.len(_coconut_match_temp_3) < 1:  #49 (line in Coconut source)
                                raise _coconut.TypeError("too many positional args in class match (pattern requires 1; 'str' only supports %s)" % (_coconut.len(_coconut_match_temp_3),))  #49 (line in Coconut source)
                            _coconut_match_temp_4 = _coconut.getattr(_coconut_match_temp_0, _coconut_match_temp_3[0], _coconut_sentinel)  #49 (line in Coconut source)
                            if _coconut_match_temp_4 is not _coconut_sentinel:  #49 (line in Coconut source)
                                _coconut_match_set_name_code = _coconut_match_temp_4  #49 (line in Coconut source)
                                _coconut_match_check_0 = True  #49 (line in Coconut source)
                        if _coconut_match_check_0:  #49 (line in Coconut source)
                            if _coconut_match_set_name_code is not _coconut_sentinel:  #49 (line in Coconut source)
                                code = _coconut_match_set_name_code  #49 (line in Coconut source)





        if not _coconut_match_check_0:  #49 (line in Coconut source)
            raise _coconut_FunctionMatchError('data Markdown(str(code))', _coconut_match_args)  #49 (line in Coconut source)

        return _coconut.tuple.__new__(_coconut_cls, (code,))  #49 (line in Coconut source)

class SeparatedBy(_coconut.collections.namedtuple("SeparatedBy", ('sep', 'objs'))):  #50 (line in Coconut source)
    __slots__ = ()  #50 (line in Coconut source)
    _coconut_is_data = True  #50 (line in Coconut source)
    __match_args__ = ('sep', 'objs')  #50 (line in Coconut source)
    def __add__(self, other): return _coconut.NotImplemented  #50 (line in Coconut source)
    def __mul__(self, other): return _coconut.NotImplemented  #50 (line in Coconut source)
    def __rmul__(self, other): return _coconut.NotImplemented  #50 (line in Coconut source)
    __ne__ = _coconut.object.__ne__  #50 (line in Coconut source)
    def __eq__(self, other):  #50 (line in Coconut source)
        return self.__class__ is other.__class__ and _coconut.tuple.__eq__(self, other)  #50 (line in Coconut source)
    def __hash__(self):  #50 (line in Coconut source)
        return _coconut.tuple.__hash__(self) ^ _coconut.hash(self.__class__)  #50 (line in Coconut source)
    def __new__(_coconut_cls, _coconut_match_first_arg=_coconut_sentinel, *_coconut_match_args, **_coconut_match_kwargs):  #50 (line in Coconut source)
        _coconut_match_check_1 = False  #50 (line in Coconut source)
        _coconut_FunctionMatchError = _coconut_get_function_match_error()  #50 (line in Coconut source)
        if _coconut_match_first_arg is not _coconut_sentinel:  #50 (line in Coconut source)
            _coconut_match_args = (_coconut_match_first_arg,) + _coconut_match_args  #50 (line in Coconut source)
        if (_coconut.len(_coconut_match_args) <= 2) and (_coconut.sum((_coconut.len(_coconut_match_args) > 0, "sep" in _coconut_match_kwargs)) == 1) and (_coconut.sum((_coconut.len(_coconut_match_args) > 1, "objs" in _coconut_match_kwargs)) == 1):  #50 (line in Coconut source)
            _coconut_match_temp_5 = _coconut_match_args[0] if _coconut.len(_coconut_match_args) > 0 else _coconut_match_kwargs.pop("sep")  #50 (line in Coconut source)
            _coconut_match_temp_10 = _coconut_match_args[1] if _coconut.len(_coconut_match_args) > 1 else _coconut_match_kwargs.pop("objs")  #50 (line in Coconut source)
            _coconut_match_temp_6 = _coconut.getattr(str, "_coconut_is_data", False) or _coconut.isinstance(str, _coconut.tuple) and _coconut.all(_coconut.getattr(_coconut_x, "_coconut_is_data", False) for _coconut_x in str)  # type: ignore  #50 (line in Coconut source)
            _coconut_match_temp_11 = _coconut.getattr(list, "_coconut_is_data", False) or _coconut.isinstance(list, _coconut.tuple) and _coconut.all(_coconut.getattr(_coconut_x, "_coconut_is_data", False) for _coconut_x in list)  # type: ignore  #50 (line in Coconut source)
            if not _coconut_match_kwargs:  #50 (line in Coconut source)
                _coconut_match_check_1 = True  #50 (line in Coconut source)
        if _coconut_match_check_1:  #50 (line in Coconut source)
            _coconut_match_check_1 = False  #50 (line in Coconut source)
            if not _coconut_match_check_1:  #50 (line in Coconut source)
                _coconut_match_set_name_sep = _coconut_sentinel  #50 (line in Coconut source)
                if (_coconut_match_temp_6) and (_coconut.isinstance(_coconut_match_temp_5, str)) and (_coconut.len(_coconut_match_temp_5) >= 1):  #50 (line in Coconut source)
                    _coconut_match_set_name_sep = _coconut_match_temp_5[0]  #50 (line in Coconut source)
                    _coconut_match_temp_7 = _coconut.len(_coconut_match_temp_5) <= _coconut.max(1, _coconut.len(_coconut_match_temp_5.__match_args__)) and _coconut.all(i in _coconut.getattr(_coconut_match_temp_5, "_coconut_data_defaults", {}) and _coconut_match_temp_5[i] == _coconut.getattr(_coconut_match_temp_5, "_coconut_data_defaults", {})[i] for i in _coconut.range(1, _coconut.len(_coconut_match_temp_5.__match_args__))) if _coconut.hasattr(_coconut_match_temp_5, "__match_args__") else _coconut.len(_coconut_match_temp_5) == 1  # type: ignore  #50 (line in Coconut source)
                    if _coconut_match_temp_7:  #50 (line in Coconut source)
                        _coconut_match_check_1 = True  #50 (line in Coconut source)
                if _coconut_match_check_1:  #50 (line in Coconut source)
                    if _coconut_match_set_name_sep is not _coconut_sentinel:  #50 (line in Coconut source)
                        sep = _coconut_match_set_name_sep  #50 (line in Coconut source)

            if not _coconut_match_check_1:  #50 (line in Coconut source)
                if (not _coconut_match_temp_6) and (_coconut.isinstance(_coconut_match_temp_5, str)):  #50 (line in Coconut source)
                    _coconut_match_check_1 = True  #50 (line in Coconut source)
                if _coconut_match_check_1:  #50 (line in Coconut source)
                    _coconut_match_check_1 = False  #50 (line in Coconut source)
                    if not _coconut_match_check_1:  #50 (line in Coconut source)
                        _coconut_match_set_name_sep = _coconut_sentinel  #50 (line in Coconut source)
                        if _coconut.type(_coconut_match_temp_5) in _coconut_self_match_types:  #50 (line in Coconut source)
                            _coconut_match_set_name_sep = _coconut_match_temp_5  #50 (line in Coconut source)
                            _coconut_match_check_1 = True  #50 (line in Coconut source)
                        if _coconut_match_check_1:  #50 (line in Coconut source)
                            if _coconut_match_set_name_sep is not _coconut_sentinel:  #50 (line in Coconut source)
                                sep = _coconut_match_set_name_sep  #50 (line in Coconut source)

                    if not _coconut_match_check_1:  #50 (line in Coconut source)
                        _coconut_match_set_name_sep = _coconut_sentinel  #50 (line in Coconut source)
                        if not _coconut.type(_coconut_match_temp_5) in _coconut_self_match_types:  #50 (line in Coconut source)
                            _coconut_match_temp_8 = _coconut.getattr(str, '__match_args__', ())  # type: _coconut.typing.Any  # type: ignore  #50 (line in Coconut source)
                            if not _coconut.isinstance(_coconut_match_temp_8, _coconut.tuple):  #50 (line in Coconut source)
                                raise _coconut.TypeError("str.__match_args__ must be a tuple")  #50 (line in Coconut source)
                            if _coconut.len(_coconut_match_temp_8) < 1:  #50 (line in Coconut source)
                                raise _coconut.TypeError("too many positional args in class match (pattern requires 1; 'str' only supports %s)" % (_coconut.len(_coconut_match_temp_8),))  #50 (line in Coconut source)
                            _coconut_match_temp_9 = _coconut.getattr(_coconut_match_temp_5, _coconut_match_temp_8[0], _coconut_sentinel)  #50 (line in Coconut source)
                            if _coconut_match_temp_9 is not _coconut_sentinel:  #50 (line in Coconut source)
                                _coconut_match_set_name_sep = _coconut_match_temp_9  #50 (line in Coconut source)
                                _coconut_match_check_1 = True  #50 (line in Coconut source)
                        if _coconut_match_check_1:  #50 (line in Coconut source)
                            if _coconut_match_set_name_sep is not _coconut_sentinel:  #50 (line in Coconut source)
                                sep = _coconut_match_set_name_sep  #50 (line in Coconut source)




        if _coconut_match_check_1:  #50 (line in Coconut source)
            _coconut_match_check_1 = False  #50 (line in Coconut source)
            if not _coconut_match_check_1:  #50 (line in Coconut source)
                _coconut_match_set_name_objs = _coconut_sentinel  #50 (line in Coconut source)
                if (_coconut_match_temp_11) and (_coconut.isinstance(_coconut_match_temp_10, list)) and (_coconut.len(_coconut_match_temp_10) >= 1):  #50 (line in Coconut source)
                    _coconut_match_set_name_objs = _coconut_match_temp_10[0]  #50 (line in Coconut source)
                    _coconut_match_temp_12 = _coconut.len(_coconut_match_temp_10) <= _coconut.max(1, _coconut.len(_coconut_match_temp_10.__match_args__)) and _coconut.all(i in _coconut.getattr(_coconut_match_temp_10, "_coconut_data_defaults", {}) and _coconut_match_temp_10[i] == _coconut.getattr(_coconut_match_temp_10, "_coconut_data_defaults", {})[i] for i in _coconut.range(1, _coconut.len(_coconut_match_temp_10.__match_args__))) if _coconut.hasattr(_coconut_match_temp_10, "__match_args__") else _coconut.len(_coconut_match_temp_10) == 1  # type: ignore  #50 (line in Coconut source)
                    if _coconut_match_temp_12:  #50 (line in Coconut source)
                        _coconut_match_check_1 = True  #50 (line in Coconut source)
                if _coconut_match_check_1:  #50 (line in Coconut source)
                    if _coconut_match_set_name_objs is not _coconut_sentinel:  #50 (line in Coconut source)
                        objs = _coconut_match_set_name_objs  #50 (line in Coconut source)

            if not _coconut_match_check_1:  #50 (line in Coconut source)
                if (not _coconut_match_temp_11) and (_coconut.isinstance(_coconut_match_temp_10, list)):  #50 (line in Coconut source)
                    _coconut_match_check_1 = True  #50 (line in Coconut source)
                if _coconut_match_check_1:  #50 (line in Coconut source)
                    _coconut_match_check_1 = False  #50 (line in Coconut source)
                    if not _coconut_match_check_1:  #50 (line in Coconut source)
                        _coconut_match_set_name_objs = _coconut_sentinel  #50 (line in Coconut source)
                        if _coconut.type(_coconut_match_temp_10) in _coconut_self_match_types:  #50 (line in Coconut source)
                            _coconut_match_set_name_objs = _coconut_match_temp_10  #50 (line in Coconut source)
                            _coconut_match_check_1 = True  #50 (line in Coconut source)
                        if _coconut_match_check_1:  #50 (line in Coconut source)
                            if _coconut_match_set_name_objs is not _coconut_sentinel:  #50 (line in Coconut source)
                                objs = _coconut_match_set_name_objs  #50 (line in Coconut source)

                    if not _coconut_match_check_1:  #50 (line in Coconut source)
                        _coconut_match_set_name_objs = _coconut_sentinel  #50 (line in Coconut source)
                        if not _coconut.type(_coconut_match_temp_10) in _coconut_self_match_types:  #50 (line in Coconut source)
                            _coconut_match_temp_13 = _coconut.getattr(list, '__match_args__', ())  # type: _coconut.typing.Any  # type: ignore  #50 (line in Coconut source)
                            if not _coconut.isinstance(_coconut_match_temp_13, _coconut.tuple):  #50 (line in Coconut source)
                                raise _coconut.TypeError("list.__match_args__ must be a tuple")  #50 (line in Coconut source)
                            if _coconut.len(_coconut_match_temp_13) < 1:  #50 (line in Coconut source)
                                raise _coconut.TypeError("too many positional args in class match (pattern requires 1; 'list' only supports %s)" % (_coconut.len(_coconut_match_temp_13),))  #50 (line in Coconut source)
                            _coconut_match_temp_14 = _coconut.getattr(_coconut_match_temp_10, _coconut_match_temp_13[0], _coconut_sentinel)  #50 (line in Coconut source)
                            if _coconut_match_temp_14 is not _coconut_sentinel:  #50 (line in Coconut source)
                                _coconut_match_set_name_objs = _coconut_match_temp_14  #50 (line in Coconut source)
                                _coconut_match_check_1 = True  #50 (line in Coconut source)
                        if _coconut_match_check_1:  #50 (line in Coconut source)
                            if _coconut_match_set_name_objs is not _coconut_sentinel:  #50 (line in Coconut source)
                                objs = _coconut_match_set_name_objs  #50 (line in Coconut source)





        if not _coconut_match_check_1:  #50 (line in Coconut source)
            raise _coconut_FunctionMatchError('data SeparatedBy(str(sep), list(objs))', _coconut_match_args)  #50 (line in Coconut source)

        return _coconut.tuple.__new__(_coconut_cls, (sep, objs))  #50 (line in Coconut source)



@_coconut_mark_as_match  #53 (line in Coconut source)
def assemble_prompt(_coconut_match_first_arg=_coconut_sentinel, *_coconut_match_args, **_coconut_match_kwargs):  #53 (line in Coconut source)
    """Assemble a concrete prompt from the given structured prompt data."""  #54 (line in Coconut source)

    _coconut_match_check_2 = False  #55 (line in Coconut source)
    _coconut_FunctionMatchError = _coconut_get_function_match_error()  #55 (line in Coconut source)
    if _coconut_match_first_arg is not _coconut_sentinel:  #55 (line in Coconut source)
        _coconut_match_args = (_coconut_match_first_arg,) + _coconut_match_args  #55 (line in Coconut source)
    _coconut_match_kwargs_store = _coconut_match_kwargs  #55 (line in Coconut source)
    if not _coconut_match_check_2:  #55 (line in Coconut source)
        _coconut_match_kwargs = _coconut_match_kwargs_store.copy()  #55 (line in Coconut source)
        if (_coconut.len(_coconut_match_args) <= 1) and (_coconut.sum((_coconut.len(_coconut_match_args) > 0, "content" in _coconut_match_kwargs)) == 1):  #55 (line in Coconut source)
            _coconut_match_temp_15 = _coconut_match_args[0] if _coconut.len(_coconut_match_args) > 0 else _coconut_match_kwargs.pop("content")  #55 (line in Coconut source)
            _coconut_match_temp_16 = _coconut.getattr(str, "_coconut_is_data", False) or _coconut.isinstance(str, _coconut.tuple) and _coconut.all(_coconut.getattr(_coconut_x, "_coconut_is_data", False) for _coconut_x in str)  # type: ignore  #55 (line in Coconut source)
            if not _coconut_match_kwargs:  #55 (line in Coconut source)
                _coconut_match_check_2 = True  #55 (line in Coconut source)
        if _coconut_match_check_2:  #55 (line in Coconut source)
            _coconut_match_check_2 = False  #55 (line in Coconut source)
            if not _coconut_match_check_2:  #55 (line in Coconut source)
                _coconut_match_set_name_content = _coconut_sentinel  #55 (line in Coconut source)
                if (_coconut_match_temp_16) and (_coconut.isinstance(_coconut_match_temp_15, str)) and (_coconut.len(_coconut_match_temp_15) >= 1):  #55 (line in Coconut source)
                    _coconut_match_set_name_content = _coconut_match_temp_15[0]  #55 (line in Coconut source)
                    _coconut_match_temp_17 = _coconut.len(_coconut_match_temp_15) <= _coconut.max(1, _coconut.len(_coconut_match_temp_15.__match_args__)) and _coconut.all(i in _coconut.getattr(_coconut_match_temp_15, "_coconut_data_defaults", {}) and _coconut_match_temp_15[i] == _coconut.getattr(_coconut_match_temp_15, "_coconut_data_defaults", {})[i] for i in _coconut.range(1, _coconut.len(_coconut_match_temp_15.__match_args__))) if _coconut.hasattr(_coconut_match_temp_15, "__match_args__") else _coconut.len(_coconut_match_temp_15) == 1  # type: ignore  #55 (line in Coconut source)
                    if _coconut_match_temp_17:  #55 (line in Coconut source)
                        _coconut_match_check_2 = True  #55 (line in Coconut source)
                if _coconut_match_check_2:  #55 (line in Coconut source)
                    if _coconut_match_set_name_content is not _coconut_sentinel:  #55 (line in Coconut source)
                        content = _coconut_match_set_name_content  #55 (line in Coconut source)

            if not _coconut_match_check_2:  #55 (line in Coconut source)
                if (not _coconut_match_temp_16) and (_coconut.isinstance(_coconut_match_temp_15, str)):  #55 (line in Coconut source)
                    _coconut_match_check_2 = True  #55 (line in Coconut source)
                if _coconut_match_check_2:  #55 (line in Coconut source)
                    _coconut_match_check_2 = False  #55 (line in Coconut source)
                    if not _coconut_match_check_2:  #55 (line in Coconut source)
                        _coconut_match_set_name_content = _coconut_sentinel  #55 (line in Coconut source)
                        if _coconut.type(_coconut_match_temp_15) in _coconut_self_match_types:  #55 (line in Coconut source)
                            _coconut_match_set_name_content = _coconut_match_temp_15  #55 (line in Coconut source)
                            _coconut_match_check_2 = True  #55 (line in Coconut source)
                        if _coconut_match_check_2:  #55 (line in Coconut source)
                            if _coconut_match_set_name_content is not _coconut_sentinel:  #55 (line in Coconut source)
                                content = _coconut_match_set_name_content  #55 (line in Coconut source)

                    if not _coconut_match_check_2:  #55 (line in Coconut source)
                        _coconut_match_set_name_content = _coconut_sentinel  #55 (line in Coconut source)
                        if not _coconut.type(_coconut_match_temp_15) in _coconut_self_match_types:  #55 (line in Coconut source)
                            _coconut_match_temp_18 = _coconut.getattr(str, '__match_args__', ())  # type: _coconut.typing.Any  # type: ignore  #55 (line in Coconut source)
                            if not _coconut.isinstance(_coconut_match_temp_18, _coconut.tuple):  #55 (line in Coconut source)
                                raise _coconut.TypeError("str.__match_args__ must be a tuple")  #55 (line in Coconut source)
                            if _coconut.len(_coconut_match_temp_18) < 1:  #55 (line in Coconut source)
                                raise _coconut.TypeError("too many positional args in class match (pattern requires 1; 'str' only supports %s)" % (_coconut.len(_coconut_match_temp_18),))  #55 (line in Coconut source)
                            _coconut_match_temp_19 = _coconut.getattr(_coconut_match_temp_15, _coconut_match_temp_18[0], _coconut_sentinel)  #55 (line in Coconut source)
                            if _coconut_match_temp_19 is not _coconut_sentinel:  #55 (line in Coconut source)
                                _coconut_match_set_name_content = _coconut_match_temp_19  #55 (line in Coconut source)
                                _coconut_match_check_2 = True  #55 (line in Coconut source)
                        if _coconut_match_check_2:  #55 (line in Coconut source)
                            if _coconut_match_set_name_content is not _coconut_sentinel:  #55 (line in Coconut source)
                                content = _coconut_match_set_name_content  #55 (line in Coconut source)





        if _coconut_match_check_2:  #55 (line in Coconut source)

                return content.rstrip()  #55 (line in Coconut source)


    if not _coconut_match_check_2:  #57 (line in Coconut source)
        _coconut_match_kwargs = _coconut_match_kwargs_store.copy()  #57 (line in Coconut source)
        if (_coconut.len(_coconut_match_args) <= 1) and (_coconut.sum((_coconut.len(_coconut_match_args) > 0, "objs" in _coconut_match_kwargs)) == 1):  #57 (line in Coconut source)
            _coconut_match_temp_20 = _coconut_match_args[0] if _coconut.len(_coconut_match_args) > 0 else _coconut_match_kwargs.pop("objs")  #57 (line in Coconut source)
            _coconut_match_temp_21 = _coconut.getattr(list, "_coconut_is_data", False) or _coconut.isinstance(list, _coconut.tuple) and _coconut.all(_coconut.getattr(_coconut_x, "_coconut_is_data", False) for _coconut_x in list)  # type: ignore  #57 (line in Coconut source)
            if not _coconut_match_kwargs:  #57 (line in Coconut source)
                _coconut_match_check_2 = True  #57 (line in Coconut source)
        if _coconut_match_check_2:  #57 (line in Coconut source)
            _coconut_match_check_2 = False  #57 (line in Coconut source)
            if not _coconut_match_check_2:  #57 (line in Coconut source)
                _coconut_match_set_name_objs = _coconut_sentinel  #57 (line in Coconut source)
                if (_coconut_match_temp_21) and (_coconut.isinstance(_coconut_match_temp_20, list)) and (_coconut.len(_coconut_match_temp_20) >= 1):  #57 (line in Coconut source)
                    _coconut_match_set_name_objs = _coconut_match_temp_20[0]  #57 (line in Coconut source)
                    _coconut_match_temp_22 = _coconut.len(_coconut_match_temp_20) <= _coconut.max(1, _coconut.len(_coconut_match_temp_20.__match_args__)) and _coconut.all(i in _coconut.getattr(_coconut_match_temp_20, "_coconut_data_defaults", {}) and _coconut_match_temp_20[i] == _coconut.getattr(_coconut_match_temp_20, "_coconut_data_defaults", {})[i] for i in _coconut.range(1, _coconut.len(_coconut_match_temp_20.__match_args__))) if _coconut.hasattr(_coconut_match_temp_20, "__match_args__") else _coconut.len(_coconut_match_temp_20) == 1  # type: ignore  #57 (line in Coconut source)
                    if _coconut_match_temp_22:  #57 (line in Coconut source)
                        _coconut_match_check_2 = True  #57 (line in Coconut source)
                if _coconut_match_check_2:  #57 (line in Coconut source)
                    if _coconut_match_set_name_objs is not _coconut_sentinel:  #57 (line in Coconut source)
                        objs = _coconut_match_set_name_objs  #57 (line in Coconut source)

            if not _coconut_match_check_2:  #57 (line in Coconut source)
                if (not _coconut_match_temp_21) and (_coconut.isinstance(_coconut_match_temp_20, list)):  #57 (line in Coconut source)
                    _coconut_match_check_2 = True  #57 (line in Coconut source)
                if _coconut_match_check_2:  #57 (line in Coconut source)
                    _coconut_match_check_2 = False  #57 (line in Coconut source)
                    if not _coconut_match_check_2:  #57 (line in Coconut source)
                        _coconut_match_set_name_objs = _coconut_sentinel  #57 (line in Coconut source)
                        if _coconut.type(_coconut_match_temp_20) in _coconut_self_match_types:  #57 (line in Coconut source)
                            _coconut_match_set_name_objs = _coconut_match_temp_20  #57 (line in Coconut source)
                            _coconut_match_check_2 = True  #57 (line in Coconut source)
                        if _coconut_match_check_2:  #57 (line in Coconut source)
                            if _coconut_match_set_name_objs is not _coconut_sentinel:  #57 (line in Coconut source)
                                objs = _coconut_match_set_name_objs  #57 (line in Coconut source)

                    if not _coconut_match_check_2:  #57 (line in Coconut source)
                        _coconut_match_set_name_objs = _coconut_sentinel  #57 (line in Coconut source)
                        if not _coconut.type(_coconut_match_temp_20) in _coconut_self_match_types:  #57 (line in Coconut source)
                            _coconut_match_temp_23 = _coconut.getattr(list, '__match_args__', ())  # type: _coconut.typing.Any  # type: ignore  #57 (line in Coconut source)
                            if not _coconut.isinstance(_coconut_match_temp_23, _coconut.tuple):  #57 (line in Coconut source)
                                raise _coconut.TypeError("list.__match_args__ must be a tuple")  #57 (line in Coconut source)
                            if _coconut.len(_coconut_match_temp_23) < 1:  #57 (line in Coconut source)
                                raise _coconut.TypeError("too many positional args in class match (pattern requires 1; 'list' only supports %s)" % (_coconut.len(_coconut_match_temp_23),))  #57 (line in Coconut source)
                            _coconut_match_temp_24 = _coconut.getattr(_coconut_match_temp_20, _coconut_match_temp_23[0], _coconut_sentinel)  #57 (line in Coconut source)
                            if _coconut_match_temp_24 is not _coconut_sentinel:  #57 (line in Coconut source)
                                _coconut_match_set_name_objs = _coconut_match_temp_24  #57 (line in Coconut source)
                                _coconut_match_check_2 = True  #57 (line in Coconut source)
                        if _coconut_match_check_2:  #57 (line in Coconut source)
                            if _coconut_match_set_name_objs is not _coconut_sentinel:  #57 (line in Coconut source)
                                objs = _coconut_match_set_name_objs  #57 (line in Coconut source)





        if _coconut_match_check_2:  #57 (line in Coconut source)

                return assemble_prompt(SeparatedBy("\n", objs))  #58 (line in Coconut source)


    if not _coconut_match_check_2:  #60 (line in Coconut source)
        _coconut_match_kwargs = _coconut_match_kwargs_store.copy()  #60 (line in Coconut source)
        if _coconut.len(_coconut_match_args) == 1:  #60 (line in Coconut source)
            _coconut_match_temp_25 = _coconut.getattr(SeparatedBy, "_coconut_is_data", False) or _coconut.isinstance(SeparatedBy, _coconut.tuple) and _coconut.all(_coconut.getattr(_coconut_x, "_coconut_is_data", False) for _coconut_x in SeparatedBy)  # type: ignore  #60 (line in Coconut source)
            if not _coconut_match_kwargs:  #60 (line in Coconut source)
                _coconut_match_check_2 = True  #60 (line in Coconut source)
        if _coconut_match_check_2:  #60 (line in Coconut source)
            _coconut_match_check_2 = False  #60 (line in Coconut source)
            if not _coconut_match_check_2:  #60 (line in Coconut source)
                _coconut_match_set_name_sep = _coconut_sentinel  #60 (line in Coconut source)
                _coconut_match_set_name_objs = _coconut_sentinel  #60 (line in Coconut source)
                if (_coconut_match_temp_25) and (_coconut.isinstance(_coconut_match_args[0], SeparatedBy)) and (_coconut.len(_coconut_match_args[0]) >= 2):  #60 (line in Coconut source)
                    _coconut_match_set_name_sep = _coconut_match_args[0][0]  #60 (line in Coconut source)
                    _coconut_match_set_name_objs = _coconut_match_args[0][1]  #60 (line in Coconut source)
                    _coconut_match_temp_26 = _coconut.len(_coconut_match_args[0]) <= _coconut.max(2, _coconut.len(_coconut_match_args[0].__match_args__)) and _coconut.all(i in _coconut.getattr(_coconut_match_args[0], "_coconut_data_defaults", {}) and _coconut_match_args[0][i] == _coconut.getattr(_coconut_match_args[0], "_coconut_data_defaults", {})[i] for i in _coconut.range(2, _coconut.len(_coconut_match_args[0].__match_args__))) if _coconut.hasattr(_coconut_match_args[0], "__match_args__") else _coconut.len(_coconut_match_args[0]) == 2  # type: ignore  #60 (line in Coconut source)
                    if _coconut_match_temp_26:  #60 (line in Coconut source)
                        _coconut_match_check_2 = True  #60 (line in Coconut source)
                if _coconut_match_check_2:  #60 (line in Coconut source)
                    if _coconut_match_set_name_sep is not _coconut_sentinel:  #60 (line in Coconut source)
                        sep = _coconut_match_set_name_sep  #60 (line in Coconut source)
                    if _coconut_match_set_name_objs is not _coconut_sentinel:  #60 (line in Coconut source)
                        objs = _coconut_match_set_name_objs  #60 (line in Coconut source)

            if not _coconut_match_check_2:  #60 (line in Coconut source)
                if (not _coconut_match_temp_25) and (_coconut.isinstance(_coconut_match_args[0], SeparatedBy)):  #60 (line in Coconut source)
                    _coconut_match_check_2 = True  #60 (line in Coconut source)
                if _coconut_match_check_2:  #60 (line in Coconut source)
                    _coconut_match_check_2 = False  #60 (line in Coconut source)
                    if not _coconut_match_check_2:  #60 (line in Coconut source)
                        if _coconut.type(_coconut_match_args[0]) in _coconut_self_match_types:  #60 (line in Coconut source)
                            raise _coconut.TypeError("too many positional args in class match (pattern requires 2; 'SeparatedBy' only supports 1)")  #60 (line in Coconut source)
                            _coconut_match_check_2 = True  #60 (line in Coconut source)

                    if not _coconut_match_check_2:  #60 (line in Coconut source)
                        _coconut_match_set_name_sep = _coconut_sentinel  #60 (line in Coconut source)
                        _coconut_match_set_name_objs = _coconut_sentinel  #60 (line in Coconut source)
                        if not _coconut.type(_coconut_match_args[0]) in _coconut_self_match_types:  #60 (line in Coconut source)
                            _coconut_match_temp_27 = _coconut.getattr(SeparatedBy, '__match_args__', ())  # type: _coconut.typing.Any  # type: ignore  #60 (line in Coconut source)
                            if not _coconut.isinstance(_coconut_match_temp_27, _coconut.tuple):  #60 (line in Coconut source)
                                raise _coconut.TypeError("SeparatedBy.__match_args__ must be a tuple")  #60 (line in Coconut source)
                            if _coconut.len(_coconut_match_temp_27) < 2:  #60 (line in Coconut source)
                                raise _coconut.TypeError("too many positional args in class match (pattern requires 2; 'SeparatedBy' only supports %s)" % (_coconut.len(_coconut_match_temp_27),))  #60 (line in Coconut source)
                            _coconut_match_temp_28 = _coconut.getattr(_coconut_match_args[0], _coconut_match_temp_27[0], _coconut_sentinel)  #60 (line in Coconut source)
                            _coconut_match_temp_29 = _coconut.getattr(_coconut_match_args[0], _coconut_match_temp_27[1], _coconut_sentinel)  #60 (line in Coconut source)
                            if (_coconut_match_temp_28 is not _coconut_sentinel) and (_coconut_match_temp_29 is not _coconut_sentinel):  #60 (line in Coconut source)
                                _coconut_match_set_name_sep = _coconut_match_temp_28  #60 (line in Coconut source)
                                _coconut_match_set_name_objs = _coconut_match_temp_29  #60 (line in Coconut source)
                                _coconut_match_check_2 = True  #60 (line in Coconut source)
                        if _coconut_match_check_2:  #60 (line in Coconut source)
                            if _coconut_match_set_name_sep is not _coconut_sentinel:  #60 (line in Coconut source)
                                sep = _coconut_match_set_name_sep  #60 (line in Coconut source)
                            if _coconut_match_set_name_objs is not _coconut_sentinel:  #60 (line in Coconut source)
                                objs = _coconut_match_set_name_objs  #60 (line in Coconut source)





        if _coconut_match_check_2:  #60 (line in Coconut source)

                return (sep.join)((map)(assemble_prompt, objs))  #61 (line in Coconut source)


    if not _coconut_match_check_2:  #63 (line in Coconut source)
        _coconut_match_kwargs = _coconut_match_kwargs_store.copy()  #63 (line in Coconut source)
        if (_coconut.len(_coconut_match_args) <= 1) and (_coconut.sum((_coconut.len(_coconut_match_args) > 0, "tags" in _coconut_match_kwargs)) == 1):  #63 (line in Coconut source)
            _coconut_match_temp_30 = _coconut_match_args[0] if _coconut.len(_coconut_match_args) > 0 else _coconut_match_kwargs.pop("tags")  #63 (line in Coconut source)
            _coconut_match_temp_31 = _coconut.getattr(dict, "_coconut_is_data", False) or _coconut.isinstance(dict, _coconut.tuple) and _coconut.all(_coconut.getattr(_coconut_x, "_coconut_is_data", False) for _coconut_x in dict)  # type: ignore  #63 (line in Coconut source)
            if not _coconut_match_kwargs:  #63 (line in Coconut source)
                _coconut_match_check_2 = True  #63 (line in Coconut source)
        if _coconut_match_check_2:  #63 (line in Coconut source)
            _coconut_match_check_2 = False  #63 (line in Coconut source)
            if not _coconut_match_check_2:  #63 (line in Coconut source)
                _coconut_match_set_name_tags = _coconut_sentinel  #63 (line in Coconut source)
                if (_coconut_match_temp_31) and (_coconut.isinstance(_coconut_match_temp_30, dict)) and (_coconut.len(_coconut_match_temp_30) >= 1):  #63 (line in Coconut source)
                    _coconut_match_set_name_tags = _coconut_match_temp_30[0]  #63 (line in Coconut source)
                    _coconut_match_temp_32 = _coconut.len(_coconut_match_temp_30) <= _coconut.max(1, _coconut.len(_coconut_match_temp_30.__match_args__)) and _coconut.all(i in _coconut.getattr(_coconut_match_temp_30, "_coconut_data_defaults", {}) and _coconut_match_temp_30[i] == _coconut.getattr(_coconut_match_temp_30, "_coconut_data_defaults", {})[i] for i in _coconut.range(1, _coconut.len(_coconut_match_temp_30.__match_args__))) if _coconut.hasattr(_coconut_match_temp_30, "__match_args__") else _coconut.len(_coconut_match_temp_30) == 1  # type: ignore  #63 (line in Coconut source)
                    if _coconut_match_temp_32:  #63 (line in Coconut source)
                        _coconut_match_check_2 = True  #63 (line in Coconut source)
                if _coconut_match_check_2:  #63 (line in Coconut source)
                    if _coconut_match_set_name_tags is not _coconut_sentinel:  #63 (line in Coconut source)
                        tags = _coconut_match_set_name_tags  #63 (line in Coconut source)

            if not _coconut_match_check_2:  #63 (line in Coconut source)
                if (not _coconut_match_temp_31) and (_coconut.isinstance(_coconut_match_temp_30, dict)):  #63 (line in Coconut source)
                    _coconut_match_check_2 = True  #63 (line in Coconut source)
                if _coconut_match_check_2:  #63 (line in Coconut source)
                    _coconut_match_check_2 = False  #63 (line in Coconut source)
                    if not _coconut_match_check_2:  #63 (line in Coconut source)
                        _coconut_match_set_name_tags = _coconut_sentinel  #63 (line in Coconut source)
                        if _coconut.type(_coconut_match_temp_30) in _coconut_self_match_types:  #63 (line in Coconut source)
                            _coconut_match_set_name_tags = _coconut_match_temp_30  #63 (line in Coconut source)
                            _coconut_match_check_2 = True  #63 (line in Coconut source)
                        if _coconut_match_check_2:  #63 (line in Coconut source)
                            if _coconut_match_set_name_tags is not _coconut_sentinel:  #63 (line in Coconut source)
                                tags = _coconut_match_set_name_tags  #63 (line in Coconut source)

                    if not _coconut_match_check_2:  #63 (line in Coconut source)
                        _coconut_match_set_name_tags = _coconut_sentinel  #63 (line in Coconut source)
                        if not _coconut.type(_coconut_match_temp_30) in _coconut_self_match_types:  #63 (line in Coconut source)
                            _coconut_match_temp_33 = _coconut.getattr(dict, '__match_args__', ())  # type: _coconut.typing.Any  # type: ignore  #63 (line in Coconut source)
                            if not _coconut.isinstance(_coconut_match_temp_33, _coconut.tuple):  #63 (line in Coconut source)
                                raise _coconut.TypeError("dict.__match_args__ must be a tuple")  #63 (line in Coconut source)
                            if _coconut.len(_coconut_match_temp_33) < 1:  #63 (line in Coconut source)
                                raise _coconut.TypeError("too many positional args in class match (pattern requires 1; 'dict' only supports %s)" % (_coconut.len(_coconut_match_temp_33),))  #63 (line in Coconut source)
                            _coconut_match_temp_34 = _coconut.getattr(_coconut_match_temp_30, _coconut_match_temp_33[0], _coconut_sentinel)  #63 (line in Coconut source)
                            if _coconut_match_temp_34 is not _coconut_sentinel:  #63 (line in Coconut source)
                                _coconut_match_set_name_tags = _coconut_match_temp_34  #63 (line in Coconut source)
                                _coconut_match_check_2 = True  #63 (line in Coconut source)
                        if _coconut_match_check_2:  #63 (line in Coconut source)
                            if _coconut_match_set_name_tags is not _coconut_sentinel:  #63 (line in Coconut source)
                                tags = _coconut_match_set_name_tags  #63 (line in Coconut source)





        if _coconut_match_check_2:  #63 (line in Coconut source)

                return (assemble_prompt)((list)(tags.items()))  #64 (line in Coconut source)


    if not _coconut_match_check_2:  #66 (line in Coconut source)
        _coconut_match_kwargs = _coconut_match_kwargs_store.copy()  #66 (line in Coconut source)
        _coconut_match_set_name_tag = _coconut_sentinel  #66 (line in Coconut source)
        _coconut_match_set_name_content = _coconut_sentinel  #66 (line in Coconut source)
        if _coconut.len(_coconut_match_args) == 1:  #66 (line in Coconut source)
            if (_coconut.isinstance(_coconut_match_args[0], _coconut.abc.Sequence)) and (_coconut.len(_coconut_match_args[0]) == 2):  #66 (line in Coconut source)
                _coconut_match_set_name_tag = _coconut_match_args[0][0]  #66 (line in Coconut source)
                _coconut_match_set_name_content = _coconut_match_args[0][1]  #66 (line in Coconut source)
                if not _coconut_match_kwargs:  #66 (line in Coconut source)
                    _coconut_match_check_2 = True  #66 (line in Coconut source)
        if _coconut_match_check_2:  #66 (line in Coconut source)
            if _coconut_match_set_name_tag is not _coconut_sentinel:  #66 (line in Coconut source)
                tag = _coconut_match_set_name_tag  #66 (line in Coconut source)
            if _coconut_match_set_name_content is not _coconut_sentinel:  #66 (line in Coconut source)
                content = _coconut_match_set_name_content  #66 (line in Coconut source)

        if _coconut_match_check_2:  #66 (line in Coconut source)

                return "<{_coconut_format_0}>\n{_coconut_format_1}\n</{_coconut_format_2}>".format(_coconut_format_0=(tag), _coconut_format_1=(assemble_prompt(content)), _coconut_format_2=(tag))  #67 (line in Coconut source)


    if not _coconut_match_check_2:  #69 (line in Coconut source)
        _coconut_match_kwargs = _coconut_match_kwargs_store.copy()  #69 (line in Coconut source)
        if _coconut.len(_coconut_match_args) == 1:  #69 (line in Coconut source)
            _coconut_match_temp_35 = _coconut.getattr(Markdown, "_coconut_is_data", False) or _coconut.isinstance(Markdown, _coconut.tuple) and _coconut.all(_coconut.getattr(_coconut_x, "_coconut_is_data", False) for _coconut_x in Markdown)  # type: ignore  #69 (line in Coconut source)
            if not _coconut_match_kwargs:  #69 (line in Coconut source)
                _coconut_match_check_2 = True  #69 (line in Coconut source)
        if _coconut_match_check_2:  #69 (line in Coconut source)
            _coconut_match_check_2 = False  #69 (line in Coconut source)
            if not _coconut_match_check_2:  #69 (line in Coconut source)
                _coconut_match_set_name_code = _coconut_sentinel  #69 (line in Coconut source)
                if (_coconut_match_temp_35) and (_coconut.isinstance(_coconut_match_args[0], Markdown)) and (_coconut.len(_coconut_match_args[0]) >= 1):  #69 (line in Coconut source)
                    _coconut_match_set_name_code = _coconut_match_args[0][0]  #69 (line in Coconut source)
                    _coconut_match_temp_36 = _coconut.len(_coconut_match_args[0]) <= _coconut.max(1, _coconut.len(_coconut_match_args[0].__match_args__)) and _coconut.all(i in _coconut.getattr(_coconut_match_args[0], "_coconut_data_defaults", {}) and _coconut_match_args[0][i] == _coconut.getattr(_coconut_match_args[0], "_coconut_data_defaults", {})[i] for i in _coconut.range(1, _coconut.len(_coconut_match_args[0].__match_args__))) if _coconut.hasattr(_coconut_match_args[0], "__match_args__") else _coconut.len(_coconut_match_args[0]) == 1  # type: ignore  #69 (line in Coconut source)
                    if _coconut_match_temp_36:  #69 (line in Coconut source)
                        _coconut_match_check_2 = True  #69 (line in Coconut source)
                if _coconut_match_check_2:  #69 (line in Coconut source)
                    if _coconut_match_set_name_code is not _coconut_sentinel:  #69 (line in Coconut source)
                        code = _coconut_match_set_name_code  #69 (line in Coconut source)

            if not _coconut_match_check_2:  #69 (line in Coconut source)
                if (not _coconut_match_temp_35) and (_coconut.isinstance(_coconut_match_args[0], Markdown)):  #69 (line in Coconut source)
                    _coconut_match_check_2 = True  #69 (line in Coconut source)
                if _coconut_match_check_2:  #69 (line in Coconut source)
                    _coconut_match_check_2 = False  #69 (line in Coconut source)
                    if not _coconut_match_check_2:  #69 (line in Coconut source)
                        _coconut_match_set_name_code = _coconut_sentinel  #69 (line in Coconut source)
                        if _coconut.type(_coconut_match_args[0]) in _coconut_self_match_types:  #69 (line in Coconut source)
                            _coconut_match_set_name_code = _coconut_match_args[0]  #69 (line in Coconut source)
                            _coconut_match_check_2 = True  #69 (line in Coconut source)
                        if _coconut_match_check_2:  #69 (line in Coconut source)
                            if _coconut_match_set_name_code is not _coconut_sentinel:  #69 (line in Coconut source)
                                code = _coconut_match_set_name_code  #69 (line in Coconut source)

                    if not _coconut_match_check_2:  #69 (line in Coconut source)
                        _coconut_match_set_name_code = _coconut_sentinel  #69 (line in Coconut source)
                        if not _coconut.type(_coconut_match_args[0]) in _coconut_self_match_types:  #69 (line in Coconut source)
                            _coconut_match_temp_37 = _coconut.getattr(Markdown, '__match_args__', ())  # type: _coconut.typing.Any  # type: ignore  #69 (line in Coconut source)
                            if not _coconut.isinstance(_coconut_match_temp_37, _coconut.tuple):  #69 (line in Coconut source)
                                raise _coconut.TypeError("Markdown.__match_args__ must be a tuple")  #69 (line in Coconut source)
                            if _coconut.len(_coconut_match_temp_37) < 1:  #69 (line in Coconut source)
                                raise _coconut.TypeError("too many positional args in class match (pattern requires 1; 'Markdown' only supports %s)" % (_coconut.len(_coconut_match_temp_37),))  #69 (line in Coconut source)
                            _coconut_match_temp_38 = _coconut.getattr(_coconut_match_args[0], _coconut_match_temp_37[0], _coconut_sentinel)  #69 (line in Coconut source)
                            if _coconut_match_temp_38 is not _coconut_sentinel:  #69 (line in Coconut source)
                                _coconut_match_set_name_code = _coconut_match_temp_38  #69 (line in Coconut source)
                                _coconut_match_check_2 = True  #69 (line in Coconut source)
                        if _coconut_match_check_2:  #69 (line in Coconut source)
                            if _coconut_match_set_name_code is not _coconut_sentinel:  #69 (line in Coconut source)
                                code = _coconut_match_set_name_code  #69 (line in Coconut source)





        if _coconut_match_check_2:  #69 (line in Coconut source)

                return "\n```python\n{_coconut_format_0}\n```\n".format(_coconut_format_0=(assemble_prompt(code)))  #70 (line in Coconut source)



    if not _coconut_match_check_2:  #73 (line in Coconut source)
        raise _coconut_FunctionMatchError('case def assemble_prompt:', _coconut_match_args)  #73 (line in Coconut source)

def trim_source_code(source_code, relevant_line_numbers):  #73 (line in Coconut source)
    """Trim the given source code down if necessary."""  #74 (line in Coconut source)
    verbosity = get_verbosity()  #75 (line in Coconut source)

    if not relevant_line_numbers:  #77 (line in Coconut source)
        relevant_line_numbers = [verbosity * 20,]  #78 (line in Coconut source)

    if len(source_code) < verbosity * 1500:  #80 (line in Coconut source)
        return source_code  #81 (line in Coconut source)

    source_lines = (list)(source_code.splitlines())  #83 (line in Coconut source)

    if len(source_lines) < verbosity * 30:  #85 (line in Coconut source)
        return source_code  #86 (line in Coconut source)

    start_lineno = max(min(relevant_line_numbers) - verbosity * 10, 1)  #88 (line in Coconut source)
    stop_lineno = min(max(relevant_line_numbers) + verbosity * 10, len(source_lines))  #92 (line in Coconut source)

    remainder_truncated_msg = ["<remainder truncated>",] if stop_lineno < len(source_lines) else []  #97 (line in Coconut source)
    if start_lineno <= verbosity * 10:  #98 (line in Coconut source)
        return "\n".join(source_lines[:stop_lineno] + remainder_truncated_msg)  #99 (line in Coconut source)
    else:  #100 (line in Coconut source)
        return "\n".join(source_lines[:verbosity * 10] + ["<middle truncated>",] + source_lines[start_lineno - 1:stop_lineno] + remainder_truncated_msg)  #101 (line in Coconut source)



def generate_prompt(all_debug_context, max_context_items):  #109 (line in Coconut source)
    """Generate a full prompt and attachment for Claude using the given debug context."""  #110 (line in Coconut source)
    verbosity = get_verbosity()  #111 (line in Coconut source)

    prompt_cmpts = ["""The assistant is being called by the `claude_here` debugging library, which the user is using to ask you for debugging help.""",]  #113 (line in Coconut source)
    if verbosity >= DEFAULT_VERBOSITY:  #114 (line in Coconut source)
        prompt_cmpts += ["""To help you understand the context of how `claude_here` works, here is the full `claude_here` README:""",]  #115 (line in Coconut source)
# The most important bits are that any cases where you see `import claude_here` or `breakpoint()` are the user asking you for help. It is expected that `claude_here` will be imported and not used.
        with open(README_FILE, "r") as readme_file:  #117 (line in Coconut source)
            prompt_cmpts += [{"claude_here_readme.md": readme_file.read()},]  #118 (line in Coconut source)

    prompt_cmpts += ["""The assistant's goal is to assist the user in resolving their Python code issues effectively. Here is the information that you will be working with:""",]  #120 (line in Coconut source)

    for filepath, debug_contexts in all_debug_context.items():  #122 (line in Coconut source)
        coconut_filepath = os.path.splitext(filepath)[0] + ".coco"  #123 (line in Coconut source)
        if os.path.exists(coconut_filepath):  #124 (line in Coconut source)
            filepath = coconut_filepath  #125 (line in Coconut source)
        filename = os.path.basename(filepath)  #126 (line in Coconut source)

        file_prompt_cmpts = []  #128 (line in Coconut source)
        seen_code = {""}  #129 (line in Coconut source)
        if os.path.isfile(filepath) and not in_stdlib(filepath):  #130 (line in Coconut source)
            with open(filepath, "r") as fobj:  #131 (line in Coconut source)
                source_code = fobj.read()  #132 (line in Coconut source)
            seen_code.add(source_code)  #133 (line in Coconut source)
            file_prompt_cmpts += [{"source_code": trim_source_code(source_code, relevant_line_numbers=(tuple)((filter)(_coconut_complex_partial(_coconut.operator.is_not, {1: None}, 2, ()), (map)(_coconut.operator.attrgetter("lineno"), debug_contexts))))},]  #134 (line in Coconut source)

        for ctx in _coconut_iter_getitem(debug_contexts, _coconut.slice(-max_context_items, None)):  #141 (line in Coconut source)
            info_dict = {}  #142 (line in Coconut source)
            if ctx.raw_source not in seen_code:  #143 (line in Coconut source)
                if ctx.source_type is not None:  #144 (line in Coconut source)
                    info_dict["surrounding_code"] = {ctx.source_type: ctx.raw_source}  #145 (line in Coconut source)
                else:  #146 (line in Coconut source)
                    info_dict["surrounding_code"] = ctx.raw_source  #147 (line in Coconut source)
                seen_code.add(ctx.raw_source)  #148 (line in Coconut source)
            if ctx.function is not None:  #149 (line in Coconut source)
                info_dict["executing_function"] = ctx.function  #150 (line in Coconut source)
            if ctx.raw_context:  #151 (line in Coconut source)
                info_dict["executing_line"] = ctx.raw_context  #152 (line in Coconut source)
            if ctx.lineno is not None:  #153 (line in Coconut source)
                info_dict["line_number"] = (str)(ctx.lineno)  #154 (line in Coconut source)
            info_dict |= ctx.extra_info  #155 (line in Coconut source)
            file_prompt_cmpts += [{ctx.name: info_dict},]  #156 (line in Coconut source)

        prompt_cmpts += [{filename: (SeparatedBy)("\n\n", file_prompt_cmpts)},]  #158 (line in Coconut source)

    if verbosity >= DEFAULT_VERBOSITY // 2:  #160 (line in Coconut source)
        prompt_cmpts += [POSTAMBLE,]  #161 (line in Coconut source)

    attachment = assemble_prompt((SeparatedBy)("\n\n", prompt_cmpts))  #163 (line in Coconut source)
    return (_coconut_mk_anon_namedtuple(('prompt', 'attachment'))(BASE_PROMPT, attachment))  #164 (line in Coconut source)
