import ast
import inspect
import pathlib
import sys
import textwrap
import types
import typing
from inspect import Parameter


import IPython
import dill

from .constants import EXPLORATORY_PREFIX
from .generate_tests import generate_tests
from .incrementor import Incrementor
from .utils import is_builtin_obj, CallStatistics, PredicateType


class Carver:
    def __init__(self, parsed_in, ipython, verbose):
        self.calls: dict[str, list[CallStatistics]] = dict()

        self.parsed_in: ast.AST = parsed_in
        self.ipython: IPython.InteractiveShell = ipython
        self.verbose: bool = verbose
        self.assignment_targets = None
        self.visited_function_markers: set[tuple[str, int, str]] = set()
        self.desired_function = None
        self.desired_function_marker: tuple[str, int, str] = ("", 0, "")
        self.called_function = None
        match parsed_in:
            case ast.Assign(targets=[x], value=ast.Call(func=y)):
                self.assignment_targets = ipython.ev(
                    ast.unparse(RewriteToName().visit(x))
                )
                self.called_function = ipython.ev(ast.unparse(y))

    # Start of `with` block
    def __enter__(self):
        self.original_trace_function = sys.gettrace()
        sys.settrace(self.traceit)
        return self

    # End of `with` block
    def __exit__(self, exc_type, exc_value, tb):
        sys.settrace(self.original_trace_function)

    def add_call(self, function_name, call_stats):
        """Add given call to list of calls"""
        if function_name not in self.calls:
            self.calls[function_name] = []
        self.calls[function_name].append(call_stats)

    # Tracking function: Record all calls and all args
    def traceit(self, frame: types.FrameType, event, _):
        if event != "call":
            return None
        code = frame.f_code
        function_name = code.co_name
        if function_name == "hijack_print":
            value = frame.f_locals["values"]
            if (
                isinstance(value, tuple)
                and len(value) == 2
                and value[0] == EXPLORATORY_PREFIX
            ):
                assert self.desired_function is not None
                if self.desired_function == self.called_function:
                    self.calls[self.desired_function.__qualname__][-1].appendage.extend(
                        extract_tests_from_frame(
                            value[1],
                            frame,
                            self.assignment_targets,
                            self.ipython,
                            self.verbose,
                        )
                    )
                else:
                    self.calls[self.desired_function.__qualname__][-1].appendage.extend(
                        extract_tests_from_frame(
                            value[1], frame, "ret", self.ipython, self.verbose
                        )
                    )
            return None
        function_marker = (
            code.co_filename,
            code.co_firstlineno,
            code.co_name,
        )
        if (
            self.desired_function is None
            and function_marker not in self.visited_function_markers
        ):
            self.visited_function_markers.add(function_marker)
            correct_call_checker = ContainCorrectCall()
            try:
                parsed_ast = ast.parse(textwrap.dedent(inspect.getsource(frame)))
                correct_call_checker.visit(parsed_ast)
            except Exception as e:
                pass
            if correct_call_checker.is_correct_call:
                self.desired_function = get_function_obj(frame, function_name)
                self.desired_function_marker = function_marker

        if function_marker == self.desired_function_marker:
            call_stats = get_call_statistics(frame, self.desired_function)
            self.add_call(self.desired_function.__qualname__, call_stats)
        return None

    def call_statistics(self, function_name) -> list[CallStatistics]:
        """Return a list of all arguments of the given function
        as (VAR, VALUE) pairs."""
        return self.calls.get(function_name, [])


class RewriteToName(ast.NodeTransformer):
    def visit_Name(self, node):
        return ast.Constant(node.id)


class ContainCorrectCall(ast.NodeVisitor):
    def __init__(self):
        self.is_correct_call = False

    def visit_Call(self, node):
        match node:
            case ast.Call(
                func=ast.Name(id="print"), args=[ast.Constant(value="--explore"), _]
            ):
                self.is_correct_call = True


