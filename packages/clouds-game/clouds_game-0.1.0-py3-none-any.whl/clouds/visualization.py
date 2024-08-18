import math
from collections import defaultdict

import pygame

from clouds.base.model import ExecutedOpportunity


class PyGameVisualizer:
    """
    Class using pygame to visualize a Clouds game.
    """

    GREY = (100, 100, 100)
    RED = (255, 75, 75)
    DARK_RED = (150, 0, 0)
    GREEN = (100, 255, 100)
    DARK_GREEN = (0, 150, 0)
    WHITE = (240, 240, 240)
    LIGHT_GREY = (150, 150, 150)
    DARK_GREY = (50, 50, 50)
    GREY_RED = (150, 100, 100)

    def __init__(
        self,
        results: list[set[ExecutedOpportunity]],
        show_point_animation: bool = True,
        screen_size_x: int = 1500,
        screen_size_y: int = 800,
    ):
        """
        Constructor for PyGameVisualizer
        """
        self._opportunities: list[set[tuple[ExecutedOpportunity, int]]] = [
            {(result, turn[result]) for result in turn} for turn in PyGameVisualizer._distribute_opportunities(results)
        ]
        self._opportunities_per_requests: dict[str, set[ExecutedOpportunity]] = defaultdict(set)
        for turn in self._opportunities:
            for opp, _ in turn:
                self._opportunities_per_requests[opp.request].add(opp)
        self._time = -1
        self._max_time = len(self._opportunities)
        self._points = 0
        self._glob_offset_x = 0.0
        self._glob_offset_len = 0.0
        self._glob_height = 0
        self._already_shown_opportunities: set[ExecutedOpportunity] = set()
        self._already_shown_finished_requests: set[str] = set()
        self._screen_size_x = screen_size_x
        self._screen_size_y = screen_size_y
        self._show_point_animation = show_point_animation
        self._point_animation: list = []
        self._auto_mode: bool = False

        pygame.init()
        self._screen = pygame.display.set_mode((self._screen_size_x, self._screen_size_y))
        self._font = pygame.font.SysFont(None, 35, True, False)

    def _get_all_opportunities(self) -> list[ExecutedOpportunity]:
        return [opp for turn in self._opportunities for opp, _ in turn]

    def _move_timeline_forward(self, moving_speed: float):
        """ """
        moving_offset: float = 0
        while moving_offset <= 400:
            self._update_timeline(moving_offset, True)
            moving_offset += 10 * moving_speed
        self._time += 1

    def _move_timeline_backwards(self, moving_speed: float):
        """ """
        moving_offset: float = 0
        while moving_offset >= -400:
            self._update_timeline(moving_offset, False)
            moving_offset -= 10 * moving_speed
        self._time -= 1

    def _get_color_opportunity(
        self, opportunity: ExecutedOpportunity
    ) -> tuple[tuple[int, int, int], tuple[int, int, int]]:
        if opportunity not in self._already_shown_opportunities:
            return self.WHITE, self.DARK_GREY

        if opportunity.request in self._already_shown_finished_requests:
            return self.GREEN, self.DARK_GREEN

        match opportunity.chosen, opportunity.valid, opportunity.cloudy:
            case False, _, _:
                return self.WHITE, self.DARK_GREY
            case True, False, _:
                return self.RED, self.DARK_RED
            case True, True, True:
                return self.LIGHT_GREY, self.DARK_GREY
            case True, True, False:
                return self.GREEN, self.DARK_GREEN
            # case _:
            #   return self.WHITE, self.DARK_GREY

    def _draw_opportunity_rectangle(
        self, opportunity: ExecutedOpportunity, offset_x: float, moving_offset: float, row: int, offset_len: float
    ):
        color, color_border = self._get_color_opportunity(opportunity)
        pygame.draw.rect(
            self._screen,
            color,
            [
                offset_x + 100 + 400 * opportunity.start - 400 * (self._time - 1) - moving_offset,
                self._screen_size_y - 250 - row * 100,
                400 * (opportunity.end - opportunity.start) * offset_len,
                95,
            ],
        )
        pygame.draw.rect(
            self._screen,
            color_border,
            [
                offset_x + 100 + 400 * opportunity.start - 400 * (self._time - 1) - moving_offset,
                self._screen_size_y - 250 - row * 100,
                400 * (opportunity.end - opportunity.start) * offset_len,
                95,
            ],
            4,
        )

    def _show_executed_opportunity(self, opportunity: ExecutedOpportunity, moving_offset: float, row: int):
        # Handle offsets, to be refactored
        offset_len = 1.0
        offset_x = 1.0
        if math.floor(opportunity.start) == self._time + 2 and moving_offset > 0:
            offset_len = 1 + moving_offset / 400
        elif math.floor(opportunity.start) == self._time + 1 and moving_offset < 0:
            offset_len = 2 + moving_offset / 400
        elif math.floor(opportunity.start) == self._time + 1:
            offset_len = 2
        if math.floor(opportunity.start) == self._time + 1 and moving_offset > 0:
            offset_len = 2 - moving_offset / 400
        elif math.floor(opportunity.start) == self._time and moving_offset < 0:
            offset_len = 1 - moving_offset / 400

        if math.floor(opportunity.start) == self._time + 2 and moving_offset > 0:
            offset_x = -moving_offset + (opportunity.start - math.floor(opportunity.start)) * moving_offset
        elif math.floor(opportunity.start) == self._time + 1 and moving_offset < 0:
            offset_x = (
                -400 - moving_offset + (opportunity.start - math.floor(opportunity.start)) * (400 + moving_offset)
            )
        elif math.floor(opportunity.start) == self._time + 1 and moving_offset == 0:
            offset_x = -400 + (opportunity.start - math.floor(opportunity.start)) * 400
        elif math.floor(opportunity.start) == self._time + 1 and moving_offset > 0:
            offset_x = -400 + (opportunity.start - math.floor(opportunity.start)) * (400 - moving_offset)
        elif math.floor(opportunity.start) == self._time and moving_offset < 0:
            offset_x = -400 + (opportunity.start - math.floor(opportunity.start)) * -moving_offset
        elif math.floor(opportunity.start) <= self._time:
            offset_x = -400

        if (
            opportunity not in self._already_shown_opportunities
            and opportunity.start < self._time + moving_offset / 400 - offset_x / 400
        ):
            # First time we pass an opportunity
            if opportunity.resolves_request():
                # If it resolves the request, we show an animation,
                # and set the other opportunities of the request to already shown
                # self._show_point_animation = True
                # self._point_animation.append(opportunity)
                # self._glob_offset_x = offset_x
                # self._glob_offset_len = offset_len
                # self._glob_height = row
                for other in self._opportunities_per_requests[opportunity.request]:
                    self._already_shown_opportunities.add(other)
                self._already_shown_finished_requests.add(opportunity.request)
                self._points += opportunity.points
            self._already_shown_opportunities.add(opportunity)
            self._draw_opportunity_rectangle(
                opportunity=opportunity, offset_x=offset_x, moving_offset=moving_offset, row=row, offset_len=offset_len
            )
        else:
            self._draw_opportunity_rectangle(
                opportunity=opportunity, offset_x=offset_x, moving_offset=moving_offset, row=row, offset_len=offset_len
            )

        if (opportunity.end - opportunity.start) * offset_len >= 0.3:
            font = pygame.font.SysFont(None, 30, False, False)
        else:
            font = pygame.font.SysFont(
                None, round(30 * ((opportunity.end - opportunity.start) * offset_len - 0.02) / 0.3), False, False
            )
        text = font.render(opportunity.request, True, self.DARK_GREY)
        self._screen.blit(
            text,
            [
                110 + 400 * opportunity.start - 400 * (self._time - 1) - moving_offset + offset_x,
                self._screen_size_y - 240 - row * 100,
                400 * (opportunity.end - opportunity.start),
                95,
            ],
        )
        text = font.render("Punkte: " + str(opportunity.points), True, self.DARK_GREY)
        self._screen.blit(
            text,
            [
                110 + 400 * opportunity.start - 400 * (self._time - 1) - moving_offset + offset_x,
                self._screen_size_y - 180 - row * 100,
                400 * (opportunity.end - opportunity.start),
                95,
            ],
        )

    @staticmethod
    def _distribute_opportunities(turns: list[set[ExecutedOpportunity]]) -> list[dict[ExecutedOpportunity, int]]:
        result: list[dict[ExecutedOpportunity, int]] = []
        for opportunities in turns:
            turn_result: dict[ExecutedOpportunity, int] = {}
            for opportunity in sorted(opportunities, key=lambda x: x.start):
                turn_result[opportunity] = max(
                    [turn_result[opp] + 1 for opp in opportunities if opportunity.overlaps(opp) and opp in turn_result]
                    + [0]
                )
            result.append(turn_result)
        return result

    def _draw_timeline(self, moving_offset: float, forward_direction: bool):
        pos_line = 0
        for m in range(12):  # dicke Striche
            if pos_line == 4 and forward_direction is not False:
                pygame.draw.rect(
                    self._screen,
                    self.WHITE,
                    [-300 + 400 * pos_line - moving_offset * 2, self._screen_size_y - 100, 5, 50],
                )
            elif pos_line == 2 and forward_direction is False:
                pygame.draw.rect(
                    self._screen,
                    self.WHITE,
                    [-300 + 400 * pos_line - moving_offset * 2, self._screen_size_y - 100, 5, 50],
                )
            elif (pos_line == 3) and moving_offset != 0:
                print("")
            elif not (pos_line == 2 and moving_offset == 0):
                pygame.draw.rect(
                    self._screen, self.WHITE, [-300 + 400 * pos_line - moving_offset, self._screen_size_y - 100, 5, 50]
                )
            else:
                pygame.draw.rect(
                    self._screen, self.RED, [-300 + 400 * pos_line - moving_offset, self._screen_size_y - 100, 5, 50]
                )
                pos_line += 1
            if pos_line < 3 and not pos_line + self._time == -1:  # Schrift
                text = self._font.render(f"Time: {pos_line + self._time}", True, self.WHITE)
            else:
                text = self._font.render(f"Time: {pos_line - 1 + self._time}", True, self.WHITE)
            if (not pos_line == 2 or moving_offset > 30 or moving_offset < -30) and not pos_line + self._time == -1:
                if not pos_line == 3:
                    if (pos_line == 4 and forward_direction is not True) or (
                        pos_line == 2 and forward_direction is False
                    ):
                        self._screen.blit(text, [-340 + 400 * pos_line - moving_offset * 2, self._screen_size_y - 35])
                    else:
                        self._screen.blit(text, [-340 + 400 * pos_line - moving_offset, self._screen_size_y - 35])

            pos_small_line = 0
            if not pos_line == 3:  # dünne Striche
                if pos_line == 4 and forward_direction is True:
                    for n in range(9):
                        pygame.draw.rect(
                            self._screen,
                            self.WHITE,
                            [
                                -260
                                + 40 * moving_offset / 400
                                + 400 * pos_line
                                + 40 * pos_small_line * (1 + moving_offset / 400)
                                - moving_offset * 2,
                                self._screen_size_y - 70,
                                5,
                                20,
                            ],
                        )
                        pos_small_line += 1
                elif pos_line == 1 and forward_direction is False:
                    for n in range(9):
                        pygame.draw.rect(
                            self._screen,
                            self.WHITE,
                            [
                                -260
                                + 40 * -moving_offset / 400
                                + 400 * pos_line
                                + 40 * pos_small_line * (1 - moving_offset / 400)
                                - moving_offset,
                                self._screen_size_y - 70,
                                5,
                                20,
                            ],
                        )
                        pos_small_line += 1
                elif (not pos_line == 2 or moving_offset == 0) and not pos_line == 2:
                    for n in range(9):
                        pygame.draw.rect(
                            self._screen,
                            self.WHITE,
                            [
                                -260 + 400 * pos_line + 40 * pos_small_line - moving_offset,
                                self._screen_size_y - 70,
                                5,
                                20,
                            ],
                        )
                        pos_small_line += 1

            else:
                if pos_line == 3 and forward_direction is True:
                    for n in range(9):
                        pygame.draw.rect(
                            self._screen,
                            self.WHITE,
                            [
                                -400
                                - 260
                                + 40 * (1 - moving_offset / 400)
                                + 400 * pos_line
                                + 40 * pos_small_line * (2 - moving_offset / 400)
                                - moving_offset,
                                self._screen_size_y - 70,
                                5,
                                20,
                            ],
                        )
                        pos_small_line += 1
                elif pos_line == 3 and forward_direction is False:
                    for n in range(9):
                        pygame.draw.rect(
                            self._screen,
                            self.WHITE,
                            [
                                -400
                                - 260
                                + 40 * -moving_offset / 400
                                + 400 * pos_line
                                + 40 * pos_small_line * (2 + moving_offset / 400)
                                - moving_offset * 2,
                                self._screen_size_y - 70,
                                5,
                                20,
                            ],
                        )
                        pos_small_line += 1
                elif (pos_line != 3 or moving_offset == 0) and not (pos_line == 2 and forward_direction is True):
                    for n in range(9):
                        pygame.draw.rect(
                            self._screen,
                            self.WHITE,
                            [
                                -220 + 400 * (pos_line - 1) + 80 * pos_small_line - moving_offset,
                                self._screen_size_y - 70,
                                5,
                                20,
                            ],
                        )
                        pos_small_line += 1
            pos_line += 1

    def _show_total_points(self):
        pygame.draw.rect(self._screen, self.WHITE, [10, 10, 230, 60])
        pygame.draw.rect(self._screen, self.DARK_GREY, [10, 10, 230, 60], 4)
        points_text = self._font.render("Punkte: " + str(self._points).rjust(9), True, self.RED)
        self._screen.blit(points_text, [30, 28])

    def _show_current_time(self):
        current_time_text = self._font.render("Jetzt", True, self.RED)
        self._screen.blit(current_time_text, [470, self._screen_size_y - 35])
        for g in range(math.floor((self._screen_size_y - 100) / 70)):
            pygame.draw.rect(self._screen, self.GREY_RED, [500, -20 + 70 * g, 5, 50])

    def _show_point_animations(self, moving_offset: float):
        eintrag = self._point_animation[-1]
        point_x = self._glob_offset_x + 100 + 400 * eintrag.start - 400 * (self._time - 1) - moving_offset
        point_y = float(self._screen_size_y - 250 - self._glob_height * 100)
        point_dx = -2.0
        point_dy = 0.0
        for i in range(65):
            pygame.draw.ellipse(self._screen, self.GREEN, [point_x - 2.5, point_y - 2.5, 5, 5])
            point_x += point_dx
            point_y += point_dy
            point_dy += -0.2 * 1.7
            if i > 25:
                point_dx += 0.12 * 1.7
            else:
                point_dx -= 0.12 * 2.2
            if i > 40:
                point_dy -= 1
            pygame.time.wait(10)
            pygame.display.flip()
        self._points += eintrag.points
        pygame.time.wait(100)
        self._show_point_animation = False

    def _update_timeline(self, moving_offset: float, forward_direction: bool):
        self._screen.fill(self.GREY)

        self._draw_timeline(moving_offset=moving_offset, forward_direction=forward_direction)

        for turn in self._opportunities:
            for opportunity, row in turn:
                self._show_executed_opportunity(opportunity, moving_offset, row)

        self._show_total_points()
        self._show_current_time()

        # Interrupt time progress to show point gain animation
        # if self._show_point_animation:
        #    self._show_point_animations(moving_offset=moving_offset)

        pygame.display.flip()

    def visualize(self) -> None:
        """
        Visualize the game interactively using pygame
        """

        keep_running = True
        while keep_running:

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    keep_running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        if not self._auto_mode and self._time >= 0:
                            self._move_timeline_backwards(1.5)
                    elif event.key == pygame.K_RIGHT and self._time < self._max_time - 1:
                        if not self._auto_mode:
                            self._move_timeline_forward(1.5)
                    elif event.key == pygame.K_SPACE:
                        self._auto_mode = not self._auto_mode

            # Handle Auto mode
            if self._auto_mode:
                if self._time < self._max_time - 1:
                    self._move_timeline_forward(0.25)
                else:
                    self._auto_mode = False

            # Clear screen
            self._screen.fill(self.GREY)

            # Update screen and wait briefly
            self._update_timeline(0, True)
            pygame.display.flip()
            pygame.time.wait(20)

        pygame.quit()
