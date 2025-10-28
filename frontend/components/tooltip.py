# -*- coding: utf-8 -*-
"""
Componente de tooltip reutilizable + helper para ícono de ayuda.

Uso típico:
    from frontend.components.tooltip import make_help_icon

    icon = make_help_icon(parent, key="monthly_contrib", lang="es")
    icon.grid(row=..., column=...)

El 'key' debe existir en i18n.get_help(lang, key).
"""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk

# ttkbootstrap es opcional; si está disponible, lo usamos para un look más moderno.
try:
    import ttkbootstrap as tb  # type: ignore
    HAS_TTKB = True
except Exception:
    tb = None
    HAS_TTKB = False

from frontend.i18n import get_help


class HoverTooltip:
    """
    Tooltip básico que aparece al pasar el mouse por encima de un widget.
    """

    def __init__(self, widget: tk.Widget, title: str, text: str, wraplength: int = 320) -> None:
        self.widget = widget
        self.title = title
        self.text = text
        self.wraplength = wraplength
        self.tipwindow: tk.Toplevel | None = None

        self.widget.bind("<Enter>", self._enter, add="+")
        self.widget.bind("<Leave>", self._leave, add="+")
        self.widget.bind("<Motion>", self._move, add="+")

    def _enter(self, _event=None):
        if self.tipwindow:
            return
        self._show_tooltip()

    def _leave(self, _event=None):
        self._hide_tooltip()

    def _move(self, event):
        if self.tipwindow:
            # Posiciona cerca del puntero
            x = event.x_root + 12
            y = event.y_root + 8
            self.tipwindow.geometry(f"+{x}+{y}")

    def _show_tooltip(self):
        if self.tipwindow:
            return
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)  # sin borde/janela nativa
        tw.attributes("-topmost", True)

        # Estilos
        frame = ttk.Frame(tw, padding=(8, 6, 8, 6))
        frame.grid(sticky="nsew")
        tw.grid_columnconfigure(0, weight=1)
        tw.grid_rowconfigure(0, weight=1)

        lbl_title = ttk.Label(frame, text=self.title, font=("Segoe UI", 10, "bold"))
        lbl_text = ttk.Label(frame, text=self.text, wraplength=self.wraplength, justify="left")

        lbl_title.grid(row=0, column=0, sticky="w")
        lbl_text.grid(row=1, column=0, sticky="w", pady=(2, 0))

        # Fondo más amigable si hay ttkbootstrap
        if HAS_TTKB:
            style = ttk.Style()
            # uso de estilo por si queremos fondear distinto
            style.configure("Tooltip.TFrame")
            frame.configure(style="Tooltip.TFrame")

    def _hide_tooltip(self):
        if self.tipwindow:
            self.tipwindow.destroy()
            self.tipwindow = None


def make_help_icon(parent: tk.Widget, key: str, lang: str = "es") -> ttk.Label:
    """
    Crea un pequeño ícono (label) con "?" y engancha el tooltip con el texto i18n.

    parent: contenedor
    key: clave de ayuda (ej. 'monthly_contrib')
    lang: 'es' | 'en' | 'pt'
    """
    title, text = get_help(lang, key)
    if not title and not text:
        title, text = ("", "Sin ayuda disponible.")

    # Usamos una label con borde mínimo para que parezca "chip"
    lbl = ttk.Label(
        parent,
        text="?",
        width=2,
        anchor="center",
        cursor="question_arrow",
        style="HelpChip.TLabel",
    )

    # Estilo base del "chip"; con ttkbootstrap se ve más bonito, pero también funciona sin él
    style = ttk.Style()
    style.configure("HelpChip.TLabel", foreground="#0b5ed7")  # azulito
    style.map("HelpChip.TLabel", foreground=[("active", "#084298")])

    # Tooltip on hover
    HoverTooltip(lbl, title=title, text=text)
    return lbl
