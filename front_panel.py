import pygame
import math
import sys

W, H = 900, 500
BG = (40, 40, 45)
PANEL = (25, 25, 30)
BEZEL = (60, 60, 65)
RED = (220, 40, 40)
BLACK = (15, 15, 15)
YELLOW = (240, 220, 50)
WHITE = (220, 220, 220)
GRAY = (100, 100, 105)
CYAN = (0, 200, 240)
DARK = (20, 20, 22)
GOLD = (180, 160, 60)
FUSE_GLASS = (200, 180, 140, 180)
GREEN_LED = (0, 220, 80)


def draw_banana_jack(screen, cx, cy, color, label, font):
    pygame.draw.circle(screen, (50, 50, 50), (cx, cy), 24)
    pygame.draw.circle(screen, color, (cx, cy), 20)
    pygame.draw.circle(screen, BLACK, (cx, cy), 8)
    pygame.draw.circle(screen, (80, 80, 80), (cx, cy), 20, 2)
    txt = font.render(label, True, WHITE)
    screen.blit(txt, txt.get_rect(center=(cx, cy - 38)))


def draw_fuse_holder(screen, cx, cy, font):
    pygame.draw.rect(screen, (50, 50, 55), (cx - 40, cy - 12, 80, 24), border_radius=4)
    pygame.draw.rect(screen, GRAY, (cx - 40, cy - 12, 80, 24), 2, border_radius=4)
    pygame.draw.rect(screen, (60, 55, 45), (cx - 30, cy - 8, 60, 16), border_radius=8)
    pygame.draw.rect(screen, (180, 170, 140), (cx - 20, cy - 5, 40, 10), border_radius=4)
    for dx in [-28, 28]:
        pygame.draw.circle(screen, (160, 160, 160), (cx + dx, cy), 5)
    txt = font.render("FUSE", True, YELLOW)
    screen.blit(txt, txt.get_rect(center=(cx, cy - 28)))
    rating = font.render("500mA", True, GRAY)
    screen.blit(rating, rating.get_rect(center=(cx, cy + 28)))


def draw_encoder(screen, cx, cy, font):
    pygame.draw.circle(screen, (50, 50, 55), (cx, cy), 32)
    pygame.draw.circle(screen, (70, 70, 75), (cx, cy), 28)
    pygame.draw.circle(screen, (45, 45, 50), (cx, cy), 24)
    for angle in range(0, 360, 30):
        rad = math.radians(angle)
        x1 = cx + int(20 * math.cos(rad))
        y1 = cy + int(20 * math.sin(rad))
        x2 = cx + int(24 * math.cos(rad))
        y2 = cy + int(24 * math.sin(rad))
        pygame.draw.line(screen, (90, 90, 95), (x1, y1), (x2, y2), 1)
    pygame.draw.circle(screen, (100, 100, 105), (cx, cy), 28, 2)
    pygame.draw.line(screen, WHITE, (cx, cy - 18), (cx, cy - 8), 2)
    txt = font.render("SELECT", True, CYAN)
    screen.blit(txt, txt.get_rect(center=(cx, cy - 48)))
    push = font.render("push=HOLD", True, GRAY)
    screen.blit(push, push.get_rect(center=(cx, cy + 48)))


