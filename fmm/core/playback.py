import time
import random
from fmm.core.generators import fractalize, generate_midi, spread_octaves, random_pattern
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

def route_midi(port, message, channel):
    message.channel = channel
    port.send(message)

def _play_loop(midi_port, callback, decay):
    repeats = 0
    RAMP_VEL_AT = 1

    while True:
        # status.params_changed = False
        msg_list = callback()

        pattern = Pattern(msg_list)

        if (repeats >= RAMP_VEL_AT):
            pattern.decay_velocity(repeats, decay)

        if not pattern.is_velocity_above_threshold(1):
            break
        
        fractal = fractalize(pattern, params.bpm, params.depth, params.branching_factor)
        fractal = spread_octaves(fractal, params.octave_spread)

        mid = generate_midi(fractal, params.depth, params.bpm)
        play_midi(midi_port, mid)

        repeats += 1

    midi_port.reset()

def play_loop(midi_port, callback):
    # Prevent multiplt threads from playing at once
    if (status.is_playing):
         return

    base_pattern = Pattern(callback())

    status.is_playing = True

    # Fractalize user input
    _play_loop(midi_port, callback, 0.4)

    # Automatically generate a fractal as an "answer" to user input
    _play_loop(midi_port, lambda: random_pattern(base_pattern.key, [1, 0.5], 4, params.bpm), 0.5)

    status.is_playing = False
