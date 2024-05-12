
import uuid
import json

import GraphLibrary
from .CommandType import CommandType


class CommandEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, CommandType):
            return obj.value
        if isinstance(obj, uuid.UUID):
            return str(obj)
        if isinstance(obj, GraphLibrary.Node) or isinstance(obj, GraphLibrary.Edge):
            return obj.to_dict()  # Используем to_dict для объектов Node и Edge
        if isinstance(obj, Command):
            return obj.to_dict()
        if isinstance(obj, dict):
            return {k: self.default(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [self.default(item) for item in obj]
        return json.JSONEncoder.default(self, obj)


class Command:
    def __init__(self, obj_id, command_name: CommandType, value=None):
        self.obj_id = obj_id
        self.command_name: str = command_name.to_string()
        self.value = value

    def to_dict(self):
        return {
            "Value": self.value,
            "ObjId": self.obj_id,
            "CommandName": self.command_name,
        }


