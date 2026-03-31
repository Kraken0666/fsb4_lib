import struct
from typing import List, Dict
from .fsb4_structs import FSB4Header, FSB4DirectoryEntry
from .fsb4_constants import (
    FSB4_HEADER_FORMAT,
    FSB4_HEADER_SIZE,
    FSB4_DIR_OFFSET,
    FSB4_SYNC_OFFSET,
    FSB4_ENTRY_FORMAT,
    FSB4_ENTRY_SIZE,
)
from .fsb4_helpers import format_time


class FSB4Metadata:
    def __init__(self, filename: str):
        self.filename: str = filename
        self.header: FSB4Header | None = None
        self.directory: List[FSB4DirectoryEntry] = []

    def get_header(self) -> FSB4Header:
        with open(self.filename, "rb") as f:
            data = f.read(FSB4_HEADER_SIZE)
            if len(data) != FSB4_HEADER_SIZE:
                raise EOFError("Not a valid FSB4 file")

            unpacked = struct.unpack(FSB4_HEADER_FORMAT, data)
            header = FSB4Header(
                magic=unpacked[0].decode("ascii"),
                num_files=unpacked[1],
                dir_len=unpacked[2],
                dat_len=unpacked[3],
                version=(unpacked[4] >> 16),
                flags=unpacked[5],
                reserved=unpacked[6],
                bank_uuid=unpacked[7],
            )
            if header.magic != "FSB4":
                raise ValueError(f"Invalid FSB4 magic: {header.magic}")

            self.header = header
            return header

    def get_samples(self) -> List[FSB4DirectoryEntry]:
        if self.header is None:
            raise ValueError("Header not loaded")

        self.directory.clear()
        with open(self.filename, "rb") as f:
            f.seek(FSB4_DIR_OFFSET)
            for i in range(self.header.num_files):
                entry_len_bytes = f.read(2)
                if len(entry_len_bytes) != 2:
                    raise EOFError(f"Unexpected EOF at entry {i}")
                entry_len = struct.unpack("<H", entry_len_bytes)[0]

                entry_bytes = f.read(entry_len - 2)
                if len(entry_bytes) != entry_len - 2:
                    raise EOFError(f"Incomplete entry {i}")

                unpacked = struct.unpack(
                    FSB4_ENTRY_FORMAT, entry_bytes[:FSB4_ENTRY_SIZE])
                filename = unpacked[0].split(
                    b"\x00", 1)[0].decode("utf-8", errors="ignore")

                entry = FSB4DirectoryEntry(
                    entry_len=entry_len,
                    filename=filename,
                    sample_len=unpacked[1],
                    compressed_len=unpacked[2],
                    loop_start=unpacked[3],
                    loop_end=unpacked[4],
                    play_mode=unpacked[5],
                    sample_rate=unpacked[6],
                    bank_volume=unpacked[7],
                    pan=unpacked[8],
                    playback_priority=unpacked[9],
                    num_channels=unpacked[10],
                    min_distance=unpacked[11],
                    max_distance=unpacked[12],
                    var_freq=unpacked[13],
                    var_vol=unpacked[14],
                    var_pan=unpacked[15],
                )
                self.directory.append(entry)

        return self.directory

    def get_syncpoints(self) -> List[Dict[str, object]]:
        if self.header is None:
            self.get_header()
        if not self.directory:
            self.get_samples()

        sample_rate = self.directory[0].sample_rate
        startpoints = []

        with open(self.filename, "rb") as f:
            f.seek(FSB4_SYNC_OFFSET)
            header_bytes = f.read(8)
            if len(header_bytes) != 8:
                raise EOFError("Could not read syncpoint header")

            magic, num_startpoint = struct.unpack("<4sI", header_bytes)
            if magic.decode("ascii") != "SYNC":
                raise ValueError(
                    f"Unexpected syncpoint magic: {magic.decode('ascii')}")

            for _ in range(num_startpoint):
                entry_bytes = f.read(260)
                if len(entry_bytes) != 260:
                    raise EOFError("Incomplete startpoint entry")

                start_samples, label_bytes, _ = struct.unpack(
                    "<I10s246s", entry_bytes)
                label = label_bytes.decode("ascii").rstrip("\x00")
                startpoints.append(
                    {
                        "label": label,
                        "sample_offset": start_samples,
                        "time_formatted": format_time(start_samples, sample_rate),
                    }
                )

        return startpoints
