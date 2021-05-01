import mido
import threading
from dearpygui import core, simple
from fmm.pattern import Pattern
from fmm.note import Note
import fmm.theory as theory
import fmm.midi as midi
import fmm.status as status

class App:
    def __init__(self):
        self.port = None
        self.figures = [theory.FIGURE_8TH_NOTE, theory.FIGURE_QUARTER_NOTE]
        self.depth = 3
        self.branching_factor = 2

    def play(self):
        if not status.is_playing:
            status.is_playing = True

            play_thread = threading.Thread(target=midi.infinite_play, args=(
                self.depth, self.branching_factor, self.figures, 'F', 20, self.port))
            play_thread.start()
        else:
            status.is_playing = False

    def start(self):
        self.port = mido.open_output('IAC Driver Bus 1')

        with simple.window('Fractal Melody Machine'):
            core.add_text('Fractal Melody Machine')
            core.add_button('Play', callback=self.play)

        core.start_dearpygui(primary_window='Fractal Melody Machine') 

