import asyncio
import time
from datetime import datetime
from uuid import UUID

from PIL import Image
from bleak import BleakClient

from ESL import ESL
from tram_times import get_next_trams
from utils import make_tram_img, image2hex

ESL_MAC = "A4:C1:38:7D:43:A9"
PRIMARY_SERVICE_UUID = UUID("13187b10-eba9-a3ba-044e-83d3217d9a38")
WRITE_CHARACTERISTIC_UUID = UUID("4b646063-6264-f3a7-8941-e65356ea82fe")
MAX_CHUNK_SIZE = 480
SLEEP_SECONDS = 60 * 15

async def main(img_hex: str):
    async with BleakClient(ESL_MAC, timeout=30) as client:
        if client.is_connected:
            esl = ESL(client, WRITE_CHARACTERISTIC_UUID)
            await esl.upload_image(img_hex, MAX_CHUNK_SIZE)
        else:
            print(f"Failed to connect to {ESL_MAC}")


if __name__ == "__main__":
    while True:
        try:
            next_trams = get_next_trams(3, datetime.now())
            img: Image = make_tram_img(next_trams)
            img_hex = image2hex(img)
            asyncio.run(main(img_hex))
            time.sleep(SLEEP_SECONDS)
        except:
            print("Failed to refresh trams")
