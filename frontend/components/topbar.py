"""
topbar.py
---------
Componente visual reutilizable para la barra superior:
- botones A- / A+ (cambiar tamaño de fuente)
- checkbox Modo daltonismo
- selector de idioma (ES / EN / PT)
- etiqueta de accesibilidad

Este componente NO debe crear la ventana raíz.
Debe recibir un frame `parent` y las callbacks/variables
que ya existen en App (app_main).
"""

"""Placeholder for the reusable top navigation bar component."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk

try:
    import ttkbootstrap as tb  # type: ignore

    FrameBase = tb.Frame
except Exception:  # pragma: no cover
    FrameBase = ttk.Frame  # type: ignore


class TopBar:
    """Top bar with accessibility and session controls."""

    def __init__(self, parent: tk.Misc) -> None:
        self.frame = FrameBase(parent)
        # TODO: botón A- / A+ para tamaño de letra
        # TODO: toggle de daltonismo / alto contraste
        # TODO: selector de idioma
        # TODO: avatar de usuario / login (usando auth_client más adelante)
        # TODO: aplicar layout horizontal con espaciado consistente y fondo semitransparente tipo glassmorphism

    def get_frame(self) -> tk.Misc:
        return self.frame


__all__ = ["TopBar"]
