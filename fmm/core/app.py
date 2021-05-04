import abc
import fmm.core.theory as theory
import fmm.core.params as params

class App(metaclass=abc.ABCMeta):
    def __init__(self):
        self.port = None
        # Set default params
        params.figures = [theory.FIGURE_8TH_NOTE, theory.FIGURE_QUARTER_NOTE]
        params.key = 'C'
        params.depth = 2
        params.branching_factor = 2
        params.bpm = 60
        params.change_prob = 0.3

    @abc.abstractmethod
    def play(self):
        pass

    @abc.abstractmethod
    def start(self):
        pass

