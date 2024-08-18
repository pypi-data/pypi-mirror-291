#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __coconut_hash__ = 0x89f64279

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
import io  #2 (line in Coconut source)
import inspect  #3 (line in Coconut source)
import traceback  #4 (line in Coconut source)
import builtins  #5 (line in Coconut source)
import random  #6 (line in Coconut source)
from dis import dis  #7 (line in Coconut source)
from collections import defaultdict  #8 (line in Coconut source)

from claude_here.util import fixpath  #10 (line in Coconut source)
from claude_here.util import get_verbosity  #10 (line in Coconut source)


ALL_DEBUG_CONTEXT = defaultdict(list)  #13 (line in Coconut source)


reset = ALL_DEBUG_CONTEXT.clear  #16 (line in Coconut source)


def include_file(filepath):  #19 (line in Coconut source)
    """Ensure that the given filepath is included in the context sent to Claude."""  #20 (line in Coconut source)
    ALL_DEBUG_CONTEXT[fixpath(filepath)]  #21 (line in Coconut source)



class DebugContext(_coconut.typing.NamedTuple("DebugContext", [("name", 'str'), ("frame_info", '_coconut.typing.Any'), ("source_type", '_coconut.typing.Optional[str]'), ("raw_source", 'str'), ("extra_info", 'dict[str, str]')])):  #24 (line in Coconut source)
    """Collection of information gathered about a debug event."""  #31 (line in Coconut source)
    __slots__ = ()  #32 (line in Coconut source)
    _coconut_is_data = True  #32 (line in Coconut source)
    __match_args__ = ('name', 'frame_info', 'source_type', 'raw_source', 'extra_info')  #32 (line in Coconut source)
    def __add__(self, other): return _coconut.NotImplemented  #32 (line in Coconut source)
    def __mul__(self, other): return _coconut.NotImplemented  #32 (line in Coconut source)
    def __rmul__(self, other): return _coconut.NotImplemented  #32 (line in Coconut source)
    __ne__ = _coconut.object.__ne__  #32 (line in Coconut source)
    def __eq__(self, other):  #32 (line in Coconut source)
        return self.__class__ is other.__class__ and _coconut.tuple.__eq__(self, other)  #32 (line in Coconut source)
    def __hash__(self):  #32 (line in Coconut source)
        return _coconut.tuple.__hash__(self) ^ _coconut.hash(self.__class__)  #32 (line in Coconut source)
    def __init__(self, *args, **kwargs):  #32 (line in Coconut source)
        ALL_DEBUG_CONTEXT[self.filename].append(self)  #33 (line in Coconut source)

    @property  #34 (line in Coconut source)
    def filename(self):  #35 (line in Coconut source)
        return fixpath((lambda _coconut_x: os.path.join(os.getcwd(), "<stdin>") if _coconut_x is None else _coconut_x)((lambda _coconut_x: None if _coconut_x is None else _coconut_x.filename)(self.frame_info)))  #35 (line in Coconut source)

    @property  #36 (line in Coconut source)
    def lineno(self):  #37 (line in Coconut source)
        return (lambda _coconut_x: None if _coconut_x is None else _coconut_x.lineno)(self.frame_info)  #37 (line in Coconut source)

    @property  #38 (line in Coconut source)
    def function(self):  #39 (line in Coconut source)
        return (lambda _coconut_x: None if _coconut_x is None else _coconut_x.function)(self.frame_info)  #39 (line in Coconut source)

    @property  #40 (line in Coconut source)
    def context_lines(self):  #41 (line in Coconut source)
        return (lambda _coconut_x: None if _coconut_x is None else _coconut_x.code_context)(self.frame_info)  #41 (line in Coconut source)

    @property  #42 (line in Coconut source)
    def context_index(self):  #43 (line in Coconut source)
        return (lambda _coconut_x: None if _coconut_x is None else _coconut_x.index)(self.frame_info)  #43 (line in Coconut source)

    @property  #44 (line in Coconut source)
    def raw_context(self):  #45 (line in Coconut source)
        return "".join(self.context_lines) if self.context_lines else ""  #45 (line in Coconut source)



IGNORED_VARS = set(dir(builtins)) | {"claude_here"}  #48 (line in Coconut source)


