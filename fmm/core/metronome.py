import time
from fmm.core.utils.converters import beats2seconds
from fmm.core.utils.repeated_timer import RepeatedTimer
import fmm.core.status as status

class Metronome:
    def __init__(self, bpm, beats_measure):
        self.bpm = bpm
        self.beats_measure = beats_measure
        self.current_beat = 0
        self.elapsed_measures = 0

        timer_interval = beats2seconds(1, self.bpm)
        self.timer = RepeatedTimer(timer_interval, self._beat)

    def _beat(self):
        if self.current_beat == 0:
            print('Strong beat')
        else:
            print('Weak beat')

        self.current_beat += 1

        if (self.current_beat >= self.beats_measure):
            self.current_beat = 0
            self.elapsed_measures += 1

    def start(self):
        self.current_beat = 0
        self.elapsed_measures = 0
        self.timer.start()

    def stop(self):
        self.timer.stop()

    """
    def start(self):
        sleep_interval = beats2seconds(1, self.bpm)

        while status.is_playing:
            for i in range(self.beats_measure):
                # Allow metronome to be stopped when in the middle of a measure
                if not status.is_playing:
                    print('Stop right there')
                    break

                if i == 0:
                    print('Strong beat')
                else:    
                    print('Weak beat')
                
                time.sleep(sleep_interval)
    """