def get_call_statistics(frame, current_function) -> CallStatistics:
    """Return call arguments in the given frame"""
    local_vars = frame.f_locals.copy()
    arguments = inspect.signature(current_function)
    predicate = determine_predicate(current_function)
    function_locals = dict()
    for key in local_vars:
        value = local_vars[key]
        function_locals[key] = extract_value(key, value)

    return CallStatistics(
        arguments.parameters,
        function_locals,
        predicate,
        [],
    )


def get_class_instance(frame):
    return eval("__class__", frame.f_globals, frame.f_locals)  # hack


def extract_value(key, value):
    try:
        if is_builtin_obj(value):
            return "DIRECT", repr(value)
        else:
            return "PICKLE", dill.dumps(value)
    except Exception as e:
        print(f"Non-serialisable local object {key} encountered; exception {e}")
        return "NO-GO", value


def determine_predicate(function) -> PredicateType:
    sourcelines = inspect.getsourcelines(function)
    first_line = sourcelines[0][0]
    if first_line.startswith("def "):
        return PredicateType.NONE
    if first_line.startswith("    @classmethod"):
        return PredicateType.CLASS
    return PredicateType.OBJECT


def get_function_obj(
    frame: types.FrameType, function_name: str
) -> types.MethodType | types.FunctionType:
    first_line = inspect.getsourcelines(frame)[0][0]
    if first_line.startswith("    "):
        # Static methods are cringe so I don't support them
        if "@classmethod" in first_line:  # please don't use classmethod()
            return getattr(frame.f_locals["cls"], function_name)
        assert "self" in frame.f_locals
        return getattr(frame.f_locals["self"], function_name)
    else:
        return frame.f_globals[function_name]


def extract_tests_from_frame(obj, frame, assignment_target_names, ipython, verbose):
    caller_frame = frame.f_back
    code_list, global_index_start = inspect.getsourcelines(caller_frame)
    parsed_ast = ast.parse(textwrap.dedent(inspect.getsource(caller_frame)))
    expression_parser = ExpressionParser(caller_frame, global_index_start)
    expression_parser.visit(parsed_ast)
    explore_expression = expression_parser.expression
    return_type_determiner = DetermineReturnType()
    return_type_determiner.visit(
        ast.parse(code_list[-1].strip())
    )  # Assuming that this is the correct deal
    name_rewriter = RewriteToName()
    ret = ipython.ev(ast.unparse(name_rewriter.visit(return_type_determiner.ret)))
    name_replacements = match_return_with_assignment(assignment_target_names, ret)
    reparsed_var_expression = ast.parse(explore_expression)
    name_replacer = ReplaceNames(name_replacements)
    var_name = ast.unparse(name_replacer.visit(reparsed_var_expression))
    return generate_tests(obj, var_name, ipython, verbose)


def match_return_with_assignment(
    assign_to: str | tuple[typing.Any] | list[typing.Any],
    return_from: str | tuple[typing.Any] | list[typing.Any],
) -> dict[str, str]:
    match assign_to, return_from:
        case str(), str():
            return {return_from: assign_to}
        case str(), _:
            result = dict()
            for i, sub_ret in enumerate(return_from):
                result[sub_ret] = f"{assign_to}[{i}]"
            return result
        case _, str():
            return {return_from: f"({', '.join(assign_to)})"}
        case _, _:
            result = dict()
            for sub_assign, sub_ret in zip(assign_to, return_from):
                result.update(match_return_with_assignment(sub_assign, sub_ret))
            return result


