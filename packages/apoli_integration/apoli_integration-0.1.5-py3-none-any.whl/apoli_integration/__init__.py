from contextlib import contextmanager
from dataclasses import dataclass, field, replace
from functools import partial
from pathlib import Path
from typing import Any, Callable, ClassVar, Generator, List
from enum import Enum

from beet import Context, DataPack
from beet import Generator as BeetGenerator
from beet import JsonFile, NamespaceFileScope
from beet.core.utils import required_field
from bolt import Runtime
from bolt_control_flow import BranchInfo, Case, CaseResult, WrappedCases
from colorama import init
from mecha import (
    AstChildren,
    AstCommand,
    AstCommandSentinel,
    AstJson,
    AstLiteral,
    AstNode,
    AstRoot,
    AstString,
    Diagnostic,
    Mecha,
    MutatingReducer,
    Serializer,
    Visitor,
    rule,
)
from tokenstream import set_location

RED = "\033[91m"
STANDARD_BLUE = "\033[34m"
BLUE = "\033[36m"
LIGHT_GREY = "\033[37m"
DARK_GREY = "\033[90m"
RESET = "\033[0m"

def getError(file_path, error_text, line_number, column_number, line_texts):
    current_file = Path(__file__).stem
    return f"""{RED}ERROR  |{RESET} {DARK_GREY}{current_file}{RESET}  {RED}{error_text}{RESET}
       {RED}|{RESET} {BLUE}{file_path}:{line_number}:{column_number}{RESET}
       {RED}|{RESET}     {line_number-1} |      {line_texts[0]}
       {RED}|{RESET}     {line_number} |      {line_texts[1]} 
       {RED}|{RESET}     {" " * len(str(line_number))} : {' ' * (column_number - 1)} ^{'^' * (len("test text") - 1)}
       {RED}|{RESET}     {line_number+1} |      {line_texts[2]}
       
"""


#print(getError("src\data\\test\\functions\main.mcfunction", "Identifier \"description\" is not defined.", 13, 5, ['name={"text": "whoop!",','description="StonTest",','condition=entity.is_sneaking() and entity.is_on_fire(),']))

class EquipmentSlot(Enum):
    MAINHAND = "mainhand"
    OFFHAND = "offhand"
    HEAD = "head"
    CHEST = "chest"
    LEGS = "legs"
    FEET = "feet"

# the plugin entrypoint that gets called when
# the plugin is required in a pipeline
def apoli(ctx: Context):
    init()
    """The Apoli plugin."""
    ctx.require("bolt_control_flow")

    # register power data pack resource
    ctx.data.extend_namespace.append(PowerFile)
    runtime = ctx.inject(Runtime)
    mc = ctx.inject(Mecha)

    runtime.globals["entity"] = Entity(ctx)
    runtime.globals["power"] = Power(ctx)
    runtime.globals["MetaUtils"] = MetaUtils(ctx)
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

#region AST Nodes
# the command ast nodes that keep apoli-specific ast.
# sentinel commands are useful for storing data that is processed
# in later compilation steps and does not emit any command directly in
# the output pack
@dataclass(frozen=True, kw_only=True)
class AstApoliCommand(AstCommandSentinel):
    arguments: AstChildren["AstApoliTypedObject"] = AstChildren()

@dataclass(frozen=True, kw_only=True)
class AstApoliPowerCommand(AstApoliCommand):
    resource_location: str
    arguments: AstChildren["AstApoliPower"] = AstChildren()

@dataclass(frozen=True, kw_only=True)
class AstApoliField(AstNode):
    key: str
    value: AstNode

@dataclass(frozen=True, kw_only=True)
class AstApoliTypedObject(AstNode):
    type: str
    fields: AstChildren[AstApoliField] = AstChildren()

@dataclass(frozen=True, kw_only=True)
class AstApoliPower(AstApoliTypedObject):
    file_name: str
    file_subname: str
    type: str
    name: str
    description: str
    condition: "AstApoliCondition"

@dataclass(frozen=True, kw_only=True)
class AstApoliMultiplePower(AstApoliPower):
    pass

@dataclass(frozen=True, kw_only=True)
class AstApoliCondition(AstApoliTypedObject):
    type: str
    inverted: bool = False

@dataclass(frozen=True, kw_only=True)
class AstApoliAction(AstApoliTypedObject):
    type: str

@dataclass(frozen=True, kw_only=True)
class AstApoliLiteral(AstNode):
    value: Any

#endregion

def create_action(type: str, **fields: Any) -> AstApoliAction:
    ast_fields = AstChildren(
        AstApoliField(
            key=key,
            value=AstApoliLiteral(value=value)
            if not isinstance(value, AstNode)
            else value,
        )
        for key, value in fields.items()
    )
    return AstApoliAction(type=type, fields=ast_fields)

