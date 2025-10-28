"""Placeholder for the investment evolution table component."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk

try:
    import ttkbootstrap as tb  # type: ignore

    FrameBase = tb.Frame
except Exception:  # pragma: no cover
    FrameBase = ttk.Frame  # type: ignore


class EvolutionTable:
    """Table that will list year-by-year investment results."""

    def __init__(self, parent: tk.Misc) -> None:
        self.frame = FrameBase(parent)
        # TODO: montar Treeview con columnas: Año, Saldo final, Aporte acumulado, Ganancia, Valor real, Comisiones, Impuestos
        # TODO: aplicar estilo zebra rows y header con fondo gris claro
        # TODO: integrar scrollbars vertical/horizontal con estilo consistente
        # TODO: mostrar totales resumidos en un footer opcional

    def get_frame(self) -> tk.Misc:
        return self.frame


__all__ = ["EvolutionTable"]
