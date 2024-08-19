"""Library for downloading music in mp3 format and adding metadata
Allows simplified use via command line"""

# Library information

__description__ = "Music downloader with added metadata"
__status__ = "Educational"
__license__ = "Unlicense"
__version__ = "1.0.0"

__author__ = "RuanMiguel-DRD"
__maintainer__ = __author__
__credits__ = __author__

__url__ = "https://github.com/RuanMiguel-DRD/You-MP3"
__email__ = "ruanmigueldrd@outlook.com"

__keywords__ = [
    # Categories
    "audio", "conversion", "downloader", "music",

    # Dependencies
    "ffmpeg", "mutagen", "pillow", "yt-dlp",

    # Others 
    "metadata", "youtube", "mp3"
]

# Imports

from .definitions import DictionaryTypeError, PlaylistError, FFmpegError
from .definitions import _CONFIG

from .downloader import download_music

from .metadata import add_metadata, create_cover

__all__ = [
    "DictionaryTypeError", "PlaylistError", "FFmpegError", "_CONFIG",
    "download_music", "add_metadata", "create_cover"
]