def draw_screen_cutout(screen, x, y, w, h, font):
    pygame.draw.rect(screen, BLACK, (x - 3, y - 3, w + 6, h + 6), border_radius=6)
    pygame.draw.rect(screen, (10, 30, 10), (x, y, w, h), border_radius=4)
    pygame.draw.rect(screen, GRAY, (x - 3, y - 3, w + 6, h + 6), 2, border_radius=6)
    lines = ["12.47 V", "~~~~~~~~"]
    small = pygame.font.Font(None, 28)
    big = pygame.font.Font(None, 48)
    reading = big.render("12.47 V", True, GREEN_LED)
    screen.blit(reading, reading.get_rect(center=(x + w // 2, y + h // 3)))
    wave_y = y + h * 2 // 3
    points = []
    for i in range(w - 20):
        px = x + 10 + i
        py = wave_y + int(15 * math.sin(i * 0.08))
        points.append((px, py))
    if len(points) > 1:
        pygame.draw.lines(screen, GREEN_LED, False, points, 1)
    label = font.render("5\" DSI TOUCH", True, GRAY)
    screen.blit(label, label.get_rect(center=(x + w // 2, y + h + 16)))


def draw_power_jack(screen, cx, cy, font):
    pygame.draw.circle(screen, (50, 50, 55), (cx, cy), 14)
    pygame.draw.circle(screen, BLACK, (cx, cy), 10)
    pygame.draw.circle(screen, (60, 60, 65), (cx, cy), 14, 2)
    pygame.draw.circle(screen, (80, 80, 80), (cx, cy), 4)
    txt = font.render("5V USB-C", True, GRAY)
    screen.blit(txt, txt.get_rect(center=(cx, cy - 26)))


def draw_led(screen, cx, cy, color, label, font):
    pygame.draw.circle(screen, (40, 40, 40), (cx, cy), 8)
    pygame.draw.circle(screen, color, (cx, cy), 5)
    pygame.draw.circle(screen, (80, 80, 80), (cx, cy), 8, 1)
    txt = font.render(label, True, GRAY)
    screen.blit(txt, txt.get_rect(center=(cx, cy + 18)))


def main():
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Pi DMM — Front Panel")

    font = pygame.font.Font(None, 22)
    title_font = pygame.font.Font(None, 40)
    sub_font = pygame.font.Font(None, 18)

    screen.fill(BG)

    panel_rect = pygame.Rect(30, 30, W - 60, H - 60)
    pygame.draw.rect(screen, PANEL, panel_rect, border_radius=12)
    pygame.draw.rect(screen, BEZEL, panel_rect, 3, border_radius=12)

    screw_positions = [
        (50, 50), (W - 50, 50), (50, H - 50), (W - 50, H - 50)
    ]
    for sx, sy in screw_positions:
        pygame.draw.circle(screen, (70, 70, 75), (sx, sy), 8)
        pygame.draw.circle(screen, (40, 40, 45), (sx, sy), 4)
        pygame.draw.circle(screen, (90, 90, 95), (sx, sy), 8, 1)

    title = title_font.render("Pi DMM", True, CYAN)
    screen.blit(title, title.get_rect(center=(W // 2, 55)))
    sub = sub_font.render("VAC  VDC  OHM  CONT  SCOPE", True, GRAY)
    screen.blit(sub, sub.get_rect(center=(W // 2, 78)))

    draw_screen_cutout(screen, 80, 100, 340, 200, font)

    draw_fuse_holder(screen, 530, 140, font)

    draw_banana_jack(screen, 510, 260, RED, "V/Ω", font)
    draw_banana_jack(screen, 590, 260, YELLOW, "COM", font)

    draw_encoder(screen, 730, 170, font)

    draw_power_jack(screen, 730, 280, font)

    draw_led(screen, 660, 370, GREEN_LED, "PWR", font)
    draw_led(screen, 700, 370, RED, "OVL", font)

    mode_labels = ["VAC", "VDC", "Ω", "CONT", "SCOPE"]
    arc_cx, arc_cy = 730, 170
    for i, label in enumerate(mode_labels):
        angle = math.radians(-140 + i * 70)
        lx = arc_cx + int(58 * math.cos(angle))
        ly = arc_cy + int(58 * math.sin(angle))
        txt = sub_font.render(label, True, CYAN)
        screen.blit(txt, txt.get_rect(center=(lx, ly)))

    spec_lines = [
        "AC: 0-240V RMS",
        "DC: 0-50V",
        "Ω: 0-10MΩ",
        "CONT: <50Ω beep",
    ]
    for i, line in enumerate(spec_lines):
        txt = sub_font.render(line, True, GRAY)
        screen.blit(txt, (80, 330 + i * 20))

    hw_lines = [
        "Pi 5 + ADS1115 ADC",
        "ZMPT101B AC isolation",
    ]
    for i, line in enumerate(hw_lines):
        txt = sub_font.render(line, True, GRAY)
        screen.blit(txt, (80, 420 + i * 20))

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
