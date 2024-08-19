"Module for handling metadata and creating covers"

from mutagen.id3 import ID3
from mutagen.id3._frames import APIC, TCON, TDRC, TIT2, TPE1, USLT
from mutagen.id3._specs import Encoding

from PIL import Image

from os.path import splitext


def add_metadata(mp3_path: str, data: dict[str, str | bytes]) -> None:
    """Add metadata to an mp3 file

    Args:
        mp3_path: string containing the path to the mp3 file
        data: dictionary with organized metadata
    """

    metadata = ID3()

    metadata["TPE1"] = TPE1(text=data["artist"])
    metadata["TIT2"] = TIT2(text=data["title"])
    metadata["TDRC"] = TDRC(text=data["date"])

    if "genres" in data:
        metadata["TCON"] = TCON(text=data["genres"])

    if "lyric" in data:
        metadata["SYLT"] = USLT(
            text=data["lyric"],
            encoding=Encoding.UTF8,
            lang="und"
        )

    if "cover" in data:
        metadata["APIC"] = APIC(
                data=data["cover"],
                mime="image/jpeg",
                type=0
            )

    metadata.save(mp3_path)


def create_cover(image_path: str, image_size: tuple[int, int] = (600, 600)) -> str:
    """Creates a jpeg cover to be implemented in mp3 files

    Args:
        image_path: string containing path to the image that will generate a cover
        image_size (optional): tuple containing the height and width of the image in integers

    Returns:
        file_name: string containing the path of the created cover file
    """

    image_data = Image.open(image_path)
    image_data = image_data.resize(image_size)

    file_name: str
    file_name, _ = splitext(image_path)
    file_name = f"{file_name}.cover.jpeg"

    image_data.save(file_name, "JPEG")

    return file_name
