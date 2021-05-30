class Pattern:
    def __init__(self, messages):
        self.messages = list(map(lambda msg: msg.copy(), messages))
        self._order = 0

    @property
    def order(self):
        return self._order

    @order.setter
    def order(self, value):
        for i in range(len(self.messages)):
            if not self.messages[i].is_meta and not self.messages[i].type == 'reset':
                self.messages[i] = self.messages[i].copy(channel=value)

        self._order = value

    def shift_octave(self, offset):
        for i in range(len(self.messages)):
            self.messages[i].note += offset * 12

    def set_message_times(self, branching_factor):
        # Skip first message to anchor time at the start
        for i in range(1, len(self.messages)):
            time = self.messages[i].time / pow(branching_factor, self.order)
            self.messages[i] = self.messages[i].copy(time=time)

    def __repr__(self):
        return '<' + str(self.messages) + '|' + str(self.order) + '>'

    def __str__(self):
        return '<' + str(self.messages) + '|' + str(self.order) + '>'

    def __len__(self):
        return len(self.messages)

    def __getitem__(self, i):
        return self.messages[i]

    def __setitem__(self, i, note):
        self.messages[i] = note
