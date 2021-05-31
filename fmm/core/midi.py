import time
import random
from fmm.core.generators import fractalize, generate_midi, spread_octaves
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

def infinite_play(midi_port, callback):
    while status.is_playing:
        # status.params_changed = False
        fractal = callback()
        fractal = spread_octaves(fractal, params.octave_spread)
        mid = generate_midi(fractal, params.depth, params.bpm)
        play_midi(midi_port, mid)

    midi_port.reset()
