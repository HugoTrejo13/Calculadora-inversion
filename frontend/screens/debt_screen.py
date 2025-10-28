"""Placeholder for the debt simulator screen layout."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk

try:
    import ttkbootstrap as tb  # type: ignore

    FrameBase = tb.Frame
except Exception:  # pragma: no cover
    FrameBase = ttk.Frame  # type: ignore


class DebtScreen:
    """Debt tab wrapper."""

    def __init__(self, parent: tk.Misc) -> None:
        self.frame = FrameBase(parent)
        # TODO: mover formulario de parámetros del crédito aquí
        # TODO: mover tabla de amortización aquí
        # TODO: mover panel de resumen y botón de cálculo aquí

    def get_frame(self) -> tk.Misc:
        return self.frame


__all__ = ["DebtScreen"]
