import time
import os
import asyncio
from PIL import Image
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser

async def fix_thumb(thumb):
    if thumb is not None:
        metadata = extractMetadata(createParser(thumb))
        if metadata is not None and metadata.has("width") and metadata.has("height"):
            width = metadata.get("width")
            height = metadata.get("height")
        else:
            width, height = 1280, 720
        Image.open(thumb).convert("RGB").save(thumb)
        img = Image.open(thumb)
        img.save(thumb, "JPEG")
        return width, height, thumb
    return 1280, 720, None
    
async def take_screen_shot(video_file, output_directory, ttl):
    out_put_file_name = f"{output_directory}/{time.time()}.jpg"
    file_genertor_command = [
        "ffmpeg",
        "-ss",
        str(ttl),
        "-i",
        video_file,
        "-vframes",
        "1",
        out_put_file_name
    ]
    process = await asyncio.create_subprocess_exec(
        *file_genertor_command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await process.communicate()
    e_response = stderr.decode().strip()
    t_response = stdout.decode().strip()
    if os.path.lexists(out_put_file_name):
        return out_put_file_name
    return None
