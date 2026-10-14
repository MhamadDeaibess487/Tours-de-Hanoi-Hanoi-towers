"""Shared desktop palette and widget states, using standard Tkinter only."""

from tkinter import ttk

BACKGROUND = "#0f172a"
SURFACE = "#1e293b"
TEXT = "#f1f5f9"
MUTED = "#cbd5e1"
ACCENT = "#38bdf8"


def apply_dark_theme(root):
    root.configure(background=BACKGROUND)
    # Tk-based name dialogs inherit these defaults too.
    for pattern, value in {
        "*background": BACKGROUND,
        "*foreground": TEXT,
        "*Entry.background": SURFACE,
        "*Entry.insertBackground": TEXT,
        "*Entry.selectBackground": "#0369a1",
        "*Button.background": SURFACE,
        "*Button.activeBackground": "#334155",
        "*Button.activeForeground": TEXT,
        "*Button.highlightBackground": BACKGROUND,
    }.items():
        root.option_add(pattern, value)
    style = ttk.Style(root)
    style.theme_use("clam")
    style.configure(".", background=BACKGROUND, foreground=TEXT)
    style.configure("TFrame", background=BACKGROUND)
    style.configure("TLabel", background=BACKGROUND, foreground=TEXT)
    style.configure("Muted.TLabel", foreground=MUTED)
    style.configure("Counter.TLabel", foreground=ACCENT, font=("TkDefaultFont", 12, "bold"))
    style.configure(
        "TButton",
        background=SURFACE,
        foreground=TEXT,
        padding=(10, 8),
        bordercolor="#475569",
        lightcolor=SURFACE,
        darkcolor=SURFACE,
        focuscolor=ACCENT,
    )
    style.map(
        "TButton",
        background=[("disabled", SURFACE), ("pressed", "#475569"), ("active", "#334155")],
        foreground=[("disabled", "#94a3b8")],
        bordercolor=[("focus", ACCENT)],
    )
    style.configure(
        "Primary.TButton", background="#0369a1", foreground="white", lightcolor="#0369a1", darkcolor="#0369a1"
    )
    style.map("Primary.TButton", background=[("pressed", "#075985"), ("active", "#0284c7")])
    style.configure(
        "TCheckbutton", background=BACKGROUND, foreground=TEXT, indicatorbackground=SURFACE, indicatorforeground=ACCENT
    )
    style.map(
        "TCheckbutton",
        background=[("active", BACKGROUND)],
        indicatorbackground=[("selected", "#0369a1"), ("active", "#334155")],
    )
    style.configure(
        "TSpinbox",
        fieldbackground=SURFACE,
        background=SURFACE,
        foreground=TEXT,
        insertcolor=TEXT,
        arrowcolor=TEXT,
        bordercolor="#475569",
    )
    style.map("TSpinbox", background=[("active", "#334155")], bordercolor=[("focus", ACCENT)])
    style.configure("Horizontal.TScale", background=SURFACE, troughcolor="#334155", bordercolor=BACKGROUND)
    style.map("Horizontal.TScale", background=[("active", "#475569")])
    style.configure(
        "Vertical.TScrollbar", background=SURFACE, troughcolor=BACKGROUND, arrowcolor=TEXT, bordercolor=BACKGROUND
    )
    style.map("Vertical.TScrollbar", background=[("active", "#475569")])
    style.configure(
        "Treeview",
        background=BACKGROUND,
        fieldbackground=BACKGROUND,
        foreground=TEXT,
        rowheight=32,
        bordercolor=SURFACE,
    )
    style.map("Treeview", background=[("selected", "#075985")], foreground=[("selected", "white")])
    style.configure(
        "Treeview.Heading",
        background=SURFACE,
        foreground=TEXT,
        padding=8,
        font=("TkDefaultFont", 10, "bold"),
        bordercolor="#334155",
    )
    style.map("Treeview.Heading", background=[("active", "#334155")])
