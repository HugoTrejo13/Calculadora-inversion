"""Placeholder for the Home screen layout."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk

try:  # Optional ttkbootstrap integration
    import ttkbootstrap as tb  # type: ignore

    FrameBase = tb.Frame
except Exception:  # pragma: no cover - fallback when ttkbootstrap is not available
    FrameBase = ttk.Frame  # type: ignore


class HomeScreen:
    """Home tab wrapper."""

    def __init__(self, parent: tk.Misc) -> None:
        self.frame = FrameBase(parent)
        # TODO: mover hero + botones de navegación aquí
        # TODO: mover mensaje de accesibilidad (hint) aquí

    def get_frame(self) -> tk.Misc:
        return self.frame


__all__ = ["HomeScreen"]
