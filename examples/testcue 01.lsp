{
    "cues": [
        {
            "_type_": "GstMediaCue",
            "controller": {
                "keyboard": [],
                "midi": [],
                "osc": []
            },
            "default_start_action": "FadeInStart",
            "default_stop_action": "FadeOutStop",
            "description": "Audio Effect Cue",
            "duration": 1175,
            "fadein_duration": 0.0,
            "fadein_type": "Linear",
            "fadeout_duration": 0.0,
            "fadeout_type": "Linear",
            "id": "865fba99-c158-45d9-9f70-2e51340856b4",
            "index": 0,
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
                        "_mtime": 1791021359.0,
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
            "name": "1. Akt Szene 1 Block 2",
            "next_action": "DoNothing",
            "post_wait": 0.0,
            "pre_wait": 0.0,
            "stylesheet": "background:#3584e4;font-size:10pt;",
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
                    "end": null,
                    "fade": false,
                    "start": "snippet",
                    "type": "String"
                },
                {
                    "end": 0,
                    "fade": false,
                    "start": 0,
                    "type": "Integer"
                },
                {
                    "end": 0,
                    "fade": false,
                    "start": 0,
                    "type": "Integer"
                },
                {
                    "end": 0,
                    "fade": false,
                    "start": 0,
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
            "description": "X32 snippet cue",
            "duration": 0.0,
            "fade_type": "Linear",
            "fadein_duration": 0.0,
            "fadein_type": "Linear",
            "fadeout_duration": 0.0,
            "fadeout_type": "Linear",
            "id": "90a476e4-e3c5-4eb4-8891-b1c128407901",
            "index": 1,
            "name": "1. Akt Szene 1 Block 4",
            "next_action": "DoNothing",
            "path": "/load",
            "post_wait": 0.0,
            "pre_wait": 0.0,
            "stylesheet": "background:#57e389;font-size:10pt;",
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
            "description": "MagicQ Light Cue",
            "duration": 0.0,
            "fade_type": "Linear",
            "fadein_duration": 0.0,
            "fadein_type": "Linear",
            "fadeout_duration": 0.0,
            "fadeout_type": "Linear",
            "id": "9299ef7a-eefb-46c1-ae50-532e97e03a36",
            "index": 2,
            "name": "1. Akt Szene 1 Block 5",
            "next_action": "DoNothing",
            "path": "/mq/pb/1/2",
            "post_wait": 0.0,
            "pre_wait": 0.0,
            "stylesheet": "background:#e01b24;font-size:10pt;",
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
                    "end": null,
                    "fade": false,
                    "start": "snippet",
                    "type": "String"
                },
                {
                    "end": 0,
                    "fade": false,
                    "start": 1,
                    "type": "Integer"
                },
                {
                    "end": 0,
                    "fade": false,
                    "start": 0,
                    "type": "Integer"
                },
                {
                    "end": 0,
                    "fade": false,
                    "start": 0,
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
            "description": "X32 Snippet Cue",
            "duration": 0.0,
            "fade_type": "Linear",
            "fadein_duration": 0.0,
            "fadein_type": "Linear",
            "fadeout_duration": 0.0,
            "fadeout_type": "Linear",
            "id": "037084ec-c461-4ee8-ab69-47242745eec0",
            "index": 3,
            "name": "1. Akt Szene 2 Block 10",
            "next_action": "TriggerAfterWait",
            "path": "/load",
            "post_wait": 0.0,
            "pre_wait": 0.0,
            "stylesheet": "background:#ff7800;font-size:11pt;",
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
            "description": "Audio Effect Cue",
            "duration": 1175,
            "fadein_duration": 0.0,
            "fadein_type": "Linear",
            "fadeout_duration": 0.0,
            "fadeout_type": "Linear",
            "id": "0c3f16c7-215f-4914-9f2b-0ed2d398412d",
            "index": 4,
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
                        "_mtime": 1791021359.0,
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
            "name": "1. Akt Szene 2 Block 10",
            "next_action": "DoNothing",
            "post_wait": 0.0,
            "pre_wait": 0.0,
            "stylesheet": "background:#ff7800;font-size:11pt;",
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
                    "end": null,
                    "fade": false,
                    "start": "snippet",
                    "type": "String"
                },
                {
                    "end": 0,
                    "fade": false,
                    "start": 2,
                    "type": "Integer"
                },
                {
                    "end": 0,
                    "fade": false,
                    "start": 0,
                    "type": "Integer"
                },
                {
                    "end": 0,
                    "fade": false,
                    "start": 0,
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
            "description": "",
            "duration": 0.0,
            "fade_type": "Linear",
            "fadein_duration": 0.0,
            "fadein_type": "Linear",
            "fadeout_duration": 0.0,
            "fadeout_type": "Linear",
            "id": "b4daa52b-9e0c-495d-bacb-638a50d3aca3",
            "index": 5,
            "name": "1. Akt Szene 3 Block 20",
            "next_action": "DoNothing",
            "path": "/load",
            "post_wait": 0.0,
            "pre_wait": 0.0,
            "stylesheet": "background:#9141ac;font-size:11pt;",
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
                    442,
                    1569
                ],
                [
                    422,
                    2560,
                    840
                ],
                [
                    2985,
                    841
                ]
            ]
        },
        "layout_type": "ListLayout"
    }
}