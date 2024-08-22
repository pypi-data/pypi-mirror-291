from contextlib import contextmanager
from dataclasses import dataclass, field, replace
from functools import partial
from typing import Any, Callable, ClassVar, Generator

from beet import Context, DataPack
from beet import Generator as BeetGenerator
from beet import JsonFile, NamespaceFileScope
from beet.core.utils import required_field
from bolt import Runtime
from bolt_control_flow import BranchInfo, Case, CaseResult, WrappedCases
from mecha import (
    AstChildren,
    AstCommand,
    AstCommandSentinel,
    AstNode,
    AstRoot,
    Diagnostic,
    Mecha,
    MutatingReducer,
    Serializer,
    Visitor,
    rule,
)
from tokenstream import set_location


# the plugin entrypoint that gets called when
# the plugin is required in a pipeline
def apoli(ctx: Context):
    """The Apoli plugin."""
    ctx.require("bolt_control_flow")

    # register power data pack resource
    ctx.data.extend_namespace.append(PowerFile)

    mecha = ctx.inject(Mecha)

    # extend mecha transform with the Apoli transformer
    converter = ApoliJsonConverter(serialize=mecha.serialize)
    mecha.transform.extend(
        ApoliTransformer(generate=ctx.generate, pack=ctx.data, converter=converter)
    )

beet_default = apoli

class PowerFile(JsonFile):
    """Class representing a power file."""

    scope: ClassVar[NamespaceFileScope] = ("powers",)
    extension: ClassVar[str] = ".json"


# the command ast nodes that keep apoli-specific ast.
# sentinel commands are useful for storing data that is processed
# in later compilation steps and does not emit any command directly in
# the output pack
@dataclass(frozen=True, kw_only=True)
class AstApoliCommand(AstCommandSentinel):
    arguments: AstChildren["AstApoliAction"] = AstChildren()

@dataclass(frozen=True, kw_only=True)
class AstApoliPowerCommand(AstApoliCommand):
    resource_location: str
    arguments: AstChildren["AstApoliPower"] = AstChildren()  # type: ignore


# apoli ast nodes wrapped by AstApoliCommand sentinel

@dataclass(frozen=True, kw_only=True)
class AstApoliCondition(AstNode):
    type: str
    negated: bool = False


@dataclass(frozen=True, kw_only=True)
class AstApoliConstant(AstApoliCondition):
    type: str = field(default="apoli:constant", init=False)
    value: Any


@dataclass(frozen=True, kw_only=True)
class AstApoliPower(AstNode):
    type: str
    entity_action: "AstApoliAction"


@dataclass(frozen=True, kw_only=True)
class AstApoliAction(AstNode):
    type: str


@dataclass(frozen=True, kw_only=True)
class AstApoliExecuteCommand(AstApoliAction):
    type: str = field(default="apoli:execute_command", init=False)
    command: AstCommand


@dataclass(frozen=True, kw_only=True)
class AstApoliAnd(AstApoliAction):
    type: str = field(default="apoli:and", init=False)
    actions: AstChildren[AstApoliAction]


@dataclass(frozen=True, kw_only=True)
class AstApoliIfElifElseCase(AstNode):
    condition: AstApoliCondition
    action: AstApoliAction


@dataclass(frozen=True, kw_only=True)
class AstApoliIfElifElse(AstApoliAction):
    type: str = field(default="apoli:if_elif_else", init=False)
    actions: AstChildren[AstApoliIfElifElseCase]


@dataclass(frozen=True, kw_only=True)
class AstApoliIfElse(AstApoliAction):
    type: str = field(default="apoli:if_else", init=False)
    condition: AstApoliCondition
    if_action: AstApoliAction
    else_action: AstApoliAction | None = None


