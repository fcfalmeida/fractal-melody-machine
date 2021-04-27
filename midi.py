from mido import Message, MidiFile, MidiTrack, second2tick, bpm2tempo
import converters

def generate_midi(fractal, branching_factor, depth, bpm, base_duration):
    mid = MidiFile(type=1)
    tracks = [MidiTrack() for i in range(depth)]

    mid.tracks.extend(tracks)

    base_duration_ticks = converters.beats2ticks(base_duration, bpm, mid.ticks_per_beat)

    for p in fractal:
        duration = base_duration_ticks / (pow(branching_factor, p.order))

        for note in p.notes:
            note_on = Message('note_on', note=note, velocity=80, time=0)
            note_off = Message('note_off', note=note, velocity=127, time=int(duration))
            tracks[p.order].append(note_on)
            tracks[p.order].append(note_off)

    return mid