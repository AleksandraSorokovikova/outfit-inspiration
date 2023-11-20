import aiohttp
import aiofiles
import asyncio
import os
import pandas as pd

df = pd.read_csv(
    "/Users/evgeniia.vu/Desktop/CUB study/ADL/complete-the-look-dataset/datasets/raw_train.tsv",
    sep="\t",
)


def files_name(directory):
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


def convert_to_url(signature):
    prefix = "http://i.pinimg.com/400x/%s/%s/%s/%s.jpg"
    return prefix % (signature[0:2], signature[2:4], signature[4:6], signature)


async def download_and_save_image(session, url, save_directory, file_name):
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


async def main():
    save_directory = "/Users/evgeniia.vu/Desktop/CUB study/ADL/datasets/clothes/images"
    args_list = []

    async with aiohttp.ClientSession() as session:
        files = files_name(save_directory)
        unique_files = df.image_signature.unique()
        rest = list(set(unique_files) - set(files))

        for image_sig in rest:
            url = convert_to_url(image_sig)
            file_name = f"{image_sig}.jpg"
            args_list.append((session, url, save_directory, file_name))

        tasks = [download_and_save_image(*args) for args in args_list]
        await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
