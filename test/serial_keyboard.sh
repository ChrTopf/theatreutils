#!/bin/zsh

if ! command -v oscsend >/dev/null 2>&1; then
    echo "oscsend not found (provided by the 'liblo' package)."
    read -rp "Install liblo now? [y/N] " answer
    case "$answer" in
        [yY]|[yY][eE][sS])
            sudo pacman -S --needed liblo || { echo "Installation failed." >&2; exit 1; }
            ;;
        *)
            echo "liblo is required. Aborting." >&2
            exit 1
            ;;
    esac
fi

cd ../
source .venv/bin/python
python src/serial_keyboard.py --port /dev/ttyACM1 --baud 9600 --command "oscsend localhost 9000 /lisp/go"
