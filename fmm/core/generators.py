import random
from mido import MetaMessage, MidiFile, MidiTrack, bpm2tempo
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

def spread_octaves(fractal, octave_offsets):
    for pattern in fractal:
        pattern.shift_octave(octave_offsets[pattern.order])

    return fractal
