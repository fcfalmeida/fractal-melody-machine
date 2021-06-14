import math
from fmm.theory import closest_key

class Pattern:
    def __init__(self, messages):
        self.messages = list(map(lambda msg: msg.copy(), messages))
        self._order = 0
        self.key = closest_key(messages)

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

    def is_velocity_above_threshold(self, vel_threshold):
        for msg in self.messages:
            if msg.type == 'note_on' and msg.velocity < vel_threshold:
                return False
        
        return True

    def decay_velocity(self, time, rate):
        for i, msg in enumerate(self.messages):
            velocity = msg.velocity
            velocity -= velocity * math.sqrt(time) * rate

            # prevent velocity from going below 0
            if (velocity < 0):
                velocity = 0

            self.messages[i].velocity = int(velocity)

    def __len__(self):
        return len(self.messages)

    def __getitem__(self, i):
        return self.messages[i]

    def __setitem__(self, i, note):
        self.messages[i] = note
