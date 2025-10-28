"""
plan_screen.py
--------------
Pantalla principal del "Plan de inversión":
- Inputs de simulación: monto inicial, aporte mensual, horizonte (años),
  rendimiento %, inflación %, impuestos/comisiones.
- Resumen de resultados (valor final, aportes totales, ganancia generada,
  valor ajustado por inflación).
- Tabla de evolución anual con scroll.

Esta pantalla NO debe crear la ventana root.
Debe recibir un frame `parent` que viene desde App (app_main.py)
 y construir SU layout ahí dentro, en columnas limpias.

Objetivo UX:
- Columna izquierda: parámetros / sliders / impuestos.
- Columna derecha: info educativa y/o FAQ.
- Abajo: resumen y tabla.
"""

"""Placeholder for the investment plan screen layout."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk

try:
    import ttkbootstrap as tb  # type: ignore

    FrameBase = tb.Frame
except Exception:  # pragma: no cover
    FrameBase = ttk.Frame  # type: ignore


class PlanScreen:
    """Plan tab wrapper."""

    def __init__(self, parent: tk.Misc) -> None:
        self.frame = FrameBase(parent)
        # TODO: mover sección "Parámetros de inversión" aquí
        # TODO: mover sección "Perfil / Instrumento" aquí
        # TODO: mover tabla de evolución anual aquí
        # TODO: mover resumen con botón de copiar aquí

    def get_frame(self) -> tk.Misc:
        return self.frame


__all__ = ["PlanScreen"]
