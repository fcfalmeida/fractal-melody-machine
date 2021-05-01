import random
from mido import Message, MetaMessage, MidiFile, MidiTrack, second2tick, bpm2tempo
from fmm.utils.converters import beats2ticks
from fmm.note import Note
from fmm.pattern import Pattern

def fractalize(pattern, depth, bf=2):
    fractal = []

    for level in range(depth):
        n = pow(bf, level)

        for j in range(n):
            p = Pattern(pattern.notes)
            p.order = level
            fractal.append(p)

    return fractal

def generate_midi(fractal, branching_factor, depth, bpm):
    mid = MidiFile(type=1)
    tracks = [MidiTrack() for i in range(depth)]

    mid.tracks.extend(tracks)

    tempo = int(bpm2tempo(bpm))
    for track in tracks:
        track.append(MetaMessage('set_tempo', tempo=tempo))

    for p in fractal:
        for note in p.notes:
            duration = beats2ticks(note.duration, bpm, mid.ticks_per_beat) / (pow(branching_factor, p.order))

            note_on = Message('note_on', note=note.number, velocity=80, time=0, channel=p.order)
            note_off = Message('note_off', note=note.number, velocity=127, time=int(duration), channel=p.order)
            tracks[p.order].append(note_on)
            tracks[p.order].append(note_off)

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
