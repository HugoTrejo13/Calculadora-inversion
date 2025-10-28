"""
summary_card.py
---------------
Componente visual reutilizable para mostrar KPIs financieros:
- Valor final (nominal)
- Aportes totales
- Ganancia generada
- Valor ajustado por inflación

Debe renderizarse como una tarjeta / frame con borde suave,
márgenes consistentes y tipografía clara.
NO debe recalcular la inversión por sí solo;
debe recibir los números ya calculados desde la pantalla (plan_screen).
"""

"""Placeholder for the KPI summary card component."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk

try:
    import ttkbootstrap as tb  # type: ignore

    FrameBase = tb.Frame
    LabelBase = tb.Label
except Exception:  # pragma: no cover
    FrameBase = ttk.Frame  # type: ignore
    LabelBase = ttk.Label  # type: ignore


class SummaryCard:
    """Small card with a headline metric."""

    def __init__(self, parent: tk.Misc, title: str, value: str, subtitle: str | None = None, icon: tk.PhotoImage | None = None) -> None:
        self.frame = FrameBase(parent)
        self.title = title
        self.value = value
        self.subtitle = subtitle
        self.icon = icon

        # TODO: aplicar estilo tarjeta con padding, borde redondeado, sombra suave (estética fintech)
        # TODO: mostrar icono + título + valor grande
        # TODO: utilizar tipografía secundaria para el subtitle y colores accesibles

    def get_frame(self) -> tk.Misc:
        return self.frame


__all__ = ["SummaryCard"]
