import time
import random
from fractal import fractalize
from generators import generate_midi, random_pattern, spread_octaves
from theory import notes_in_key

def play_midi(port, midi_file):
    for message in midi_file:
        time.sleep(message.time)
        if not message.is_meta:
            port.send(message)

def _next_fractal(note_numbers, figures, depth, branching_factor):
    pattern = random_pattern(note_numbers, figures, 4)
    fractal = fractalize(pattern, depth, branching_factor)
    fractal = spread_octaves(fractal, [-1, -1, 0, 1, 2])

    return fractal

def infinite_play(depth, branching_factor, figures, key, bpm, midi_port):
    change_prob = 0.3
    note_numbers = notes_in_key(key)

    fractal = _next_fractal(note_numbers, figures, depth, branching_factor)

    while True:
        # change pattern with a probability
        if random.random() < change_prob:
            fractal = _next_fractal(note_numbers, figures, depth, branching_factor)

        mid = generate_midi(fractal, branching_factor, depth, bpm, 4)
        play_midi(midi_port, mid)
