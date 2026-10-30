"""Draw an original procedural still for the included sample."""
from pathlib import Path

def create(path, width=960, height=540):
    pixels = bytearray()
    for y in range(height):
        for x in range(width):
            r = int(14 + 20 * y / height)
            g = int(27 + 19 * y / height)
            b = int(43 + 22 * y / height)
            if y > 422:
                r, g, b = 18, 30, 38
            # Window frame, lantern, warm light and simple rain strokes.
            if 236 < x < 724 and 58 < y < 418:
                r, g, b = 32, 54, 66
                if x % 47 < 2 and (y + x * 3) % 92 < 40:
                    r, g, b = 92, 128, 138
            if 222 < x < 738 and (y < 70 or y > 406):
                r, g, b = 97, 74, 56
            if 222 < x < 238 or 722 < x < 738:
                if 58 < y < 418:
                    r, g, b = 97, 74, 56
            if 456 < x < 504 and 268 < y < 367:
                r, g, b = 226, 164, 75
                if x < 464 or x > 496 or y < 276 or y > 359:
                    r, g, b = 111, 72, 45
            if 470 < x < 490 and 246 < y < 270:
                r, g, b = 111, 72, 45
            pixels.extend((r, g, b))
    Path(path).write_bytes(f"P6\n{width} {height}\n255\n".encode() + pixels)
