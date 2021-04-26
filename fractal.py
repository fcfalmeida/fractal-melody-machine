from pattern import Pattern

def fractalize(pattern, depth, bf=2):
    fractal = []

    for level in range(depth):
        n = pow(bf, level)

        for j in range(n):
            p = Pattern(pattern.notes)
            p.order = level
            fractal.append(p)

    return fractal
