#!/bin/zsh
cd ../
source .venv/bin/python
python src/osc_relay.py --listen-host "0.0.0.0" --x32 "192.168.240.250:10032" --magicq "192.168.240.100:8000"