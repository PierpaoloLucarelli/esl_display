from PIL import Image, ImageDraw
from PIL.Image import Dither


def hex_to_bytes(hex_string: str):
    cleaned_hex = hex_string.replace(" ", "").replace(",", "").replace("0x", "")
    return bytearray.fromhex(cleaned_hex)


def bytes2hex(_bytes):
    return "".join(hex(item)[2:].zfill(2) for item in _bytes)


def image2hex(image, width=255, height=122, dither=Dither.NONE):
    image = image.resize((width, height)).rotate(90, expand=True)
    return bytes2hex(image.resize((height, width)).convert("1", dither=dither).tobytes())


def make_tram_img(next_trams: list[str]):
    image = Image.new("L", (250, 122), 255)
    draw = ImageDraw.Draw(image)
    # draw.rectangle((50, 50, 200, 72), fill=(255,), outline=(0,), width=5)
    for i, tram in enumerate(next_trams):
        draw.text((25, 35 + (i * 20)), str(tram), fill=(0,), font_size=16)
    return image
