import time
from mido import second2tick, bpm2tempo, Message, MetaMessage
from fmm.core.utils.helpers import check_all_notes_off
from fmm.core.utils.repeated_timer import RepeatedTimer
from fmm.core.constants import TICKS_PER_BEAT

class PatternRecorder:
    def __init__(self, bpm, on_finish=None):
        self.bpm = bpm
        self.record_idle_time = 2
        self.on_finish = on_finish
        self.recording = False
        self.idle_timer = RepeatedTimer(self.record_idle_time, self._stop)
        self.last_message_time = 0
        self.recorded_messages = []
        self._buffer = []

    def _reset(self):
        self._buffer = []
        self.last_message_time = 0

    def record_message(self, message):
        if not self.recording:
            return

        self.idle_timer.reset()

        current_time = time.time()

        # Initialize time to the time the first message arrives at
        if not self._buffer:
            self.last_message_time = current_time

        delta_time = current_time - self.last_message_time
        self.last_message_time = current_time

        # TODO: get the ticks per beat value from some constant
        message.time = second2tick(delta_time, TICKS_PER_BEAT, bpm2tempo(self.bpm))
        self._buffer.append(message)
        print(message)

    def start(self):
        self._reset()
        self.idle_timer.start()
        self.recording = True

        print('Recording MIDI...')

    def _stop(self):
        if not check_all_notes_off(self._buffer):
            return

        self.idle_timer.stop()
        self.recording = False
        
        print('Done recording.')

        # Copy buffer to recorded_messages
        self.recorded_messages = self._buffer.copy()
        self._buffer = []

        self.on_finish()