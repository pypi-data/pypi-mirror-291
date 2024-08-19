"Module for using the tool via the command line"

from argparse import ArgumentParser, Namespace

from os import remove
from os.path import splitext

from typing import Any
from types import NoneType

from definitions import _CONFIG
from downloader import download_music
from metadata import add_metadata, create_cover


def main():
    "Main function of the code"

    arguments: ArgumentParser = ArgumentParser(
        prog="you-mp3",
        description="Program to download mp3 music directly from YouTube",
        epilog="https://github.com/RuanMiguel-DRD/You-MP3",
    )

    arguments.add_argument(
        "url",
        help="link to the song or playlist you want to download",
        type=str
    )

    arguments.add_argument(
        "-l",
        dest="lyric",
        help="path to file containing song lyrics",
        type=str
    )

    arguments.add_argument(
        "-g",
        dest="genres",
        help="musical genres that will be attributed to the music",
        nargs="*",
        type=str
    )

    arguments.add_argument(
        "-q",
        dest="quality",
        default="medium",
        choices=["low", "medium", "high"],
        help="choose the sound quality level",
        type=str
    )

    args: Namespace = arguments.parse_args()

    url: str = args.url
    lyric: str | NoneType = args.lyric
    genres: str | NoneType = args.genres
    quality: str = args.quality


    if type(lyric) == NoneType:
        lyric = "Unknown Lyric"

    else:
        try:
            lyric = open(lyric, "r", encoding="utf-8").read()

        except:
            lyric = "Unknown Lyric"
            print("Could not read the file containing the song's lyrics")


    if type(genres) == NoneType:
        genres = "Unknown Genre"

    else:
        first_genre: bool = True

        for gen in genres:

            if first_genre == True:
                first_genre = False
                genres = gen

            else:
                genres = f"{genres};{gen}"


    match quality:

        case "low":
            quality = "128"

        case "medium":
            quality = "192"

        case "high":
            quality = "320"


    config: dict[str, Any] = _CONFIG
    config["postprocessors"][0]["preferredquality"] = quality

    metadata: dict[str, Any] = download_music(url, config)

    metadata["lyric"] = lyric
    metadata["genres"] = genres

    path: str = metadata["path"]
    path, _ = splitext(path)

    path_cover: str = create_cover(f"{path}.webp")
    metadata["cover"] = open(path_cover, "rb").read()

    add_metadata(f"{path}.mp3", metadata)

    remove(path_cover)
    remove(f"{path}.webp")


    print("Music downloaded successfully")

if __name__ == "__main__":
    main()
