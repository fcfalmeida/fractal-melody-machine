import mido
import threading
from dearpygui import core, simple
from fmm.core.app import App
import fmm.core.theory as theory
import fmm.core.midi as midi
import fmm.core.status as status
import fmm.core.params as params

class GUIApp(App):
    def __init__(self):
        super().__init__()

        # TODO set default params
        params.figures = []

    def play(self):
        if not status.is_playing:
            status.is_playing = True

            play_thread = threading.Thread(target=midi.infinite_play, args=(self.port,))
            play_thread.start()
        else:
            status.is_playing = False

    def change_key(self):
        params.key = core.get_value('ComboKey')

    def change_bpm(self):
        params.bpm = core.get_value('SliderBPM')

    def change_prob(self):
        prob = core.get_value('SliderProb')
        params.change_prob = round(prob, 2)

    def change_figures(self, figure):
        checked = core.get_value(figure)
        figure_value = float(figure)
        
        if checked:
            params.figures.append(figure_value)
        else:
            params.figures.remove(figure_value)

        print(params.figures)

    def change_midi_port(self):
        self.port.close()

        port_name = core.get_value('ComboPort')
        mido.open_output(port_name)

    def change_depth(self):
        params.depth = core.get_value('SliderDepth')
        print(params.depth)

    def change_bf(self):
        params.branching_factor = core.get_value('SliderBF')
        print(params.branching_factor)

    def start(self):
        available_ports = mido.get_output_names()

        if len(available_ports) > 0:
            self.port = mido.open_output(available_ports[0])

        with simple.window('Fractal Melody Machine'):
            core.add_table('LayoutTable', [], hide_headers=True, height=80)

            core.add_columns('LayoutTableCols', 3, border=False)
            
            # Left Column
            #########################################################################################################
            core.add_text('Key')
            core.add_combo('ComboKey', items=list(theory.KEYS.keys()), default_value=params.key, label='', width=100, callback=self.change_key)

            core.add_text('BPM')
            core.add_slider_int('SliderBPM', default_value=60, min_value=20, max_value=200, label='', width=100, callback=self.change_bpm)

            core.add_text('Change Probability')
            core.add_slider_float('SliderProb', default_value=0.7, min_value=0.0, max_value=1.0, format='%.2f', label='', width=100, callback=self.change_prob)

            core.add_text('Figures')
            core.add_child('FigureWindow', width=300, height=150)

            core.add_table('FigureTable', [], hide_headers=True, height=10)

            core.add_columns('FigureTableCols', 2, border=False)

            core.add_checkbox(str(theory.FIGURE_WHOLE_NOTE), label='Whole note', callback=self.change_figures)
            core.add_checkbox(str(theory.FIGURE_QUARTER_NOTE), label='Quarter note', callback=self.change_figures)
            core.add_checkbox(str(theory.FIGURE_16TH_NOTE), label='16th note', callback=self.change_figures)
            core.add_checkbox(str(theory.FIGURE_64TH_NOTE), label='64th note', callback=self.change_figures)

            core.add_next_column()

            core.add_checkbox(str(theory.FIGURE_HALF_NOTE), label='Half note', callback=self.change_figures)
            core.add_checkbox(str(theory.FIGURE_8TH_NOTE), label='8th note', callback=self.change_figures)
            core.add_checkbox(str(theory.FIGURE_32ND_NOTE), label='32nd note', callback=self.change_figures)

            core.end()
            #########################################################################################################

            core.add_next_column()

            # Middle Column
            #########################################################################################################

            core.add_text('MIDI Port')
            core.add_combo('ComboPort', items=mido.get_output_names(), default_value=self.port.name, label='', width=100, callback=self.change_midi_port)
            core.add_spacing(count=5)
            core.add_button('Play', callback=self.play, width=100, height=50)

            #########################################################################################################

            core.add_next_column()

            # Right Column
            #########################################################################################################

            core.add_text('Depth')
            core.add_slider_int('SliderDepth', default_value=4, min_value=1, max_value=16, label='', width=100, callback=self.change_depth)

            core.add_text('Branching Factor')
            core.add_slider_int('SliderBF', default_value=2, min_value=2, max_value=4, label='', width=100, callback=self.change_bf)

            #########################################################################################################

            # Close table
            # core.end()

        core.start_dearpygui(primary_window='Fractal Melody Machine') 

