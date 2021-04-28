from interval import MIN_SECOND, SECOND

def notes_in_key(key):
    keys = {
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

    intervals = [SECOND, SECOND, MIN_SECOND, SECOND, SECOND, SECOND]
    root = keys[key]
    notes = [root]

    for i in range(len(intervals)):
        notes.append(notes[i] + intervals[i])

    return notes