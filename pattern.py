from copy import deepcopy
from note import Note

class Pattern:
    def __init__(self, notes):
        self.notes = notes
        self.order = 0

    def shift_octave(self, offset):
        self.notes = list(map(lambda note: Note(note.number + offset * 12, note.duration), self.notes))

    def __repr__(self):
        return '<' + str(self.notes) + '|' + str(self.order) + '>'

    def __str__(self):
        return '<' + str(self.notes) + '|' + str(self.order) + '>'

    def __len__(self):
        return len(self.notes)

    def __getitem__(self, i):
        return self.notes[i]

    def __setitem__(self, i, note):
        self.notes[i] = note
