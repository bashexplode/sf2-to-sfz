#!/usr/bin/env python3
# Author: bash explode
import argparse
import os
import re
import wave
import sys
import logging
import math

from sf2utils.sf2parse import Sf2File
from sf2utils.generator import Sf2Gen

# Set logging level (only errors will be shown)
logging.getLogger().setLevel(logging.ERROR)

### RIPPED FROM SF2UTILS AND REPURPOSED ###
gen_map = {
    "OPER_START_ADDR_OFFSET": 0,
    "OPER_END_ADDR_OFFSET": 1,
    "OPER_START_LOOP_ADDR_OFFSET": 2,
    "OPER_END_LOOP_ADDR_OFFSET": 3,
    "OPER_START_ADDR_COARSE_OFFSET": 4,
    "OPER_MOD_LFO_TO_PITCH": 5,
    "OPER_VIB_LFO_TO_PITCH": 6,
    "OPER_MOD_ENV_TO_PITCH": 7,
    "OPER_INITIAL_FILTER_CUTOFF": 8,
    "OPER_INITIAL_FILTER_Q": 9,
    "OPER_MOD_LFO_TO_FILTER_CUTOFF": 10,
    "OPER_MOD_ENV_TO_FILTER_CUTOFF": 11,
    "OPER_END_ADDR_COARSE_OFFSET": 12,
    "OPER_MOD_LFO_TO_VOLUME": 13,
    "OPER_CHORUS_EFFECTS_SEND": 15,
    "OPER_REVERB_EFFECTS_SEND": 16,
    "OPER_PAN": 17,
    "OPER_DELAY_MOD_LFO": 21,
    "OPER_FREQ_MOD_LFO": 22,
    "OPER_DELAY_VIB_LFO": 23,
    "OPER_FREQ_VIB_LFO": 24,
    "OPER_DELAY_MOD_ENV": 25,
    "OPER_ATTACK_MOD_ENV": 26,
    "OPER_HOLD_MOD_ENV": 27,
    "OPER_DECAY_MOD_ENV": 28,
    "OPER_SUSTAIN_MOD_ENV": 29,
    "OPER_RELEASE_MOD_ENV": 30,
    "OPER_DELAY_VOL_ENV": 33,
    "OPER_ATTACK_VOL_ENV": 34,
    "OPER_HOLD_VOL_ENV": 35,
    "OPER_DECAY_VOL_ENV": 36,
    "OPER_SUSTAIN_VOL_ENV": 37,
    "OPER_RELEASE_VOL_ENV": 38,
    "OPER_KEYNUM_TO_VOL_ENV_HOLD": 39,
    "OPER_KEYNUM_TO_VOL_ENV_DECAY": 40,
    "OPER_INSTRUMENT": 41,
    "OPER_KEY_RANGE": 43,
    "OPER_VEL_RANGE": 44,
    "OPER_START_LOOP_ADDR_COARSE_OFFSET": 45,
    "OPER_INITIAL_ATTENUATION": 48,
    "OPER_END_LOOP_ADDR_COARSE_OFFSET": 50,
    "OPER_COARSE_TUNE": 51,
    "OPER_FINE_TUNE": 52,
    "OPER_SAMPLE_ID": 53,
    "OPER_SAMPLE_MODES": 54,
    "OPER_SCALE_TUNING": 56,
    "OPER_EXCLUSIVE_CLASS": 57,
    "OPER_OVERRIDING_ROOT_KEY": 58,
}

