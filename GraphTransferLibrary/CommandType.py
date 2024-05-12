
from enum import Enum


class CommandType(Enum):
    CREATE = "Create"
    SET_NAME = "SetName"
    SET_COLOR = "SetColor"
    SET_SIZE = "SetSize"
    SET_SELECTED = "SetSelected"
    SET_VISITED = "SetVisited"
    SET_VALUE = "SetValue"
    ADD_CHILD = "AddChild"
    DELETE_CHILD = "DeleteChild"
    DELETE = "Delete"
    SET_EDGE_PARAMETERS = "SetEdgeParametres"

    def to_string(self):
        return self.value
