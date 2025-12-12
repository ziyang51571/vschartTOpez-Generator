vschartTOpez Generator
=============

**English** | [简体中文](./README.zh-CN.md)

vivid/stasis -> pez Chart Conversion
Parses .vsb, .vsd files and packages them into Phigros fanmade format.

### Environment Requirements

- Python 3.8+
- Install dependencies:

```bash
pip install -r requirements.txt
```

- Prepare the following directory structure before starting:

```
vschartTOpez/
├─ vsb_parser.py
├─ vsb2pez.py
├─ vsd_parser.py
├─ Charts/              # Original .vsb charts (original directory structure)
├─ song_information.bin # Track .vsd data
├─ audiogroup_default/  # Audio sources: music_chart_*.ogg/wav
├─ Sprites/             # Cover art: song_*_0.png (optional)
└─ black.png            # Default cover background
```

### Usage Steps

1. Parse `song_information.bin`
   ```bash
   python vsd_parser.py
   ```
   Generates `song_information.json` in the same directory.


2. Batch parse .vsb files
   ```
   python vsb_parser.py
   ```
   Outputs to `vsbjson/` while preserving original directory structure.


3. Generate pez packages
   ```
   python vsb2pez.py
   ```
   Get `.pez` files in `pezOutput/`.

### Notes

- Charts will NOT be packaged if audio files are missing;
- Script will warn when cover art is missing, but still treats conversion as successful and uses `black.png` as cover."# vschartTOpez-Generator" 