def format_vars(vardict, max_size=float("inf"), max_len=float("inf")):  #51 (line in Coconut source)
    """Format the given locals or globals for sending to Claude."""  #52 (line in Coconut source)
    filtered_vars = {name: val for name, val in vardict.items() if not name.startswith(("__", "@", ".")) and name not in IGNORED_VARS}  #53 (line in Coconut source)

    truncated = False  #58 (line in Coconut source)
    if len(filtered_vars) > max_size:  #59 (line in Coconut source)
        filtered_vars = ((dict)((_coconut_complex_partial(random.sample, {1: max_size}, 2, ()))((tuple)((filtered_vars).items()))))  #60 (line in Coconut source)
        truncated = True  #67 (line in Coconut source)

    var_repr = repr(filtered_vars)  #69 (line in Coconut source)
    if len(var_repr) > max_len:  #70 (line in Coconut source)
        var_repr = (var_repr)[_coconut.slice(None, max_len)]  #71 (line in Coconut source)

    if truncated:  #73 (line in Coconut source)
        var_repr = var_repr.removesuffix("}") + ", <remainder truncated>}"  #74 (line in Coconut source)
    return var_repr  #75 (line in Coconut source)



def get_source(frame):  #78 (line in Coconut source)
    """Extract the source code from frame."""  #79 (line in Coconut source)
    try:  #80 (line in Coconut source)
        source_lines, source_lineno = inspect.getsourcelines(frame)  #81 (line in Coconut source)
    except OSError:  #82 (line in Coconut source)
        fake_file = io.StringIO()  #83 (line in Coconut source)
        dis(frame.f_code, file=fake_file)  #84 (line in Coconut source)
        fake_file.seek(0)  #85 (line in Coconut source)
        return (_coconut_mk_anon_namedtuple(('source_type', 'raw_source'))("dis", fake_file.read()))  #86 (line in Coconut source)
    else:  #87 (line in Coconut source)
        return (_coconut_mk_anon_namedtuple(('source_type', 'raw_source'))(None, "".join(source_lines)))  #88 (line in Coconut source)



def collect_stack_info(stack_level=1, **kwargs):  #91 (line in Coconut source)
    """Collect information about the callee site for sending to Claude."""  #92 (line in Coconut source)
    cur_frame = inspect.currentframe()  #93 (line in Coconut source)
    outer_frame = reduce(lambda frame, _: frame.f_back, range(stack_level), cur_frame)  #94 (line in Coconut source)
    return collect_frame_info("breakpoint", outer_frame, **kwargs)  #99 (line in Coconut source)



def collect_frame_info(debug_context_name, frame, extra_info=None):  #102 (line in Coconut source)
    """Collect information about the given frame for sending to Claude."""  #103 (line in Coconut source)
    frame_info = inspect.getframeinfo(frame)  #104 (line in Coconut source)
    _coconut_match_to_0 = get_source(frame)  #105 (line in Coconut source)
    _coconut_match_check_0 = False  #105 (line in Coconut source)
    _coconut_match_set_name_source_type = _coconut_sentinel  #105 (line in Coconut source)
    _coconut_match_set_name_raw_source = _coconut_sentinel  #105 (line in Coconut source)
    if (_coconut.isinstance(_coconut_match_to_0, tuple)) and (_coconut.len(_coconut_match_to_0) == 2):  #105 (line in Coconut source)
        _coconut_match_temp_2 = _coconut.getattr(_coconut_match_to_0, 'source_type', _coconut_sentinel)  #105 (line in Coconut source)
        _coconut_match_temp_3 = _coconut.getattr(_coconut_match_to_0, 'raw_source', _coconut_sentinel)  #105 (line in Coconut source)
        if (_coconut_match_temp_2 is not _coconut_sentinel) and (_coconut_match_temp_3 is not _coconut_sentinel):  #105 (line in Coconut source)
            _coconut_match_set_name_source_type = _coconut_match_temp_2  #105 (line in Coconut source)
            _coconut_match_set_name_raw_source = _coconut_match_temp_3  #105 (line in Coconut source)
            _coconut_match_check_0 = True  #105 (line in Coconut source)
    if _coconut_match_check_0:  #105 (line in Coconut source)
        if _coconut_match_set_name_source_type is not _coconut_sentinel:  #105 (line in Coconut source)
            source_type = _coconut_match_set_name_source_type  #105 (line in Coconut source)
        if _coconut_match_set_name_raw_source is not _coconut_sentinel:  #105 (line in Coconut source)
            raw_source = _coconut_match_set_name_raw_source  #105 (line in Coconut source)
    if not _coconut_match_check_0:  #105 (line in Coconut source)
        raise _coconut_MatchError('(source_type=, raw_source=) = get_source(frame)', _coconut_match_to_0)  #105 (line in Coconut source)


    verbosity = get_verbosity()  #107 (line in Coconut source)
    return DebugContext(name=debug_context_name, frame_info=frame_info, source_type=source_type, raw_source=raw_source, extra_info=((lambda _coconut_x: {} if _coconut_x is None else _coconut_x)(extra_info)) | {"locals": format_vars(frame.f_locals, max_size=verbosity * 50, max_len=verbosity * 1000), "globals": format_vars(frame.f_globals, max_size=verbosity * 5, max_len=verbosity * 100)})  #108 (line in Coconut source)



