"""Tkinter/Ttkbootstrap application entry point with modular structure."""

from __future__ import annotations

import json
from pathlib import Path
import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont

from frontend.i18n import LANGUAGES

try:  # Optional ttkbootstrap support
    import ttkbootstrap as tb  # type: ignore

    BOOT = tb
except Exception:  # pragma: no cover - fallback when ttkbootstrap is missing
    BOOT = None

ASSETS_DIR = Path(__file__).resolve().parent / "assets"
STYLE_DIR = ASSETS_DIR / "style"


BaseWindow = BOOT.Window if BOOT else tk.Tk


"""
App (root Tkinter shell)
------------------------
Esta clase es la ventana principal (root) de la app.
Responsabilidades:
- crea la ventana raíz de Tkinter
- monta la barra superior / topbar
- crea el Notebook de pestañas (Inicio, Plan, Calculadora, Deuda)
- aplica idioma, accesibilidad, tema visual
- cada pestaña se llena con pantallas definidas en frontend/screens/*.py

IMPORTANTE:
Ya no construimos toda la UI en un solo archivo gigante.
Cada pantalla/tab tiene su propio módulo en frontend/screens
y cada bloque visual reutilizable vive en frontend/components.
"""


class App(BaseWindow):
    """Application root. Handles theme, locale and main notebook."""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._init_state()
        self._configure_theme()
        self._configure_typography()
        self._build_layout()

    # ------------------------------------------------------------------ #
    # Configuration helpers
    # ------------------------------------------------------------------ #
    def _init_state(self) -> None:
        self.lang = "es"
        self.strings = LANGUAGES.get(self.lang, next(iter(LANGUAGES.values())))

        self.title(self.strings.get("app_title", "Calculadora"))
        self.geometry("1200x720")
        self.minsize(980, 600)

        default_font = tkfont.nametofont("TkDefaultFont")
        self.base_font_size = default_font.cget("size")
        self.font_scale = tk.IntVar(value=0)
        self.daltonic_mode = tk.BooleanVar(value=False)

    def _configure_theme(self) -> None:
        theme_name = self._load_theme_name()
        if BOOT:
            self.style = BOOT.Style(theme_name)
        else:
            self.style = ttk.Style(self)

    def _configure_typography(self) -> None:
        typo_path = STYLE_DIR / "typography.json"
        if not typo_path.exists():
            return
        try:
            with open(typo_path, "r", encoding="utf-8") as fh:
                data = json.load(fh)
        except Exception:
            return

        base_size = data.get("base_font_size")
        if isinstance(base_size, int):
            self.base_font_size = base_size
            self._apply_font_size()

    def _load_theme_name(self) -> str:
        theme_path = STYLE_DIR / "theme.json"
        if not (BOOT and theme_path.exists()):
            return "flatly"
        try:
            with open(theme_path, "r", encoding="utf-8") as fh:
                payload = json.load(fh)
        except Exception:
            return "flatly"
        return payload.get("theme_name", "flatly")

    def _apply_font_size(self) -> None:
        target_size = self.base_font_size + self.font_scale.get()
        target_size = max(8, min(22, target_size))
        for family in ("TkDefaultFont", "TkTextFont", "TkHeadingFont", "TkMenuFont", "TkFixedFont"):
            try:
                tkfont.nametofont(family).configure(size=target_size)
            except tk.TclError:
                continue

    # ------------------------------------------------------------------ #
    # Layout builders
    # ------------------------------------------------------------------ #
    def _build_layout(self) -> None:
        container = ttk.Frame(self)
        container.pack(fill="both", expand=True)

        self._build_topbar(container)
        self._build_notebook(container)

    def _build_topbar(self, parent: ttk.Frame) -> None:
        """Create accessibility/lang controls."""
        # TODO: mover implementación real a components/topbar.py
        pass

    def _build_notebook(self, parent: ttk.Frame) -> None:
        self.notebook = ttk.Notebook(parent)
        self.notebook.pack(fill="both", expand=True)

        self.home_tab = ttk.Frame(self.notebook)
        self.plan_tab = ttk.Frame(self.notebook)
        self.calc_tab = ttk.Frame(self.notebook)
        self.debt_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.home_tab, text=self.strings.get("tab_home", "Home"))
        self.notebook.add(self.plan_tab, text=self.strings.get("tab_plan", "Plan"))
        self.notebook.add(self.calc_tab, text=self.strings.get("tab_calc", "Calc"))
        self.notebook.add(self.debt_tab, text=self.strings.get("tab_debt", "Debt"))

        self._build_home_tab(self.home_tab)
        self._build_plan_tab(self.plan_tab)
        self._build_calc_tab(self.calc_tab)
        self._build_debt_tab(self.debt_tab)

    def _build_home_tab(self, parent: ttk.Frame) -> None:
        # TODO: mover implementación real a screens/home_screen.py
        pass

    def _build_plan_tab(self, parent: ttk.Frame) -> None:
        # TODO: mover implementación real a screens/plan_screen.py
        pass

    def _build_calc_tab(self, parent: ttk.Frame) -> None:
        # TODO: mover implementación real a screens/calc_screen.py
        pass

    def _build_debt_tab(self, parent: ttk.Frame) -> None:
        # TODO: mover implementación real a screens/debt_screen.py
        pass


__all__ = ["App"]
