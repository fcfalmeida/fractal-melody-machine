import mido
import threading
from dearpygui import core, simple
from fmm.core.pattern import Pattern
from fmm.core.note import Note
import fmm.core.theory as theory
import fmm.core.midi as midi
import fmm.core.status as status
import fmm.core.params as params

class App:
    def __init__(self):
        self.port = None
        params.figures = [theory.FIGURE_8TH_NOTE, theory.FIGURE_QUARTER_NOTE]
        params.key = 'C'
        params.depth = 2
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

        with simple.window('Fractal Melody Machine'):
            core.add_text('Fractal Melody Machine')
            core.add_button('Play', callback=self.play)

        core.start_dearpygui(primary_window='Fractal Melody Machine') 

