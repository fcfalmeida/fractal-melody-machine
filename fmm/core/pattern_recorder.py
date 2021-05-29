import time
from mido import second2tick, bpm2tempo, MetaMessage
from fmm.core.metronome import Metronome

class PatternRecorder:
    def __init__(self, bpm, beats_measure, record_measures=1, on_finish=None):
        self.bpm = bpm
        self.beats_measure = beats_measure
        self.record_measures = record_measures
        self.on_finish = on_finish
        self.metronome = Metronome(bpm, beats_measure, callback=self._on_beat)
        self.recording = False
        self.last_message_time = 0
        self.recorded_messages = []

    def _on_beat(self, beat, measure):
        if (measure == self.record_measures):
            self._stop()
        
        print(f'Beat: {beat} | Measure: {measure}')

    def _reset(self):
        self.recorded_messages = []
        self.last_message_time = 0

    def record_message(self, message):
        if not self.recording:
            return

        current_time = time.time()

        # Initialize time to the on the time the first message arrives at
        if not self.recorded_messages:
            self.last_message_time = current_time

        delta_time = current_time - self.last_message_time
        self.last_message_time = current_time

        # TODO: get the ticks per beat value from some constant
        message.time = second2tick(delta_time, 480, bpm2tempo(self.bpm))
        self.recorded_messages.append(message)
        print(message)

    def start(self):
        self._reset()
        self.metronome.start()
        self.recording = True

        print('Recording MIDI...')

    def _stop(self):
        self.metronome.stop()
        self.recording = False
        
        print('Done recording.')

        tick_target = 480 * self.beats_measure
        total_ticks = 0

        for msg in self.recorded_messages:
            total_ticks += msg.time

        eot = MetaMessage('end_of_track', time=tick_target - total_ticks)
        self.recorded_messages.append(eot)

        print(eot)

        self.on_finish()