def unwrap_action(commands: AstChildren[AstCommand]) -> AstApoliAction:
    """Takes a list of commands and returns the equivalent apoli action"""
    # return the single nested apoli action
    if len(commands) == 1 and isinstance(command := commands[0], AstApoliCommand):
        return command.arguments[0]
    # turns a list of commands that contain both normal commands and
    # apoli sentinel commands into an apoli:and action.
    #
    # adjacent commands are clumped together into a single apoli:execute_command action,
    # while each apoli command sentinel becomes a separate action.
    if any(isinstance(command, AstApoliCommand) for command in commands):
        parts: list[list[AstCommand]] = [[]]

        # splits the commands so that apoli sentinel commands are separated
        # from normal commands
        for command in commands:
            if isinstance(command, AstApoliCommand):
                parts.append([command])
                parts.append([])
            else:
                parts[-1].append(command)

        if len(parts) > 1:
            parts = [cmds for cmds in parts if len(cmds)]

        # wrap each child action individually
        return AstApoliAnd(
            actions=AstChildren(unwrap_action(AstChildren(cmds)) for cmds in parts)
        )

    # create a apoli:execute_command if there are only normal commands
    #
    # this is a trick for wrapping the ast root in a "execute run: ..." command
    # and letting the mecha.contrib.nesting plugin either inline single-commands or
    # create an anonymous function
    return AstApoliExecuteCommand(
        command=AstCommand(
            identifier="execute:subcommand",
            arguments=AstChildren(
                (
                    AstCommand(
                        identifier="execute:commands",
                        arguments=AstChildren((AstRoot(commands=commands),)),
                    ),
                )
            ),
        )
    )

# The main class for interacting with apoli conditions.
#
# Implements `__not__`, `__branch__` and `__multibranch__`
# which overloads the default behaviour of bolt syntax.
# Additionally, `__logical_and__` and `__logical_or__` could also be overloaded.
#
# `__branch__` and `__multibranch__`, when called, emit the sentinel commands to
# temporarily store the generated apoli ast.
@dataclass
class Condition:
    ctx: Context = field(repr=False)
    type: str
    negated: bool = False

    @property
    def runtime(self):
        return self.ctx.inject(Runtime)

    def to_ast(self) -> AstApoliCondition:
        return AstApoliCondition(type=self.type, negated=self.negated)

    def __not__(self):
        return replace(self, negated=not self.negated)

    @contextmanager
    def __branch__(self):
        with self.runtime.scope() as cmds:
            yield True

        if_action = unwrap_action(AstChildren(cmds))

        action = AstApoliIfElse(condition=self.to_ast(), if_action=if_action)
        command = AstApoliCommand(arguments=AstChildren((action,)))

        self.runtime.commands.append(command)

    @contextmanager
    def __multibranch__(self, info: BranchInfo):
        case = ActionIfElseCase(self.ctx)
        yield case

        if_action = unwrap_action(case.if_commands)
        else_action = unwrap_action(case.else_commands)

        # this produces nested apoli:if_else actions. you could check if `else_action`
        # is AstApolifIfElse or AstApoliIfElifElse node and flatten all cases into
        # a single AstApoliIfElifElse node. this could also be done in ApoliTransformer
        # as a separate rule.
        action = AstApoliIfElse(
            condition=self.to_ast(), if_action=if_action, else_action=else_action
        )
        command = AstApoliCommand(arguments=AstChildren((action,)))
        self.runtime.commands.append(command)

# this is necessary for catching the if and else body commands
# using the bolt-control-flow mechanism
@dataclass
class ActionIfElseCase(WrappedCases):
    ctx: Context = field(repr=False)

    if_commands: AstChildren[AstCommand] = AstChildren()
    else_commands: AstChildren[AstCommand] = AstChildren()

    @contextmanager
    def __case__(self, case: Case):
        runtime = self.ctx.inject(Runtime)

        with runtime.scope() as cmds:
            yield CaseResult.maybe()

        commands = AstChildren(cmds)

        if case:
            self.if_commands = commands
        else:
            self.else_commands = commands


