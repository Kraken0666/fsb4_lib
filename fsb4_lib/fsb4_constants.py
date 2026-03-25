import struct

# File header format and size
FSB4_HEADER_FORMAT = "<4s5IQ16s"
FSB4_HEADER_SIZE = struct.calcsize(FSB4_HEADER_FORMAT)

# Directory and syncpoint offsets
FSB4_DIR_OFFSET = 0x30
FSB4_SYNC_OFFSET = 0x80

# Directory entry format
FSB4_ENTRY_FORMAT = "<30sIIIIIIHHHHIIIHH"
FSB4_ENTRY_SIZE = struct.calcsize(FSB4_ENTRY_FORMAT)
