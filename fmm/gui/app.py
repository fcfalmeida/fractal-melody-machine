import mido
import threading
from dearpygui import core, simple, demo
from fmm.core.app import App
import fmm.core.theory as theory
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

        # demo.show_demo()

        with simple.window('Fractal Melody Machine'):
            core.add_table('LayoutTable', [], hide_headers=True, height=80)

            core.add_columns('LayoutTableCols', 3, border=False)
            
            # Left Column
            #########################################################################################################
            core.add_text('Key')
            core.add_combo('ComboKey', items=list(theory.KEYS.keys()), label='', width=100)

            core.add_text('BPM')
            core.add_slider_int('SliderBPM', default_value=60, min_value=20, max_value=200, label='', width=100)

            core.add_text('Change Probability')
            core.add_slider_float('SliderProb', default_value=0.7, min_value=0.0, max_value=1.0, format='%.2f', label='', width=100)

            core.add_text('Figures')
            core.add_child('FigureWindow', width=300, height=150)

            core.add_table('FigureTable', [], hide_headers=True, height=10)

            core.add_columns('FigureTableCols', 2, border=False)

            core.add_checkbox('Whole note')
            core.add_checkbox('Quarter note')
            core.add_checkbox('16th note')
            core.add_checkbox('64th note')

            core.add_next_column()

            core.add_checkbox('Half note')
            core.add_checkbox('8th note')
            core.add_checkbox('32nd note')

            core.end()
            #########################################################################################################

            core.add_next_column()

            # Middle Column
            #########################################################################################################

            core.add_text('MIDI Port')
            core.add_combo('ComboMIDI', items=mido.get_input_names(), label='', width=100)
            core.add_spacing(count=5)
            core.add_button('Play', callback=self.play, width=100, height=50)

            #########################################################################################################

            core.add_next_column()

            # Right Column
            #########################################################################################################

            core.add_text('Depth')
            core.add_slider_int('SliderDepth', default_value=4, min_value=1, max_value=16, label='', width=100)

            core.add_text('Branching Factor')
            core.add_slider_int('SliderBF', default_value=2, min_value=2, max_value=4, label='', width=100)

            #########################################################################################################

            # Close table
            # core.end()

        core.start_dearpygui(primary_window='Fractal Melody Machine') 

