{
    "cues": [
        {
            "_type_": "OscCue",
            "args": [
                {
                    "end": null,
                    "fade": false,
                    "start": "VS2 B14",
                    "type": "String"
                }
            ],
            "controller": {
                "keyboard": [],
                "midi": [],
                "osc": []
            },
            "default_start_action": "Start",
            "default_stop_action": "Stop",
            "description": "Mute Lisa,\nUnmute Beate",
            "duration": 0.0,
            "fade_type": "Linear",
            "fadein_duration": 0.0,
            "fadein_type": "Linear",
            "fadeout_duration": 0.0,
            "fadeout_type": "Linear",
            "id": "d35601ba-f590-46b1-9ae7-e48b736c68c4",
            "index": 0,
            "name": "Vorspann Scene 2 Block 14",
            "next_action": "DoNothing",
            "path": "/next/scene",
            "post_wait": 0.0,
            "pre_wait": 0.0,
            "stylesheet": "background:#ffffff;color:#000000;font-size:11pt;",
            "timecode": {
                "enabled": false,
                "replace_hours": false,
                "track": 0
            },
            "triggers": {}
        },
        {
            "_type_": "CollectionCue",
            "controller": {
                "keyboard": [],
                "midi": [],
                "osc": []
            },
            "default_start_action": "Start",
            "default_stop_action": "Stop",
            "description": "Executes multiple actions at once",
            "duration": 0,
            "fadein_duration": 0.0,
            "fadein_type": "Linear",
            "fadeout_duration": 0.0,
            "fadeout_type": "Linear",
            "id": "00c2d154-890c-4886-80c8-93cb48a83913",
            "index": 1,
            "name": "Akt 1 Scene 1 Block 30",
            "next_action": "DoNothing",
            "post_wait": 0.0,
            "pre_wait": 0.0,
            "stylesheet": "font-size:11pt;",
            "targets": [
                [
                    "72c8efea-673c-459e-b5ca-ee4f7baac614",
                    "Default"
                ],
                [
                    "661b45aa-80f2-40d7-8f24-1ea9e43ec9c0",
                    "Default"
                ],
                [
                    "f42250af-7520-49fa-986a-b972dae1d50d",
                    "Default"
                ]
            ],
            "timecode": {
                "enabled": false,
                "replace_hours": false,
                "track": 0
            },
            "triggers": {}
        },
        {
            "_type_": "OscCue",
            "args": [
                {
                    "end": 0,
                    "fade": false,
                    "start": 1,
                    "type": "Integer"
                }
            ],
            "controller": {
                "keyboard": [],
                "midi": [],
                "osc": []
            },
            "default_start_action": "Start",
            "default_stop_action": "Stop",
            "description": "Mute Beate,\nUnmute Lisa",
            "duration": 0.0,
            "fade_type": "Linear",
            "fadein_duration": 0.0,
            "fadein_type": "Linear",
            "fadeout_duration": 0.0,
            "fadeout_type": "Linear",
            "id": "72c8efea-673c-459e-b5ca-ee4f7baac614",
            "index": 2,
            "name": "-- Akt 1 Scene 1 Block 30 Mutes",
            "next_action": "DoNothing",
            "path": "/send/osc/command/here",
            "post_wait": 0.0,
            "pre_wait": 0.0,
            "stylesheet": "font-size:11pt;",
            "timecode": {
                "enabled": false,
                "replace_hours": false,
                "track": 0
            },
            "triggers": {}
        },
        {
            "_type_": "GstMediaCue",
            "controller": {
                "keyboard": [],
                "midi": [],
                "osc": []
            },
            "default_start_action": "FadeInStart",
            "default_stop_action": "FadeOutStop",
            "description": "Play some audio effect",
            "duration": 1175,
            "fadein_duration": 0.0,
            "fadein_type": "Linear",
            "fadeout_duration": 0.0,
            "fadeout_type": "Linear",
            "id": "661b45aa-80f2-40d7-8f24-1ea9e43ec9c0",
            "index": 3,
            "media": {
                "duration": 1175,
                "elements": {
                    "AutoSink": {},
                    "DbMeter": {
                        "interval": 33000000,
                        "peak_falloff": 20,
                        "peak_ttl": 1000000000
                    },
                    "Equalizer10": {
                        "band0": 0,
                        "band1": 0,
                        "band2": 0,
                        "band3": 0,
                        "band4": 0,
                        "band5": 0,
                        "band6": 0,
                        "band7": 0,
                        "band8": 0,
                        "band9": 0
                    },
                    "UriInput": {
                        "_mtime": 1791021359.4770043,
                        "buffer_size": -1,
                        "download": false,
                        "duration": 1175,
                        "uri": "mac-quack.mp3",
                        "use_buffering": false
                    },
                    "Volume": {
                        "mute": false,
                        "normal_volume": 1.0,
                        "volume": 1.0
                    }
                },
                "loop": 0,
                "pipe": [
                    "UriInput",
                    "Volume",
                    "Equalizer10",
                    "DbMeter",
                    "AutoSink"
                ],
                "start_time": 0,
                "stop_time": 0
            },
            "name": "-- Akt 1 Scene 1 Block 30 Sound",
            "next_action": "DoNothing",
            "post_wait": 0.0,
            "pre_wait": 0.0,
            "stylesheet": "font-size:11pt;",
            "timecode": {
                "enabled": false,
                "replace_hours": false,
                "track": 0
            },
            "triggers": {}
        },
        {
            "_type_": "OscCue",
            "args": [],
            "controller": {
                "keyboard": [],
                "midi": [],
                "osc": []
            },
            "default_start_action": "Start",
            "default_stop_action": "Stop",
            "description": "Mute Herbert,\nUnmute Lisa",
            "duration": 0.0,
            "fade_type": "Linear",
            "fadein_duration": 0.0,
            "fadein_type": "Linear",
            "fadeout_duration": 0.0,
            "fadeout_type": "Linear",
            "id": "ad407605-67e6-4231-a8ca-cd5f43775951",
            "index": 4,
            "name": "Akt 2 Scene 2 Block 35",
            "next_action": "DoNothing",
            "path": "",
            "post_wait": 0.0,
            "pre_wait": 0.0,
            "stylesheet": "font-size:11pt;",
            "timecode": {
                "enabled": false,
                "replace_hours": false,
                "track": 0
            },
            "triggers": {}
        },
        {
            "_type_": "MidiCue",
            "controller": {
                "keyboard": [],
                "midi": [],
                "osc": []
            },
            "default_start_action": "Start",
            "default_stop_action": "Stop",
            "description": "Light Effect: Nacht",
            "duration": 0,
            "fadein_duration": 0.0,
            "fadein_type": "Linear",
            "fadeout_duration": 0.0,
            "fadeout_type": "Linear",
            "id": "f42250af-7520-49fa-986a-b972dae1d50d",
            "index": 5,
            "message": "control_change channel=0 control=127 value=3",
            "name": "-- Akt 1 Scene 1 Block 30 Light",
            "next_action": "DoNothing",
            "post_wait": 0.0,
            "pre_wait": 0.0,
            "stylesheet": "font-size:10pt;",
            "timecode": {
                "enabled": false,
                "replace_hours": false,
                "track": 0
            },
            "triggers": {}
        }
    ],
    "meta": {
        "plugins": {
            "ActionCues": "0.6.5",
            "CacheManager": "0.6.5",
            "CartLayout": "0.6.5",
            "Controller": "0.6.5",
            "GstBackend": "0.6.5",
            "ListLayout": "0.6.5",
            "MediaInfo": "0.6.5",
            "Midi": "0.6.5",
            "Network": "0.6.5",
            "Osc": "0.6.5",
            "Presets": "0.6.5",
            "RenameCues": "0.6.5",
            "ReplayGain": "0.6.5",
            "Synchronizer": "0.6.5",
            "Timecode": "0.6.5",
            "Triggers": "0.6.5"
        },
        "version": "0.6.5"
    },
    "session": {
        "layout": {
            "accurate_time": false,
            "auto_continue": true,
            "dbmeters_visible": true,
            "go_key_disabled_while_playing": false,
            "index_column_visible": true,
            "seek_sliders_visible": true,
            "selection_mode": false,
            "view_sizes": [
                [
                    293,
                    1039
                ],
                [
                    280,
                    1703,
                    559
                ],
                [
                    1986,
                    560
                ]
            ]
        },
        "layout_type": "ListLayout"
    }
}