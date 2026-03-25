from .fsb4_flags import FSOUND_FLAGS


def decode_FSOUND_FLAGS(value: int):
    """Return list of FSOUND_FLAGS names set in value."""
    flags_set = FSOUND_FLAGS(value)
    return [flag.name for flag in FSOUND_FLAGS if flag in flags_set]


def format_time(samples: int, sample_rate: int, formatted: bool = True):
    """Convert samples to time. Returns formatted string or tuple."""
    time_sec = samples / sample_rate
    minutes = int(time_sec // 60)
    seconds = int(time_sec % 60)
    millis = int((time_sec - int(time_sec)) * 1000)
    if formatted:
        return f"{minutes}:{seconds:02d}.{millis:03d}"
    return minutes, seconds, millis, time_sec
