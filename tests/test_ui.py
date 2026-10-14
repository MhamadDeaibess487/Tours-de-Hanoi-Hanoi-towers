import os
import tkinter as tk
from unittest.mock import patch
import pytest
from hanoi.ui import App
from hanoi.scores import ScoreStore

pytestmark = pytest.mark.skipif(not os.environ.get("DISPLAY"), reason="An X display is required")


def finish_move(root, app):
    timed_out = []

    def check():
        if app.moving is None:
            root.quit()
        else:
            root.after(10, check)

    def timeout():
        timed_out.append(True)
        root.quit()

    root.after(10, check)
    deadline = root.after(2000, timeout)
    root.mainloop()
    root.after_cancel(deadline)
    assert not timed_out


def test_graphical_game_and_animation(tmp_path):
    root = tk.Tk()
    app = App(root, ScoreStore(tmp_path / "scores.json"))
    root.update()
    try:
        app.disks.set("invalid")
        app.new()
        assert app.game.disks == 3
        app.disks.set("1")
        app.new()
        app.choose(0)
        app.choose(1)
        assert app.moving is not None
        app.choose(2)
        assert app.game.moves == 1
        app.undo()
        assert app.game.moves == 0
        with patch("hanoi.ui.simpledialog.askstring", return_value="Graphical player"):
            app.choose(0)
            app.choose(2)
            finish_move(root, app)
        assert app.game.won and len(app.store.load()) == 1
        app.start_solution()
        assert app.demo.won
        app.pause()
        assert app.job is None
        app.pause()
        app.stop()
        assert app.demo is None and app.game.won
        app.scores()
        root.geometry("800x500")
        root.update()
        assert len(app.canvas.find_all()) > 0
    finally:
        app.close()


def test_animation_event_loop_preserves_player_game(tmp_path):
    root = tk.Tk()
    app = App(root, ScoreStore(tmp_path / "scores.json"))
    root.update()
    try:
        app.game.move(0, 1)
        before = [tower.copy() for tower in app.game.towers]
        app.delay.set(50)
        app.start_solution()
        app.pause()
        assert app.demo.moves == 1 and app.job is None and app.move_job is None
        frozen = app.moving["progress"]
        root.update()
        assert app.moving["progress"] == frozen
        app.pause()
        timed_out = []

        def check():
            if app.demo.won and app.moving is None:
                root.quit()
            else:
                root.after(10, check)

        def timeout():
            timed_out.append(True)
            root.quit()

        root.after(10, check)
        deadline = root.after(2000, timeout)
        root.mainloop()
        root.after_cancel(deadline)
        assert not timed_out
        assert app.demo.won and app.demo.moves == 7
        app.stop()
        assert app.move_job is None
        assert app.game.towers == before and app.game.moves == 1
        assert app.store.load() == []
    finally:
        app.close()


def test_restart_and_stop_during_motion(tmp_path):
    root = tk.Tk()
    app = App(root, ScoreStore(tmp_path / "scores.json"))
    root.update()
    try:
        app.choose(0)
        app.choose(1)
        assert app.canvas.find_withtag("moving")
        root.geometry("800x500")
        root.update()
        app.new()
        assert app.moving is None and app.move_job is None and app.game.moves == 0
        app.start_solution()
        app.pause()
        app.stop()
        assert app.demo is None and app.moving is None and app.move_job is None
        app.disks.set("1")
        app.new()
        with patch("hanoi.ui.simpledialog.askstring", return_value="Stopped animation"):
            app.choose(0)
            app.choose(2)
            app.stop()
        assert app.game.won and len(app.store.load()) == 1
        assert app.move_job is None
    finally:
        app.close()


def test_delayed_frame_uses_elapsed_time_without_redrawing_board(tmp_path):
    root = tk.Tk()
    app = App(root, ScoreStore(tmp_path / "scores.json"))
    root.update()
    try:
        app.delay.set(1000)
        with patch("hanoi.ui.perf_counter", return_value=10.0):
            app.choose(0)
            app.choose(1)
        initial_items = app.canvas.find_all()
        initial_position = app.canvas.coords("moving_shape")
        root.after_cancel(app.move_job)
        with patch("hanoi.ui.perf_counter", return_value=10.5):
            app.tick_move()
        assert app.moving["progress"] == 0.5
        assert app.canvas.find_all() == initial_items
        assert app.canvas.coords("moving_shape") != initial_position
        root.after_cancel(app.move_job)
        with patch("hanoi.ui.perf_counter", return_value=11.1):
            app.tick_move()
        assert app.moving is None and app.move_job is None
        assert app.game.moves == 1
    finally:
        app.close()
