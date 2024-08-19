"Module containing configuration constants and error classes"

from os import getcwd

from shutil import which

from typing import Any


class DictionaryTypeError(BaseException):
    'Error, YoutubeDL did not return a dictionary when using the "extract_info" method'

    def __init__(self):
        super().__init__(self.__doc__)


class PlaylistError(BaseException):
    'Error, the provided url belongs to a playlist, please provide a url of a single song at a time'

    def __init__(self):
        super().__init__(self.__doc__)


class FFmpegError(BaseException):
    'Error, "ffmpeg_location" not defined in YoutubeDL configuration variable'

    def __init__(self):
        super().__init__(self.__doc__)


_CONFIG: dict[str, Any] = {
    "noplaylist": True,
    "writethumbnail": True,
    "extract_audio": True,
    "format": "bestaudio/best",
    "ffmpeg_location": which("ffmpeg"),
    "postprocessors": [
        {
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }
    ],
    "outtmpl": f"{getcwd()}/%(title)s.%(ext)s",
    "force_generic_extractor": False,
    "quiet": False
}
"Configuration dictionary for music download"
