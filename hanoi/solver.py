"""Lazy recursive solution: O(2**n) time, O(n) auxiliary space."""


def solve(disks: int, source: int = 0, target: int = 2, auxiliary: int = 1):
    if type(disks) is not int or not 1 <= disks <= 10:
        raise ValueError("Le nombre de disques doit être compris entre 1 et 10.")
    if any(type(t) is not int for t in (source, target, auxiliary)) or set((source, target, auxiliary)) != {0, 1, 2}:
        raise ValueError("Les trois tours doivent être distinctes et comprises entre 0 et 2.")

    def generate(n, start, end, spare):
        if n:
            yield from generate(n - 1, start, spare, end)
            yield start, end
            yield from generate(n - 1, spare, end, start)

    return generate(disks, source, target, auxiliary)
