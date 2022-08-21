import os
import threading
import multiprocessing
import collections

import pygame
import time
import math
import random
import os
import click

from bot import start_bot


def aspect_scale(img, bx, by):
    ix, iy = img.get_size()
    if ix > iy:
        scale_factor = bx / float(ix)
        sy = scale_factor * iy
        if sy > by:
            scale_factor = by / float(iy)
            sx = scale_factor * ix
            sy = by
        else:
            sx = bx
    else:
        scale_factor = by / float(iy)
        sx = scale_factor * ix
        if sx > bx:
            scale_factor = bx / float(ix)
            sx = bx
            sy = scale_factor * iy
        else:
            sy = by

    return pygame.transform.scale(img, (sx, sy))


def load_image(filename):
    info = pygame.display.Info()
    display_w, display_h = info.current_w, info.current_h
    image = pygame.image.load(filename)
    image = aspect_scale(image, display_w, display_h)
    return image


@click.command()
@click.argument("bot-key")
@click.option("--images-dir", default="imgs/")
@click.option("--window", is_flag=True)
@click.option("--display", type=int, default=0)
@click.option("--display-time", type=int, default=8)
def main(
    bot_key: str, window: bool, display: int, images_dir: str, display_time: float
):
    os.makedirs(images_dir, exist_ok=True)

    bot = multiprocessing.Process(
        target=start_bot, args=(bot_key, images_dir), daemon=True
    )
    bot.start()

    pygame.init()
    pygame.display.set_caption("Image")

    if window:
        surface = pygame.display.set_mode((1024, 768))
    else:
        surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN, display=display)

    info = pygame.display.Info()
    display_w, display_h = info.current_w, info.current_h

    clock = pygame.time.Clock()
    counter = collections.Counter()

    def draw(image):
        surface.blit(image, ((display_w - image.get_width()) // 2, 0))

    def show(old_image, new_image):
        for i in range(0, 260, 4):
            clock.tick(40)
            surface.fill((0, 0, 0))
            if old_image:
                old_image.set_alpha(255 - i)
                draw(old_image)
            if new_image:
                new_image.set_alpha(i)
                draw(new_image)
            pygame.display.update()

    def sample_images():
        while True:
            try:
                images = [
                    img for img in os.listdir(images_dir) if not img.endswith(".part")
                ]
                if not images:
                    return None
                time.sleep(display_time / 2)
                priorities = []
                for img in images:
                    count = math.exp(-counter.get(img, 0))
                    priorities.append(count)
                chosen = random.choices(images, weights=priorities)[0]
                counter[chosen] += 1
                return load_image(os.path.join(images_dir, chosen))
            except Exception as e:
                print(e)
                continue

    image1 = sample_images()

    while True:
        image2 = sample_images()

        show(image1, image2)
        time.sleep(display_time / 2)
        image1 = image2

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                bot.kill()
                pygame.quit()
                return
        pygame.display.update()


if __name__ == "__main__":
    main()
