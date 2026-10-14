"""Validated JSON scores with atomic replacement."""

import json
import os
from pathlib import Path
import tempfile
import sys
from datetime import datetime, timezone


def default_path():
    if os.name == "nt":
        base = Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData/Local"))
    elif sys.platform == "darwin":
        base = Path.home() / "Library/Application Support"
    else:
        base = Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local/share"))
    return base / "hanoi/scores.json"


class ScoreStore:
    def __init__(self, path=None):
        self.path = Path(path) if path else default_path()

    def load(self):
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
        except FileNotFoundError:
            return []
        except (OSError, ValueError) as error:
            raise ValueError(f"Impossible de lire les scores : {error}") from error
        if not isinstance(data, list) or any(
            not isinstance(row, dict)
            or not isinstance(row.get("name"), str)
            or not row["name"].strip()
            or type(row.get("disks")) is not int
            or not 1 <= row["disks"] <= 10
            or type(row.get("moves")) is not int
            or row["moves"] < 2 ** row["disks"] - 1
            or not isinstance(row.get("date"), str)
            for row in data
        ):
            raise ValueError("Le fichier de scores contient des données invalides.")
        return data

    def add(self, name, game):
        name = name.strip()
        if not name or len(name) > 40:
            raise ValueError("Le nom doit contenir entre 1 et 40 caractères.")
        if not game.won:
            raise ValueError("Seules les parties gagnées peuvent être enregistrées.")
        rows = self.load()
        rows.append(dict(name=name, disks=game.disks, moves=game.moves, date=datetime.now(timezone.utc).isoformat()))
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temp = None
        try:
            with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=self.path.parent, delete=False) as stream:
                temp = Path(stream.name)
                json.dump(rows, stream, ensure_ascii=False, indent=2)
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(temp, self.path)
        finally:
            if temp and temp.exists():
                temp.unlink()

    def ranking(self):
        return sorted(self.load(), key=lambda row: (row["disks"], row["moves"], row["date"]))
