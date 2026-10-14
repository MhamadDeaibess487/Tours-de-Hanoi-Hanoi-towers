"""Rules and reversible state, independent of any interface."""

from dataclasses import dataclass, field


@dataclass
class Game:
    disks: int = 3
    challenge: bool = False
    towers: list[list[int]] = field(init=False)
    history: list[tuple[int, int]] = field(default_factory=list, init=False)

    def __post_init__(self) -> None:
        if type(self.disks) is not int or not 1 <= self.disks <= 10:
            raise ValueError("Le nombre de disques doit être compris entre 1 et 10.")
        self.towers = [list(range(self.disks, 0, -1)), [], []]

    @property
    def moves(self) -> int:
        return len(self.history)

    @property
    def minimum(self) -> int:
        return 2**self.disks - 1

    @property
    def won(self) -> bool:
        return self.towers == [[], [], list(range(self.disks, 0, -1))]

    @property
    def exhausted(self) -> bool:
        return self.challenge and self.moves >= self.minimum + 5 and not self.won

    def move(self, source: int, target: int) -> None:
        if any(type(t) is not int or t not in range(3) for t in (source, target)):
            raise ValueError("Choisissez une tour de 1 à 3.")
        if self.won or self.exhausted:
            raise ValueError("La partie est terminée. Annulez ou commencez une nouvelle partie.")
        if source == target:
            raise ValueError("Choisissez deux tours différentes.")
        if not self.towers[source]:
            raise ValueError("La tour de départ est vide.")
        disk = self.towers[source][-1]
        if self.towers[target] and disk > self.towers[target][-1]:
            raise ValueError("Un grand disque ne peut pas être posé sur un plus petit.")
        self.towers[target].append(self.towers[source].pop())
        self.history.append((source, target))

    def undo(self) -> None:
        if not self.history:
            raise ValueError("Aucun coup à annuler.")
        source, target = self.history.pop()
        self.towers[source].append(self.towers[target].pop())
