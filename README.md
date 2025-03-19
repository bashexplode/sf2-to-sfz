# SF2 to SFZ Converter

This Python tool converts SoundFont 2 (SF2) files into SFZ format. It extracts sample and instrument data from an SF2 file, then creates a separate SFZ file for each preset along with dedicated sample folders. The exported regions include detailed information such as pitch key center (with tuning), key and velocity ranges, and loop settings.

I made this because I kept finding SF2 files that I wanted to use in Serum 2. You can copy the folder it outputs directly into your `Documents\Xfer\Serum 2 Presets\Multisamples\User` folder, and it should work.

This is a work in progress and there's still a few features to grab from the SF2 files, but it should give you the baseline of what's needed for the Multisample Oscillator in Serum 2. IT CURRENTLY ONLY PULLS THE PRESETS FROM THE SF2 FILE. Future state would be to pull all instruments on top of the presets, and then have this as an application for easier conversion, but for now people that are slightly more technical can use this!

If you want a feature, add it and make a pull request.

## Features

- **Preset-Specific Output:**  
  For each preset, the tool creates:
  - A dedicated sample folder named:  
    `<OUTPUT_BASE> <PresetName> Samples`
  - A separate SFZ file named:  
    `<OUTPUT_BASE> <PresetName>.sfz`
- **Sample Naming:**  
  Samples are exported with filenames using the true (sanitized) sample names from the SF2 file. Duplicate names are automatically disambiguated.
- **Region Tags:**  
  Each SFZ region includes:
  - `sample`: The exported sample file name.
  - `pitch_keycenter`: Derived from the instrument’s root key if available (bag.base_note); otherwise, the sample's original pitch.
  - `tune`: Computed from coarse and fine tuning values (coarse × 100 + fine) if available.
  - `lokey` and `hikey`: The key range of the region.
  - `lovel` and `hivel`: The velocity range of the region.
  - Loop parameters (if the sample is meant to loop):  
    `loop_mode`, `loop_start`, `loop_end`, and `loop_crossfade`.
- **Control Section:**  
  Each SFZ file begins with a `<control>` block setting `default_path` to the preset’s sample folder (as a relative path).

## Requirements

- Python 3.x
- [sf2utils](https://github.com/AuburnSounds/sf2utils)

Install `sf2utils` using pip:

```bash
pip install sf2utils
```

## Usage

Place the `sf2_to_sfz.py` script in your working directory and run:

```bash
python sf2_to_sfz.py input.sf2 output.sfz
```

Where:
- `input.sf2` is the path to your SF2 file.
- `output.sfz` is the base output file name. The script uses the basename (without extension) for naming the base folder, sample folders, and SFZ files.

For example, if you run:

```bash
python sf2_to_sfz.py mySound.sf2 mySound.sfz
```

The tool will create a base folder named `mySound` containing:
- Sample folders like `mySound Instrument1 Samples`, `mySound Instrument2 Samples`, etc.
- SFZ files like `mySound Instrument1.sfz`, `mySound Instrument2.sfz`, etc.

## Output Structure

After running the tool, your output directory structure will look similar to:

```
mySound/                   # Base folder (derived from output base name)
├── mySound Instrument1 Samples/   # Sample folder for preset "Instrument1"
│    ├── mySound-Instrument1-TrueSampleName.wav
│    └── ...
├── mySound Instrument1.sfz  # SFZ file for preset "Instrument1"
├── mySound Instrument2 Samples/   # Sample folder for preset "Instrument2"
│    └── ...
└── mySound Instrument2.sfz  # SFZ file for preset "Instrument2"
```

Each SFZ file contains region definitions with tags like:

```sfz
<control>
default_path=SC-22 Instrument1 Samples

<region>
sample=SC-22-Instrument1-TrueSampleName.wav
pitch_keycenter=60 tune=350
lokey=21
hikey=108
lovel=0
hivel=127
loop_mode=loop_continuous
loop_start=1000
loop_end=5000
loop_crossfade=0
```

## Customization

- **Mapping Generators:**  
  You can modify how SF2 generator values (e.g., tuning, envelopes) map to SFZ opcodes by editing the corresponding sections in the script.
- **Loop Settings:**  
  The loop parameters (mode, start, end, crossfade) are automatically added if the sample is flagged for looping. Adjust the values as needed.
- **Additional Parameters:**  
  Extend the region block to include more parameters if desired.

## License

This tool is provided "as-is" without any warranty. Feel free to modify and distribute it as needed.

## Acknowledgments

- [sf2utils](https://github.com/AuburnSounds/sf2utils) for providing the SF2 parsing functionality.
- SoundFont 2 and SFZ format documentation for details on the file formats.

---
