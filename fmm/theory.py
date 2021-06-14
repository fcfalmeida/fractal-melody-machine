from fmm.utils.helpers import list_similarity

# Figures
FIGURE_WHOLE_NOTE = 4
FIGURE_HALF_NOTE = 2
FIGURE_QUARTER_NOTE = 1
FIGURE_8TH_NOTE = 0.5
FIGURE_16TH_NOTE = 0.25
FIGURE_32ND_NOTE = 0.125
FIGURE_64TH_NOTE = 0.0625

# Intervals
INTERVAL_MIN_SECOND = 1
INTERVAL_SECOND = 2

KEYS = {
    'C': 60,
    'C#/Db': 61,
    'D': 62,
    'D#/Eb': 63,
    'E': 64,
    'F': 65,
    'F#/Gb': 66,
    'G': 67,
    'G#/Ab': 68,
    'A': 69,
    'A#/Bb': 70,
    'B': 71
}

def notes_in_key(key):
    # major scale intervals
    intervals = [
        INTERVAL_SECOND, 
        INTERVAL_SECOND, 
        INTERVAL_MIN_SECOND, 
        INTERVAL_SECOND, 
        INTERVAL_SECOND, 
        INTERVAL_SECOND
    ]
    root = KEYS[key]
    notes = [root]

    for i in range(len(intervals)):
        notes.append(notes[i] + intervals[i])

    return notes

def get_pitch_class(note):
    return note % 12

def closest_key(msg_list):
    highest_similarity = 0
    best_match = None

    # Filter messages that are not note_on
    note_ons = list(filter(lambda msg: msg.type == 'note_on', msg_list))

    pattern_pitch_classes = list(map(lambda msg: get_pitch_class(msg.note), note_ons))

    for key in KEYS.keys():
        key_notes = notes_in_key(key)

        key_pitch_classes = list(map(lambda note: get_pitch_class(note), key_notes))
        
        similarity = list_similarity(pattern_pitch_classes, key_pitch_classes)

        if similarity > highest_similarity:
            highest_similarity = similarity
            best_match = key

    return best_match