def return_gen_value(gen, gen_header):
    # Create generator object from sf2utils
    generator = Sf2Gen(gen_header)
    
    if gen is None:
        gen = generator.oper
    
    operator_name = None
    for op in gen_map.keys():
        if gen == gen_map[op]:
            operator_name = op
            break

    

    #return {operator_name: Sf2Gen(gen_header).amount}
    if operator_name == "OPER_START_ADDR_OFFSET":
        return {operator_name: generator.short}
    elif operator_name == "OPER_END_ADDR_OFFSET":
        return {operator_name: generator.short}
    elif operator_name == "OPER_START_LOOP_ADDR_OFFSET":
        return {operator_name: generator.short}
    elif operator_name == "OPER_END_LOOP_ADDR_OFFSET":
        return {operator_name: generator.short}
    elif operator_name == "OPER_START_ADDR_COARSE_OFFSET":
        return {operator_name: generator.coarse_offset}
    elif operator_name == "OPER_MOD_LFO_TO_PITCH":
        return {operator_name: generator.cents}
    elif operator_name == "OPER_VIB_LFO_TO_PITCH":
        return {operator_name: generator.cents}
    elif operator_name == "OPER_MOD_ENV_TO_PITCH":
        return {operator_name: generator.cents}
    elif operator_name == "OPER_INITIAL_FILTER_CUTOFF":
        return {operator_name: generator.absolute_cents}
    elif operator_name == "OPER_INITIAL_FILTER_Q":
        return {operator_name: generator.attenuation * 10.}
    elif operator_name == "OPER_MOD_LFO_TO_FILTER_CUTOFF":
        return {operator_name: generator.cents}
    elif operator_name == "OPER_MOD_ENV_TO_FILTER_CUTOFF":
        return {operator_name: generator.cents}
    elif operator_name == "OPER_END_ADDR_COARSE_OFFSET":
        return {operator_name: generator.coarse_offset}
    elif operator_name == "OPER_MOD_LFO_TO_VOLUME":
        return {operator_name: generator.attenuation * 10.}
    elif operator_name == "OPER_CHORUS_EFFECTS_SEND":
        return {operator_name: generator.send_amount}
    elif operator_name == "OPER_REVERB_EFFECTS_SEND":
        return {operator_name: generator.send_amount}
    elif operator_name == "OPER_PAN":
        return {operator_name: generator.pan}
    elif operator_name == "OPER_DELAY_MOD_LFO":
        return {operator_name: generator.cents}
    elif operator_name == "OPER_FREQ_MOD_LFO":
        return {operator_name: generator.absolute_cents}
    elif operator_name == "OPER_DELAY_VIB_LFO":
        return {operator_name: generator.cents}
    elif operator_name == "OPER_FREQ_VIB_LFO":
        return {operator_name: generator.absolute_cents}
    elif operator_name == "OPER_DELAY_MOD_ENV":
        return {operator_name: generator.cents}
    elif operator_name == "OPER_ATTACK_MOD_ENV":
        return {operator_name: generator.cents}
    elif operator_name == "OPER_HOLD_MOD_ENV":
        return {operator_name: generator.cents}
    elif operator_name == "OPER_DECAY_MOD_ENV":
        return {operator_name: generator.cents}
    elif operator_name == "OPER_SUSTAIN_MOD_ENV":
        return {operator_name: generator.sustain_decrease}
    elif operator_name == "OPER_RELEASE_MOD_ENV":
        return {operator_name: generator.cents}
    elif operator_name == "OPER_DELAY_VOL_ENV":
        return {operator_name: generator.cents}
    elif operator_name == "OPER_ATTACK_VOL_ENV":
        return {operator_name: generator.cents}
    elif operator_name == "OPER_HOLD_VOL_ENV":
        return {operator_name: generator.cents}
    elif operator_name == "OPER_DECAY_VOL_ENV":
        return {operator_name: generator.cents}
    elif operator_name == "OPER_SUSTAIN_VOL_ENV":
        return {operator_name: generator.positive_attenuation * 10.}
    elif operator_name == "OPER_RELEASE_VOL_ENV":
        return {operator_name: generator.cents}
    elif operator_name == "OPER_KEYNUM_TO_VOL_ENV_HOLD":
        return {operator_name: generator.cents}
    elif operator_name == "OPER_KEYNUM_TO_VOL_ENV_DECAY":
        return {operator_name: generator.cents}
    elif operator_name == "OPER_SCALE_TUNING":
            return {operator_name: generator.amount}
    else:
        return None

### END OF RIPPED FROM SF2UTILS AND REPURPOSED ###

