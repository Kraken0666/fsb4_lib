# [FSB4i]
## FSB4inspector

A Python utility for working with FSB4 audio files. Currently supports reading and parsing the FSB4 header (48 bytes) and can be used via CLI. The script is also callable as a class method, making it usable as a library for further development.  
**Dependencies:** Only Python standard libraries (`struct`, `uuid`).

---

## Features (Current)

- Extract FSB4 headers (48 bytes) from FSB4 audio files. ✅
- Command-line interface (CLI) for usage. ✅
- Callable as a class method for library-style usage. ✅
- Uses only Python standard libraries (`struct`, `uuid`). ✅

---

## Roadmap

- [x] Extract and parse the 48-byte FSB4 header.  
- [x] Command-line interface for reading FSB4 files.  
- [x] Callable as a class method for programmatic access.  
- [ ] Enable modification of FSB4 headers.  
- [ ] Add, remove, or replace audio data within FSB4 files.  
- [ ] Extract additional metadata from embedded FSB4 chunks.  
- [ ] Support batch processing of multiple FSB4 files.  
- [ ] Enhance CLI with flags for editing, previewing, and exporting FSB4 data.  
- [ ] Provide detailed output about file structure and contents.  
- [ ] Add usage examples and tutorials for both CLI and library mode.  
- [ ] Write documentation for developers and end users.

---

## Installation

```bash
git clone <your-repo-url>
cd FSB4inspector```
# No external dependencies required
