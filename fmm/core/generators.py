import random
from mido import Message, MetaMessage, MidiFile, MidiTrack, bpm2tempo
from fmm.core.pattern import Pattern
from fmm.core.theory import notes_in_key, closest_key
from fmm.core.utils.converters import beats2ticks

def fractalize(pattern, bpm, depth, bf=2):
    fractal = []

    for level in range(depth):
        n = pow(bf, level)

        for _ in range(n):
            p = Pattern(pattern.messages)
            p.order = level
            p.set_message_times(bf)
            fractal.append(p)

    return fractal

def generate_midi(fractal, depth, bpm):
    mid = MidiFile(type=1)
    tracks = [MidiTrack() for i in range(depth)]

    mid.tracks.extend(tracks)

    tempo = int(bpm2tempo(bpm))
    for track in tracks:
        track.append(MetaMessage('set_tempo', tempo=tempo))

    for pattern in fractal:
        tracks[pattern.order].extend(pattern.messages)

    return mid

def random_pattern(key, figures, beats_per_measure, bpm):
    total_duration = 0
    note_numbers = notes_in_key(key)

    while total_duration != beats_per_measure:
        total_duration = 0
        messages = []

        while total_duration < beats_per_measure:
            note = random.choice(note_numbers)
            duration = random.choice(figures)
            ticks = beats2ticks(duration, bpm, 480)

            note_on = Message('note_on', note=note, velocity=80, time=0)
            note_off = Message('note_off', note=note, velocity=0, time=ticks)

            messages.append(note_on)
            messages.append(note_off)

            total_duration = total_duration + duration

    return Pattern(messages)

def spread_octaves(fractal, octave_offsets):
    for pattern in fractal:
        pattern.shift_octave(octave_offsets[pattern.order])

    return fractal
