UNIVERSAL_REAL_TIME = 0x7F
MSC_SUB_ID = 0x02
COMMAND_FORMAT_LIGHTING = 0x01
COMMAND_GO = 0x01
DELIMITER = 0x00

# Device id 127 addresses every MSC device on the MIDI line.
ALL_CALL_DEVICE_ID = 127


class MidiShowControl:
    """Builds MIDI Show Control (MSC) lighting commands for the ChamSys MagicQ.

    The messages are returned in the text format of the mido library, which is
    what the MidiCue of the Linux Show Player stores and sends. MagicQ maps the
    MSC cue list to the playback, so `GO cue 5 in list 1` jumps playback 1 to cue 5.
    """

    def __init__(self, device_id: int, cue_list: int):
        if not 0 <= device_id <= ALL_CALL_DEVICE_ID:
            raise ValueError(f"The MSC device id {device_id} is outside of 0-{ALL_CALL_DEVICE_ID}.")
        self.device_id = device_id
        self.cue_list = cue_list

    def go(self, cue_number: int) -> str:
        data = [UNIVERSAL_REAL_TIME, self.device_id, MSC_SUB_ID, COMMAND_FORMAT_LIGHTING, COMMAND_GO]
        data += self._ascii(cue_number)
        data.append(DELIMITER)
        data += self._ascii(self.cue_list)
        # mido leaves out the SysEx start (F0) and end (F7) bytes.
        return f"sysex data=({','.join(str(byte) for byte in data)})"

    @staticmethod
    def _ascii(number: int) -> list[int]:
        return list(str(number).encode("ascii"))
