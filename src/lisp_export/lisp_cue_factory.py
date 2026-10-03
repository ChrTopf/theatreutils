import uuid

STYLESHEET = "font-size:11pt;"


class LispCueFactory:
    """Creates the JSON dictionaries of the Linux Show Player (0.6.5) cue types used by the cue generator.

    Every cue gets a fresh id. The `index` (position in the cue list) is assigned
    later by LispProjectBuilder once the order of all cues is known.
    """

    def osc_cue(self, name: str, description: str, path: str, args: list[dict]) -> dict:
        cue = self._base_cue("OscCue", name, description)
        cue.update({
            "args": args,
            "duration": 0.0,
            "fade_type": "Linear",
            "path": path,
        })
        return cue

    @staticmethod
    def osc_integer_arg(value: int) -> dict:
        return {"end": 0, "fade": False, "start": value, "type": "Integer"}

    def media_cue(self, name: str, description: str, uri: str) -> dict:
        """A cue playing the audio file `uri`, which LiSP resolves relative to the project file."""
        cue = self._base_cue("GstMediaCue", name, description)
        cue.update({
            "default_start_action": "FadeInStart",
            "default_stop_action": "FadeOutStop",
            "duration": 0,
            "media": {
                "duration": 0,
                "elements": {
                    "AutoSink": {},
                    "DbMeter": {"interval": 33000000, "peak_falloff": 20, "peak_ttl": 1000000000},
                    "Equalizer10": {f"band{band}": 0 for band in range(10)},
                    # An unknown modification time makes LiSP read the duration from the file on load.
                    "UriInput": {
                        "_mtime": -1,
                        "buffer_size": -1,
                        "download": False,
                        "duration": 0,
                        "uri": uri,
                        "use_buffering": False,
                    },
                    "Volume": {"mute": False, "normal_volume": 1.0, "volume": 1.0},
                },
                "loop": 0,
                "pipe": ["UriInput", "Volume", "Equalizer10", "DbMeter", "AutoSink"],
                "start_time": 0,
                "stop_time": 0,
            },
        })
        return cue

    def collection_cue(self, name: str, description: str, targets: list[dict]) -> dict:
        """A cue that starts all `targets` at the same time."""
        cue = self._base_cue("CollectionCue", name, description)
        cue.update({
            "duration": 0,
            "targets": [[target["id"], "Default"] for target in targets],
        })
        return cue

    @staticmethod
    def _base_cue(cue_type: str, name: str, description: str) -> dict:
        return {
            "_type_": cue_type,
            "controller": {"keyboard": [], "midi": [], "osc": []},
            "default_start_action": "Start",
            "default_stop_action": "Stop",
            "description": description,
            "fadein_duration": 0.0,
            "fadein_type": "Linear",
            "fadeout_duration": 0.0,
            "fadeout_type": "Linear",
            "id": str(uuid.uuid4()),
            "index": 0,
            "name": name,
            "next_action": "DoNothing",
            "post_wait": 0.0,
            "pre_wait": 0.0,
            "stylesheet": STYLESHEET,
            "timecode": {"enabled": False, "replace_hours": False, "track": 0},
            "triggers": {},
        }
