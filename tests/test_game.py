import copy
import pytest
from hanoi import Game, solve


@pytest.mark.parametrize("n", [0, -1, 11, True, "3"])
def test_invalid_disks(n):
    with pytest.raises(ValueError):
        Game(n)
    with pytest.raises(ValueError):
        solve(n)


@pytest.mark.parametrize("source,target", [(0, 0), (1, 0), (-1, 2), (0, 3), (True, 2)])
def test_invalid_move_preserves_state(source, target):
    game = Game()
    before = copy.deepcopy(game.towers)
    with pytest.raises(ValueError):
        game.move(source, target)
    assert game.towers == before and game.moves == 0


@pytest.mark.parametrize("n", range(1, 11))
def test_solver_and_undo(n):
    game = Game(n)
    moves = list(solve(n))
    assert len(moves) == game.minimum
    for source, target in moves:
        game.move(source, target)
    assert game.won
    with pytest.raises(ValueError):
        game.move(2, 0)
    for _ in moves:
        game.undo()
    assert game.towers == [list(range(n, 0, -1)), [], []]
    with pytest.raises(ValueError):
        game.undo()


def test_large_disk():
    game = Game()
    game.move(0, 2)
    with pytest.raises(ValueError):
        game.move(0, 2)
    assert game.moves == 1


def test_exact_challenge_limit():
    game = Game(1, True)
    for i in range(6):
        game.move(0 if i % 2 == 0 else 1, 1 if i % 2 == 0 else 0)
    assert game.exhausted and game.moves == game.minimum + 5
    with pytest.raises(ValueError):
        game.move(0, 2)
    game.undo()
    game.move(1, 2)
    assert game.won and not game.exhausted


def test_solver_towers():
    with pytest.raises(ValueError):
        solve(3, 0, 0, 2)
    assert list(solve(1, 2, 0, 1)) == [(2, 0)]
