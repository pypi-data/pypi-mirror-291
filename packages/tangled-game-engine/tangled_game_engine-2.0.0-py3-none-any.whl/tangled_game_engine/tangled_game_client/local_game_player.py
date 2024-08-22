from __future__ import annotations

import time
from typing import Dict, Optional, Type, Any, Tuple, List
from ..tangled_game.game import Game

from .base_game_player import GamePlayerBase
from ..tangled_game_agent.base_agent import GameAgentBase

class LocalGamePlayer(GamePlayerBase):

    player1: GameAgentBase
    player2: GameAgentBase
    game: Game

    def __init__(self, player1: GameAgentBase, player2: GameAgentBase, num_vertices: int, edges: List[Tuple[int, int]]):
        self.player1 = player1
        self.player2 = player2
        self.game = Game()
        self.game.create_game(num_vertices, edges)
        self.game.join_game(self.player1.id(), 1)
        self.game.join_game(self.player2.id(), 2)


    def play_game(self) -> dict:
        """Plays the game until it is over."""
        while not self.game.is_game_over():
            player = self.player1 if self.game.is_my_turn(player_id=self.player1.id()) else self.player2
            move = player.make_move(self.game)
            if move:
                type, index, state = move
                if type == Game.MoveType.QUIT.value:
                    print(f"{player.id()} quit the game.")
                    break
                self.game.make_move(player.id(), type, index, state)
            else:
                print("No moves available. Ending game.")
                break
                
        final_state = self.game.get_game_state()
        return final_state

__all__ = ["LocalGamePlayer"]
