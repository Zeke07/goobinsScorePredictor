from midi2audio import FluidSynth
from mingus.containers import Bar
import mingus.extra.lilypond as lp
from mingus.midi import midi_file_out
from mingus.core import scales

def main():

    bar = Bar('C', (4, 4))
    for beat in range(4):
        # duration subdivides the bar already
        bar.place_notes(['C','E','G'], duration=4)

    # generate sheet music as png
    lp.to_png(lp.from_Bar(bar), "./sheet_music/data_1.png")

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
    sf = 'soundfonts/YDP-GrandPiano-20160804.sf2'

    # FluidSynth instance for generating .wav from
    # the mingus MIDI file
    fs = FluidSynth(sf)
    fs.midi_to_audio('./midi_data/data_2.mid', './wav_data/data_2.wav')

    # let's test the .wav generator on a semi-dense Godowsky piece
    fs.midi_to_audio('./midi_data/godowsky_java_suite_07b_three_dances_2_(c)yogore.mid', './wav_data/godowsky.wav')

if __name__ == "__main__":
    main()