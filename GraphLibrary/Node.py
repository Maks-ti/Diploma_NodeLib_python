

from queue import Queue
from uuid import uuid4
import json
from GraphTransferLibrary import Command, CommandType


class Node:
    def __init__(self, queue=None, name="", color="", size=0.0, selected=False, visited=0, value=None):
        self.__queue: Queue = queue
        self._id = str(uuid4())
        self._name: str = name
        self._color: str = color
        self._size: int | float = size
        self._selected: bool = selected
        self._visited: int = visited
        self._value: any = value
        self._output_edges: list[Edge] = []
        self._input_edges: list[Edge] = []

        self._enqueue_command(CommandType.CREATE, self)

    def to_dict(self):
        # Создаём словарь из атрибутов объекта для последующей сериализации в JSON
        return {
            'Id': self._id,
            'Name': self._name,
            'Color': self._color,
            'Size': self._size,
            'Selected': self._selected,
            'Visited': self._visited,
            'Value': self._value,
        }

    def to_json(self):
        # Используем json.dumps для преобразования словаря в JSON-строку
        return json.dumps(self.to_dict(), ensure_ascii=False)

    def __str__(self):
        # Для удобства отладки, возвращаем JSON-представление объекта
        return self.to_json()

    def _enqueue_command(self, command_name: CommandType, value: any):
        command = Command(self._id, command_name, value)
        if self.__queue:
            self.__queue.put(command)

    @property
    def childs(self):
        return self._output_edges

    @property
    def id(self) -> str:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value):
        self._name = value
        self._enqueue_command(CommandType.SET_NAME, value)

    @property
    def color(self) -> str:
        return self._color

    @color.setter
    def color(self, value):
        self._color = value
        self._enqueue_command(CommandType.SET_COLOR, value)

    @property
    def size(self) -> int | float:
        return self._size

    @size.setter
    def size(self, value):
        self._size = value
        self._enqueue_command(CommandType.SET_SIZE, value)

    @property
    def selected(self) -> bool:
        return self._selected

    @selected.setter
    def selected(self, value):
        self._selected = value
        self._enqueue_command(CommandType.SET_SELECTED, value)

    @property
    def visited(self) -> int:
        return self._visited

    @visited.setter
    def visited(self, value):
        self._visited = value
        self._enqueue_command(CommandType.SET_VISITED, value)

    @property
    def value(self) -> any:
        return self._value

    @value.setter
    def value(self, value):
        self._value = value
        self._enqueue_command(CommandType.SET_VALUE, value)

    def add_child(self, child: 'Node', edge_parameters=None):
        new_edge = Edge(self, child, edge_parameters, self.__queue)
        child._input_edges.append(new_edge)
        self._output_edges.append(new_edge)
        self._enqueue_command(CommandType.ADD_CHILD, new_edge)

    def delete_child(self, child: 'Node'):
        edge = next((e for e in self._output_edges if e.node_to == child), None)
        if edge is None:
            raise ValueError(f"Node id = {child._id} isn't in children of Node id = {self._id}")
        child._input_edges.remove(edge)
        self._output_edges.remove(edge)
        self._enqueue_command(CommandType.DELETE_CHILD, edge.id)

    def get_child(self, child_id) -> 'Node':
        return next((edge.node_to for edge in self._output_edges if edge.node_to.id == child_id), None)

    def __delete_all_input_edges(self):
        for edge in list(self._input_edges):
            edge.node_from.delete_child(self)

    def __delete_all_output_edges(self):
        for edge in list(self._output_edges):
            self.delete_child(edge.node_to)

    def delete(self):
        self.__delete_all_input_edges()
        self.__delete_all_output_edges()
        self._enqueue_command(CommandType.DELETE, self.id)

    def __eq__(self, other):
        if isinstance(other, Node):
            return self.id == other.id
        return False


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
        return self._node_to

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


