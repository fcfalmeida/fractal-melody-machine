from itertools import groupby
from mido import Message

def check_all_notes_off(msg_list):
    msg_list_copy = msg_list.copy()
    msg_list_copy.sort(key= lambda msg: msg.note)

    for key, group in groupby(msg_list_copy, lambda msg: msg.note):
        note_group = list(group)
        # check for missing note off
        # each note on message should have a corresponding note off
        if len(note_group) % 2 != 0:
            return False

    return True