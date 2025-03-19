#!/usr/bin/env python3
# Author: bash explode
import argparse
import os
import re
import wave
import sys
import audioop
import logging

from sf2utils.sf2parse import Sf2File

# Set logging level (only errors will be shown)
logging.getLogger().setLevel(logging.ERROR)

def sanitize_filename(name):
    """
    Sanitize a string for use in a filename.
    Replaces spaces and non-alphanumeric characters with underscores.
    """
    return re.sub(r'[^A-Za-z0-9_\-]', '_', name)

def export_sample(sample, output_path):
    """
    Exports a given Sf2Sample to a WAV file at output_path.
    Uses sample.start, sample.end, and sample.sample_width to compute the expected data length.
    """
    duration = sample.end - sample.start
    expected_bytes = duration * sample.sample_width
    raw_data = sample.raw_sample_data

    if len(raw_data) != expected_bytes:
        print(f"Warning: Sample '{sample.name}' expected {expected_bytes} bytes, got {len(raw_data)} bytes", file=sys.stderr)

    with wave.open(output_path, 'wb') as wav_file:
        # Assume mono audio (adjust if stereo is needed)
        wav_file.setnchannels(1)
        wav_file.setsampwidth(sample.sample_width)
        wav_file.setframerate(sample.sample_rate)
        wav_file.writeframes(raw_data)

