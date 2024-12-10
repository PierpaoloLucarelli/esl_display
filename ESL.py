from uuid import UUID

from bleak import BleakClient
from utils import hex_to_bytes


class ESL:
    def __init__(self, client: BleakClient, write_char_uuid: UUID) -> None:
        self.client = client
        self.write_char_uuid = write_char_uuid

    async def write_to_characteristic(self, char_uuid: UUID, char_bytes: bytearray):
        return await self.client.write_gatt_char(char_uuid, char_bytes, response=True)

    async def upload_chunk(self, chunk: str):
        chunk_bytes = hex_to_bytes("03" + chunk)
        await self.write_to_characteristic(self.write_char_uuid, chunk_bytes)

    async def upload_image(self, img_hex: str, chunk_size: int):
        chunks = [img_hex[i : i + chunk_size] for i in range(0, len(img_hex), chunk_size)]
        await self.write_to_characteristic(self.write_char_uuid, hex_to_bytes("0000"))
        await self.write_to_characteristic(self.write_char_uuid, hex_to_bytes("020000"))
        for chunk in chunks:
            await self.upload_chunk(chunk)
        await self.write_to_characteristic(self.write_char_uuid, hex_to_bytes("01"))
