from mido import second2tick, bpm2tempo

def beats2seconds(beats, bpm):
    return beats / (bpm / 60)

def beats2ticks(beats, bpm, tpb):
    secs = beats2seconds(beats, bpm)

    return int(second2tick(secs, tpb, bpm2tempo(bpm)))

def parse_midi_messages(msg_list):
    # Ignore first message if it's a note off
    # TODO: Ignore all note off messages at the head of the list 
    if msg_list[0].type == 'note_off':
        del msg_list[0]

    