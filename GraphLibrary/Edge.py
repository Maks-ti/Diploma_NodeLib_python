
from queue import Queue
from uuid import uuid4
import json

from GraphTransferLibrary import Command, CommandType
from GraphLibrary import Node


class Edge:
    def __init__(self, node_from: Node, node_to: Node, parameters=None, queue: Queue[Command] = None):
        self.__queue: Queue[Command] = queue
        self._node_from: Node = node_from
        self._node_to: Node = node_to
        self._id = str(uuid4())
        self._node_from_id: str = node_from.id
        self._node_to_id: str = node_to.id
        self._parameters: dict[str, any] = parameters if parameters is not None else {}

    @property
    def id(self):
        return self._id

    @property
    def node_from_id(self):
        return self.node_from_id

    @property
    def node_to_id(self):
        return self.node_to_id

    @property
    def node_from(self):
        return self._node_from

    @property
    def node_to(self):
        return self.node_to

    @property
    def parameters(self):
        return self._parameters

    @parameters.setter
    def parameters(self, value):
        self._parameters = value
        if self.__queue:
            self.__queue.put(Command(self._id, CommandType.SET_EDGE_PARAMETERS, value))

    def to_dict(self):
        return {
            "Id": str(self._id),
            "NodeFromId": str(self._node_from_id),
            "NodeToId": str(self._node_to_id),
            "Parameters": self._parameters
        }

    def __eq__(self, other):
        if isinstance(other, Edge):
            return self._node_from_id == other.node_from_id and self.node_to_id == other.node_to_id
        return False

    def __str__(self):
        return json.dumps(self.to_dict(), ensure_ascii=False)

    def __hash__(self):
        return hash((self.node_from_id, self.node_to_id))
