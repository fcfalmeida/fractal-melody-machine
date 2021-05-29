import time
import random
from fmm.core.generators import fractalize, generate_midi, random_pattern, spread_octaves
import fmm.core.theory as theory
import fmm.core.status as status
import fmm.core.params as params

def play_midi(port, midi_file):
    for message in midi_file.play():
        if not status.is_playing:
            break
        if not message.is_meta:
            port.send(message)
            print(message)

def _next_fractal(note_numbers, figures, depth, branching_factor, octave_spread):
    pattern = random_pattern(note_numbers, figures, 4)
    fractal = fractalize(pattern, depth, branching_factor)
    fractal = spread_octaves(fractal, octave_spread)

    return fractal

def infinite_play(midi_port, callback):
    while status.is_playing:
        # status.params_changed = False
        fractal = callback()
        mid = generate_midi(fractal, params.depth, params.bpm)
        play_midi(midi_port, mid)

    midi_port.reset()