# Mapping from sf2utils generator operator names to SFZ tag names.
sf2oper_to_sfz_map = {
    "OPER_FREQ_MOD_LFO": "fillfo_depth",
    "OPER_DELAY_MOD_LFO": "fillfo_delay",
    "OPER_SUSTAIN_VOL_ENV": "fileg_sustain",   
    "OPER_RELEASE_VOL_ENV": "fileg_release",
    "OPER_HOLD_VOL_ENV": "fileg_hold",
    "OPER_DELAY_VOL_ENV": "fileg_delay",       
    "OPER_DECAY_VOL_ENV": "fileg_decay",       
    #"OPER_ATTACK_VOL_ENV": "fileg_attack",
    "OPER_START_ADDR_OFFSET": "off_by",
    "OPER_INITIAL_FILTER_Q": "resonance",
    "OPER_SCALE_TUNING": "pitch_keytrack",
    "OPER_FREQ_MOD_LFO": "amplfo_freq",
    "OPER_MOD_LFO_TO_PITCH": "pitchlfo_depth",
    #"delay_mod_lfo": "pitchlfo_delay", 
    "OPER_ATTACK_MOD_ENV": "pitcheg_attack",
    "OPER_HOLD_MOD_ENV": "pitcheg_hold",
    "OPER_DECAY_MOD_ENV": "pitcheg_decay",
    "OPER_SUSTAIN_MOD_ENV": "pitcheg_sustain",
    "OPER_RELEASE_MOD_ENV": "pitcheg_release",
    "OPER_MOD_ENV_TO_PITCH": "pitcheg_depth",
    "OPER_DELAY_MOD_ENV": "pitcheg_delay",
    "OPER_MOD_ENV_TO_FILTER_CUTOFF": "fil_veltrack",
    "OPER_FREQ_VIB_LFO": "pitchlfo_freq", 
    "OPER_MOD_LFO_TO_VOLUME": "amplfo_depth",

}

# Mapping from sf2utils premade bag attribute names to SFZ tag names.
sf2_to_sfz_map = {
    "volume_envelope_attack": "ampeg_attack",
    "volume_envelope_release": "ampeg_release",
    "volume_envelope_sustain": "ampeg_sustain",
    "volume_envelope_decay": "ampeg_decay",
    "volume_envelope_attenuation": "volume",
    "volume_envelope_hold": "ampeg_hold",
    #"volume_envelope_decay": "amp_veltrack", # I don't think amp_veltrack actually maps to anything
    "pan": "pan",
    "key_range": ("lokey", "hikey"),
    "velocity_range": ("lovel", "hivel"),
    "midi_key_pitch_influence": "transpose",
    "lp_cutoff": "cutoff",       
    "reverb_send": "effect1",
    "chorus_send": "effect2",
}
# Exceptions in SFZ that SF2 don't have and are addressed elsewhere:
# "key" which is typically used for drum samples is pulled from key_range if the low range and high range are equal
# "hichan" and "lowchan" do not exist in SF2
# "pitch_keycenter" has two options in SF2 either the base_note override from instrument bag or the original_pitch from sample
# "tune" equals both SF2 instrument bag tuning*100 and fine_tuning 
# "loop_mode" differs dependent on if sample_loop_on_noteoff exists in the SF2 instrument bag, and equals loop_sustain if it exists
#                                                                                            or loop_continuous it it does not exist
# "loop_crossfade" does not exist in SF2, I just added it so it doesn't clip in Serum 2, remove if you want
# "loop_start" equals the sample start_loop time 
# "loop_end" equals the sample end_loop time 

def format_operator_parameters(generators, mapping):
    lines = []
    
    for gen in generators.keys():
        #print(gen, generators[gen])
        op_value_dict = return_gen_value(gen, generators[gen])
        if op_value_dict is None:
            continue
        gen_op = list(op_value_dict)[0]
        gen_val = op_value_dict[gen_op]
        for oper, sfz_tag in mapping.items():
            if oper == gen_op:
                if gen_val is not None:
                    # Safety Exceptions
                    if sfz_tag == "fil_veltrack":
                        lines.append("fil_type=lpf_2p")

                    # originally mapped to fillfo_delay but the SF2 value also is amplfo_delay and pitchlfo_delay for SFZ  
                    if sfz_tag == "fillfo_delay":
                        lines.append(f"amplfo_delay={gen_val}")
                        lines.append(f"pitchlfo_delay={gen_val}")
                    
                    # originally mapped to amplfo_freq but the SF2 value also is fillfo_freq for SFZ
                    if sfz_tag == "amplfo_freq":
                        lines.append(f"fillfo_freq={gen_val}")

                    # originally mapped to pitcheg_attack but the SF2 value also is fileg_attack for SFZ
                    if sfz_tag == "pitcheg_attack":
                        lines.append(f"fileg_attack={gen_val}")

                    if sfz_tag == "fileg_sustain":
                        gen_val = 100. * math.pow(10, -gen_val / 20)
                    
                    lines.append(f"{sfz_tag}={gen_val}")
    return lines


