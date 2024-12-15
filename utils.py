from datetime import datetime
from pathlib import Path

from PIL import Image, ImageDraw
from PIL.Image import Dither

LEFT_PAD = 15
COL2_X = 100
ROW_HEIGHT = 30
ICONS_PATH = (Path(__file__).parent / "icons").resolve()

def hex_to_bytes(hex_string: str):
    cleaned_hex = hex_string.replace(" ", "").replace(",", "").replace("0x", "")
    return bytearray.fromhex(cleaned_hex)


def bytes2hex(_bytes):
    return "".join(hex(item)[2:].zfill(2) for item in _bytes)


def image2hex(image, width=255, height=122, dither=Dither.NONE):
    image = image.resize((width, height)).rotate(90, expand=True)
    return bytes2hex(image.resize((height, width)).convert("1", dither=dither).tobytes())


def make_tram_img(next_trams: list[dict]):
    image = Image.new("L", (250, 122), 255)
    image.paste(make_header(), (0,0))
    for i, tram in enumerate(next_trams):
        image.paste(make_tram_row(i%2==0, tram), (0, 32 + (i*ROW_HEIGHT)))
    # image.show()
    return image

def make_header():
    image = Image.new("L", (250, 32), 0)
    draw = ImageDraw.Draw(image)
    draw.text((LEFT_PAD, 6),"Den Haag Centraal", fill=(255,), font_size=16)
    return image

def make_tram_row(white: bool, tram: dict[str, any]):
    back_col = 255 if white else 0
    acc_col = 0 if white else 255
    str_rep = "white" if white else "black"
    image = Image.new("L", (250, 30), back_col)
    draw = ImageDraw.Draw(image)
    tram_ico = Image.open(ICONS_PATH / f"tram_ico_{str_rep}.bmp")
    image.paste(tram_ico, (LEFT_PAD, 5))
    start_x = (LEFT_PAD+5)+tram_ico.width+2
    draw.rectangle([start_x, 10, start_x+13, 23], fill=(acc_col,))

    draw.text((start_x+3, 8), tram["num"], fill=(back_col,), font_size=12)

    draw.text(((LEFT_PAD*2)+10+tram_ico.width, 7), tram["dep"].strftime("%H:%M"), fill=(acc_col,), font_size=12)

    walk_ico = Image.open(ICONS_PATH / f"walk_ico_{str_rep}.bmp")
    image.paste(walk_ico, (COL2_X, 5))
    draw.text(((COL2_X+3)+tram_ico.width, 7), tram["leave"].strftime("%H:%M"), fill=(acc_col,), font_size=12)



    return image


