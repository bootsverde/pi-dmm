import pygame
import math
import random
import sys

W, H = 800, 480

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
DIM_GREEN = (0, 120, 0)
DARK_GREEN = (0, 40, 0)
FAINT_GREEN = (0, 20, 0)
BRIGHT = (150, 255, 150)
WHITE_GREEN = (200, 255, 200)

CHARS = "0123456789ABCDEFabcdef+-.:=ΩVμΔ∿πΣ√∞#@%&*!?"


class RainDrop:
    def __init__(self, x, col_h):
        self.x = x
        self.col_h = col_h
        self.reset()

    def reset(self):
        self.y = random.randint(-self.col_h, 0)
        self.speed = random.uniform(2, 8)
        self.length = random.randint(6, 22)
        self.chars = [random.choice(CHARS) for _ in range(self.length)]

    def update(self):
        self.y += self.speed
        if self.y - self.length * 14 > self.col_h:
            self.reset()
        if random.random() < 0.1:
            idx = random.randint(0, self.length - 1)
            self.chars[idx] = random.choice(CHARS)


def main():
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Matrix DMM Preview")
    clock = pygame.time.Clock()

    font_rain = pygame.font.Font(None, 20)
    font_huge = pygame.font.Font(None, 160)
    font_large = pygame.font.Font(None, 72)
    font_med = pygame.font.Font(None, 36)
    font_small = pygame.font.Font(None, 28)

    columns = W // 14
    drops = [RainDrop(i * 14, H) for i in range(columns)]

    overlay = pygame.Surface((W, H), pygame.SRCALPHA)

    t = 0
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        t += 0.02

        fade = pygame.Surface((W, H))
        fade.fill(BLACK)
        fade.set_alpha(80)
        screen.blit(fade, (0, 0))

        for drop in drops:
            drop.update()
            for j, ch in enumerate(drop.chars):
                cy = int(drop.y) - j * 14
                if 0 <= cy < H:
                    if j == 0:
                        color = WHITE_GREEN
                    elif j < 3:
                        color = BRIGHT
                    elif j < 8:
                        color = GREEN
                    elif j < 14:
                        color = DIM_GREEN
                    else:
                        color = DARK_GREEN
                    txt = font_rain.render(ch, True, color)
                    screen.blit(txt, (drop.x, cy))

        overlay.fill((0, 0, 0, 0))

        top_bg = pygame.Surface((W, 58), pygame.SRCALPHA)
        top_bg.fill((0, 0, 0, 180))
        screen.blit(top_bg, (0, 0))

        btn_names = ["VAC", "VDC", "Ω", "CONT", "SCOPE"]
        btn_count = len(btn_names)
        margin = 15
        total_space = W - 2 * margin
        btn_w = (total_space - (btn_count - 1) * 10) // btn_count
        for i, name in enumerate(btn_names):
            bx = margin + i * (btn_w + 10)
            rect = pygame.Rect(bx, 8, btn_w, 50)
            if i == 1:
                pygame.draw.rect(screen, GREEN, rect, border_radius=8)
                txt = font_med.render(name, True, BLACK)
            else:
                pygame.draw.rect(screen, (0, 30, 0), rect, border_radius=8)
                pygame.draw.rect(screen, DIM_GREEN, rect, 1, border_radius=8)
                txt = font_med.render(name, True, DIM_GREEN)
            screen.blit(txt, txt.get_rect(center=rect.center))

        reading_bg = pygame.Surface((W, 170), pygame.SRCALPHA)
        reading_bg.fill((0, 0, 0, 160))
        screen.blit(reading_bg, (0, 62))

        voltage = 12.47 + 0.03 * math.sin(t * 2)
        reading_str = f"{voltage:.2f}"
        unit_str = "V"
        rtxt = font_huge.render(reading_str, True, GREEN)
        utxt = font_large.render(unit_str, True, DIM_GREEN)
        total_w = rtxt.get_width() + 12 + utxt.get_width()
        rx = (W - total_w) // 2
        screen.blit(rtxt, (rx, 90))
        screen.blit(utxt, (rx + rtxt.get_width() + 12, 110))

        scope_rect = pygame.Rect(20, 260, W - 40, 150)
        scope_bg = pygame.Surface((scope_rect.w, scope_rect.h), pygame.SRCALPHA)
        scope_bg.fill((0, 0, 0, 160))
        screen.blit(scope_bg, scope_rect.topleft)
        pygame.draw.rect(screen, DARK_GREEN, scope_rect, 1)

        sx, sy, sw, sh = scope_rect
        for i in range(1, 8):
            gx = sx + i * sw // 8
            pygame.draw.line(screen, FAINT_GREEN, (gx, sy), (gx, sy + sh))
        for i in range(1, 4):
            gy = sy + i * sh // 4
            pygame.draw.line(screen, FAINT_GREEN, (sx, gy), (sx + sw, gy))
        center_y = sy + sh // 2
        pygame.draw.line(screen, DARK_GREEN, (sx, center_y), (sx + sw, center_y))

        points = []
        for i in range(sw - 4):
            px = sx + 2 + i
            py = center_y + int(40 * math.sin(0.05 * i + t * 3)) + int(15 * math.sin(0.15 * i + t * 5))
            points.append((px, py))
        if len(points) > 1:
            pygame.draw.lines(screen, GREEN, False, points, 2)
            glow_points = [(p[0], p[1]) for p in points]
            glow_surf2 = pygame.Surface((sw, sh), pygame.SRCALPHA)
            shifted = [(p[0] - sx, p[1] - sy) for p in glow_points]
            if len(shifted) > 1:
                pygame.draw.lines(glow_surf2, (0, 255, 0, 40), False, shifted, 6)
                screen.blit(glow_surf2, (sx, sy))

        hold_rect = pygame.Rect(W - 150, H - 42, 130, 36)
        hold_bg = pygame.Surface((hold_rect.w, hold_rect.h), pygame.SRCALPHA)
        hold_bg.fill((0, 0, 0, 180))
        screen.blit(hold_bg, hold_rect.topleft)
        pygame.draw.rect(screen, DIM_GREEN, hold_rect, 1, border_radius=6)
        htxt = font_med.render("HOLD", True, DIM_GREEN)
        screen.blit(htxt, htxt.get_rect(center=hold_rect.center))

        clock.tick(30)
        pygame.display.flip()

    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    main()