# this class implements the power decorator functionality
# decorating a function with 'power' calls the function immediately,
# wrapping the produced commands into a AstApoliPowerCommand node
# that gets transformed later
@dataclass
class Power:
    ctx: Context

    @property
    def runtime(self):
        return self.ctx.inject(Runtime)

    def decorate(self, type: str, path: str | None, f: Callable[[], None]):
        # generate default path if not provided
        if path is None:
            name = f.__name__
            path = self.ctx.generate.path(name)

        # collect commands generated from the function
        with self.runtime.scope() as cmds:
            f()

        action = unwrap_action(AstChildren(cmds))
        power = AstApoliPower(type=type, entity_action=action)
        command = AstApoliPowerCommand(
            resource_location=path, arguments=AstChildren((power,))
        )
        self.runtime.commands.append(command)
        return f

    def __call__(self, type: str, path: str | None = None):
        return partial(self.decorate, type, path)


@dataclass
class ApoliTransformer(MutatingReducer):
    """
    Transformer for Apoli commands.

    Traverses the child commands of nested root, filters out Apoli commands
    and emits power resource files.
    """

    generate: BeetGenerator = required_field()
    pack: DataPack = required_field()
    converter: "ApoliJsonConverter" = required_field()

    @rule(AstRoot)
    def apoli_command(self, node: AstRoot) -> Generator[Any, Any, Any]:
        commands: list[AstCommand] = []
        changed = False

        for command in node.commands:
            # don't touch commands that are not from this plugin
            if not isinstance(command, AstApoliCommand):
                commands.append(command)
                continue

            # prevent the user from using apoli actions in functions/command roots.
            # the error location is not precise though
            #
            # if possible, this could actually produce some anonymous power and
            # directly up trigger it using a command, kinda like how anonymous functions work
            if not isinstance(command, AstApoliPowerCommand):
                yield set_location(
                    Diagnostic("error", "Invalid Apoli command outside of power root."),
                    location=node.location,
                    end_location=node.location,
                )
                continue

            changed = True

            power_ast = command.arguments[0]
            json = self.converter(power_ast)
            # generates a power file at the specified location
            # with the generated json as contents
            self.generate(command.resource_location, PowerFile(json))
        if changed:
            node = replace(node, commands=AstChildren(commands))

        return node


@dataclass
class ApoliJsonConverter(Visitor):
    """Converts Apoli AST to JSON."""

    serialize: Serializer = required_field()

    @rule(AstApoliPower)
    def power(self, node: AstApoliPower) -> Generator[AstNode, Any, Any]:
        entity_action = yield node.entity_action

        return {"type": node.type, "entity_action": entity_action}

    @rule(AstApoliAction)
    def action(self, node: AstApoliAction) -> Any:
        return {
            "type": node.type,
        }

    @rule(AstApoliIfElse)
    def if_else(self, node: AstApoliIfElse) -> Generator[AstNode, Any, Any]:
        condition = yield node.condition
        if_action = yield node.if_action

        result = {
            "condition": condition,
            "if_action": if_action,
        }

        if not node.else_action:
            return result

        else_action = yield node.else_action

        return {
            **result,
            "else_action": else_action,
        }

    @rule(AstApoliCondition)
    def condition(self, node: AstApoliCondition) -> Any:
        return {"type": node.type, "negated": node.negated}

    @rule(AstApoliConstant)
    def constant(self, node: AstApoliConstant) -> Any:
        return {"type": node.type, "value": node.value}

    @rule(AstApoliExecuteCommand)
    def execute_command(self, node: AstApoliExecuteCommand) -> Any:
        command = self.serialize(node.command)

        return {"type": node.type, "command": command}

    @rule(AstApoliIfElifElseCase)
    def if_elif_else_case(
            self, node: AstApoliIfElifElseCase
    ) -> Generator[AstNode, Any, Any]:
        condition = yield node.condition
        action = yield node.action

        return {
            "condition": condition,
            "action": action,
        }

    @rule(AstApoliIfElifElse)
    def if_elif_else(self, node: AstApoliIfElifElse) -> Generator[AstNode, Any, Any]:
        cases: list[Any] = []

        for case in node.actions:
            case_result = yield case
            cases.append(case_result)

        return {"type": node.type, "actions": cases}

    @rule(AstApoliAnd)
    def and_action(self, node: AstApoliAnd) -> Generator[AstNode, Any, Any]:
        actions: list[Any] = []

        for action in node.actions:
            action_result = yield action
            actions.append(action_result)

        return {"type": node.type, "actions": actions}
