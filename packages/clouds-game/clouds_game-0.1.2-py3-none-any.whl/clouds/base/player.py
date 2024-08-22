from __future__ import annotations

import abc
from pathlib import Path
from typing import Any

from clouds.base.model import PlanFunction, AktuellerZustand, AufnahmeMöglichkeit


class Player(abc.ABC):
    """
    Class implementing a player's algorithm, including imports of self-written code.
    """

    @abc.abstractmethod
    def call_ai(self, current_state: AktuellerZustand) -> list[AufnahmeMöglichkeit]:
        """
        Abstract method called by game to proceed one round
        """

    @abc.abstractmethod
    def name(self) -> str:
        """
        Get the name of the player
        """


class LocalPlayer(Player):
    """
    Class implementing a player's algorithm, including imports of self-written code.
    """

    def __init__(self, name_: str, file_path: Path):
        """
        Initialize a new player.
        :param name_: The name of the player.
        :param file_path: The path to the source file for the AI.
        """
        self._name = name_
        self.file_path = file_path
        self.plan_function = LocalPlayer.load_module(file_path)

    def call_ai(self, current_state: AktuellerZustand) -> list[AufnahmeMöglichkeit]:
        """
        This method calls the underlying parsed plan function with the current state and
        returns its result.
        """
        return self.plan_function(current_state)

    def name(self) -> str:
        return self._name

    @staticmethod
    def load_module(file_path: Path) -> PlanFunction:
        """
        Load the PlanFunction from a file
        """
        try:
            with open(file_path, mode="r", encoding="utf-8") as file:
                # Read source code
                code = file.read()

                # Compile and execute module
                module = compile(code, file_path, "exec")
                module_dict: dict[str, Any] = {}
                # There is no safe way to do what we are doing here.
                # pylint: disable=exec-used
                exec(module, module_dict)

                # Get PlanFunction from class
                if "plan" not in module_dict:
                    raise KeyError(f"No 'plan' method found in {file_path}")
                fct = module_dict["plan"]

                return fct
        except Exception as e:
            raise ImportError(f"Failed to load plan function from file {file_path}: {e}") from e
