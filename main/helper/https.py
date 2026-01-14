import aiofiles
import aiohttp
from httpx import AsyncClient, Timeout

fetch = AsyncClient(
    http2=True,
    verify=False,
    headers={
        "Accept-Language": "en-US,en;q=0.9,id-ID;q=0.8,id;q=0.7",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edge/107.0.1418.42",
    },
    timeout=Timeout(80),
)


async def upload_media(media):
    base_url = "https://0x0.st"
    async with aiohttp.ClientSession() as session:
        form_data = aiohttp.FormData()
        form_data.add_field("reqtype", "fileupload")

        async with aiofiles.open(media, mode="rb") as file:
            file_data = await file.read()
            form_data.add_field(
                "fileToUpload",
                file_data,
                filename=media,
                content_type="application/octet-stream",
            )

        async with session.post(base_url, data=form_data) as response:
            response.raise_for_status()
            return (await response.text()).strip()


"""
async def upload_media(media):
    # media = await m.reply_to_message.download()
    url = "https://itzpire.com/tools/upload"
    with open(media, "rb") as file:
        files = {"file": file}
        response = await fetch.post(url, files=files)
    if response.status_code == 200:
        data = response.json()
        link = data["fileInfo"]["url"]
        return link
    else:
        return f"{response.text}"
"""
