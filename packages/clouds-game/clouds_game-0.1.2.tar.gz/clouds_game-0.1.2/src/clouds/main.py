import random
from logging import Logger
from pathlib import Path
from typing import Optional
import logging

import click

from clouds.base.player import LocalPlayer, Player
from clouds.game import GameLoop
from clouds.sample_ai.basic import GreedyAlgorithm
from clouds.samples import RandomGameGenerator, ConcreteSamples
from clouds.visualization import PyGameVisualizer

logger: Logger = logging.getLogger("Main")


@click.group()
def main():
    """
    Main entry point for CLI of Clouds.
    """


@click.option(
    "--seed-game-state", default=None, type=int, show_default=True, help="Seed für den Zufallsgenerator des Spielinputs"
)
@click.option(
    "--seed-game-play", default=None, type=int, show_default=True, help="Seed für den Zufallsgenerator des Spielablaufs"
)
@click.option(
    "--error-cloud-statistics",
    default=0.2,
    type=float,
    show_default=True,
    help="Standardabweichung des Fehlers der Wolkenstatistik",
)
@click.option(
    "--error-cloud-forecast",
    default=0.1,
    type=float,
    show_default=True,
    help="Standardabweichung des Fehlers der Wolkenvorhersage",
)
@click.option("--rounds", default=10, type=int, show_default=True, help="Anzahl Spielrunden")
@click.option(
    "--size", default=2, type=int, show_default=True, help="Skalierung der Größe der Aufträge und Aufnahmemöglichkeiten"
)
@click.option(
    "--visualize",
    default=True,
    type=bool,
    show_default=True,
    help="Soll Ablauf des Spiels visualisiert werden oder nicht",
)
@click.option(
    "--show-point-animation",
    default=False,
    type=bool,
    show_default=True,
    help="Soll Visualisierung eine Zwischenanimation für erhaltene Punkte abspielen",
)
@click.option("--user-name", default="Local Player", type=str, show_default=True, help="Name des Spielers")
@click.option(
    "--log-level",
    default="debug",
    type=str,
    show_default=True,
    help="Log level, kann debug, info, warning, error oder critical sein",
)
@click.argument("ai-file", default=None, type=click.Path(exists=True), required=False)
@main.command()
def run_single_game(
    seed_game_state,
    seed_game_play,
    error_cloud_statistics,
    error_cloud_forecast,
    rounds,
    size,
    visualize,
    show_point_animation,
    user_name,
    log_level,
    ai_file,
) -> None:
    """
    Run a single random game
    """

    # Configure logging
    logging.basicConfig(
        filename="clouds.log",
        encoding="utf-8",
        format="[%(asctime)s] [%(name)-20.20s] [%(levelname)-7.7s] [%(message)s]",
        level=log_level.upper(),
    )
    logger.info("==============================")
    logger.info("=== Spiele ein neues Spiel ===")
    logger.info("==============================")

    # Create game state
    initial_game_generator = RandomGameGenerator(
        standard_deviation_statistical_cloud_coverage=error_cloud_statistics,
        standard_deviation_forecast_cloud_coverage=error_cloud_forecast,
        rounds=rounds,
        size_scale=size,
        random_seed=seed_game_state,
    )
    initial_game_state = initial_game_generator.create_new_game()
    logger.info(
        f"Erstelle ein einzelnes Spiel mit Parametern rounds={rounds}, size={size}, error_cloud_statistics={error_cloud_statistics}, error_cloud_forecast={error_cloud_forecast}, seed_game_state={initial_game_generator.original_random_seed}"
    )

    # Load Player
    player: Player
    if ai_file:
        player = LocalPlayer(name_=user_name, file_path=ai_file)
    else:
        player = GreedyAlgorithm()
    logger.info(f"Benutze KI {player.name} aus der Datei {ai_file}")

    loop = GameLoop(
        initial_state=initial_game_state,
        player=player,
        random_seed=seed_game_play,
    )
    logger.info(f"Spiele Spiel mit seed_game_play={loop.original_random_seed}")

    results = []
    while loop.ongoing():
        results.append(loop.proceed_round())

    logger.info(f"Endgültige Punktzahl: {loop.state.player_visible_state.punktestand}")
    logger.debug(
        f"""Erfolgreich ausgeführte Aufträge: {
        ', '.join([f'{auftrag.name} mit {auftrag.punkte} Punkten' 
                   for auftrag in loop.state.player_visible_state.erledigte_aufträge])}"""
    )

    if visualize:
        visualizer = PyGameVisualizer(results=results, show_point_animation=show_point_animation)
        visualizer.visualize()


