from itertools import groupby
from mido import Message

def add_missing_noteoffs(msg_list, delta_time):
    msg_list_copy = msg_list.copy()
    msg_list_copy.sort(key= lambda msg: msg.note)
    noteoff_list = []

    for key, group in groupby(msg_list_copy, lambda msg: msg.note):
        note_group = list(group)
        # check for missing note off
        if len(note_group) % 2 != 0:
            noteoff = Message('note_off', note=note_group[0].note, velocity=0, time=delta_time)
            noteoff_list.append(noteoff)

    msg_list.extend(noteoff_list)

    return msg_list