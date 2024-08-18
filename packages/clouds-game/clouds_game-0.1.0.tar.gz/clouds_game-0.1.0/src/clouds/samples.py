import itertools
import math
import random
import string
from typing import Optional

from immutables import Map

from clouds.base.model import TotalGameState, AufnahmeMöglichkeit, Auftrag, AktuellerZustand


class RandomGameGenerator:
    """
    Class for generating reasonable random games based on an optionally provided seed.
    """

    def __init__(
        self,
        random_seed: Optional[int],
        standard_deviation_statistical_cloud_coverage: float,
        standard_deviation_forecast_cloud_coverage: float,
        rounds: Optional[int],
        size_scale: int,
    ):
        """
        Initialize a new RandomGameGenerator instance.
        :param random_seed: Optional seed for the pseudo-random number generator used to create  new games.
        """
        if random_seed is not None:
            self._random_generator = random.Random(random_seed)
            self.original_random_seed = random_seed
        else:
            self.original_random_seed = random.randint(0, 100000)
            self._random_generator = random.Random(self._original_random_seed)

        if rounds is not None:
            self._rounds = rounds
        else:
            self._rounds = self._random_generator.randint(2, 100)

        self._standard_deviation_statistical_cloud_coverage = standard_deviation_statistical_cloud_coverage
        self._standard_deviation_forecast_cloud_coverage = standard_deviation_forecast_cloud_coverage
        self._size_scale = size_scale

    def create_new_game(self) -> TotalGameState:
        """
        Create a new instance of a Clouds game
        :return:
        """
        # Create requests and opportunities
        request_data = self._create_requests()
        opportunities = self._create_opportunities(requests=request_data)

        # Determine the sequence of turns
        turn_sequence = self._create_turns(
            [
                opportunity
                for opportunity_per_request in opportunities.values()
                for opportunity in opportunity_per_request
            ]
        )

        # Determine overlaps
        overlaps = self._determine_overlaps(turn_sequence)

        # Determine actual probabilities of opportunities
        actual_probabilities = self._create_actual_probabilities(opportunities)

        # Determine cloud forecasts of opportunities
        cloud_forecasts = self._create_forecast_probabilities(actual_probabilities)

        return TotalGameState(
            player_visible_state=AktuellerZustand(
                aufträge=Map(
                    {
                        request: frozenset(request_opportunities)
                        for request, request_opportunities in opportunities.items()
                    }
                ),
                erledigte_aufträge=frozenset({}),
                folge_aufnahme_möglichkeiten=tuple(frozenset(turn) for turn in turn_sequence),
                wolken_vorhersage=Map(
                    {
                        opportunity: forecast
                        for opportunity, forecast in cloud_forecasts.items()
                        if opportunity in turn_sequence[0]
                    }
                ),
                nicht_erlaubte_aufnahmen=frozenset(overlaps),
                punktestand=0,
                maximaler_speicher_verbrauch=100,
                aktuelle_spielrunde=0,
            ),
            actual_probabilities=actual_probabilities,
            forecast_probabilities=cloud_forecasts,
        )

    def _create_requests(self) -> list[Auftrag]:
        """
        Create a set of data points for Auftrag
        :return: set of requests
        """
        number_requests = self._size_scale * 10
        return [
            Auftrag(
                name="".join(self._random_generator.choices(string.ascii_lowercase, k=6)),
                punkte=self._random_generator.randint(1, 100),
                statistische_wolken_wahrscheinlichkeit=self._random_generator.random(),
                speicher_verbrauch=self._random_generator.randint(1, 20),
            )
            for _ in range(number_requests)
        ]

    def _create_opportunities(self, requests: list[Auftrag]) -> dict[Auftrag, list[AufnahmeMöglichkeit]]:
        """
        Create a set of opportunities per request
        """
        result: dict[Auftrag, list[AufnahmeMöglichkeit]] = {}
        number_of_opportunities = range(1, self._size_scale * 3 + 2)
        probabilities_of_number_of_opportunities = [math.exp(-0.5 * r) for r in number_of_opportunities]
        count_opportunities = self._random_generator.choices(
            population=number_of_opportunities, weights=probabilities_of_number_of_opportunities, k=len(requests)
        )
        for index_request, request in enumerate(requests):
            result[request] = []
            for index_opportunity in range(count_opportunities[index_request]):
                start = self._random_generator.random() * self._rounds
                length = RandomGameGenerator._clamp(
                    target=self._random_generator.normalvariate(mu=0.3, sigma=0.1),
                    min_=0.1,
                    max_=0.99 * (math.ceil(start) - start),
                )
                result[request].append(
                    AufnahmeMöglichkeit(
                        name=f"{request.name}_{index_opportunity}", start=start, ende=start + length, auftrag=request
                    )
                )
        return result

    def _determine_overlaps(
        self, turns: list[list[AufnahmeMöglichkeit]]
    ) -> list[tuple[AufnahmeMöglichkeit, AufnahmeMöglichkeit]]:
        """
        Determine pairwise overlaps of opportunities
        """

        def overlap(opportunity_1: AufnahmeMöglichkeit, opportunity_2: AufnahmeMöglichkeit) -> Optional[bool]:
            if (
                opportunity_1.start is None
                or opportunity_1.ende is None
                or opportunity_2.start is None
                or opportunity_2.ende is None
            ):
                return None
            return opportunity_1.start <= opportunity_2.ende and opportunity_2.start <= opportunity_1.ende

        result = []
        for turn in turns:
            for opportunity1, opportunity2 in itertools.combinations(turn, 2):
                if overlap(opportunity1, opportunity2) is not None:
                    if overlap(opportunity1, opportunity2):
                        result.append((opportunity1, opportunity2))
                else:
                    if self._random_generator.random() <= 0.3:
                        result.append((opportunity1, opportunity2))
        return result

    @staticmethod
    def _clamp(target: float, min_: float, max_: float) -> float:
        return min(max(target, min_), max_)

    def _create_actual_probabilities(
        self, opportunities: dict[Auftrag, list[AufnahmeMöglichkeit]]
    ) -> dict[AufnahmeMöglichkeit, float]:
        """
        Create actual cloud coverage probabilities from statistical cloud coverage probabilities.

        They are distributed normally around the statistical probabilities.
        """
        return {
            opportunity: self._random_generator.normalvariate(
                request.statistische_wolken_wahrscheinlichkeit, self._standard_deviation_statistical_cloud_coverage
            )
            for request, request_opportunities in opportunities.items()
            for opportunity in request_opportunities
        }

    def _create_forecast_probabilities(
        self, actual_probabilities: dict[AufnahmeMöglichkeit, float]
    ) -> dict[AufnahmeMöglichkeit, float]:
        """
        Create cloud forecast probabilities depending on actual cloud coverage probabilities.

        They are distributed normally around the actual probabilities.
        """
        return {
            opportunity: self._random_generator.normalvariate(
                probability, self._standard_deviation_forecast_cloud_coverage
            )
            for opportunity, probability in actual_probabilities.items()
        }

    def _create_turns(self, opportunities: list[AufnahmeMöglichkeit]) -> list[list[AufnahmeMöglichkeit]]:
        """
        Split the set of opportunities into turns
        """
        result: list[list[AufnahmeMöglichkeit]] = [[] for _ in range(self._rounds)]
        for opportunity in opportunities:
            if opportunity.start is not None and opportunity.ende is not None:
                block_start = math.floor(opportunity.start)
                block_end = math.floor(opportunity.ende)
                if block_start != block_end:
                    raise ValueError(
                        f"AufnahmeMöglichkeit {opportunity.name} hat Start {opportunity.start} und Ende {opportunity.ende} nicht im gleichen Block"
                    )
                result[block_start].append(opportunity)
            else:
                block = self._random_generator.randint(0, self._rounds - 1)
                result[block].append(opportunity)
        return result