@click.option(
    "--seed-game-state", default=None, type=int, show_default=True, help="Seed für den Zufallsgenerator des Spielinputs"
)
@click.option(
    "--error-cloud-statistics",
    default=0.2,
    type=float,
    show_default=True,
    help="Standardabweichung des Fehlers der Wolkenstatistik",
)
@click.option(
    "--error-cloud-forecast",
    default=0.1,
    type=float,
    show_default=True,
    help="Standardabweichung des Fehlers der Wolkenvorhersage",
)
@click.option("--rounds", default=10, type=int, show_default=True, help="Anzahl Spielrunden")
@click.option(
    "--size", default=2, type=int, show_default=True, help="Skalierung der Größe der Aufträge und Aufnahmemöglichkeiten"
)
@click.option("--user-name", default="Local Player", type=str, show_default=True, help="Name des Spielers")
@click.option("--repetitions", default=1000, type=int, show_default=True, help="Anzahl von Testläufen")
@click.option(
    "--log-level",
    default="debug",
    type=str,
    show_default=True,
    help="Log level, kann debug, info, warning, error oder critical sein",
)
@click.argument("ai-file", default=None, type=click.Path(exists=True), required=False)
@main.command()
def analyze_single_game(
    seed_game_state,
    error_cloud_statistics,
    error_cloud_forecast,
    rounds,
    size,
    user_name,
    repetitions,
    log_level,
    ai_file,
) -> None:
    """
    Run a single random game state with an AI but repeatedly to get statistical data
    """

    # Configure logging
    logging.basicConfig(
        filename="clouds.log",
        encoding="utf-8",
        format="[%(asctime)s] [%(name)-20.20s] [%(levelname)-7.7s] [%(message)s]",
        level=log_level.upper(),
    )
    logger.info("==================================")
    logger.info("=== Analysiere ein neues Spiel ===")
    logger.info("==================================")

    # Create game state
    initial_game_generator = RandomGameGenerator(
        standard_deviation_statistical_cloud_coverage=error_cloud_statistics,
        standard_deviation_forecast_cloud_coverage=error_cloud_forecast,
        rounds=rounds,
        size_scale=size,
        random_seed=seed_game_state,
    )
    initial_game_state = initial_game_generator.create_new_game()
    logger.info(
        f"Analysiere Spiel mit Parametern rounds={rounds}, size={size}, error_cloud_statistics={error_cloud_statistics}, error_cloud_forecast={error_cloud_forecast}, seed_game_state={initial_game_generator.original_random_seed} über {repetitions} mal"
    )

    # Load Player
    player: Player
    if ai_file:
        player = LocalPlayer(name_=user_name, file_path=ai_file)
    else:
        player = GreedyAlgorithm()
    logger.info(f"Benutze KI {player.name} aus der Datei {ai_file}")

    results = []
    for _ in range(repetitions):
        seed_game_play = random.randint(1, 100000)
        loop = GameLoop(
            initial_state=initial_game_state,
            player=player,
            random_seed=seed_game_play,
        )
        while loop.ongoing():
            loop.proceed_round()
        results.append(loop.state.player_visible_state.punktestand)

    logger.info(f"Endgültige Punktzahlen: {results}")
    logger.info(f"Durchschnittliche Punktzahl: {sum(results) * 1.0 / repetitions}")


if __name__ == "__main__":
    main()
