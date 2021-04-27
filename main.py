from pattern import Pattern
from fractal import fractalize
from midi import generate_midi

depth = 5
branching_factor = 2

notes = [60, 61, 62, 63, 64, 65]
pattern = Pattern([60, 61, 62, 63, 64, 65])
fractal = fractalize(pattern, depth, branching_factor)

mid = generate_midi(fractal, branching_factor, depth, 120, 4)

print(fractal)

mid.save('test.mid')