from __future__ import annotations

from enum import IntEnum
from typing import Dict, List, Tuple
from .game_types import Vertex, Edge, InvalidPlayerError, InvalidGameStateError, InvalidMoveError

class Game:
    vertices: List[Vertex] = []
    edges: List[Edge] = []
    player1_id: str = ""
    player2_id: str = ""
    turn_count: int = 0
    current_player_index: int = 0   # Player index who's turn it is (1 or 2)
    
    class MoveType(IntEnum):
        NONE = -1   # No legal moves or it's not the player's turn
        NODE = 0
        EDGE = 1
        QUIT = 2

    def __init__(self):
        pass
    

    def _get_player_node(self, player_index: int = 0) -> int:
        """Return the node that the player owns, or -1 if none."""
        if player_index == 0:
            player_index = self.current_player_index

        state_id = Vertex.State.P1 if player_index == 1 else Vertex.State.P2
        return next((node.node_id for node in self.vertices if node.state == state_id), -1)

    def is_my_turn(self, player_id: str) -> bool:
        """Return True if it is the player's turn, False otherwise."""
        return player_id in [self.player1_id, self.player2_id] and player_id == [self.player1_id, self.player2_id][self.current_player_index-1]
                                                                                                                   
    def is_game_over(self) -> bool:
        """Return True if the game is over. This is the case iff all edges are claimed and both players have a node."""

        # Check that all edges are claimed
        if any(edge.state == Edge.State.NONE for edge in self.edges):
            return False
        return self._get_player_node(1) != -1 and self._get_player_node(2) != -1
    

    def create_game(self, num_vertices:int = 0, edges: List[Tuple[int, int]] = None):
        """Initialize the game with the token and number of vertices and edges.
        """
        if num_vertices > 0:
            self.vertices = [Vertex(node) for node in range(num_vertices)]

        if edges:  
            # Check that the edges are valid
            if any(node1 >= num_vertices or node2 >= num_vertices for node1, node2 in edges):
                raise InvalidGameStateError("Edge vertices are out of range")
            if any(node1 > node2 or node1 == node2 for node1, node2 in edges):
                raise InvalidGameStateError("Edge vertices are invalid. Node1 >= Node2.")
            
            # Sort the edges by tuple value 0 then 1
            edges.sort(key=lambda x: (x[0], x[1]))
            self.edges = [Edge(node1, node2) for node1, node2 in edges if node1 < num_vertices and node2 < num_vertices and node1 < node2]

        self.turn_count = 0
        self.current_player_index = 1

    def join_game(self, player_id: str, player_num: int):
        """
        Join the game with the player_id and player_num.
        
        player_id: str, the player ID
        player_num: int, the player number, either 1 or 2, or 0 for either player
        """

        if player_num not in [0, 1, 2]:
            raise InvalidPlayerError("Invalid player number")
        
        if player_num == 0:

            if player_id == self.player1_id or not self.player1_id:
                self.player1_id = player_id
            elif player_id == self.player2_id or not self.player2_id:
                self.player2_id = player_id
            else:
                raise InvalidPlayerError("Game is full")
            
        if player_num == 1 and (not self.player1_id or self.player1_id == player_id):
            self.player1_id = player_id
        elif player_num == 2 and (not self.player2_id or self.player2_id == player_id):
            self.player2_id = player_id
        else:
            raise InvalidPlayerError("Player not allowed to join game")
        
    def get_game_state(self) -> Dict[str, any]:
        """Return the game state as a dictionary.
        "state": {
            "num_nodes": int,
            "edges": List[Tuple[int, int, int]],    # List of edges as vertex pairs and edge state
            "player1_id": str,
            "player2_id": str,
            "turn_count": int,
            "current_player_index": int (1 or 2),
            "player1_node": int, # -1 if no node
            "player2_node": int, # -1 if no node
        }
        """
        game_state = {
            "num_nodes": len(self.vertices),
            "edges": [(edge.vertices[0], edge.vertices[1], edge.state.value) for edge in self.edges],
            "player1_id": self.player1_id,
            "player2_id": self.player2_id,
            "turn_count": self.turn_count,
            "current_player_index": self.current_player_index,
            "player1_node":  self._get_player_node(0),
            "player2_node": self._get_player_node(1),
        }
        return game_state

    def set_game_state(self, state: Dict[str, any], validate: bool = True) -> None:
        """Set the game state from a dictionary.
        """

        # game_state = {
        #     "num_nodes": len(self.vertices),
        #     "edges": [(edge.vertices[0], edge.vertices[1], edge.state.value) for edge in self.edges],
        #     "player1_id": self.player1_id,
        #     "player2_id": self.player2_id,
        #     "turn_count": self.turn_count,
        #     "current_player_index": self.current_player_index,
        #     "player1_node":  self.get_player_node(0),
        #     "player2_node": self.get_player_node(1),
        # }
        # Use the dictionary to set the game state

        # Check that the turn count and current player index match and are valid
        if index:=state["current_player_index"] not in [1,2]:
            raise InvalidGameStateError(f"Invalid current player index (must be 1 or 2): {index}")
        if state["turn_count"] % 2 != index-1:
            raise InvalidGameStateError(f"Invalid turn count. Doesn't match current player index.")

        # Validate the data if requested
        if validate:
            # Check that the state has the correct keys
            if not all(key in state for key in ["num_nodes", "edges", "player1_id", "player2_id", "turn_count", "current_player_index", "player1_node", "player2_node"]):
                raise InvalidGameStateError("Missing keys in game state")

            # Check that the game details match, such as vertex count and edge count
            if state["num_nodes"] != len(self.vertices) or len(state["edges"]) != len(self.edges):
                raise InvalidGameStateError("Game state does not match game details")
            
            # Check that the player IDs match
            if state["player1_id"] != self.player1_id or state["player2_id"] != self.player2_id:
                print(f"Player IDs do not match: {state['player1_id']} != {self.player1_id} or {state['player2_id']} != {self.player2_id}")
                raise InvalidGameStateError("Player IDs do not match")
            
        else:
            # Set the game state without validation by creating a new game with the state details
            self.create_game(state["num_nodes"], [(edge[0], edge[1]) for edge in state["edges"]])
            self.player1_id = state["player1_id"]
            self.player2_id = state["player2_id"]
                    

        self.turn_count = state["turn_count"]
        self.current_player_index = state["current_player_index"]
        for index, edge in enumerate(self.edges):
            # Check that edge vertices match
            if edge.vertices[0] != state["edges"][index][0] or edge.vertices[1] != state["edges"][index][1]:
                raise InvalidGameStateError(f"Edge vertices do not match for edge {index}")
            edge.state = Edge.State(state["edges"][index][2])

        for index, vertex in enumerate(self.vertices):
            if state["player1_node"] == index:
                vertex.state = Vertex.State.P1
            elif state["player2_node"] == index:
                vertex.state = Vertex.State.P2
            else:
                vertex.state = Vertex.State.NONE

    def get_legal_moves(self, player_id: str) -> List[List[int, int, int]]:
        """Return a list of legal moves for the player.
        """
        legal_moves: List[List[int, int, int]] = []
        edge_move_count = 0

        # Check that the player exists
        if player_id not in [self.player1_id, self.player2_id]:
            raise InvalidPlayerError("Player not in game.")
        
        # Check if the player_id is the current player
        if (player_id != [self.player1_id, self.player2_id][self.current_player_index-1]):
            legal_moves.append([Game.MoveType.NONE.value, 0, 0])
        else:
            # Find valid edge moves
            for index, edge in enumerate(self.edges):
                if edge.state == Edge.State.NONE:
                    edge_move_count += 1
                    legal_moves.append([Game.MoveType.EDGE.value, index, Edge.State.NEITHER.value])
                    legal_moves.append([Game.MoveType.EDGE.value, index, Edge.State.FM.value])
                    legal_moves.append([Game.MoveType.EDGE.value, index, Edge.State.AFM.value])

            # See if the current player has a node, if not, the can select any unclaimed node
            if self._get_player_node() == -1:
                if edge_move_count == 1:
                    # If there's only one edge move, the player can't take it, so they must take a node
                    legal_moves.clear()

                for vertex in self.vertices:
                    if vertex.state == Vertex.State.NONE:
                        legal_moves.append([Game.MoveType.NODE.value, vertex.node_id, self.current_player_index])

            # Add the quit move if there are any legal moves
            if legal_moves:
                legal_moves.append([Game.MoveType.QUIT.value, 0, 0])

        return legal_moves

    def make_move(self, player_id:str,  move_type: int, move_index: int, move_state: int):
        """Make a move in the game.
        move_type: int, the type of move, either NODE, EDGE, or QUIT
        move_index: int, the index of the move
        move_state: int, the state of the move
        """

        # For now, skip "QUIT" move type
        if move_type == Game.MoveType.QUIT.value:
            return False


        # Check that the player exists
        if player_id not in [self.player1_id, self.player2_id]:
            raise InvalidPlayerError("Player not in game.")
        
        if player_id != [self.player1_id, self.player2_id][self.current_player_index-1]:
            # Maybe handle a quit request even if not current player?
            raise InvalidPlayerError("Not this player's turn.")

        legal_moves = self.get_legal_moves(player_id)
        if [move_type, move_index, move_state] not in legal_moves:
            raise InvalidMoveError("Invalid move")        

        if move_type not in [Game.MoveType.NODE.value, Game.MoveType.EDGE.value]:
            raise InvalidMoveError("Invalid move type")
        
        if move_type == Game.MoveType.NODE.value:
            if move_index >= len(self.vertices):
                raise InvalidMoveError("Invalid node index")
            node = self.vertices[move_index]
            if node.state != Vertex.State.NONE:
                raise InvalidMoveError("Node already claimed")
            
            if move_state not in [1, 2]:
                raise InvalidMoveError("Selected node state not valid.")
            
            node.state = Vertex.State.P1 if move_state == 1 else Vertex.State.P2

        elif move_type == Game.MoveType.EDGE.value:
            if move_index >= len(self.edges):
                raise InvalidMoveError("Invalid edge index")
            
            edge = self.edges[move_index]
            if edge.state != Edge.State.NONE:
                raise InvalidMoveError("Edge already claimed")
            if move_state == Edge.State.NONE.value or move_state > Edge.State.AFM.value:
                raise InvalidMoveError("Selected edge state not valid.")
            
            edge.state = Edge.State(move_state)

        self.current_player_index = 1 if self.current_player_index == 2 else 2
        self.turn_count += 1

        if self.is_game_over():
            # Game over, calculate the score
            pass

__all__ = ["Game", "InvalidMoveError", "InvalidPlayerError", "InvalidGameStateError"]