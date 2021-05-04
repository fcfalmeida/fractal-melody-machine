import mido
import threading
import signal
import sys
from fmm.core.app import App
import fmm.core.midi as midi
import fmm.core.theory as theory
import fmm.core.status as status
import fmm.core.params as params

def quit(sig, frame):
    sys.exit(0)

class NoGUIApp(App):
    def __init__(self):
        super().__init__()

        params.figures = [theory.FIGURE_8TH_NOTE, theory.FIGURE_QUARTER_NOTE]
        params.key = 'D'
        params.depth = 4
        params.branching_factor = 2
        params.bpm = 60

    def play(self):
        if not status.is_playing:
            status.is_playing = True

            play_thread = threading.Thread(target=midi.infinite_play, args=(self.port,))
            play_thread.start()
        else:
            status.is_playing = False

    def start(self):
        self.port = mido.open_output('IAC Driver Bus 1')

        # Graceful exit when CTRL+C is presset
        signal.signal(signal.SIGINT, quit)

        print('Press Enter to Play/Pause. CTRL+C to quit.')

        while True:
            inp = input()

            if not inp:
                self.play()

                if status.is_playing:
                    print('Playing...')
                else:
                    print('Stopped.')
