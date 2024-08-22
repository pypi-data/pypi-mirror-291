from __future__ import annotations

from abc import ABC, abstractmethod

from typing import Type

class GamePlayerBase(ABC):

    @abstractmethod
    def play_game(self,  *args, **kwargs) -> dict:
        """
        Play the game and return the final state.
        """
        pass

    @classmethod
    def start_game(cls, client_class: Type[GamePlayerBase], *args, **kwargs) -> None:
        """
        Starts the game client with the specified subclass.

        Args:
            client_class (Type[GamePlayerBase]): The subclass of GamePlayerBase to start.
        
        Command line arguments:
            --game (str): The game token.
            --player (str): The player ID.
            --host (str): The host address.
        """

        client = client_class(*args, **kwargs)
        client.play_game()

        print("Game over")
        print("Final state is:")
        print(client.game.get_game_state())

__all__ = ["GamePlayerBase"]