def generate_sfz_for_preset(preset, sf2, output_base, base_folder):
    """
    For a given preset, this function creates:
      - A sample folder: "<base_folder>/<output_base> <PresetName> Samples"
      - An SFZ file: "<base_folder>/<output_base> <PresetName>.sfz"
    
    It exports all samples used by the preset using their true (sanitized) names (ensuring uniqueness)
    and writes the SFZ regions including key, velocity ranges, and pitch information.
    
    For pitch_keycenter, it uses the instrument’s root key (bag.base_note) if available, otherwise
    the sample's original_pitch. If the bag contains both coarse tuning (OPER_COARSE_TUNE) and
    fine tuning (OPER_FINE_TUNE), these are combined (coarse * 100 + fine) and appended as the SFZ "tune" parameter.
    
    Additionally, if the sample is meant to loop (bag.sample_loop is True), the following parameters
    are added:
      loop_mode, loop_start, loop_end, and loop_crossfade.
    
    The SFZ file begins with a control tag setting default_path to the preset’s sample folder.
    """
    # Skip the sentinel preset.
    if preset.name == "EOP":
        return

    # Prepare preset name variants.
    preset_name_clean = preset.name.strip()
    preset_name_nospace = preset_name_clean.replace(" ", "")

    # Create the samples folder for this preset inside the base folder.
    sample_folder = os.path.join(base_folder, f"{output_base} {preset_name_clean} Samples")
    if not os.path.exists(sample_folder):
        os.makedirs(sample_folder)
    # Define the SFZ filename for this preset.
    sfz_filename = os.path.join(base_folder, f"{output_base} {preset_name_clean}.sfz")

    with open(sfz_filename, 'w') as f:
        # Write header comments and control tag with default sample folder.
        f.write("// " + preset_name_clean + "\n")
        f.write("// Converted from SF2 to SFZ\n")
        f.write("// By bash explode\n\n")
        f.write("<control>\n")
        f.write(f"default_path={os.path.basename(sample_folder)}\n\n")
        
        # If the preset has a global bag, extract envelope parameters.
        if preset.bags and preset.bags[0].instrument is None:
            global_bag = preset.bags[0]
            globaltag = "<global>\n"
            globaltagset = False
            #print("global bag found")
            if hasattr(global_bag, "volume_envelope_attack") and global_bag.volume_envelope_attack is not None:
                if not globaltagset:
                    f.write(globaltag)
                    globaltagset = True
                f.write(f"ampeg_attack={global_bag.volume_envelope_attack}\n")
            if hasattr(global_bag, "volume_envelope_release") and global_bag.volume_envelope_release is not None:
                if not globaltagset:
                        f.write(globaltag)
                        globaltagset = True
                f.write(f"ampeg_release={global_bag.volume_envelope_release}\n")
            if hasattr(global_bag, "volume_envelope_decay") and global_bag.volume_envelope_decay is not None:
                if not globaltagset:
                        f.write(globaltag)
                        globaltagset = True
                f.write(f"amp_veltrack={global_bag.volume_envelope_decay}\n")
        f.write("\n")
        
        # Dictionary for deduplicating sample filenames (keyed by sample id)
        preset_sample_files = {}
        # Track used base names for uniqueness.
        used_names = {}
        
        # Iterate over instruments referenced by the preset.
        for instrument in preset.instruments:
            if not hasattr(instrument, "bags"):
                continue
            for bag in instrument.bags:
                sample = bag.sample
                if sample is None or sample.name == "EOS":
                    continue

                key = id(sample)
                if key not in preset_sample_files:
                    # Use the true sample name, sanitized.
                    base_name = sanitize_filename(sample.name.strip())
                    if base_name in used_names:
                        used_names[base_name] += 1
                        base_name = f"{base_name}-{used_names[base_name]}"
                    else:
                        used_names[base_name] = 1
                    sample_filename = f"{output_base}-{preset_name_nospace}-{base_name}.wav"
                    sample_path = os.path.join(sample_folder, sample_filename)
                    try:
                        export_sample(sample, sample_path)
                    except Exception as e:
                        print(f"Failed to export sample for preset {preset.name} ({sample.name}): {e}", file=sys.stderr)
                        sample_filename = "UNKNOWN"
                    preset_sample_files[key] = sample_filename
                else:
                    sample_filename = preset_sample_files[key]
                # Write a region block referencing this sample.
                f.write("<region>\n")
                f.write(f"sample={sample_filename}\n")
                # Determine tuning from bag, if available.
                tune = None
                finetune = None
                if (hasattr(bag, "tuning") and bag.tuning is not None):
                    tune = bag.tuning * 100 
                else:
                    tune = 0
                if (hasattr(bag, "fine_tuning") and bag.fine_tuning is not None):
                    finetune = bag.fine_tuning
                else:
                    finetune = 0
                tune = tune + finetune
                if tune == 0:
                    tune = None
                # Determine pitch_keycenter: use bag.base_note if available; else sample.original_pitch.
                pk = None
                if hasattr(bag, "base_note") and bag.base_note is not None:
                    pk = bag.base_note
                elif hasattr(sample, "original_pitch"):
                    pk = sample.original_pitch
                    
                # Write the pitch_keycenter (and tune if available) on one line.
                if pk is not None:
                    if tune is not None:
                        f.write(f"pitch_keycenter={pk} tune={tune}\n")
                    else:
                        f.write(f"pitch_keycenter={pk}\n")
                
                if bag.key_range is not None:
                    low, high = bag.key_range
                    f.write(f"lokey={low}\n")
                    f.write(f"hikey={high}\n")
                if bag.velocity_range is not None:
                    low, high = bag.velocity_range
                    f.write(f"lovel={low}\n")
                    f.write(f"hivel={high}\n")
                # Add loop parameters if the sample is meant to loop.
                if hasattr(bag, "sample_loop") and bag.sample_loop:
                    if hasattr(bag, "sample_loop_on_noteoff") and bag.sample_loop_on_noteoff:
                        loop_mode = "loop_sustain"
                    else:
                        loop_mode = "loop_continuous"
                    f.write(f"loop_mode={loop_mode}\n")
                    f.write(f"loop_start={sample.start_loop}\n")
                    f.write(f"loop_end={sample.end_loop}\n")
                    f.write("loop_crossfade=0.01\n")
                f.write("\n")
    print(f"SFZ file generated: {sfz_filename}")

def main():
    parser = argparse.ArgumentParser(description="Convert an SF2 file to separate SFZ files per preset.")
    parser.add_argument("input", help="Input SF2 file")
    parser.add_argument("output", help="Output SFZ base file (e.g., mySound.sfz). The base name (without extension) is used for naming the base folder, sample folders, and sample files.")
    args = parser.parse_args()

    # Derive the output base name (without extension).
    output_base = os.path.splitext(os.path.basename(args.output))[0]
    # Create a base folder using the output base name.
    base_folder = output_base
    if not os.path.exists(base_folder):
        os.makedirs(base_folder)

    # Open the SF2 file explicitly and keep it open during processing.
    f = open(args.input, "rb")
    try:
        sf2 = Sf2File(f)
        for preset in sf2.presets:
            generate_sfz_for_preset(preset, sf2, output_base, base_folder)
    finally:
        f.close()

if __name__ == "__main__":
    main()
