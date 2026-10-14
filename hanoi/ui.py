"""Event-driven Tkinter interface with a scalable Canvas."""

import tkinter as tk
import customtkinter as ctk
from tkinter import ttk, simpledialog
from .game import Game
from .scores import ScoreStore
from .solver import solve
from .theme import apply_dark_theme, BACKGROUND, SURFACE


class App:
    def __init__(self, root, store=None):
        self.root = root
        self.store = store or ScoreStore()
        self.game = Game()
        self.selected = None
        self.job = None
        self.move_job = None
        self.moving = None
        self.animation = None
        self.demo = None
        self.paused = False
        self.recorded = False
        root.title("Tours de Hanoï")
        apply_dark_theme(root)
        ctk.set_appearance_mode("dark")
        root.geometry("1000x650")
        root.minsize(700, 450)
        root.protocol("WM_DELETE_WINDOW", self.close)
        self.disks = tk.StringVar(value="3")
        self.challenge = tk.BooleanVar()
        self.delay = tk.IntVar(value=400)
        self.status = tk.StringVar(value="Choisissez une tour de départ puis une destination.")
        self.counter = tk.StringVar()
        header = ttk.Frame(root, padding=12)
        header.pack(fill="x")
        ttk.Label(header, text="TOURS DE HANOÏ", font=("TkDefaultFont", 18, "bold")).pack(side="left")
        ttk.Label(header, text="Disques").pack(side="left", padx=(25, 5))
        ttk.Spinbox(header, from_=1, to=10, textvariable=self.disks, width=4).pack(side="left")
        ttk.Checkbutton(header, text="Défi : minimum + 5", variable=self.challenge).pack(side="left", padx=12)
        tools = ttk.Frame(root, padding=(12, 0))
        tools.pack(fill="x")
        for text, command in [
            ("Nouvelle partie", self.new),
            ("Annuler", self.undo),
            ("Solution", self.start_solution),
            ("Pause / reprendre", self.pause),
            ("Arrêter", self.stop),
            ("Scores", self.scores),
        ]:
            self.button(tools, text, command, primary=text == "Nouvelle partie").pack(side="left", padx=3)
        ttk.Label(root, textvariable=self.counter, padding=10, style="Counter.TLabel").pack()
        self.canvas = tk.Canvas(root, background="#101827", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True, padx=12)
        self.canvas.bind("<Configure>", lambda event: self.draw())
        self.canvas.bind("<Button-1>", self.click)
        for index in range(3):
            root.bind(str(index + 1), lambda event, tower=index: self.choose(tower))
        root.bind("<Escape>", lambda event: self.cancel_selection())
        footer = ttk.Frame(root, padding=12)
        footer.pack(fill="x")
        ttk.Label(footer, textvariable=self.status).pack(side="left")
        ttk.Label(footer, text="Durée (ms)").pack(side="right")
        ttk.Scale(footer, from_=50, to=1000, variable=self.delay).pack(side="right")
        ttk.Label(
            root,
            text="Clavier : 1, 2, 3 pour les tours · Échap pour désélectionner",
            padding=(0, 0, 0, 8),
            style="Muted.TLabel",
        ).pack()
        self.draw()

    def cancel_selection(self):
        self.selected = None
        self.draw()

    def new(self):
        try:
            game = Game(int(self.disks.get()), self.challenge.get())
        except ValueError as error:
            self.status.set(str(error))
            return
        self.stop(notify=False)
        self.game = game
        self.recorded = False
        self.selected = None
        self.status.set("Nouvelle partie : déplacez les disques sur la tour 3.")
        self.draw()

    def click(self, event):
        self.canvas.focus_set()
        self.choose(min(2, max(0, int(event.x / (self.canvas.winfo_width() / 3)))))

    def choose(self, tower):
        # Ignore number keys while typing the disk count.
        if isinstance(self.root.focus_get(), (ttk.Spinbox, ttk.Entry)):
            return
        if self.moving is not None:
            self.status.set("Attendez la fin du déplacement.")
            return
        if self.demo is not None:
            self.status.set("Arrêtez la démonstration pour reprendre votre partie.")
            return
        if self.selected is None:
            if not self.game.towers[tower]:
                self.status.set("Cette tour est vide.")
                return
            self.selected = tower
            self.status.set(f"Tour {tower + 1} sélectionnée. Choisissez la destination.")
        else:
            source = self.selected
            self.selected = None
            try:
                self.animate_move(self.game, source, tower, self.after_player_move)
            except ValueError as error:
                self.status.set(str(error))
        self.draw()

    def after_player_move(self):
        self.status.set("Coup joué. Choisissez la prochaine tour de départ.")
        if self.game.won:
            self.status.set(f"Victoire en {self.game.moves} coups !")
            if not self.recorded:
                name = simpledialog.askstring("Victoire !", "Votre nom pour enregistrer le score :", parent=self.root)
                if name is not None:
                    try:
                        self.store.add(name, self.game)
                        self.recorded = True
                    except (ValueError, OSError) as error:
                        self.show_error("Score non enregistré", str(error))
        elif self.game.exhausted:
            self.status.set("Limite du défi atteinte. Annulez ou commencez une nouvelle partie.")
        self.draw()

    def undo(self):
        self.stop(notify=False)
        try:
            self.game.undo()
            self.status.set("Dernier coup annulé.")
        except ValueError as error:
            self.status.set(str(error))
        self.selected = None
        self.draw()

    def start_solution(self):
        self.stop(notify=False)
        self.demo = Game(self.game.disks)
        self.animation = iter(solve(self.game.disks))
        self.selected = None
        self.status.set("Démonstration depuis le départ ; votre partie est conservée.")
        self.step()

    def step(self):
        self.job = None
        if self.paused or self.demo is None:
            return
        try:
            source, target = next(self.animation)
        except StopIteration:
            self.status.set("Solution terminée. « Arrêter » restaure votre partie.")
            return
        self.animate_move(self.demo, source, target, self.next_solution_move)

    def next_solution_move(self):
        if self.demo is not None and not self.paused:
            self.job = self.root.after(50, self.step)

    def animate_move(self, game, source, target, complete):
        source_level = len(game.towers[source]) - 1
        game.move(source, target)
        self.moving = dict(
            disk=game.towers[target][-1],
            source=source,
            target=target,
            source_level=source_level,
            target_level=len(game.towers[target]) - 1,
            progress=0.0,
            duration=max(50, int(self.delay.get())),
            complete=complete,
        )
        self.draw()
        self.move_job = self.root.after(16, self.tick_move)

    def tick_move(self):
        self.move_job = None
        if self.moving is None or self.paused:
            return
        self.moving["progress"] = min(1.0, self.moving["progress"] + 16 / self.moving["duration"])
        if self.moving["progress"] >= 1:
            complete = self.moving["complete"]
            self.moving = None
            self.draw()
            complete()
        else:
            self.draw()
            self.move_job = self.root.after(16, self.tick_move)

    def pause(self):
        if self.demo is None:
            return
        self.paused = not self.paused
        if self.paused:
            if self.job:
                self.root.after_cancel(self.job)
                self.job = None
            if self.move_job:
                self.root.after_cancel(self.move_job)
                self.move_job = None
            self.status.set("Démonstration en pause.")
        else:
            self.status.set("Démonstration en cours.")
            if self.moving is not None:
                self.move_job = self.root.after(16, self.tick_move)
            else:
                self.step()

    def stop(self, notify=True):
        complete = self.moving["complete"] if notify and self.moving and self.demo is None else None
        if self.move_job:
            self.root.after_cancel(self.move_job)
        self.move_job = None
        self.moving = None
        if self.job:
            self.root.after_cancel(self.job)
        self.job = None
        self.demo = None
        self.animation = None
        self.paused = False
        self.selected = None
        self.status.set("Votre partie est conservée. Choisissez une tour.")
        self.draw()
        if complete:
            complete()

    def draw(self):
        self.canvas.delete("all")
        game = self.demo if self.demo is not None else self.game
        width, height = max(1, self.canvas.winfo_width()), max(1, self.canvas.winfo_height())
        cell, baseline = width / 3, height - 45
        disk_height = min(28, (height - 95) / (game.disks + 1))
        colors = [
            "#38bdf8",
            "#818cf8",
            "#c084fc",
            "#f472b6",
            "#fb7185",
            "#fb923c",
            "#facc15",
            "#a3e635",
            "#34d399",
            "#2dd4bf",
        ]
        for tower, stack in enumerate(game.towers):
            center = cell * (tower + 0.5)
            self.canvas.create_rectangle(center - 5, 55, center + 5, baseline, fill="#64748b", outline="")
            self.canvas.create_rectangle(
                center - cell * 0.43,
                baseline,
                center + cell * 0.43,
                baseline + 7,
                fill="#f8fafc" if self.selected == tower else "#475569",
                outline="",
            )
            self.canvas.create_text(
                center, baseline + 25, text=f"Tour {tower + 1}", fill="#f8fafc", font=("TkDefaultFont", 12)
            )
            for level, disk in enumerate(stack):
                if self.moving is not None and disk == self.moving["disk"]:
                    continue
                half = cell * (0.12 + 0.29 * disk / game.disks)
                bottom = baseline - level * disk_height
                self.canvas.create_rectangle(
                    center - half,
                    bottom - disk_height + 2,
                    center + half,
                    bottom - 1,
                    fill=colors[disk - 1],
                    outline="#101827",
                )
                self.canvas.create_text(center, bottom - disk_height / 2, text=str(disk), fill="#101827")
        if self.moving is not None:
            move = self.moving
            start_x = cell * (move["source"] + 0.5)
            end_x = cell * (move["target"] + 0.5)
            start_y = baseline - move["source_level"] * disk_height
            end_y = baseline - move["target_level"] * disk_height
            points = [(start_x, start_y), (start_x, 35), (end_x, 35), (end_x, end_y)]
            progress = min(move["progress"] * 3, 2.999999)
            stage = int(progress)
            t = progress - stage
            t = t * t * (3 - 2 * t)  # Smooth easing within each segment.
            x = points[stage][0] + (points[stage + 1][0] - points[stage][0]) * t
            y = points[stage][1] + (points[stage + 1][1] - points[stage][1]) * t
            disk = move["disk"]
            half = cell * (0.12 + 0.29 * disk / game.disks)
            self.canvas.create_rectangle(
                x - half, y - disk_height + 2, x + half, y - 1, fill=colors[disk - 1], outline="#101827", tags="moving"
            )
            self.canvas.create_text(x, y - disk_height / 2, text=str(disk), fill="#101827", tags="moving")
        prefix = "Solution · " if self.demo is not None else ""
        limit = f" · limite : {game.minimum + 5}" if game.challenge else ""
        self.counter.set(f"{prefix}{game.moves} coups · minimum : {game.minimum}{limit}")

    def scores(self):
        try:
            rows = self.store.ranking()
        except (ValueError, OSError) as error:
            self.show_error("Scores", str(error))
            return
        window = tk.Toplevel(self.root)
        window.title("Classement")
        window.configure(background=BACKGROUND)
        window.geometry("740x420")
        window.minsize(600, 300)
        heading = ttk.Frame(window, padding=16)
        heading.pack(fill="x")
        ttk.Label(heading, text="CLASSEMENT", font=("TkDefaultFont", 16, "bold")).pack(anchor="w")
        ttk.Label(
            heading, text="Par nombre de disques, puis par nombre de coups · Dates UTC", style="Muted.TLabel"
        ).pack(anchor="w", pady=(6, 0))
        body = ttk.Frame(window, padding=(16, 0, 16, 16))
        body.pack(fill="both", expand=True)
        table = ttk.Treeview(body, columns=("disks", "name", "moves", "date"), show="headings")
        for column, title in [("disks", "Disques"), ("name", "Joueur"), ("moves", "Coups"), ("date", "Date UTC")]:
            table.heading(column, text=title)
            table.column(column, width=160)
        scroll = ttk.Scrollbar(body, orient="vertical", command=table.yview)
        table.configure(yscrollcommand=scroll.set)
        table.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")
        table.tag_configure("even", background=BACKGROUND)
        table.tag_configure("odd", background=SURFACE)
        table.tag_configure("best", foreground="#7dd3fc")
        best = {}
        for index, row in enumerate(rows):
            best.setdefault(row["disks"], row["moves"])
            tags = ["even" if index % 2 == 0 else "odd"]
            if row["moves"] == best[row["disks"]]:
                tags.append("best")
            table.insert("", "end", values=(row["disks"], row["name"], row["moves"], row["date"][:10]), tags=tags)
        if not rows:
            table.insert("", "end", values=("", "Aucun score enregistré", "", ""))

    def show_error(self, title, message):
        window = tk.Toplevel(self.root)
        window.title(title)
        window.configure(background=BACKGROUND)
        window.transient(self.root)
        frame = ttk.Frame(window, padding=20)
        frame.pack(fill="both", expand=True)
        ttk.Label(frame, text=title, foreground="#fda4af", font=("TkDefaultFont", 12, "bold")).pack(anchor="w")
        ttk.Label(frame, text=message, wraplength=450).pack(anchor="w", pady=12)
        button = self.button(frame, "Fermer", window.destroy)
        button.pack(anchor="e")
        button.focus_set()
        window.bind("<Escape>", lambda event: window.destroy())

    def button(self, parent, text, command, primary=False):
        button = ctk.CTkButton(
            parent,
            text=text,
            command=command,
            corner_radius=12,
            width=110,
            height=38,
            bg_color=BACKGROUND,
            fg_color="#0369a1" if primary else SURFACE,
            hover_color="#0284c7" if primary else "#334155",
            text_color="#f1f5f9",
            border_width=1,
            border_color="#475569",
        )
        button.bind("<Return>", lambda event: command())
        button.bind("<space>", lambda event: command())
        return button

    def close(self):
        if self.move_job:
            self.root.after_cancel(self.move_job)
        if self.job:
            self.root.after_cancel(self.job)
        self.root.destroy()


def run():
    try:
        root = tk.Tk()
    except tk.TclError as error:
        raise SystemExit(f"Affichage graphique indisponible : {error}. Utilisez python -m hanoi --cli.") from error
    App(root)
    root.mainloop()
