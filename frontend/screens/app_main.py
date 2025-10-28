from __future__ import annotations

from typing import Callable

import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont

# --- parche de path para poder importar "frontend" como paquete ---
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]  # sube 2 niveles: screens -> frontend -> raíz del repo
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
# -----------------------------------------------------------------


from frontend.i18n import get_strings
from frontend.screens.calc_screen import CalcScreen
from frontend.screens.debt_screen import DebtScreen
from frontend.screens.plan_screen import PlanScreen
from frontend.screens.calc_screen import InvestmentCalcFrame


try:  # Optional theme enhancement
    import ttkbootstrap as tb
except Exception:  # pragma: no cover - ttkbootstrap is optional
    tb = None


class HomeScreen(ttk.Frame):
    """Pantalla de bienvenida simple con accesos directos básicos."""

    def __init__(
        self,
        parent: tk.Misc,
        strings: dict,
        base_font_size: int,
        on_start_plan: Callable[[], None],
        on_open_calc: Callable[[], None],
    ) -> None:
        super().__init__(parent)
        self.strings = strings
        self.base_font_size = base_font_size
        self._on_start_plan = on_start_plan
        self._on_open_calc = on_open_calc
        self._build_ui()

    def _build_ui(self) -> None:
        wrapper = ttk.Frame(self, padding=20)
        wrapper.pack(expand=True, fill="both")

        self.title_label = ttk.Label(
            wrapper,
            text=self.strings["home_title"],
            font=("TkDefaultFont", self.base_font_size + 6, "bold"),
        )
        self.title_label.pack(pady=(0, 10))

        self.subtitle_label = ttk.Label(
            wrapper,
            text=self.strings["home_sub"],
            wraplength=520,
            justify="left",
        )
        self.subtitle_label.pack(pady=(0, 20))

        buttons = ttk.Frame(wrapper)
        buttons.pack(pady=10)

        self.start_plan_btn = ttk.Button(
            buttons,
            text=self.strings["home_start"],
            command=self._on_start_plan,
        )
        self.start_plan_btn.grid(row=0, column=0, padx=8)

        self.open_calc_btn = ttk.Button(
            buttons,
            text=self.strings["home_calc"],
            command=self._on_open_calc,
        )
        self.open_calc_btn.grid(row=0, column=1, padx=8)

        self.hint_label = ttk.Label(
            wrapper,
            text=self.strings["hint"],
            font=("TkDefaultFont", max(8, self.base_font_size - 2)),
            justify="left",
        )
        self.hint_label.pack(pady=(20, 0))

    def update_base_font(self, base_font_size: int) -> None:
        self.base_font_size = base_font_size
        self.title_label.config(font=("TkDefaultFont", self.base_font_size + 6, "bold"))
        self.hint_label.config(font=("TkDefaultFont", max(8, self.base_font_size - 2)))


