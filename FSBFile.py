import uuid
from struct import unpack

class FSB4Data(object):
    def __init__(self, filename):
        self.filename = filename
        self.data = []
        self.header = None

    def extract_fsb4_header(self):
        with open(self.filename, 'rb') as f:
            fsb4_header_bytes = f.read(48)
            if len(fsb4_header_bytes) != 48:
                raise EOFError("Invalid FSB4 header")
            self.header = unpack('<4s5IQ16s', fsb4_header_bytes)

            # Split header data
            magic      = self.header[0].decode('ascii')
            num_files  = self.header[1]
            dir_len    = self.header[2]
            dat_len    = self.header[3]
            version    = self.header[4]
            flags      = self.header[5]
            null_bytes = self.header[6]
            bank_uuid  = self.header[7]

            # -DEBUG- print out
            print("Magic:", magic)
            print("Num Files:", num_files)
            print("Dir Length:", dir_len)
            print("Data Length:", dat_len)
            print("Version:", version)
            print("Flags:", flags)
            print("Null Bytes:", null_bytes)
            formatted_uuid = str(uuid.UUID(bytes=bank_uuid))
            print("UUID:", formatted_uuid)

            return self.header

    def extract_fsb4_syncpoints(self):
        return None

if __name__ == "__main__":
    from sys import argv

    if len(argv) < 2:
        print("Usage: FSBFile.py <input>")
        exit(1)

    fsb = FSB4Data(argv[1])
    fsb.extract_fsb4_header()
