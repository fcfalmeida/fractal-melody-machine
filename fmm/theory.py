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

    # major scale intervals
    intervals = [
        INTERVAL_SECOND, 
        INTERVAL_SECOND, 
        INTERVAL_MIN_SECOND, 
        INTERVAL_SECOND, 
        INTERVAL_SECOND, 
        INTERVAL_SECOND
    ]
    root = keys[key]
    notes = [root]

    for i in range(len(intervals)):
        notes.append(notes[i] + intervals[i])

    return notes