class ExpressionParser(ast.NodeVisitor):
    def __init__(self, caller_frame: types.FrameType, global_index_start: int):
        self.expression: str = ""
        self.caller_frame: types.FrameType = caller_frame
        self.lineno: int = caller_frame.f_lineno - global_index_start + 1
        self.stack: dict[str, tuple[str, str]] = dict()

    def visit_For(
        self, node
    ):  # method is quite scuffed. There's quite a load of ways ppl can write scuffed
        if not (
            node.lineno <= self.lineno <= node.end_lineno
        ):  # The loop actually contains the desired print statement
            self.generic_visit(node)
            return
        self.stack.update(
            extract_loop_params(node.target, node.iter, self.caller_frame, -1)
        )
        self.generic_visit(node)

    def visit_Call(self, node):
        if node.lineno == self.lineno and getattr(node.func, "id", "") == "print":
            name_replacer = ReplaceNamesWithSuffix(self.stack)
            parsed_obj_name = name_replacer.visit(node.args[1])
            self.expression = ast.unparse(parsed_obj_name)


def extract_loop_params(
    target_node: ast.expr,
    iterator_node: ast.expr,
    caller_frame: types.FrameType,
    override_index: int,
) -> dict[str, tuple[str, str]]:
    match target_node, iterator_node:
        case (ast.Name(), ast.Call(func=ast.Name(id="range"))):
            return {
                target_node.id: (
                    repr(
                        eval(
                            target_node.id,
                            caller_frame.f_globals,
                            caller_frame.f_locals,
                        )
                    ),
                    "",
                )
            }
        case (ast.Name(), _):
            unparsed_iterator = ast.unparse(iterator_node)
            evaluated_iterator = eval(
                unparsed_iterator, caller_frame.f_globals, caller_frame.f_locals
            )
            obj = eval(
                target_node.id,
                caller_frame.f_globals,
                caller_frame.f_locals,
            )
            if isinstance(evaluated_iterator, dict):
                return {target_node.id: (f"{repr(obj)}", "")}
            if isinstance(evaluated_iterator, typing.Sequence):
                if override_index == -1:
                    index = evaluated_iterator.index(obj)
                else:
                    index = override_index
                return {
                    target_node.id: (
                        f"{unparsed_iterator}",
                        f"[{index}]",  # TODO: support nonunique lists
                    )
                }

            try:  # handles sets, hopefully
                iterator_node_list = list(evaluated_iterator)
                if override_index == -1:
                    index = iterator_node_list.index(obj)
                else:
                    index = override_index
                return {
                    target_node.id: (
                        f"list({unparsed_iterator})",
                        f"[{index}]",  # TODO: support nonunique lists
                    )
                }
            except Exception:
                pass
            return dict()
        case (ast.Tuple() | ast.List(), ast.Call(func=ast.Attribute(attr="items"))):
            key, value_node = target_node.elts
            key_str = eval(
                ast.unparse(key),
                caller_frame.f_globals,
                caller_frame.f_locals,
            )
            return {
                key.id: (f"{repr(key_str)}", ""),
                value_node.id: (
                    f"{ast.unparse(iterator_node.func.value)}",
                    f"[{repr(key_str)}]",
                ),
            }
        case (ast.Tuple() | ast.List(), ast.Call(func=ast.Name(id="enumerate"))):
            index_node, value_node = target_node.elts
            index_num = eval(
                ast.unparse(index_node),
                caller_frame.f_globals,
                caller_frame.f_locals,
            )
            result = {index_node.id: (f"{index_num}", "")}
            result.update(
                extract_loop_params(
                    value_node, iterator_node.args[0], caller_frame, index_num
                )
            )
            return result
        case (ast.Tuple() | ast.List(), ast.Call(func=ast.Name(id="zip"))):
            assert isinstance(target_node, ast.Tuple)
            assert len(target_node.elts) == len(iterator_node.args)
            result = dict()
            for item, item_list in zip(target_node.elts, iterator_node.args):
                result.update(
                    extract_loop_params(item, item_list, caller_frame, override_index)
                )
            return result
        case _:
            raise Exception("unhandled", ast.dump(target_node), ast.dump(iterator_node))


class ReplaceNames(ast.NodeTransformer):
    def __init__(self, names: dict[str, str]):
        self.names = names

    def visit_Name(self, node):
        temp_id = node.id
        if temp_id in self.names:
            temp_id = self.names[temp_id]
        node.id = temp_id
        return node


