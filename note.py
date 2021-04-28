class Note:
    def __init__(self, number, duration):
        self.number = number
        self.duration = duration

    def __repr__(self):
        return str(self.number) + ' | ' + str(self.duration)