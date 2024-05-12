
import json
from queue import Queue
from uuid import uuid4
from GraphTransferLibrary import Command, CommandType
from GraphLibrary import Edge


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