class ReplaceNamesWithSuffix(ast.NodeTransformer):
    def __init__(self, names: dict[str, tuple[str, str]]):
        self.names = names

    def visit_Name(self, node):
        temp_id = node.id
        suffixes = []
        while temp_id in self.names:
            temp_id, suffix = self.names.get(temp_id)
            suffixes.append(suffix)
        suffixes.reverse()
        if len(temp_id) >= 2 and temp_id[0] == temp_id[-1] == "'":
            temp_id = temp_id[0] + temp_id[1:-1] + temp_id[-1]  # sanitize string
        for suf in suffixes:
            temp_id += suf
        node.id = temp_id
        return node


class DetermineReturnType(ast.NodeVisitor):
    def __init__(self):
        self.ret = None

    def visit_Return(self, node):
        self.ret = node.value


def add_call_string(
    function_name, stat: CallStatistics, ipython, dest, line, incrementor
) -> tuple[str, list[str]]:
    """Return function_name(arg[0], arg[1], ...) as a string, pickling complex objects
    function call, setup
    """
    setup_code = []
    arglist = []
    if stat.predicate == PredicateType.OBJECT:
        value, setup = call_value_wrapper(
            stat.locals["self"], ipython, line, incrementor, dest
        )
        setup_code.extend(setup)
        function_name = value + "." + function_name
    elif stat.predicate == PredicateType.CLASS:
        value, setup = call_value_wrapper(
            stat.locals["cls"], ipython, line, incrementor, dest
        )
        setup_code.extend(setup)
        function_name = value + "." + function_name
    for (
        param_name,
        param_obj,
    ) in stat.parameters.items():  # note: well-order is guaranteed
        if param_name in ["/", "*"]:
            continue
        match param_obj.kind:
            case Parameter.POSITIONAL_ONLY:
                value, setup = call_value_wrapper(
                    stat.locals[param_name], ipython, line, incrementor, dest
                )
                setup_code.extend(setup)
                arglist.append(value)
            case Parameter.KEYWORD_ONLY | Parameter.POSITIONAL_OR_KEYWORD:
                value, setup = call_value_wrapper(
                    stat.locals[param_name], ipython, line, incrementor, dest
                )
                setup_code.extend(setup)
                arglist.append(f"{param_name}={value}")
            case Parameter.VAR_POSITIONAL:
                for arg_name in stat.locals[param_name]:
                    value, setup = call_value_wrapper(
                        stat.locals[arg_name], ipython, line, incrementor, dest
                    )
                    setup_code.extend(setup)
                    arglist.append(value)
            case Parameter.VAR_KEYWORD:
                for arg_name in stat.locals[param_name]:
                    value, setup = call_value_wrapper(
                        stat.locals[arg_name], ipython, line, incrementor, dest
                    )
                    setup_code.extend(setup)
                    arglist.append(f"{arg_name}={value}")
    return f"{function_name}({', '.join(arglist)})", setup_code


def call_value_wrapper(
    argument,
    ipython: IPython.InteractiveShell,
    line: int,
    incrementor: Incrementor,
    dest,
) -> tuple[str, list[str]]:
    mode, representation = argument
    varname = f"line{line}_arg{incrementor.get_next_counter()}"
    if mode == "DIRECT":
        return representation, []
    if mode == "PICKLE":
        unpickled = dill.loads(representation)
        for key in ipython.user_ns:
            obj = ipython.user_ns[key]
            if type(unpickled) is type(obj) and obj == unpickled:
                return key, []
        pathlib.Path(dest).mkdir(parents=True, exist_ok=True)
        full_path = f"{dest}/{varname}"
        with open(full_path, "wb") as f:
            f.write(representation)
        setup_code = [
            f"with open('{full_path}', 'rb') as f: \n    {varname} = pickle.load(f)"
        ]
        setup_code.extend(generate_tests(unpickled, varname, ipython, False))
        return varname, setup_code
    return repr(representation), []
