import mido
import time
import threading
from dearpygui import core, simple
from pattern import Pattern
from note import Note
from fractal import fractalize
from generators import generate_midi, random_pattern, spread_octaves
from theory import notes_in_key
import figure
import midi
import status

print(mido.get_output_names())

port = mido.open_output('IAC Driver Bus 1')

figures = [figure.NOTE_8TH, figure.NOTE_QUARTER]

depth = 3
branching_factor = 2

def play():
    if not status.is_playing:
        print('Play')
        status.is_playing = True
        play_thread = threading.Thread(target=midi.infinite_play, args=(depth, branching_factor, figures, 'F', 20, port))
        play_thread.start()
    else:
        print('Stop')
        status.is_playing = False

with simple.window('Fractal Melody Machine'):
    core.add_text("Hello world")
    core.add_button("Play", callback=play)
    core.add_input_text("string")
    core.add_slider_float("float")

core.start_dearpygui(primary_window='Fractal Melody Machine') 

#mid.save('test.mid')