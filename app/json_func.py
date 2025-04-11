import json
import aiofiles


async def load_json(file_path):
    async with aiofiles.open(file_path, mode="r", encoding="utf-8") as f:
        contents = await f.read()
        return json.loads(contents)

async def save_json(file_path, data):
    async with aiofiles.open(file_path, mode='w', encoding='utf-8') as f:
        await f.write(json.dumps(data, indent=4))