from itertools import groupby
from mido import Message

def check_all_notes_off(msg_list):
    msg_list_copy = msg_list.copy()
    msg_list_copy.sort(key=lambda msg: msg.note)

    for _, group in groupby(msg_list_copy, lambda msg: msg.note):
        note_group = list(group)
        # check for missing note off
        # each note on message should have a corresponding note off
        if len(note_group) % 2 != 0:
            return False

    return True

def list_similarity(list1, list2):
    return len(set(list1) & set(list2))


def vel_zero_to_noteoff(msg_list):
    msg_list_cpy = msg_list.copy()

    for i, msg in enumerate(msg_list_cpy):
        if msg.type == 'note_on' and msg.velocity == 0:
            msg_list_cpy[i] = Message(
                type='note_off', velocity=0, note=msg.note, time=msg.time, channel=msg.channel)

    return msg_list_cpy
