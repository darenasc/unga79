import json
from pathlib import Path

import pandas as pd
import requests
from tqdm import tqdm
from youtube_transcript_api import YouTubeTranscriptApi

from unga79.config import DATA_DIR, URL_SPEECHES


def save_json(data: dict, country: str, output_path: Path = DATA_DIR / "2024"):
    """Save the transcript as JSON file.

    Args:
        data (dict): `dict` with the transcript.
        country (str): Country of the speech.
        output_path (Path, optional): . Defaults to DATA_DIR/"2024".
    """
    with open(output_path / f"{country}.json", "w") as outfile:
        json.dump(data, outfile)


def get_transcript(video_id: str) -> dict | None:
    """Collect the transcript from YouTube.

    Args:
        video_id (str): `id` of the YouTube video.

    Returns:
        dict: The video's transcript.
    """
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return transcript
    except Exception as e:
        print(e)
        return None


def download_all_transcripts(
    df_speeches: pd.DataFrame, overwrite: bool = False, path: Path = DATA_DIR / "2024"
):
    """Downloads the transcript of all the urls in the dataframe.

    Args:
        df_speeches (pd.DataFrame): Dataframe with urls to speeches.
        overwrite (bool, optional): Download again if the file already exists.
            Defaults to False.
        path (Path, optional): Path to save the json files. Defaults to
            DATA_DIR/"2024".
    """
    path.mkdir(parents=True, exist_ok=True)
    pbar = tqdm(df_speeches.iterrows(), total=len(df_speeches))
    for _, r in pbar:
        pbar.set_description(r["country"])
        if (path / f"{r['country']}.json").is_file() and not overwrite:
            continue
        transcript = get_transcript(r["url"].split("?v=")[-1])
        if transcript:
            save_json(transcript, r["country"])


def get_video_url_list(
    url: str = URL_SPEECHES,
    save: bool = True,
    path: Path = DATA_DIR / "UN Speeches.csv",
) -> pd.DataFrame:
    """Return a dataframe with columns ['url', 'country', 'start', 'end'].

    The function download the spreadsheet, store it locally and then returns the stored copy of the spreadsheet.

    Args:
        url (str): URL of the google spreadsheet with the data.
        save (bool, optional): _description_. Defaults to True.
        path (Path, optional): _description_. Defaults to DATA_DIR/"UN Speeches.csv".

    Returns:
        pd.DataFrame: Dataframe with data of the speeches.
    """

    def save_spreadsheet(path: Path):
        with open(path, "wb") as f:
            f.write(response.content)

    response = requests.get(url)

    if save:
        save_spreadsheet(path)

    df_speech_url = pd.read_csv(path)
    return df_speech_url


def get_corpus_from_file(
    country: str, start: int = 0, end: int = 3600, path: Path = DATA_DIR / "2024"
) -> str:
    """Returns a string with the transcript of a video.

    Args:
        country (str): Country of origin.
        start (int, optional): Second when the speaker starts speaking. Defaults to 0.
        end (int, optional): Second when the speaking finish speaking. Defaults to 3600.
        path (Path, optional): Path where the transcripts are stored. Defaults to DATA_DIR/"2024".

    Returns:
        str: A string with the transcript of a video.
    """
    with open(path / f"{country}.json") as f:
        json_data = json.load(f)
    corpus = [x["text"] for x in json_data if x["start"] > start and x["start"] < end]
    large_corpus = " ".join([x for x in corpus])
    return large_corpus


def get_seconds_from_str(start: str, end: str) -> tuple[int, int]:
    if isinstance(start, str):
        hours, minutes, seconds = start.split(":")
        start_seconds = int(hours) * 60 * 60 + int(minutes) * 60 + int(seconds)
    else:
        start_seconds = 0
    if isinstance(end, str):
        hours, minutes, seconds = end.split(":")
        end_seconds = int(hours) * 60 * 60 + int(minutes) * 60 + int(seconds)
    else:
        end_seconds = 3600
    return start_seconds, end_seconds
