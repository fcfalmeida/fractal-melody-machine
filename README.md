# Fractal Melody Machine
The Fractal Melody Machine is a MIDI melody generator written in Python inspired by the concept of fractals.

The project is divided in 3 modules:
- The `core` module implements the core functionality of the Fractal Melody Machine
- The `gui` module is the GUI version of the Fractal Melody Machine, developed using the [dearpygui](https://github.com/hoffstadt/DearPyGui) library. Still very under development.
- The `nogui` module is a version of the Fractal Melody Machine that will run on the terminal

# Installation

```bash
pip3 install requirements.txt
pip3 install fmm/gui/requirements.txt
```

If you don't need the GUI version you can skip installing the requirements for it.

# Running

For the GUI version:

```bash
python3 -m fmm.gui
```

And similarly, for the NoGUI version:

```bash
python3 -m fmm.nogui
```
