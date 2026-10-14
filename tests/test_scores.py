import pytest
from hanoi import Game, solve
from hanoi.scores import ScoreStore


def win(n):
    game = Game(n)
    for source, target in solve(n):
        game.move(source, target)
    return game


def test_roundtrip_and_ranking(tmp_path):
    store = ScoreStore(tmp_path / "nested/scores.json")
    assert store.load() == []
    store.add("Alice", win(3))
    store.add("Alice", win(1))
    game = Game(1)
    game.move(0, 1)
    game.move(1, 0)
    game.move(0, 2)
    store.add("Bob", game)
    rows = ScoreStore(store.path).ranking()
    assert [(r["name"], r["disks"], r["moves"]) for r in rows] == [("Alice", 1, 1), ("Bob", 1, 3), ("Alice", 3, 7)]
    assert list(store.path.parent.iterdir()) == [store.path]


@pytest.mark.parametrize("content", ["broken", "{}", "[{}]", '[{"name":"A","disks":1,"moves":0,"date":"x"}]'])
def test_corruption_preserved(tmp_path, content):
    path = tmp_path / "scores.json"
    path.write_text(content)
    with pytest.raises(ValueError):
        ScoreStore(path).add("Alice", win(1))
    assert path.read_text() == content


def test_invalid_score(tmp_path):
    store = ScoreStore(tmp_path / "scores.json")
    with pytest.raises(ValueError):
        store.add(" ", win(1))
    with pytest.raises(ValueError):
        store.add("Alice", Game())


def test_failed_replace_preserves_old_scores(tmp_path, monkeypatch):
    store = ScoreStore(tmp_path / "scores.json")
    store.add("Alice", win(1))
    before = store.path.read_bytes()

    def fail(*args):
        raise OSError("Disk write failed")

    monkeypatch.setattr("hanoi.scores.os.replace", fail)
    with pytest.raises(OSError):
        store.add("Bob", win(2))
    assert store.path.read_bytes() == before
    assert list(tmp_path.iterdir()) == [store.path]
