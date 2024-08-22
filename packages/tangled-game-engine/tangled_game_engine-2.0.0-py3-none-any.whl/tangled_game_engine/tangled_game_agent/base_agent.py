from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Tuple
from ..tangled_game.game import Game

class GameAgentBase(ABC):
    player_id: str

    def __init__(self, player_id: str):
        self.player_id = player_id

    def id(self) -> str:
        return self.player_id

    @abstractmethod
    def make_move(self, game: Game) -> Tuple[int, int, int]:
        """Make a move in the game.
        game: Game: The game instance

        Returns a tuple of the move type, move index, and move state.
        """
        pass


__all__ = ["GameAgentBase"]