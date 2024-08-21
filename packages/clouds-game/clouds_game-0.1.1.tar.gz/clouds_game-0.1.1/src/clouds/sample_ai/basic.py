import logging

from clouds.base.model import *
from clouds.base.player import Player


class SimplePlayer(Player):

    def name(self) -> str:
        return "SimplePlayer"

    def call_ai(self, current_state: AktuellerZustand) -> list[AufnahmeMöglichkeit]:
        result = []
        for auftrag in current_state.aktuelle_aufnahme_möglichkeiten():
            if auftrag.punkte() >= 5:
                result.append(auftrag)

        return result


class GreedyAlgorithm(Player):

    def name(self) -> str:
        return "GreedyPlayer"

    def call_ai(self, current_state: AktuellerZustand) -> list[AufnahmeMöglichkeit]:

        logger = logging.getLogger(self.name())

        result: list[AufnahmeMöglichkeit] = []

        sorted_opportunities = sorted(
            current_state.aktuelle_aufnahme_möglichkeiten(), key=lambda x: (x.punkte(), x.start), reverse=True
        )

        currently_used_memory = 0
        for opportunity in sorted_opportunities:
            if currently_used_memory + opportunity.speicher_verbrauch() > current_state.maximaler_speicher_verbrauch:
                continue
            if current_state.überlappt_irgendein(opportunity, result):
                continue
            if opportunity.auftrag in current_state.erledigte_aufträge:
                continue
            result.append(opportunity)

        logger.debug(
            f"In Runde {current_state.aktuelle_spielrunde} gewählt: {', '.join(opp.auftrag.name for opp in result)}"
        )

        return result