def format_bag_parameters(bag, mapping):
    """
    Given a bag (global or instrument), iterates over the mapping dictionary.
    For each attribute in the mapping, if the bag has that attribute and its value is not None,
    a corresponding line (or lines) is created in the form:
    SFZ_TAG=VALUE

    For attributes mapping to a tuple (e.g., key_range), it outputs two lines.
    
    Returns the formatted string (with newline characters) to be written to the SFZ file.
    """
    
    lines = []
    for attr, sfz_tag in mapping.items():
        if hasattr(bag, attr):
            val = getattr(bag, attr)
            #print(attr, val)
            if val is not None:
                # If the mapping value is a tuple, assume the bag attribute is a 2-element tuple.
                if isinstance(sfz_tag, tuple):
                    if isinstance(val, (list, tuple)) and len(val) == 2:
                        # Exception for drum samples
                        if attr == "key_range":
                            if val[0] == val[1]:
                                lines.append("lochan=10 hichan=10")
                                lines.append(f"key={val[0]}")
                                continue
                        lines.append(f"{sfz_tag[0]}={val[0]} {sfz_tag[1]}={val[1]}")
                else:
                    if attr == "volume_envelope_sustain":
                        val = 100. * math.pow(10, -val / 20)
                    lines.append(f"{sfz_tag}={val}")
    for mod in bag.mods:
        print(mod)
    gen_params = format_operator_parameters(bag.gens, sf2oper_to_sfz_map)
    if gen_params is not None:
        lines.extend(gen_params)
    if lines:
        return "\n".join(lines) + "\n"
    return ""

def write_parameters(f, param_str):
    """
    Writes the given parameter string (if non-empty) to the open file f.
    """
    if param_str:
        f.write(param_str)

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
        f.write("// Converted from SF2 to SFZ by bash explode\n\n")
        f.write("<control>\n")
        f.write(f"default_path={os.path.basename(sample_folder)}\n\n")
        
        # If the preset has a global bag, extract envelope parameters.
        #print(preset.bags)
        if preset.bags:
            global_params = ""
            for global_bag in preset.bags:
                global_results = format_bag_parameters(global_bag, sf2_to_sfz_map)
                if global_results:
                    global_params = global_params + global_results
                
            if global_params:
                f.write("<global>\n")
                write_parameters(f, global_params)
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
                region_preset_instrument_params = format_bag_parameters(bag, sf2_to_sfz_map)
                write_parameters(f, region_preset_instrument_params)
                # Determine tuning from bag, if available.
                tune = None
                finetune = None
                transpose = None
                if (hasattr(bag, "tuning") and bag.tuning is not None):
                    tune = bag.tuning * 100 
                    # weird edge case with library, I don't think anyone wants to go that many semi-tones
                    if tune >= 100 or tune <= -100:
                        tune = 0
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
                    if transpose is not None:
                        f.write(f"pitch_keycenter={pk}\ntranspose={transpose}\n")
                    elif tune is not None:
                        f.write(f"pitch_keycenter={pk} tune={tune}\n")
                    else:
                        f.write(f"pitch_keycenter={pk}\n")
                
                # Add loop parameters if the sample is meant to loop.
                if hasattr(bag, "sample_loop") and bag.sample_loop:
                    if hasattr(bag, "sample_loop_on_noteoff") and bag.sample_loop_on_noteoff:
                        loop_mode = "loop_sustain"
                    else:
                        loop_mode = "loop_continuous"
                    f.write(f"loop_mode={loop_mode}\n")
                    f.write(f"loop_start={bag.cooked_loop_start}\n")
                    #f.write(f"loop_start={sample.start_loop}\n")
                    f.write(f"loop_end={bag.cooked_loop_end - 1}\n")
                    #f.write(f"loop_end={sample.end_loop}\n")
                    f.write("loop_crossfade=0.01\n")
                f.write("\n")
    print(f"SFZ file generated: {sfz_filename}")

def main():
    parser = argparse.ArgumentParser(description="Convert an SF2 file to separate SFZ files per preset.")
    parser.add_argument("input", help="Input SF2 file")
    parser.add_argument("output", help="Output SFZ base file (e.g., mySound.sfz). The base name (without extension) is used for naming the base folder, sample folders, and sample files.")
    
    # If no arguments (or not enough) are given, print help and exit.
    if len(sys.argv) < 3:
        parser.print_help()
        sys.exit(1)
    
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
