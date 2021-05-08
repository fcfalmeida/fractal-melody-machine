import time
import random
from fmm.core.generators import fractalize, generate_midi, random_pattern, spread_octaves
import fmm.core.theory as theory
import fmm.core.status as status
import fmm.core.params as params

def play_midi(port, midi_file):
    for message in midi_file:
        if not status.is_playing:
            break
        time.sleep(message.time)
        if not message.is_meta:
            port.send(message)

def _next_fractal(note_numbers, figures, depth, branching_factor):
    pattern = random_pattern(note_numbers, figures, 4)
    fractal = fractalize(pattern, depth, branching_factor)
    fractal = spread_octaves(fractal, [-1, -1, 0, 1, 2])

    return fractal

def infinite_play(midi_port):
    note_numbers = theory.notes_in_key(params.key)

    fractal = _next_fractal(note_numbers, params.figures, params.depth, params.branching_factor)

    while status.is_playing:
        # change pattern with a probability
        if random.random() < params.change_prob:
            fractal = _next_fractal(note_numbers, params.figures, params.depth, params.branching_factor)

        mid = generate_midi(fractal, params.branching_factor, params.depth, params.bpm)
        play_midi(midi_port, mid)

    midi_port.reset()