IGNORE_PACKAGES = {"claude_here", "builtins", "importlib"}  #120 (line in Coconut source)


def get_frame_package(frame):  #123 (line in Coconut source)
    """Get the package name for the given frame."""  #124 (line in Coconut source)
    return frame.f_globals.get("__package__") or frame.f_globals.get("__name__")  #125 (line in Coconut source)



def filter_traceback(orig_tb):  #128 (line in Coconut source)
    """Filter out traceback frames from claude_here."""  #129 (line in Coconut source)
    new_tb_top = orig_tb  #130 (line in Coconut source)
    while new_tb_top is not None and get_frame_package(new_tb_top.tb_frame) in IGNORE_PACKAGES:  #131 (line in Coconut source)
        new_tb_top = new_tb_top.tb_next  #132 (line in Coconut source)

    if new_tb_top is not None:  #134 (line in Coconut source)
        tb_cursor_plus_1 = new_tb_top  #135 (line in Coconut source)
        tb_cursor = tb_cursor_plus_1.tb_next  #136 (line in Coconut source)
        while tb_cursor is not None:  #137 (line in Coconut source)
            tb_cursor_minus_1 = tb_cursor.tb_next  #138 (line in Coconut source)
            if get_frame_package(tb_cursor.tb_frame) in IGNORE_PACKAGES:  #139 (line in Coconut source)
                tb_cursor_plus_1.tb_next = tb_cursor_minus_1  #140 (line in Coconut source)
                tb_cursor_plus_1, tb_cursor = (tb_cursor_plus_1, tb_cursor_minus_1)  #141 (line in Coconut source)
            else:  #145 (line in Coconut source)
                tb_cursor_plus_1, tb_cursor = (tb_cursor, tb_cursor_minus_1)  #146 (line in Coconut source)

    return new_tb_top  #151 (line in Coconut source)



def get_tb_frames(tb):  #154 (line in Coconut source)
    """Yield all the frames in the given traceback."""  #155 (line in Coconut source)
    while tb is not None:  #156 (line in Coconut source)
        yield tb.tb_frame  #157 (line in Coconut source)
        tb = (tb).tb_next  #158 (line in Coconut source)



def collect_exc_info(exc_type, exc_val, exc_tb):  #161 (line in Coconut source)
    """Collect information about the given exception for sending to Claude."""  #162 (line in Coconut source)
    filtered_tb = (lambda _coconut_x: exc_tb if _coconut_x is None else _coconut_x)(filter_traceback(exc_tb))  #163 (line in Coconut source)

    extra_info = {"traceback": (("".join)(traceback.format_exception(exc_type, exc_val, filtered_tb)))}  #165 (line in Coconut source)

    if filtered_tb is None:  #172 (line in Coconut source)
        return DebugContext(name="exception", frame_info=None, source_type=None, raw_source="", extra_info=extra_info)  #173 (line in Coconut source)

    else:  #181 (line in Coconut source)
        all_frames = (tuple)((get_tb_frames)(filtered_tb))  #182 (line in Coconut source)
        verbosity = get_verbosity()  #183 (line in Coconut source)
        for frame in all_frames[:verbosity // 2] + all_frames[-(1 + verbosity // 2):-1]:  #184 (line in Coconut source)
            collect_frame_info("exception_frame", frame)  #185 (line in Coconut source)

        return collect_frame_info("exception", all_frames[-1], extra_info)  #187 (line in Coconut source)
