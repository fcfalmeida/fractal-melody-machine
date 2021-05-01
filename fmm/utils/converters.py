from mido import second2tick, bpm2tempo

def beats2seconds(beats, bpm):
    return beats / (bpm / 60)

def beats2ticks(beats, bpm, tpb):
    secs = beats2seconds(beats, bpm)

    return int(second2tick(secs, tpb, bpm2tempo(bpm)))