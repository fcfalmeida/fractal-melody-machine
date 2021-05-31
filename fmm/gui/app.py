import mido
import threading
import re
from dearpygui import core, simple
from fmm.core.app import App
from fmm.core.pattern_recorder import PatternRecorder
from fmm.core.generators import fractalize
from fmm.core.pattern import Pattern
import fmm.core.theory as theory
import fmm.core.midi as midi
import fmm.core.status as status
import fmm.core.params as params


class GUIApp(App):
    def __init__(self):
        super().__init__()

        self.MAX_DEPTH = 16

        # TODO set default params
        params.figures = []
        params.octave_spread = [0] * self.MAX_DEPTH

        self.recorder = PatternRecorder(params.bpm, self.play)

    def play(self):
        if not status.is_playing:
            status.is_playing = True

            play_thread = threading.Thread(
                target=midi.infinite_play, args=(self.out_port, self.create_fractal))
            play_thread.start()

    def change_key(self):
        params.key = core.get_value('ComboKey')

        status.params_changed = True

    def change_bpm(self):
        params.bpm = core.get_value('SliderBPM')

        # Update recorder bpm
        self.recorder = PatternRecorder(params.bpm, 4, on_finish=self.play)

        status.params_changed = True

    def change_prob(self):
        prob = core.get_value('SliderProb')
        params.change_prob = round(prob, 2)

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

        self.recorder.record_message(message)

    def create_fractal(self):
        pattern = Pattern(self.recorder.recorded_messages)

        return fractalize(pattern, params.bpm, params.depth, params.branching_factor)

    def start(self):
        available_out_ports = mido.get_output_names()
        available_in_ports = mido.get_input_names()

        if len(available_in_ports) > 0:
            status.current_in_port = mido.open_input(
                available_in_ports[0], callback=self.get_midi_input)

        if len(available_out_ports) > 0:
            self.out_port = mido.open_output(available_out_ports[0])

        simple.show_style_editor()
        core.set_main_window_size(350, 400)
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

            core.add_text('Depth')
            core.add_slider_int('SliderDepth', default_value=4, min_value=1,
                                max_value=16, label='', width=100, callback=self.change_depth)

            core.add_text('Branching Factor')
            core.add_slider_int('SliderBF', default_value=2, min_value=2,
                                max_value=4, label='', width=100, callback=self.change_bf)

            core.add_text('Octave Spread')
            core.add_child('OctaveWindow', width=300, height=150)

        core.start_dearpygui(primary_window='Fractal Melody Machine')
