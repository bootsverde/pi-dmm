import pygame
import math
import sys
import time

W, H = 800, 480

BLACK = (0, 0, 0)
WHITE = (220, 220, 220)
GREEN = (0, 255, 0)
RED = (255, 50, 50)
CYAN = (0, 220, 255)
GRAY = (60, 60, 60)
DARK_GRAY = (30, 30, 30)
LIGHT_GRAY = (120, 120, 120)
ORANGE = (255, 160, 0)
YELLOW = (255, 255, 0)


def draw_arc_gauge(screen, cx, cy, radius, value, max_val, label, unit, fonts, color):
    start_angle = math.radians(225)
    end_angle = math.radians(-45)
    sweep = start_angle - end_angle

    pygame.draw.arc(screen, (40, 40, 40),
                    (cx - radius, cy - radius, radius * 2, radius * 2),
                    math.radians(-45), math.radians(225), 4)

    green_end = 0.7 * sweep
    yellow_end = 0.85 * sweep
    segments = 60
    for i in range(segments):
        frac = i / segments
        angle = start_angle - frac * sweep
        if frac < 0.7:
            c = GREEN
        elif frac < 0.85:
            c = YELLOW
        else:
            c = RED
        x1 = cx + int((radius - 8) * math.cos(angle))
        y1 = cy - int((radius - 8) * math.sin(angle))
        x2 = cx + int((radius + 2) * math.cos(angle))
        y2 = cy - int((radius + 2) * math.sin(angle))
        pygame.draw.line(screen, c, (x1, y1), (x2, y2), 2)

    num_ticks = 10
    for i in range(num_ticks + 1):
        frac = i / num_ticks
        angle = start_angle - frac * sweep
        inner = radius - 18
        outer = radius - 8
        x1 = cx + int(inner * math.cos(angle))
        y1 = cy - int(inner * math.sin(angle))
        x2 = cx + int(outer * math.cos(angle))
        y2 = cy - int(outer * math.sin(angle))
        pygame.draw.line(screen, LIGHT_GRAY, (x1, y1), (x2, y2), 2)

        tick_val = max_val * frac
        txt = fonts["tiny"].render(f"{tick_val:.0f}", True, LIGHT_GRAY)
        tx = cx + int((inner - 14) * math.cos(angle))
        ty = cy - int((inner - 14) * math.sin(angle))
        screen.blit(txt, txt.get_rect(center=(tx, ty)))

    for i in range(num_ticks * 5 + 1):
        frac = i / (num_ticks * 5)
        angle = start_angle - frac * sweep
        inner = radius - 12
        outer = radius - 8
        x1 = cx + int(inner * math.cos(angle))
        y1 = cy - int(inner * math.sin(angle))
        x2 = cx + int(outer * math.cos(angle))
        y2 = cy - int(outer * math.sin(angle))
        pygame.draw.line(screen, (60, 60, 60), (x1, y1), (x2, y2), 1)

    norm = min(value / max_val, 1.0)
    needle_angle = start_angle - norm * sweep
    needle_len = radius - 25
    nx = cx + int(needle_len * math.cos(needle_angle))
    ny = cy - int(needle_len * math.sin(needle_angle))

    tail_len = 15
    tx = cx - int(tail_len * math.cos(needle_angle))
    ty = cy + int(tail_len * math.sin(needle_angle))

    perp = needle_angle + math.pi / 2
    bw = 4
    p1 = (tx + int(bw * math.cos(perp)), ty - int(bw * math.sin(perp)))
    p2 = (tx - int(bw * math.cos(perp)), ty + int(bw * math.sin(perp)))
    pygame.draw.polygon(screen, color, [p1, (nx, ny), p2])
    pygame.draw.line(screen, WHITE, (tx, ty), (nx, ny), 1)

    pygame.draw.circle(screen, (80, 80, 80), (cx, cy), 8)
    pygame.draw.circle(screen, color, (cx, cy), 5)

    val_str = f"{value:.2f}"
    val_txt = fonts["large"].render(val_str, True, color)
    unit_txt = fonts["med"].render(unit, True, LIGHT_GRAY)
    total = val_txt.get_width() + 8 + unit_txt.get_width()
    vx = cx - total // 2
    screen.blit(val_txt, (vx, cy + 20))
    screen.blit(unit_txt, (vx + val_txt.get_width() + 8, cy + 28))

    lbl = fonts["med"].render(label, True, CYAN)
    screen.blit(lbl, lbl.get_rect(center=(cx, cy + 60)))


def draw_mini_scope(screen, rect, t, fonts):
    sx, sy, sw, sh = rect
    pygame.draw.rect(screen, DARK_GRAY, rect)
    pygame.draw.rect(screen, LIGHT_GRAY, rect, 1)

    for i in range(1, 4):
        gx = sx + i * sw // 4
        pygame.draw.line(screen, (40, 40, 40), (gx, sy), (gx, sy + sh))
    cy = sy + sh // 2
    pygame.draw.line(screen, (40, 40, 40), (sx, cy), (sx + sw, cy))

    points = []
    for i in range(sw - 4):
        px = sx + 2 + i
        py = cy + int((sh // 3) * math.sin(0.06 * i + t * 3))
        points.append((px, py))
    if len(points) > 1:
        pygame.draw.lines(screen, GREEN, False, points, 2)


def draw_cont_indicator(screen, cx, cy, radius, is_cont, resistance, fonts):
    pygame.draw.circle(screen, DARK_GRAY, (cx, cy), radius)
    pygame.draw.circle(screen, LIGHT_GRAY, (cx, cy), radius, 2)

    if is_cont:
        pygame.draw.circle(screen, GREEN, (cx, cy), radius - 10)
        txt = fonts["large"].render("CONT", True, BLACK)
        screen.blit(txt, txt.get_rect(center=(cx, cy - 10)))
        val = fonts["med"].render(f"{resistance:.1f} Ω", True, BLACK)
        screen.blit(val, val.get_rect(center=(cx, cy + 20)))
    else:
        inner = radius - 10
        pygame.draw.circle(screen, (30, 15, 15), (cx, cy), inner)
        txt = fonts["large"].render("OPEN", True, RED)
        screen.blit(txt, txt.get_rect(center=(cx, cy - 10)))
        val = fonts["med"].render("O.L", True, RED)
        screen.blit(val, val.get_rect(center=(cx, cy + 20)))


def main():
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Gauge Preview — Dials & Gauges")
    clock = pygame.time.Clock()

    fonts = {
        "huge": pygame.font.Font(None, 80),
        "large": pygame.font.Font(None, 44),
        "med": pygame.font.Font(None, 30),
        "small": pygame.font.Font(None, 24),
        "tiny": pygame.font.Font(None, 18),
    }

    t = 0
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        t += 0.02
        screen.fill(BLACK)

        voltage = 12.47 + 2.0 * math.sin(t * 0.5)
        draw_arc_gauge(screen, 200, 200, 150, voltage, 50, "VDC", "V", fonts, GREEN)

        resistance = 470 + 30 * math.sin(t * 0.3)
        draw_arc_gauge(screen, 580, 200, 150, resistance, 1000, "OHMS", "Ω", fonts, CYAN)

        scope_rect = pygame.Rect(20, 340, 360, 120)
        draw_mini_scope(screen, scope_rect, t, fonts)
        scope_lbl = fonts["small"].render("SCOPE", True, CYAN)
        screen.blit(scope_lbl, (25, 325))

        is_cont = math.sin(t * 0.7) > 0
        draw_cont_indicator(screen, 600, 410, 55, is_cont, 12.3, fonts)

        clock.tick(30)
        pygame.display.flip()

    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    main()
