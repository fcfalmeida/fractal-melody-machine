import mido
import threading
import re
from dearpygui import core, simple
from fmm.pattern_recorder import PatternRecorder
from fmm.generators import fractalize
from fmm.pattern import Pattern
import fmm.theory as theory
import fmm.playback as playback
import fmm.status as status
import fmm.params as params


class App():
    def __init__(self):
        self.MAX_DEPTH = 16
        self.out_port = None

        # Set default params
        params.depth = 2
        params.branching_factor = 2
        params.bpm = 60
        params.figures = [theory.FIGURE_QUARTER_NOTE, theory.FIGURE_8TH_NOTE]
        params.octave_spread = [0] * self.MAX_DEPTH

        self.recorder = PatternRecorder(params.bpm, self.play)

    def play(self):
        play_thread = threading.Thread(
            target=playback.play_loop, args=(self.out_port, self.create_fractal))
        play_thread.start()

    def change_key(self, key):
        core.set_value('DetectedKey', f'Detected Key: {key}')

    def change_bpm(self):
        params.bpm = core.get_value('SliderBPM')

        # Update recorder bpm
        self.recorder = PatternRecorder(params.bpm, self.play)

        status.params_changed = True

    def change_figures(self, figure):
        checked = core.get_value(figure)
        figure_value = float(figure)

        if checked:
            params.figures.append(figure_value)
        else:
            params.figures.remove(figure_value)

        status.params_changed = True

    def change_midi_in_port(self):
        status.current_in_port.close()

        port_name = core.get_value('ComboInPort')
        status.current_in_port = mido.open_input(
            port_name, callback=self.get_midi_input)

    def change_midi_out_port(self):
        self.out_port.close()

        port_name = core.get_value('ComboOutPort')
        self.out_port = mido.open_output(port_name)

    def change_depth(self):
        params.depth = core.get_value('SliderDepth')

        status.params_changed = True

        # Clear sliders
        for layer in range(self.MAX_DEPTH):
            text = f'Layer {layer+1}'
            slider_name = f'SliderOct{layer}'

            try:
                core.delete_item(text)
                core.delete_item(slider_name)
            except SystemError:
                pass

        # Add sliders
        for layer in range(params.depth):
            text = f'Layer {layer+1}'
            slider_name = f'SliderOct{layer}'

            core.add_text(text, parent='OctaveWindow')
            core.add_slider_int(slider_name, default_value=params.octave_spread[layer], min_value=-2,
                                max_value=2, label='', width=100, parent='OctaveWindow', callback=self.change_octave)

    def change_bf(self):
        params.branching_factor = core.get_value('SliderBF')

        status.params_changed = True

    def change_octave(self, name):
        depth = re.findall('\d+', name)[0]
        depth = int(depth)

        octave_offset = core.get_value(name)
        params.octave_spread[depth] = octave_offset

    def get_midi_input(self, message):
        if not self.recorder.recording and message.type == 'note_on':
            self.recorder.start()

        playback.route_midi(self.out_port, message, 0)
        self.recorder.record_message(message)

    def create_fractal(self):
        pattern = Pattern(self.recorder.recorded_messages)

        self.change_key(pattern.key)

        return pattern

    def start(self):
        available_out_ports = mido.get_output_names()
        available_in_ports = mido.get_input_names()

        if len(available_in_ports) > 0:
            status.current_in_port = mido.open_input(
                available_in_ports[0], callback=self.get_midi_input)

        if len(available_out_ports) > 0:
            self.out_port = mido.open_output(available_out_ports[0])

        core.set_main_window_size(350, 550)
        core.set_main_window_title('Fractal Melody Machine')
        core.set_theme('Gold')

        with simple.window('Fractal Melody Machine', width=500, height=300):
            core.add_text('MIDI Input Port')
            core.add_combo('ComboInPort', items=mido.get_input_names(
            ), default_value=status.current_in_port.name, label='', width=100, callback=self.change_midi_in_port)

            core.add_text('MIDI Output Port')
            core.add_combo('ComboOutPort', items=mido.get_output_names(
            ), default_value=self.out_port.name, label='', width=100, callback=self.change_midi_out_port)

            core.add_spacing(count=10)

            core.add_text('BPM')
            core.add_slider_int('SliderBPM', default_value=60, min_value=20, max_value=200, label='', width=100, callback=self.change_bpm)

            core.add_text('Depth')
            core.add_slider_int('SliderDepth', default_value=4, min_value=1,
                                max_value=16, label='', width=100, callback=self.change_depth)

            core.add_same_line(spacing=45)
            core.add_text('DetectedKey', default_value='Detected Key: ')

            core.add_text('Branching Factor')
            core.add_slider_int('SliderBF', default_value=2, min_value=2,
                                max_value=4, label='', width=100, callback=self.change_bf)

            core.add_text('Octave Spread')
            core.add_child('OctaveWindow', width=300, height=150)
            core.end()

            core.add_text('Figures')
            core.add_child('FigureWindow', width=300, height=150)

            core.add_table('FigureTable', [], hide_headers=True, height=10)

            core.add_columns('FigureTableCols', 2, border=False)

            core.add_checkbox(str(theory.FIGURE_WHOLE_NOTE), label='Whole note', callback=self.change_figures)
            core.add_checkbox(str(theory.FIGURE_QUARTER_NOTE), label='Quarter note', callback=self.change_figures, default_value=True)
            core.add_checkbox(str(theory.FIGURE_16TH_NOTE), label='16th note', callback=self.change_figures)
            core.add_checkbox(str(theory.FIGURE_64TH_NOTE), label='64th note', callback=self.change_figures)

            core.add_next_column()

            core.add_checkbox(str(theory.FIGURE_HALF_NOTE), label='Half note', callback=self.change_figures)
            core.add_checkbox(str(theory.FIGURE_8TH_NOTE), label='8th note', callback=self.change_figures, default_value=True)
            core.add_checkbox(str(theory.FIGURE_32ND_NOTE), label='32nd note', callback=self.change_figures)

            core.end()

            # Initialize octave spread sliders
            self.change_depth()

        core.start_dearpygui(primary_window='Fractal Melody Machine')

