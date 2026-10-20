# OSC Relay

`src/osc_relay.py` runs during the show and forwards the OSC messages of the [Linux Show Player](lisp.md) to the
Behringer X32 and the ChamSys MagicQ.

LiSP 0.6.5 sends all OSC messages to a single host. The [Cue Generator](cue-generator.md) therefore prefixes the
address of every OSC cue with the deck it is meant for. The relay removes this first address segment and forwards the
otherwise unchanged packet to the deck:

| Received from LiSP | Forwarded to | Forwarded as |
| - | - | - |
| `/x32/load ,siii "snippet" 4 0 0` | X32 (`--x32`) | `/load ,siii "snippet" 4 0 0` |
| `/mq/pb/1/5` | MagicQ (`--magicq`) | `/pb/1/5` |

```
LiSP ──UDP──► osc_relay.py ──/x32/...──► Behringer X32 (port 10023)
                           └──/mq/...───► ChamSys MagicQ
```

## Requirements

- Python 3.10 or newer, no additional packages
- The machine running the relay must reach both decks over the network.

## Usage

```shell
python3 src/osc_relay.py --x32 192.168.1.10:10023 --magicq 192.168.1.20:8000
```

The relay prints where it listens and where it routes to, followed by one line per forwarded message. Stop it with
`Ctrl+C`.

## Command line arguments

| Argument | Required | Default | Description |
| - | - | - | - |
| `--x32 <host>:<port>` | yes | | Address of the Behringer X32. The X32 always listens for OSC on port `10023`. |
| `--magicq <host>:<port>` | yes | | Address of the ChamSys MagicQ. The port is the OSC receive port configured on the MagicQ in Setup, View Settings, Network. |
| `--listen-host <address>` | no | `127.0.0.1` | The address the relay listens on. The default only accepts messages from LiSP on the same machine. Use `0.0.0.0` if LiSP runs on another machine. |
| `--listen-port <port>` | no | `9001` | The UDP port the relay listens on. The default is LiSP's default OSC destination. |
| `-h`, `--help` | no | | Prints the help and exits. |

`--x32` and `--magicq` must be of the form `<host>:<port>`, the host can be an IP address or a host name.

## Setup

1. Enable OSC on the MagicQ and note its receive port (Setup, View Settings, Network).
2. In LiSP, set the OSC destination to the host and port the relay listens on (default `localhost:9001`).
3. Start the relay before the show and keep it running.

## Behaviour

- Messages are forwarded byte for byte except for the address, so all argument types are supported.
- A packet is dropped with a message on stderr if
  - it is an OSC bundle (not supported),
  - it is no valid OSC message,
  - its first address segment is neither `x32` nor `mq`, or
  - its address consists of the route only (e.g. `/x32`).
- The relay does not wait for or forward replies of the decks.

There is no feedback whether a deck actually received a message, since OSC over UDP is not acknowledged. Watch the
decks when testing the setup. `test/test-x32-osc.py` checks whether the X32 answers to `/info`. Its IP address is
hard-coded, so adjust it first.
