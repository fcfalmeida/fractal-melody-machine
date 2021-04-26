class Pattern:
    def __init__(self, notes):
        self.notes = notes
        self.order = 0

    def __repr__(self):
        return '<' + str(self.notes) + '|' + str(self.order) + '>'

    def __str__(self):
        return '<' + str(self.notes) + '|' + str(self.order) + '>'
