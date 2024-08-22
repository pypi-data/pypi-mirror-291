from __future__ import annotations

from enum import IntEnum
from typing import Tuple

class InvalidMoveError(Exception):
    pass

class InvalidPlayerError(Exception):
    pass

class InvalidGameStateError(Exception):
    pass

class Vertex:
    class State(IntEnum):
        NONE = 0
        P1 = 1
        P2 = 2

    
    state: Vertex.State = State.NONE
    id: int = 0
    
    def __init__(self, node_id: int):
        self.node_id = node_id
        self.state = Vertex.State.NONE


class Edge:

    class State(IntEnum):
        NONE = 0
        NEITHER = 1
        FM = 2
        AFM = 3
        
    vertices: Tuple[int, int] = None
    state: Edge.State = State.NONE
    
    def __init__(self, node1_id: int, node2_id: int):
        self.vertices = (node1_id, node2_id)
        self.state = Edge.State.NONE


__all__ = ["Vertex", "Edge", "InvalidMoveError", "InvalidPlayerError", "InvalidGameStateError"]
