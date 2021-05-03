import mido
import threading
from dearpygui import core, simple
from fmm.core.app import App
import fmm.core.midi as midi
import fmm.core.status as status
import fmm.core.params as params

class GUIApp(App):
    def __init__(self):
        super().__init__()

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

