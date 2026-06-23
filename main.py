import pygame
import sys
from config import *
from dmm import DMM
from display import Display


def main():
    dmm = DMM()
    display = Display()
    clock = pygame.time.Clock()
    mode = MODE_DCV

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                action, value = display.handle_touch(event.pos)
                if action == "mode":
                    if value != mode:
                        mode = value
                        dmm.waveform.clear()
                elif action == "hold":
                    dmm.toggle_hold()

        reading = dmm.read(mode)
        waveform = dmm.get_waveform()
        display.update(mode, reading, waveform, dmm.hold)

        clock.tick(120 if mode == MODE_SCOPE else 30)

    dmm.cleanup()
    display.cleanup()
    sys.exit(0)


if __name__ == "__main__":
    main()
