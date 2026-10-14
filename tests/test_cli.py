from hanoi.cli import run
from hanoi.scores import ScoreStore


def test_cli_errors_undo_solution_scores_and_replay(monkeypatch, tmp_path, capsys):
    answers = iter(
        [
            "abc",
            "1",
            "non",
            "abc",
            "2 1",
            "1 2",
            "annuler",
            "solution",
            "1 3",
            "Alice",
            "oui",
            "1",
            "non",
            "scores",
            "quitter",
        ]
    )
    monkeypatch.setattr("builtins.input", lambda prompt: next(answers))
    store = ScoreStore(tmp_path / "scores.json")
    run(store)
    output = capsys.readouterr().out
    assert "Victoire" in output and "vide" in output and "Démonstration terminée" in output
    assert len(store.load()) == 1 and store.load()[0]["moves"] == 1
