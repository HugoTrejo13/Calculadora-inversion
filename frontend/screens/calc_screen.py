"""Placeholder for the scientific calculator screen layout."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk

try:
    import ttkbootstrap as tb  # type: ignore

    FrameBase = tb.Frame
except Exception:  # pragma: no cover
    FrameBase = ttk.Frame  # type: ignore


class CalcScreen:
    """Calculator tab wrapper."""

    def __init__(self, parent: tk.Misc) -> None:
        self.frame = FrameBase(parent)
        # TODO: mover display de la calculadora aquí
        # TODO: mover teclado numérico y operadores aquí
        # TODO: mover lógica de evaluación a un controlador reutilizable

    def get_frame(self) -> tk.Misc:
        return self.frame


__all__ = ["CalcScreen"]
