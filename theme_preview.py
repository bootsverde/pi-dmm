import pygame
import math
import sys

W, H = 800, 480

THEMES = {
    "FLUKE": {
        "bg": (45, 45, 40),
        "reading": (255, 220, 0),
        "unit": (255, 200, 0),
        "scope_trace": (255, 210, 0),
        "scope_bg": (30, 30, 28),
        "scope_grid": (55, 55, 50),
        "scope_center": (65, 65, 58),
        "btn_active": (255, 180, 0),
        "btn_inactive": (55, 55, 50),
        "btn_text_active": (30, 30, 28),
        "btn_text_inactive": (200, 190, 140),
        "btn_border": (200, 170, 0),
        "hold_color": (255, 220, 0),
        "label": (180, 170, 120),
        "scale": (150, 140, 100),
        "alert": (255, 60, 30),
    },
}


def draw_preview(screen, theme, x_off, title, fonts):
    t = THEMES[theme]
    pw = W // 2 - 30
    ph = H - 40

    panel = pygame.Rect(x_off, 20, pw, ph)
    pygame.draw.rect(screen, t["bg"], panel, border_radius=8)
    pygame.draw.rect(screen, t["btn_border"], panel, 2, border_radius=8)

    title_txt = fonts["med"].render(title, True, t["unit"])
    screen.blit(title_txt, title_txt.get_rect(center=(x_off + pw // 2, 45)))

    btn_names = ["VAC", "VDC", "Ω", "CONT", "SCOPE"]
    btn_w = (pw - 60) // 5
    for i, name in enumerate(btn_names):
        bx = x_off + 15 + i * (btn_w + 6)
        by = 60
        rect = pygame.Rect(bx, by, btn_w, 35)
        if i == 1:
            pygame.draw.rect(screen, t["btn_active"], rect, border_radius=6)
            txt = fonts["small"].render(name, True, t["btn_text_active"])
        else:
            pygame.draw.rect(screen, t["btn_inactive"], rect, border_radius=6)
            txt = fonts["small"].render(name, True, t["btn_text_inactive"])
        pygame.draw.rect(screen, t["btn_border"], rect, 1, border_radius=6)
        screen.blit(txt, txt.get_rect(center=rect.center))

    reading = fonts["huge"].render("12.47", True, t["reading"])
    unit = fonts["large"].render("V", True, t["unit"])
    total = reading.get_width() + 10 + unit.get_width()
    rx = x_off + (pw - total) // 2
    screen.blit(reading, (rx, 110))
    screen.blit(unit, (rx + reading.get_width() + 10, 125))

    sx = x_off + 15
    sy = 210
    sw = pw - 30
    sh = 140
    scope = pygame.Rect(sx, sy, sw, sh)
    pygame.draw.rect(screen, t["scope_bg"], scope)
    pygame.draw.rect(screen, t["scale"], scope, 1)

    for i in range(1, 8):
        gx = sx + i * sw // 8
        pygame.draw.line(screen, t["scope_grid"], (gx, sy), (gx, sy + sh))
    for i in range(1, 4):
        gy = sy + i * sh // 4
        pygame.draw.line(screen, t["scope_grid"], (sx, gy), (sx + sw, gy))

    cy = sy + sh // 2
    pygame.draw.line(screen, t["scope_center"], (sx, cy), (sx + sw, cy))

    points = []
    for i in range(sw - 10):
        px = sx + 5 + i
        py = cy + int(35 * math.sin(i * 0.06)) + int(12 * math.sin(i * 0.18))
        points.append((px, py))
    pygame.draw.lines(screen, t["scope_trace"], False, points, 2)

    hi = fonts["tiny"].render("3.3", True, t["scale"])
    lo = fonts["tiny"].render("-3.3", True, t["scale"])
    screen.blit(hi, (sx + sw - 35, sy + 3))
    screen.blit(lo, (sx + sw - 40, sy + sh - 18))

    hold_rect = pygame.Rect(x_off + pw - 100, sy + sh + 15, 85, 30)
    pygame.draw.rect(screen, t["btn_inactive"], hold_rect, border_radius=5)
    pygame.draw.rect(screen, t["hold_color"], hold_rect, 2, border_radius=5)
    hold_txt = fonts["small"].render("HOLD", True, t["hold_color"])
    screen.blit(hold_txt, hold_txt.get_rect(center=hold_rect.center))

    fuse_txt = fonts["small"].render("▸ FUSE OK", True, t["label"])
    screen.blit(fuse_txt, (x_off + 20, sy + sh + 20))


def main():
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Theme Preview — Classic Fluke")

    fonts = {
        "huge": pygame.font.Font(None, 80),
        "large": pygame.font.Font(None, 48),
        "med": pygame.font.Font(None, 32),
        "small": pygame.font.Font(None, 24),
        "tiny": pygame.font.Font(None, 20),
    }

    screen.fill((10, 10, 10))

    draw_preview(screen, "FLUKE", W // 4 - 5, "CLASSIC FLUKE", fonts)

    pygame.display.flip()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    main()