class ConcreteSamples:
    """
    Class containing multiple hard-coded example games for illustrations purposes.
    """

    @staticmethod
    def simple_example() -> TotalGameState:
        """
        Create a very simple game with two requests and two game rounds and a single overlap.
        """
        A = Auftrag(name="A", punkte=10, statistische_wolken_wahrscheinlichkeit=0.8, speicher_verbrauch=5)
        A1 = AufnahmeMöglichkeit(name="A_1", start=0.2, ende=0.4, auftrag=A)
        A2 = AufnahmeMöglichkeit(name="A_2", start=1.2, ende=1.4, auftrag=A)

        B = Auftrag(name="B", punkte=3, statistische_wolken_wahrscheinlichkeit=0.2, speicher_verbrauch=5)
        B1 = AufnahmeMöglichkeit(name="B_1", start=0.3, ende=0.5, auftrag=B)
        B2 = AufnahmeMöglichkeit(name="B_2", start=1.6, ende=1.8, auftrag=B)
        return TotalGameState(
            player_visible_state=AktuellerZustand(
                aufträge=Map(
                    {
                        (A, frozenset({A1, A2})),
                        (B, frozenset({B1, B2})),
                    }
                ),
                erledigte_aufträge=frozenset({}),
                folge_aufnahme_möglichkeiten=tuple([frozenset({A1, B1}), frozenset({A2, B2})]),
                wolken_vorhersage=Map({A1: 0.85, B1: 0.15}),
                nicht_erlaubte_aufnahmen=frozenset({(A1, B1)}),
                punktestand=0,
                maximaler_speicher_verbrauch=10,
                aktuelle_spielrunde=0,
            ),
            actual_probabilities={A1: 0.9, A2: 0.7, B1: 0.1, B2: 0.3},
            forecast_probabilities={A1: 0.85, A2: 0.75, B1: 0.15, B2: 0.25},
        )
