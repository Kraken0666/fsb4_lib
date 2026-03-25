from fsb4_lib import FSB4Data, decode_FSOUND_FLAGS, format_time

# Load an FSB4 soundbank
bank = FSB4Data("tests/i_english_g.fsb")

# Extract header
header = bank.get_header()
print("FSB4 Header:")
print(f"Magic: {header.magic}")
print(f"Number of samples: {header.num_files}")
print(f"Version: {header.version}")
print(f"Flags: {decode_FSOUND_FLAGS(header.flags)}")
print(f"Bank UUID: {header.bank_uuid.hex()}")

# Extract samples / directory
samples = bank.get_samples()
print("\nSamples:")
for s in samples:
    print(
        f"{s.filename} | Sample rate: {s.sample_rate} Hz | Channels: {s.num_channels} | Length: {format_time(s.sample_len, s.sample_rate)}"
    )

# Extract syncpoints
syncpoints = bank.get_syncpoints()
print("\nSyncpoints:")
for sp in syncpoints:
    print(f"{sp['label']} @ {sp['time_formatted']} (Sample: {sp['sample_offset']})")
