from typing import Union

import aiohttp
import aiofiles  # type: ignore
import asyncio
import os
import pandas as pd

df = pd.read_csv("pinterest.csv")


def files_name(directory: str) -> Union[list[str], None]:
    try:
        files = os.listdir(directory)
        files = [
            file.split(".")[0]
            for file in files
            if os.path.isfile(os.path.join(directory, file))
        ]

        return files
    except Exception as e:
        print(f"Error: {e}")
        return None


def convert_to_url(signature: str) -> str:
    prefix = "http://i.pinimg.com/400x/%s/%s/%s/%s.jpg"
    return prefix % (signature[0:2], signature[2:4], signature[4:6], signature)


async def download_and_save_image(
    session: aiohttp.ClientSession, url: str, save_directory: str, file_name: str
) -> None:
    try:
        async with session.get(url) as response:
            if response.status == 200:
                image_data = await response.read()
                save_path = os.path.join(save_directory, file_name)

                async with aiofiles.open(save_path, "wb") as file:
                    await file.write(image_data)
            else:
                print(f"Failed to download image. Status code: {response.status}")
    except Exception as e:
        print(f"Error downloading image: {e}")


async def main() -> None:
    save_directory = "pins"
    args_list = []

    async with aiohttp.ClientSession() as session:
        files = files_name(save_directory)
        unique_files = df.image_signature.unique()
        if files:
            rest = list(set(unique_files) - set(files))
        else:
            rest = unique_files

        for image_sig in rest:
            url = convert_to_url(image_sig)
            file_name = f"{image_sig}.jpg"
            args_list.append((session, url, save_directory, file_name))

        tasks = [download_and_save_image(*args) for args in args_list]
        await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
