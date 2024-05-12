
import json
import uuid
from .Command import Command, CommandEncoder


class RpcRequest:
    def __init__(self, command, manager_id, request_id):
        self.jsonrpc: str = "2.0"
        self.command: Command = command
        self.manager_id: uuid = manager_id
        self.id: uuid = request_id

    def to_json(self):
        return json.dumps({
            "jsonrpc": self.jsonrpc,
            "command": self.command.to_dict(),
            "manager_id": str(self.manager_id),
            "id": self.id
        }, cls=CommandEncoder)


class RpcResponse:
    def __init__(self, result=None, error=None):
        self.jsonrpc = "2.0"
        self.result = result
        self.error = error

    def to_json(self):
        return json.dumps({
            "jsonrpc": self.jsonrpc,
            "result": self.result,
            "error": self.error
        }, cls=CommandEncoder)
