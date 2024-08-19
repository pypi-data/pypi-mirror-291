"Module for downloading and extracting metadata from the platform"

from yt_dlp import YoutubeDL

from typing import Any

from definitions import DictionaryTypeError, PlaylistError, FFmpegError
from definitions import _CONFIG


def download_music(url: str, config: dict[str, Any] = _CONFIG) -> dict[str, str]:
    """Download the music and return your information

    Args:
        url: link to the music that will be downloaded
        config (optional): dictionary containing settings for YoutubeDL.

    Returns:
        metadata: dictionary with metadata about the downloaded music
    """

    if config["ffmpeg_location"] == None:
        raise FFmpegError

    data: dict[str, Any] | None
    with YoutubeDL({"extract_flat": True}) as youtube:
        data = youtube.extract_info(url, download=False)

        if type(data) != dict:
            raise DictionaryTypeError

        if "entries" in data:
            raise PlaylistError

        else:
            with YoutubeDL(config) as youtube:
                data = youtube.extract_info(url, download=True)
                youtube.close()

            if type(data) != dict:
                raise DictionaryTypeError

            path: str = youtube.prepare_filename(data)
            title: str = data.get("title", "Unknown Title")
            artist: str = data.get("uploader", "Unknown Artist")
            date: str = data.get("upload_date", "Unknown Date")

            if date != "Unknown Date":
                date = f"{date[:4]}-{date[4:6]}-{date[6:]}"

            else:
                date = "0000-00-00"

            metadata: dict[str, str] = {
                "path": path,
                "title": title,
                "artist": artist,
                "date": date
            }

            return metadata