def create_condition(ctx: Context, type: str, inverted: bool = False, **fields: Any) -> AstApoliAction:
    ast_fields = AstChildren(
        AstApoliField(
            key=key,
            value=AstApoliLiteral(value=value)
            if not isinstance(value, AstNode)
            else value,
        )
        for key, value in fields.items()
    )
    return Condition(ctx=ctx, type=type, inverted=inverted, fields=ast_fields)

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
        return create_action(type="apoli:and",actions=AstChildren(unwrap_action(AstChildren(cmds)) for cmds in parts)
        )

    # create a apoli:execute_command if there are only normal commands
    #
    # this is a trick for wrapping the ast root in a "execute run: ..." command
    # and letting the mecha.contrib.nesting plugin either inline single-commands or
    # create an anonymous function
    if len(commands) == 0:
        return None
    return create_action(type="execute_command",
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
    fields: AstChildren[AstApoliField]
    inverted: bool = False

    @property
    def runtime(self):
        return self.ctx.inject(Runtime)

    def to_ast(self) -> AstApoliCondition:
        return AstApoliCondition(type=self.type, inverted=self.inverted,fields=self.fields)

    def __logical_and__(self, other):
        return create_condition(self.ctx, type="apoli:and", conditions=[self.to_ast(), other().to_ast()])
    
    def __logical_or__(self, other):
        return create_condition(self.ctx, type="apoli:or", conditions=[self.to_ast(), other().to_ast()])

    def __not__(self):
        return replace(self, negated=not self.inverted)

    @contextmanager
    def __branch__(self):
        with self.runtime.scope() as cmds:
            yield True

        if_action = unwrap_action(AstChildren(cmds))

        action = create_action(type="apoli:if_else",condition=self.to_ast(), if_action=if_action)
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
        action = create_action(type="apoli:if_else",
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

@dataclass
class BaseType:
    ctx: Context
    def emit_apoli_action(self, action: AstApoliAction):
        runtime = self.ctx.inject(Runtime)
        command = AstApoliCommand(arguments=AstChildren((action,)))
        runtime.commands.append(command)

@dataclass
class Resource:
    ctx: Context
    id: str
    #region Resource Equalities
    def __eq__(self, other):
        if isinstance(other, int):
            comparison = "=="
            return create_condition(ctx=self.ctx, type="apoli:resource", resource=self.id, comparison=comparison, compare_to=other)
    def __ne__(self, other):
        if isinstance(other, int):
            comparison = "!="
            return create_condition(ctx=self.ctx, type="apoli:resource", resource=self.id, comparison=comparison, compare_to=other)
    def __lt__(self, other):
        if isinstance(other, int):
            comparison = "<"
            return create_condition(ctx=self.ctx, type="apoli:resource", resource=self.id, comparison=comparison, compare_to=other)
    def __le__(self, other):
        if isinstance(other, int):
            comparison = "<="
            return create_condition(ctx=self.ctx, type="apoli:resource", resource=self.id, comparison=comparison, compare_to=other)
    def __gt__(self, other):
        if isinstance(other, int):
            comparison = ">"
            return create_condition(ctx=self.ctx, type="apoli:resource", resource=self.id, comparison=comparison, compare_to=other)
    def __ge__(self, other):
        if isinstance(other, int):
            comparison = ">="
            return create_condition(ctx=self.ctx, type="apoli:resource", resource=self.id, comparison=comparison, compare_to=other)
    #endregion

class MetaUtils(BaseType):
    def __init__(self, ctx: Context):
        self.ctx = ctx
        self.runtime = self.ctx.inject(Runtime)

    @contextmanager
    def sleep(self, ticks: int):
        with self.runtime.scope() as cmds:
            yield True
        self.emit_apoli_action(create_action(type="apoli:delay",ticks=ticks,action=unwrap_action(AstChildren(cmds))))

@dataclass
class Item(BaseType):
    ctx: Context
    equipment_slot: EquipmentSlot
    def get_amount(self):
        return self
    
    def damage(self, amount: int = 1, ignore_unbreaking: bool = False):
        self.emit_apoli_action(create_action(type="apoli:equipped_item_action", equipment_slot=self.equipment_slot,action=create_action(type="apoli:damage", amount=amount, ignore_unbreaking=ignore_unbreaking)))

    #region Item Equalities
    def __eq__(self, other):
        if isinstance(other, int):
            comparison = "=="
            compare_to = other
            return create_condition(ctx=self.ctx, type="apoli:equipped_item", equipment_slot=self.equipment_slot,item_condition=create_condition(ctx=self.ctx, type="apoli:amount", comparison=comparison, compare_to=compare_to))
    def __ne__(self, other):
        if isinstance(other, int):
            comparison = "!="
            compare_to = other
            return create_condition(ctx=self.ctx, type="apoli:equipped_item", equipment_slot=self.equipment_slot,item_condition=create_condition(ctx=self.ctx, type="apoli:amount", comparison=comparison, compare_to=compare_to))
    def __lt__(self, other):
        if isinstance(other, int):
            comparison = "<"
            compare_to = other
            return create_condition(ctx=self.ctx, type="apoli:equipped_item", equipment_slot=self.equipment_slot,item_condition=create_condition(ctx=self.ctx, type="apoli:amount", comparison=comparison, compare_to=compare_to))
    def __le__(self, other):
        if isinstance(other, int):
            comparison = "<="
            compare_to = other
            return create_condition(ctx=self.ctx, type="apoli:equipped_item", equipment_slot=self.equipment_slot,item_condition=create_condition(ctx=self.ctx, type="apoli:amount", comparison=comparison, compare_to=compare_to))
    def __gt__(self, other):
        if isinstance(other, int):
            comparison = ">"
            compare_to = other
            return create_condition(ctx=self.ctx, type="apoli:equipped_item", equipment_slot=self.equipment_slot,item_condition=create_condition(ctx=self.ctx, type="apoli:amount", comparison=comparison, compare_to=compare_to))
    def __ge__(self, other):
        if isinstance(other, int):
            comparison = ">="
            compare_to = other
            return create_condition(ctx=self.ctx, type="apoli:equipped_item", equipment_slot=self.equipment_slot,item_condition=create_condition(ctx=self.ctx, type="apoli:amount", comparison=comparison, compare_to=compare_to))
    #endregion

@dataclass
class Entity(BaseType):
    ctx: Context
    
    def is_sneaking(self):
        return create_condition(ctx=self.ctx, type="apoli:sneaking")
    
    def is_on_fire(self):
        return create_condition(ctx=self.ctx, type="apoli:on_fire")
    
    def evaluate_command(self, command: str, comparison: str, compare_to: int):
        return create_condition(ctx=self.ctx, type="apoli:command", command=command, compare_to=compare_to, comparison=comparison)
    
    def get_item(self, equipment_slot: EquipmentSlot):
        return Item(self.ctx, equipment_slot=equipment_slot)

    def get_resource_value(self, id: str):
        return Resource(self.ctx, id)
    
    def set_resource_value(self, id: str, change: int):
        return self.emit_apoli_action(create_action(type="apoli:change_resource",resource=id,change=change,operation="set"))
    
    def add_resource_value(self, id: str, change: int):
        return self.emit_apoli_action(create_action(type="apoli:change_resource",resource=id,change=change,operation="add"))
    
    def trigger_cooldown(self, power: str):
        return self.emit_apoli_action(create_action(type="apoli:trigger_cooldown",power=power))
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

    def decorate(self, type_field: str, path: str | None, name, description, condition, fields, f: Callable[[], None]):
        # generate default path if not provided
        if path is None:
            pname = f.__name__
            path = self.ctx.generate.path(pname)

        # collect commands generated from the function
        with self.runtime.scope() as cmds:
            f()
        
        file_subname = path.split(":")[1]
        file_name = self.runtime.get_nested_location()
        
        # TODO: ADD A WAY TO GET ALL ACTIONS FOR POWERS.

        entity_action = unwrap_action(AstChildren(cmds))
        if entity_action is not None:
            fields["entity_action"] = entity_action
        power = create_power(file_name=file_name, file_subname=file_subname,type=type_field, condition=condition,name=name, description=description, **fields)
        command = AstApoliPowerCommand(resource_location=path, arguments=AstChildren((power,)))
        self.runtime.commands.append(command)
        return f

    def __call__(self, type: str, path: str | None = None, condition: Condition | None = None, name: str | AstJson = "", description: str | AstJson = "", **fields: Any):
        return partial(self.decorate, type, path, name, description, condition, fields)

def create_multiple(type: str, **fields: Any) -> AstApoliMultiplePower:
    ast_fields = AstChildren(
        AstApoliField(
            key=key,
            value=AstApoliLiteral(value=value)
            if not isinstance(value, AstNode)
            else value,
        )
        for key, value in fields.items()
    )
    file_name, file_subname, name, description = "", "", "", ""
    element = list(fields.items())[0][1]
    if isinstance(element, AstChildren):
        for child in element:
            for power in child:
                if isinstance(power, AstApoliPower):
                    file_name, file_subname, name, description = power.file_name, power.file_subname, power.name, power.description
    return AstApoliMultiplePower(type=type,file_name=file_name, file_subname=file_subname, name=name, description=description, condition=None, fields=ast_fields)

def create_power(file_name: str, file_subname: str, type: str, name, description, condition = None, **fields: Any) -> AstApoliAction:
    ast_fields = AstChildren(
        AstApoliField(
            key=key,
            value=AstApoliLiteral(value=value)
            if not isinstance(value, AstNode)
            else value,
        )
        for key, value in fields.items()
    )
    return AstApoliPower(file_name=file_name, file_subname=file_subname, type=type, name=name, description=description, condition=condition, fields=ast_fields)

#region Transformer
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


        power_asts = []

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
            
            if len(node.commands) > 1:
                power_ast = command.arguments[0]
                if not isinstance(power_ast, AstApoliMultiplePower):
                    power_asts.append(power_ast)
            else:
                power_ast = command.arguments[0]
                json = self.converter(power_ast)
                self.generate(command.resource_location, PowerFile(json))
            # generates a power file at the specified location
            # with the generated json as contents
            
        if len(power_asts) > 0:
            power_metadata = power_asts[0]
            if isinstance(power_metadata, AstApoliPower) and not isinstance(power_metadata, AstApoliMultiplePower):
                power_ast = create_multiple(type="apoli:multiple",fields=AstChildren((power_asts,)))
                json = self.converter(power_ast)
                self.generate(power_ast.file_name, PowerFile(json))
        if changed:
            node = replace(node, commands=AstChildren(commands))

        return node
#endregion

#region Json Converter
@dataclass
class ApoliJsonConverter(Visitor):
    """Converts Apoli AST to JSON."""

    serialize: Serializer = required_field()

    def build_dict(self, node: AstApoliTypedObject):
        base_dict = {"type": node.type}
        for field in node.fields:
            if isinstance(field, AstApoliField):
                if isinstance(field.value, AstCommand):
                    base_dict[field.key] = self.serialize(field.value)
                elif isinstance(field.value, AstApoliLiteral):
                    base_dict[field.key] = self.literal(self, field.value)
                elif isinstance(field.value, AstApoliTypedObject):
                    base_dict[field.key] = self.build_dict(field.value)
                else:
                    base_dict[field.key] = field.value
        return base_dict

    @rule(AstApoliMultiplePower)
    def multiple_power(self, node: AstApoliMultiplePower) -> Generator[AstNode, Any, Any]:
        base_power = {"type": node.type}
        #base_power = self.build_dict(node)
        name, description = "", ""
        for child in node.fields:
            if isinstance(child, AstApoliField):
                if isinstance(child.value, AstApoliLiteral):
                    for power in child.value.value:
                        for subpower in power:
                            if isinstance(subpower, AstApoliPower):
                                base_power[subpower.file_subname] = self.build_dict(subpower)
                                if subpower.condition is not None:
                                    condition = yield subpower.condition.to_ast()
                                    base_power[subpower.file_subname]["condition"] = condition
                                if name == "" and description == "":
                                    name, description = subpower.name, subpower.description
        if name == "" and description == "":
            base_power["hidden"] = True
        if name != "":
            base_power["name"] = name
        if description != "":
            base_power["description"] = description
        return base_power

    @rule(AstApoliPower)
    def power(self, node: AstApoliPower) -> Generator[AstNode, Any, Any]:
        base_power = self.build_dict(node)
        if node.condition is not None:
            condition = yield node.condition.to_ast()
            if condition is not None:
                base_power["condition"] = condition
        if node.name == "" and node.description == "":
            base_power["hidden"] = True
        if node.name != "":
            base_power["name"] = node.name
        if node.description != "":
            base_power["description"] = node.description
        return base_power

    @rule(AstApoliAction)
    def action(self, node: AstApoliAction) -> Any:
        base_action = self.build_dict(node)
        return base_action

    @rule(AstApoliCondition)
    def condition(self, node: AstApoliCondition) -> Any:
        base_condition = self.build_dict(node)
        if node.inverted:
            base_condition["inverted"] = True
        #print(base_condition)
        return base_condition
    
    @rule(AstApoliLiteral)
    def literal(self, node: AstApoliLiteral) -> Any:
        values = []
        if isinstance(node.value, AstChildren) or isinstance(node.value, List):
            for child in node.value:
                if isinstance(child, AstApoliAction):
                    values.append(self.action(self, child))
                if isinstance(child, AstApoliCondition):
                    values.append(self.condition(self, child))
        elif isinstance(node.value, EquipmentSlot):
            values = node.value.value
        elif isinstance(node.value, AstApoliCondition):
            values.append(self.condition(self, node.value))
        elif isinstance(node.value, Condition):
            values = self.condition(self, node.value.to_ast())
        else:
            values = node.value
        return values
    
#endregion