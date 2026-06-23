import pygame
import numpy as np
from config import *


class Display:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Pi DMM")

        self.font_huge = pygame.font.Font(None, 160)
        self.font_large = pygame.font.Font(None, 72)
        self.font_med = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 28)

        btn_w = 140
        btn_h = 50
        self.mode_buttons = []
        for i in range(len(MODE_NAMES)):
            x = 15 + i * (btn_w + 10)
            self.mode_buttons.append(pygame.Rect(x, 8, btn_w, btn_h))

        self.hold_button = pygame.Rect(SCREEN_WIDTH - 150, SCREEN_HEIGHT - 52, 130, 42)
        self.scope_rect = pygame.Rect(20, 260, SCREEN_WIDTH - 40, 170)

    def update(self, mode, reading, waveform, holding):
        self.screen.fill(BLACK)
        self._draw_mode_bar(mode)
        self._draw_reading(mode, reading, holding)
        self._draw_scope(waveform, mode)
        self._draw_hold_button(holding)
        pygame.display.flip()

    def _draw_mode_bar(self, active):
        for i, (name, rect) in enumerate(zip(MODE_NAMES, self.mode_buttons)):
            if i == active:
                pygame.draw.rect(self.screen, CYAN, rect, border_radius=8)
                text_color = BLACK
            else:
                pygame.draw.rect(self.screen, GRAY, rect, border_radius=8)
                text_color = WHITE
            pygame.draw.rect(self.screen, WHITE, rect, 2, border_radius=8)
            txt = self.font_med.render(name, True, text_color)
            self.screen.blit(txt, txt.get_rect(center=rect.center))

    def _draw_reading(self, mode, reading, holding):
        reading_str, unit = self._format_reading(mode, reading)

        color = GREEN
        if mode == MODE_CONT and reading < CONTINUITY_THRESHOLD:
            color = RED
        if holding:
            color = YELLOW

        txt = self.font_huge.render(reading_str, True, color)
        unit_txt = self.font_large.render(unit, True, LIGHT_GRAY)
        total_w = txt.get_width() + 12 + unit_txt.get_width()
        x_start = (SCREEN_WIDTH - total_w) // 2
        self.screen.blit(txt, (x_start, 90))
        self.screen.blit(unit_txt, (x_start + txt.get_width() + 12, 110))

        if holding:
            h = self.font_med.render("HOLD", True, YELLOW)
            self.screen.blit(h, (SCREEN_WIDTH - 100, 75))

        if mode == MODE_CONT and reading < CONTINUITY_THRESHOLD:
            beep = self.font_large.render("BEEP", True, RED)
            self.screen.blit(beep, (SCREEN_WIDTH - 130, 120))

    def _format_reading(self, mode, reading):
        if mode in (MODE_OHM, MODE_CONT):
            if reading == float("inf"):
                return "O.L", "Ω"
            if reading >= 1_000_000:
                return f"{reading / 1_000_000:.2f}", "MΩ"
            if reading >= 1000:
                return f"{reading / 1000:.2f}", "kΩ"
            return f"{reading:.1f}", "Ω"

        if mode == MODE_ACV:
            return f"{reading:.1f}", "V~"

        if mode == MODE_DCV:
            if abs(reading) < 1.0:
                return f"{reading * 1000:.1f}", "mV"
            return f"{reading:.2f}", "V"

        if mode == MODE_SCOPE:
            return f"{reading:.2f}", "V"

        return f"{reading:.2f}", ""

    def _draw_scope(self, waveform, mode):
        pygame.draw.rect(self.screen, DARK_GRAY, self.scope_rect)
        pygame.draw.rect(self.screen, LIGHT_GRAY, self.scope_rect, 1)

        sx, sy, sw, sh = self.scope_rect

        for i in range(1, 8):
            x = sx + i * sw // 8
            pygame.draw.line(self.screen, (40, 40, 40), (x, sy), (x, sy + sh))
        for i in range(1, 4):
            y = sy + i * sh // 4
            pygame.draw.line(self.screen, (40, 40, 40), (sx, y), (sx + sw, y))

        center_y = sy + sh // 2
        pygame.draw.line(self.screen, (50, 50, 50), (sx, center_y), (sx + sw, center_y))

        if not waveform or len(waveform) < 2:
            no_data = self.font_small.render("No signal", True, LIGHT_GRAY)
            self.screen.blit(no_data, no_data.get_rect(center=self.scope_rect.center))
            return

        data = np.array(waveform[-WAVEFORM_SAMPLES:])
        d_min, d_max = np.min(data), np.max(data)
        d_range = d_max - d_min
        if d_range < 0.001:
            d_range = 1.0
            d_min = np.mean(data) - 0.5

        points = []
        n = len(data)
        for i, val in enumerate(data):
            px = sx + int(i * sw / n)
            norm = (val - d_min) / d_range
            py = sy + sh - 5 - int(norm * (sh - 10))
            points.append((px, py))

        pygame.draw.lines(self.screen, GREEN, False, points, 2)

        hi = self.font_small.render(f"{d_max:.1f}", True, LIGHT_GRAY)
        lo = self.font_small.render(f"{d_min:.1f}", True, LIGHT_GRAY)
        self.screen.blit(hi, (sx + sw - 55, sy + 2))
        self.screen.blit(lo, (sx + sw - 55, sy + sh - 22))

    def _draw_hold_button(self, holding):
        color = YELLOW if holding else GRAY
        pygame.draw.rect(self.screen, color, self.hold_button, border_radius=6)
        pygame.draw.rect(self.screen, WHITE, self.hold_button, 2, border_radius=6)
        txt = self.font_med.render("HOLD", True, BLACK if holding else WHITE)
        self.screen.blit(txt, txt.get_rect(center=self.hold_button.center))

    def handle_touch(self, pos):
        for i, rect in enumerate(self.mode_buttons):
            if rect.collidepoint(pos):
                return ("mode", i)
        if self.hold_button.collidepoint(pos):
            return ("hold", None)
        return (None, None)

    def cleanup(self):
        pygame.quit()
