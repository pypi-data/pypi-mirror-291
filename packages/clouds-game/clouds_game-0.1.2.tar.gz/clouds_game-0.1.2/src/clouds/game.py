import logging
import random
from itertools import combinations
from typing import Optional

from immutables import Map

from clouds.base.model import AktuellerZustand, AufnahmeMöglichkeit, TotalGameState, ExecutedOpportunity
from clouds.base.player import Player


class GameLoop:
    """
    Implements the main game loop logic, in particular

    * it is instantiated with the start data
    * it calls for the players decisions and calculates the next game state
    * it keeps track of all relevant information
    """

    def __init__(self, initial_state: TotalGameState, player: Player, random_seed: Optional[int]):
        """
        Constructor of a game loop instance.
        """
        self.state: TotalGameState = initial_state
        self.player: Player = player
        if random_seed:
            self.original_random_seed = random_seed
        else:
            self.original_random_seed = random.randint(0, 100000)
        self.random_generator: random.Random = random.Random(self.original_random_seed)
        self._logger: logging.Logger = logging.getLogger("Game Loop")

    def ongoing(self) -> bool:
        """
        :return: True, if there are still rounds to be played, False otherwise
        """
        return len(self.state.player_visible_state.folge_aufnahme_möglichkeiten) > 0

    def points(self) -> int:
        """
        :return: Players current points
        """
        return self.state.player_visible_state.punktestand

    def proceed_round(self) -> set[ExecutedOpportunity]:
        """
        Proceed one round in the game loop and return the results of that round.

        This proceeds as follows:
        * Ask the player for a planning decision
        * Make sure that it replies in time and check the validity of the result
        * Check for clouds
        * Update game state
        """
        self._logger.debug(f"Runde {self.state.player_visible_state.aktuelle_spielrunde}:")

        # Query player AI for decisions
        decisions = self._ask_player_for_decision()
        self._logger.debug(
            f"Spieler hat folgende Aufnahmemöglichkeiten geplant: {', '.join([opp.name + ' (' + str(opp.punkte()) + ' P.)' for opp in decisions])}"
        )

        # Determine clouds
        cloudy_images = self._cloudy_images(decisions)
        self._logger.debug(
            f"Folgende Aufnahmemöglichkeiten waren bewölkt: {', '.join([opp.name for opp in cloudy_images])}"
        )

        # Check validity
        valid = self._check_validity(decisions)

        # Prepare results for this round
        result: set[ExecutedOpportunity] = set()
        for opportunity in self.state.player_visible_state.folge_aufnahme_möglichkeiten[0]:
            result.add(
                ExecutedOpportunity(
                    start=(
                        opportunity.start
                        if opportunity.start
                        else self.state.player_visible_state.aktuelle_spielrunde + 0.1
                    ),
                    end=(
                        opportunity.ende
                        if opportunity.ende
                        else self.state.player_visible_state.aktuelle_spielrunde + 0.9
                    ),
                    points=opportunity.auftrag.punkte,
                    request=opportunity.auftrag.name,
                    chosen=opportunity in decisions,
                    cloudy=opportunity in cloudy_images,
                    valid=valid,
                )
            )

        # Update game state
        self._update_game_state(decision=decisions, cloudy_images=cloudy_images, valid_decision=valid)

        return result

    def _ask_player_for_decision(self) -> list[AufnahmeMöglichkeit]:
        """
        Query the player for a decision on the upcoming AufnahmeMöglichkeit.
        :return: The players decision
        """
        return self.player.call_ai(self.state.player_visible_state)

    def _check_validity(self, decision: list[AufnahmeMöglichkeit]) -> bool:
        """
        Verify that the players decisions are valid.
        :param decision:
        :return:
        """
        # Check Constraints
        for opp1, opp2 in combinations(decision, 2):
            if (opp1, opp2) in self.state.player_visible_state.nicht_erlaubte_aufnahmen or (
                opp2,
                opp1,
            ) in self.state.player_visible_state.nicht_erlaubte_aufnahmen:
                self._logger.warning(
                    f"Folgende zwei Aufnahmemöglichkeiten wurden geplant, sind aber nicht erlaubt: {opp1.name} und {opp2.name}. Keine Aufnahmen diese Runde möglich"
                )
                return False

        # Check Memory
        consumed_memory = sum(opportunity.speicher_verbrauch() for opportunity in decision)
        if consumed_memory > self.state.player_visible_state.maximaler_speicher_verbrauch:
            self._logger.warning(
                f"Zu viel Speicher ({consumed_memory} von erlaubten {self.state.player_visible_state.maximaler_speicher_verbrauch}) verbraucht. Keine Aufnahmen diese Runde möglich"
            )
            return False

        return True

    def _cloudy_images(self, decision: list[AufnahmeMöglichkeit]) -> list[AufnahmeMöglichkeit]:
        """
        Execute random process to determine which AufnahmeMöglichkeit are cloud and which are not.
        :param decision:
        :return: Set of AufnahmeMöglichkeit among decision which are cloudy.
        """
        return [
            opportunity
            for opportunity, probability in self.state.actual_probabilities.items()
            if self.random_generator.random() <= probability and opportunity in decision
        ]

    def _update_game_state(
        self, decision: list[AufnahmeMöglichkeit], cloudy_images: list[AufnahmeMöglichkeit], valid_decision: bool
    ) -> None:
        """
        Update the game state based on decisions and random clouds.
        :param decision:
        :param cloudy_images:
        :param valid_decision: If the decisions were invalid, the state is updated but no points are given to the player
        """
        # Update points and requests in case of a valid decision:
        new_points = self.state.player_visible_state.punktestand
        new_requests = set(self.state.player_visible_state.erledigte_aufträge)
        if valid_decision:
            for opportunity in decision:
                if opportunity in cloudy_images:
                    self._logger.debug(
                        f"Spieler erhält keine Punkte für {opportunity.name} weil die Aufnahme bewölkt war"
                    )
                elif opportunity.auftrag in new_requests:
                    self._logger.debug(
                        f"Spieler erhält keine Punkte für {opportunity.name} weil der Auftrag bereits erledigt war"
                    )
                else:
                    self._logger.debug(
                        f"Spieler erhält {opportunity.auftrag.punkte} Punkte für die Erfüllung von Auftrag {opportunity.auftrag.name}"
                    )
                    new_points += opportunity.auftrag.punkte
                    new_requests.add(opportunity.auftrag)

        # Advance game loop
        remaining_turns = self.state.player_visible_state.folge_aufnahme_möglichkeiten[1:]
        if len(remaining_turns) > 0:
            new_opportunities = remaining_turns

            # Update cloud predictions
            new_cloud_predictions = Map(
                {
                    opportunity: probability
                    for opportunity, probability in self.state.forecast_probabilities.items()
                    if opportunity in new_opportunities[0]
                }
            )
        else:
            new_opportunities = ()
            new_cloud_predictions = Map()

        self.state = TotalGameState(
            player_visible_state=AktuellerZustand(
                aufträge=self.state.player_visible_state.aufträge,
                folge_aufnahme_möglichkeiten=new_opportunities,
                wolken_vorhersage=new_cloud_predictions,
                punktestand=new_points,
                maximaler_speicher_verbrauch=self.state.player_visible_state.maximaler_speicher_verbrauch,
                erledigte_aufträge=frozenset(new_requests),
                nicht_erlaubte_aufnahmen=self.state.player_visible_state.nicht_erlaubte_aufnahmen,
                aktuelle_spielrunde=self.state.player_visible_state.aktuelle_spielrunde + 1,
            ),
            actual_probabilities=self.state.actual_probabilities,
            forecast_probabilities=self.state.forecast_probabilities,
        )
