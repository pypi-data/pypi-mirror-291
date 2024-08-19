# SpeechService.set_transcription(self, model: str = None, kwargs: dict = {}) method is removed,
# timestamps_to_word_boundaries method is removed
from abc import ABC, abstractmethod
import typing as t
import os
import json
import sys
import hashlib
import shutil
from pathlib import Path
from manim import config, logger
from slugify import slugify
from manim_onvoice.defaults import (
    DEFAULT_VOICEOVER_CACHE_DIR,
    DEFAULT_VOICEOVER_CACHE_JSON_FILENAME,
)
from manim_onvoice.helper import (
    append_to_json_file,
    remove_bookmarks,
)
from manim_onvoice.modify_audio import adjust_speed
from manim_onvoice.tracker import AUDIO_OFFSET_RESOLUTION


# def timestamps_to_word_boundaries(segments):
#     word_boundaries = []
#     current_text_offset = 0
#     for segment in segments:
#         for dict_ in segment["words"]:
#             word = dict_["word"]
#             word_boundaries.append(
#                 {
#                     "audio_offset": int(dict_["start"] * AUDIO_OFFSET_RESOLUTION),
#                     # "duration_milliseconds": 0,
#                     "text_offset": current_text_offset,
#                     "word_length": len(word),
#                     "text": word,
#                     "boundary_type": "Word",
#                 }
#             )
#             current_text_offset += len(word)
#             # If word is not punctuation, add a space
#             # if word not in [".", ",", "!", "?", ";", ":", "(", ")"]:
#             # current_text_offset += 1

#     return word_boundaries


class SpeechService(ABC):
    """Abstract base class for a speech service."""

    def __init__(
        self,
        global_speed: float = 1.00,
        cache_dir: t.Optional[str] = None,
        **kwargs,
    ):
        """
        Args:
            global_speed (float, optional): The speed at which to play the audio.
                Defaults to 1.00.
            cache_dir (str, optional): The directory to save the audio
                files to. Defaults to ``voiceovers/``.
        """
        self.global_speed = global_speed

        if cache_dir is not None:
            self.cache_dir = cache_dir
        else:
            self.cache_dir = Path(config.media_dir) / DEFAULT_VOICEOVER_CACHE_DIR

        if os.path.exists(self.cache_dir):
            key = input("Can you remove voiceover directory? [Yes/No] : ")[-1].lower()
            if key == "y":
                shutil.rmtree(self.cache_dir)
                os.makedirs(self.cache_dir)
        else:
            os.makedirs(self.cache_dir)

    def _wrap_generate_from_text(self, text: str, path: str = None, **kwargs) -> dict:
        # Replace newlines with lines, reduce multiple consecutive spaces to single
        text = " ".join(text.split())

        dict_ = self.generate_from_text(text, cache_dir=None, path=path, **kwargs)
        original_audio = dict_["original_audio"]

        # Audio callback
        self.audio_callback(original_audio, dict_, **kwargs)

        if self.global_speed != 1:
            split_path = os.path.splitext(original_audio)
            adjusted_path = split_path[0] + "_adjusted" + split_path[1]

            adjust_speed(
                str(Path(self.cache_dir) / dict_["original_audio"]),
                str(Path(self.cache_dir) / adjusted_path),
                self.global_speed,
            )
            dict_["final_audio"] = adjusted_path
            if "word_boundaries" in dict_:
                for word_boundary in dict_["word_boundaries"]:
                    word_boundary["audio_offset"] = int(
                        word_boundary["audio_offset"] / self.global_speed
                    )
        else:
            dict_["final_audio"] = dict_["original_audio"]

        append_to_json_file(
            Path(self.cache_dir) / DEFAULT_VOICEOVER_CACHE_JSON_FILENAME, dict_
        )
        return dict_

    def get_audio_basename(self, data: dict) -> str:
        dumped_data = json.dumps(data)
        data_hash = hashlib.sha256(dumped_data.encode("utf-8")).hexdigest()
        suffix = data_hash[:8]
        input_text = data["input_text"]
        input_text = remove_bookmarks(input_text)
        print(input_text)
        slug = slugify(input_text, max_length=50, word_boundary=True, save_order=True)
        ret = f"{slug}-{suffix}"
        return ret

    @abstractmethod
    def generate_from_text(
        self, text: str, cache_dir: str = None, path: str = None
    ) -> dict:
        """Implement this method for each speech service. Refer to `AzureService` for an example.

        Args:
            text (str): The text to synthesize speech from.
            cache_dir (str, optional): The output directory to save the audio file and data to. Defaults to None.
            path (str, optional): The path to save the audio file to. Defaults to None.

        Returns:
            dict: Output data dictionary. TODO: Define the format.
        """
        raise NotImplementedError

    def get_cached_result(self, input_data, cache_dir):
        json_path = os.path.join(cache_dir / DEFAULT_VOICEOVER_CACHE_JSON_FILENAME)
        if os.path.exists(json_path):
            json_data = json.load(open(json_path, "r"))
            for entry in json_data:
                if entry["input_data"] == input_data:
                    return entry
        return None

    def audio_callback(self, audio_path: str, data: dict, **kwargs):
        """Callback function for when the audio file is ready.
        Override this method to do something with the audio file, e.g. noise reduction.

        Args:
            audio_path (str): The path to the audio file.
            data (dict): The data dictionary.
        """
        pass
