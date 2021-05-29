import random
from mido import Message, MetaMessage, MidiFile, MidiTrack, second2tick, bpm2tempo
from fmm.core.utils.converters import beats2ticks
from fmm.core.note import Note
from fmm.core.pattern import Pattern

def fractalize(pattern, bpm, depth, bf=2):
    fractal = []

    for level in range(depth):
        n = pow(bf, level)

        for j in range(n):
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

def random_pattern(note_numbers, figures, beats_per_measure):
        pattern = []
        total_duration = 0

        while total_duration != beats_per_measure:
            total_duration = 0
            pattern = []

            while total_duration < beats_per_measure:
                note = random.choice(note_numbers)
                duration = random.choice(figures)

                note = Note(note, duration)
                pattern.append(note)

                total_duration = total_duration + duration

        return Pattern(pattern)

def spread_octaves(fractal, octave_offsets):
    for pattern in fractal:
        pattern.shift_octave(octave_offsets[pattern.order])

    return fractal
