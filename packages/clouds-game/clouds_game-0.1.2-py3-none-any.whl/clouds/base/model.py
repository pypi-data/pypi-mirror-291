import dataclasses
from typing import Callable, Optional, Iterable

from immutables import Map


@dataclasses.dataclass(frozen=True)
class Auftrag:
    """
    Ein Auftrag für eine Aufnahme. Wenn man diese durchführt ohne Wolken, erhält man Punkte.
    """

    name: str
    punkte: int
    statistische_wolken_wahrscheinlichkeit: float
    speicher_verbrauch: int


@dataclasses.dataclass(frozen=True)
class AufnahmeMöglichkeit:
    """
    Eine konkrete Möglichkeit, eine Aufnahme durchzuführen.

    Die Start- und Endzeiten sind dabei egal und dienen nur zur Visualisierung.
    """

    name: str
    start: Optional[float]
    ende: Optional[float]
    auftrag: Auftrag

    def punkte(self) -> int:
        """
        Erhalte folgende Punkte, wenn die Aufnahme geplant und ohne Wolken gelingt.
        :return: Eine ganze Zahl an Punkten.
        """
        return self.auftrag.punkte

    def statistische_wolken_wahrscheinlichkeit(self) -> float:
        """
        Erhalte die statistische Wolkenwahrscheinlichkeit dieser Aufnahmemöglichkeit.
        :return: Eine Wahrscheinlichkeit zwischen 0 und 1.
        """
        return self.auftrag.statistische_wolken_wahrscheinlichkeit

    def speicher_verbrauch(self) -> int:
        """
        Erhalte den Speicherverbrauch dieser Aufnahmemöglichkeit.
        :return: Eine reelle nicht-negative Zahl, die den verbrauchten Speicher angibt.
        """
        return self.auftrag.speicher_verbrauch


@dataclasses.dataclass(frozen=True)
class AktuellerZustand:
    """
    Der Spielzustand in einer Runde, welcher für Spieler einsehbar ist.
    """

    aufträge: Map[Auftrag, frozenset[AufnahmeMöglichkeit]]
    erledigte_aufträge: frozenset[Auftrag]
    folge_aufnahme_möglichkeiten: tuple[frozenset[AufnahmeMöglichkeit], ...]
    wolken_vorhersage: Map[AufnahmeMöglichkeit, float]
    nicht_erlaubte_aufnahmen: frozenset[tuple[AufnahmeMöglichkeit, AufnahmeMöglichkeit]]
    punktestand: int
    maximaler_speicher_verbrauch: int
    aktuelle_spielrunde: int

    def aktuelle_aufnahme_möglichkeiten(self) -> list[AufnahmeMöglichkeit]:
        """
        Erhalte die Aufnahmemöglichkeiten, die aktuell gewählt werden können.
        :return: Eine Menge der Aufnahmemöglichkeiten, unter denen im aktuellen Zug gewählt werden darf.
        """
        return sorted(self.folge_aufnahme_möglichkeiten[0], key=lambda x: (x.start, x.ende, x.punkte()))

    def überlappen(self, erste: AufnahmeMöglichkeit, zweite: AufnahmeMöglichkeit) -> bool:
        """
        Gibt zurück ob `erste` und `zweite` AufnahmeMöglichkeit überlappen und dementsprechend nicht gleichzeitig
        geplant werden dürfen oder doch.
        """
        return (erste, zweite) in self.nicht_erlaubte_aufnahmen or (zweite, erste) in self.nicht_erlaubte_aufnahmen

    def überlappt_irgendein(
        self, aufnahme: AufnahmeMöglichkeit, menge_aufnahme_möglichkeiten: Iterable[AufnahmeMöglichkeit]
    ) -> bool:
        """
        Gibt zurück ob `aufnahme` mit mindestens einer AufnahmeMöglichkeit aus `menge_aufnahme_möglichkeiten` überlappt
        und dementsprechend nicht gleichzeitig geplant werden kann.
        """
        return any(True for opp in menge_aufnahme_möglichkeiten if self.überlappen(aufnahme, opp))


PlanFunction = Callable[[AktuellerZustand], list[AufnahmeMöglichkeit]]


@dataclasses.dataclass(frozen=True)
class TotalGameState:
    """
    Current game state including the player-visible AktuellerZustand as well as
    hidden internal data.
    """

    player_visible_state: AktuellerZustand
    actual_probabilities: dict[AufnahmeMöglichkeit, float]
    forecast_probabilities: dict[AufnahmeMöglichkeit, float]


@dataclasses.dataclass(frozen=True)
class ExecutedOpportunity:
    """
    The result of a single opportunity (or AufnahmeMöglichkeit).

    The full results can be reconstructed and visualized by remembering all the individual ExecutedOpportunities.
    """

    start: float
    end: float
    points: int
    request: str
    chosen: bool
    cloudy: bool
    valid: bool

    def overlaps(self, other: "ExecutedOpportunity") -> bool:
        """
        Return whether a given ExecutedOpportunity overlaps with `other`
        """
        return self.start <= other.end and other.start <= self.end

    def resolves_request(self) -> bool:
        """
        This opportunity resolves a request
        """
        return self.chosen and self.valid and not self.cloudy
