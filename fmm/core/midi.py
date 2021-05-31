import time
import random
from fmm.core.generators import fractalize, generate_midi, spread_octaves
from fmm.core.pattern import Pattern
import fmm.core.theory as theory
import fmm.core.status as status
import fmm.core.params as params

def play_midi(port, midi_file):
    for message in midi_file.play():
        #if not status.is_playing:
        #    break
        if not message.is_meta:
            port.send(message)
            print(message)

def infinite_play(midi_port, callback):
    repeats = 0
    RAMP_VEL_AT = 1

    while True:
        # status.params_changed = False
        msg_list = callback()

        pattern = Pattern(msg_list)

        if (repeats >= RAMP_VEL_AT):
            pattern.decay_velocity(repeats, 0.4)

        if not pattern.is_velocity_above_threshold(1):
            break
        
        fractal = fractalize(pattern, params.bpm, params.depth, params.branching_factor)
        fractal = spread_octaves(fractal, params.octave_spread)

        mid = generate_midi(fractal, params.depth, params.bpm)
        play_midi(midi_port, mid)

        repeats += 1

    midi_port.reset()