class MainApp(tk.Tk):
    """Tk root that wires the modular screens together."""

    def __init__(self) -> None:
        if tb:
            super().__init__()
            self.style = tb.Style("flatly")
        else:
            super().__init__()
            self.style = ttk.Style(self)

        self.strings = get_strings()

        self.title(self.strings["app_title"])
        self.geometry("1200x720")
        self.minsize(980, 600)

        self.base_font_size = tkfont.nametofont("TkDefaultFont").cget("size")
        self.high_contrast = tk.BooleanVar(value=False)

        self._build_topbar()

        self.nb = ttk.Notebook(self)
        self.nb.pack(fill="both", expand=True)

        self.home_tab = ttk.Frame(self.nb)
        self.calc_tab = ttk.Frame(self.nb)
        self.plan_tab = ttk.Frame(self.nb)
        self.debt_tab = ttk.Frame(self.nb)

        self.nb.add(self.home_tab, text=self.strings["tab_home"])
        self.nb.add(self.calc_tab, text=self.strings["tab_calc"])
        self.nb.add(self.plan_tab, text=self.strings["tab_plan"])
        self.nb.add(self.debt_tab, text=self.strings.get("tab_debt", "Deudas"))

        self._build_tab_contents()
        self._apply_font_size()

    # ------------------------------------------------------------------ UI building
    def _build_topbar(self) -> None:
        self.topbar = ttk.Frame(self)
        self.topbar.pack(fill="x", padx=8, pady=6)

        self.lbl_access = ttk.Label(self.topbar, text=self.strings["access"])
        self.lbl_access.pack(side="left", padx=(0, 6))

        self.btn_font_minus = ttk.Button(self.topbar, text=self.strings["font_minus"], command=self._font_minus, width=4)
        self.btn_font_minus.pack(side="left")

        self.btn_font_plus = ttk.Button(self.topbar, text=self.strings["font_plus"], command=self._font_plus, width=4)
        self.btn_font_plus.pack(side="left", padx=(6, 12))

        self.lbl_divider = ttk.Label(self.topbar, text="|")
        self.lbl_divider.pack(side="left", padx=(8, 8))

        self.chk_high_contrast = ttk.Checkbutton(
            self.topbar,
            text=self.strings["daltonic"],
            variable=self.high_contrast,
            command=self._toggle_contrast,
        )
        self.chk_high_contrast.pack(side="left")

    def _build_tab_contents(self) -> None:
        for tab in (self.home_tab, self.calc_tab, self.plan_tab, self.debt_tab):
            for child in tab.winfo_children():
                child.destroy()

        self.home_screen = HomeScreen(
            self.home_tab,
            strings=self.strings,
            base_font_size=self.base_font_size,
            on_start_plan=self._show_plan_tab,
            on_open_calc=self._show_calc_tab,
        )
        self.home_screen.pack(fill="both", expand=True)

        self.calc_screen = CalcScreen(self.calc_tab, base_font_size=self.base_font_size)
        self.calc_screen.pack(fill="both", expand=True)

        self.plan_screen = PlanScreen(self.plan_tab)
        self.plan_screen.pack(fill="both", expand=True)

        self.debt_screen = DebtScreen(
            self.debt_tab,
            base_font_size=self.base_font_size,
        )
        self.debt_screen.pack(fill="both", expand=True)

        self.nb.tab(self.home_tab, text=self.strings["tab_home"])
        self.nb.tab(self.calc_tab, text=self.strings["tab_calc"])
        self.nb.tab(self.plan_tab, text=self.strings["tab_plan"])
        self.nb.tab(self.debt_tab, text=self.strings.get("tab_debt", "Deudas"))

    # ------------------------------------------------------------------ Callbacks
    def _show_plan_tab(self) -> None:
        self.nb.select(self.plan_tab)

    def _show_calc_tab(self) -> None:
        self.nb.select(self.calc_tab)

    def _font_minus(self) -> None:
        self._apply_font_scale(-1)

    def _font_plus(self) -> None:
        self._apply_font_scale(1)

    def _apply_font_scale(self, delta: int) -> None:
        self.base_font_size = max(8, min(22, self.base_font_size + delta))
        for name in ("TkDefaultFont", "TkTextFont", "TkHeadingFont", "TkMenuFont", "TkFixedFont", "TkTooltipFont"):
            try:
                tkfont.nametofont(name).configure(size=self.base_font_size)
            except tk.TclError:
                continue
        self.update_idletasks()
        if hasattr(self, "home_screen"):
            self.home_screen.update_base_font(self.base_font_size)

    def _apply_font_size(self) -> None:
        font_tuple = ("TkDefaultFont", self.base_font_size)
        try:
            self.option_clear()
        except Exception:
            pass
        self.option_add("*Font", font_tuple)

    def _toggle_contrast(self) -> None:
        if tb:
            self.style.theme_use("darkly" if self.high_contrast.get() else "flatly")
            return

        style = ttk.Style()
        if self.high_contrast.get():
            try:
                style.theme_use("clam")
            except tk.TclError:
                pass
            style.configure("TScale", troughcolor="#bcbcbc")
            style.map("TButton", background=[("active", "#e6e6e6")])
        else:
            try:
                style.theme_use("default")
            except tk.TclError:
                pass
            style.configure("TScale", troughcolor="")
            style.map("TButton", background=[])

__all__ = ["MainApp"]


if __name__ == "__main__":
    MainApp().mainloop()

# =========================================================
# DEMO APP para la nueva vista de inversión
# (No rompe tu app actual. Es solo para probar InvestmentCalcFrame
# sin necesidad de cargar toda la app legacy.)
# =========================================================

class MainAppDemo(tk.Tk):
    def __init__(self):
        super().__init__()

        # título ventana
        self.title("Prototype nueva calculadora de inversión")

        # opcional: tamaño inicial decente
        self.geometry("800x700")

        # Montamos el frame nuevo
        self.calc_frame = InvestmentCalcFrame(self, lang="es")
        self.calc_frame.pack(fill="both", expand=True, padx=12, pady=12)


if __name__ == "__main__":
    # Ejecuta solo esta vista demo si corres:
    #   python frontend/screens/app_main.py
    #
    # Esto NO interfiere con tu app original, y nos deja
    # iterar la nueva calculadora pantalla por pantalla.
    demo = MainAppDemo()
    demo.mainloop()
