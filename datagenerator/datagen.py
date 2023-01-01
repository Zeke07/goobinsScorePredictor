
from midi2audio import FluidSynth
import mingus.extra.lilypond as lp
from mingus.midi import midi_file_out
from mingus.core import *
from mingus.containers import *
import random
import os
import torch
import torchaudio as ta
import matplotlib.pyplot as plt
import sounddevice as sd
import soundfile as sf

# For installation, do pip install -r requirements.txt for python libraries
# Before you run this, make folders named: midi_data, sheet_music, soundfonts, wav_data
# You to need to install a fluidsynth and lilypond via brew (macOS) and if you're on linux, figure it out.

# In the soundfonts folder, install this file: YDP-GrandPiano-20160804.sf2 from https://musescore.org/en/handbook/3/soundfonts-and-sfz-files
# Scroll to SF2 Pianos and choose 'Acoustic grand piano, release 2016-08-04'

# For the midi_data, should be in the repo.

TESTING = False
"""
This is a test suite, meant to test the functionality of the libraries.
"""
def test():
    bar = Bar('C', (4, 4))
    for beat in range(4):
        # duration subdivides the bar already
        print(bar.place_notes(['C','E'], duration=4))

    # generate sheet music as png
    lp.to_png(lp.from_Bar(bar), './sheet_music/data_1.png')

    # generate midi, loop the Bar 4 times
    midi_file_out.write_Bar("./midi_data/data_1.mid", bar=bar, bpm=40, repeat=4)

    # let's test an F# minor scale in 4/4
    bar_2 = Bar('F#', (4,4))

    # NOTE: lower case -> minor, upper case -> major
    f_sharp_scale = scales.get_notes('f#')
    f_sharp_scale.append("F#")

    for beat in range(2):
        for note in f_sharp_scale:
            bar_2.place_notes(note, 16)

    midi_file_out.write_Bar("./midi_data/data_2.mid", bar=bar_2, bpm=120, repeat=4)

    # I stored a .sf2 in my proj directory
    sf = './soundfonts/YDP-GrandPiano-20160804.sf2'


    # FluidSynth instance for generating .wav from
    # the mingus MIDI file
    fs = FluidSynth(sf)
    fs.midi_to_audio('./midi_data/data_2.mid', './wav_data/data_2.wav')

    # let's test the .wav generator on a semi-dense Godowsky piece
    fs.midi_to_audio('./midi_data/godowsky.mid', './wav_data/godowsky.wav')



# load computer-generated midi, lilypond, pdf, and .wav forms into their respective directories
def generate_data(DATA_POINTS=5, key_signature='C', time_signature=(4,4), registers=[4,5]):


    abs_path = os.path.dirname(os.path.abspath(__file__))
    # NOTES: We need to generate various attributes of the naive dataset randomly
    # We have the following constraints:
    # Key is always in Cmaj, 2 Bars only, we need to randomly generate the size of the chord
    # at each time step as well as note/duration value
    # Lower->Upper: D3-B6 maximally
    # No accidentals
    # when the randomizer picks the first note, it should have some probability of picking
    # a second note to play with a max interval of an 8th (octave, so +-1 for the register)

    # to keep things consistent, the duration will be picked for as single beat in a bar
    # so we don't have to do excess computations to add up to a bar


    note_durations = {1: 1, 2: 1, 4: 1, 8: 2, 16: 4}  # will decide to place x number of notes depending on the duration
    notes = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
    file_serial_number = 0

    for _ in range(DATA_POINTS):
        bars = []
        for measures in range(2):
            # new measure
            bar = Bar(key_signature, time_signature)

            # fill up each beat of the bar with up to two-note chords
            while not bar.is_full():

                # if the note value chosen on this iteration is too large
                # place_notes will return false and we will just keep iterating until
                # the bar fills up completely
                chosen_duration = random.choice(list(note_durations.keys()))

                # choose 1-2 notes for a chord at some interval, with a given probability

                register = random.choice(registers)

                for beat_length in range(note_durations[chosen_duration]):
                    chord = [Note(random.choice(notes), register) for n in range(random.choices([1, 2])[0])]
                    bar.place_notes(chord, chosen_duration)

            bars.append(bar)

        curr_track = Track()
        for bar in bars:
            curr_track.add_bar(bar)

        # this is just for myself to see what is associated with each data point
        lp_string = lp.from_Track(curr_track)
        lp.to_pdf(lp_string, f'{abs_path}/sheet_music/{file_serial_number}.pdf')

        # write the LilyPond representation to a file

        with open(f'{abs_path}/text_data/{file_serial_number}.txt', "w") as text_file:
            text_file.write(lp_string)

        # do some exception-checking later in case the intermediary (midi) file
        # needed to produce the .wav does not exist!
        midi_file_out.write_Track(f'{abs_path}/midi_data/{file_serial_number}.mid', curr_track, bpm=80)

        sf = './soundfonts/YDP-GrandPiano-20160804.sf2'

        # FluidSynth instance for generating .wav from
        # the mingus MIDI file
        fs = FluidSynth(sf)

        fs.midi_to_audio(f'{abs_path}/midi_data/{file_serial_number}.mid', f'{abs_path}/wav_data/{file_serial_number}.wav')

        file_serial_number += 1



def main():

    abs_path = os.path.dirname(os.path.abspath(__file__))

    # generate dataset
    if (TESTING):
        generate_data()


    waveform_dataset = []
    wav_files = os.listdir(f'{abs_path}/wav_data')

    # load() will return (tensor, sampling_rate)
    # which we can possibly choose to ignore as
    # everything is 44.1 KHz
    for file in wav_files:
        waveform_dataset.append(ta.load(f'{abs_path}/wav_data/{file}')[0])

    text_dataset = []
    text_files = os.listdir(f'{abs_path}/text_data')

    for file in text_files:
        with open(f'{abs_path}/text_data/{file}') as content:
            for line in content:
                text_dataset.append(line)

    m = -1
    for input in text_dataset:
        m = max(len(input), m)











#HELPERS: plotting wav, audio playback for testing, etc

# fun little method from pytorch's audio io page
def plot_waveform(waveform, sample_rate):

    waveform = waveform.numpy()

    num_channels, num_frames = waveform.shape
    time_axis = torch.arange(0, num_frames) / sample_rate

    figure, axes = plt.subplots(num_channels, 1)
    if num_channels == 1:
        axes = [axes]
    for c in range(num_channels):
        axes[c].plot(time_axis, waveform[c], linewidth=1)
        axes[c].grid(True)
        if num_channels > 1:
            axes[c].set_ylabel(f"Channel {c+1}")
    figure.suptitle("waveform")
    plt.show(block=False)

def play_sound(file_path):
    # Extract data and sampling rate from file
    data, fs = sf.read(file_path, dtype='float32')
    sd.play(data, fs)
    status = sd.wait()  # Wait until file is done playing



if __name__ == "__main__":
    main()


