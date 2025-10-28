"""
Helpers para configurar el tema base de la interfaz Tk/ttk.
Pensado para centralizar accesibilidad (fuentes, colores, alto contraste)
sin depender todavía de ttkbootstrap.
"""

import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont


def apply_base_theme(root: tk.Misc) -> ttk.Style:
    """
    Configura un estilo ttk base pensado para la app:
    - Selecciona un tema claro por defecto.
    - Ajusta fuentes globales a un tamaño legible (≈ 11-12 pt).
    - Define estilos para botones y etiquetas con padding y colores consistentes.
    """
    style = ttk.Style(root)

    # Intento de usar un tema claro nativo; si falla, ttk elegirá el predeterminado.
    try:
        style.theme_use("clam")
    except tk.TclError:
        pass

    # Ajuste de fuentes base (TkDefaultFont y relacionadas).
    base_size = 12
    for name in (
        "TkDefaultFont",
        "TkTextFont",
        "TkHeadingFont",
        "TkMenuFont",
        "TkFixedFont",
    ):
        try:
            tkfont.nametofont(name).configure(size=base_size)
        except tk.TclError:
            continue

    # Botones con padding amplio y tamaño consistente.
    style.configure(
        "TButton",
        padding=(16, 10),
        relief="flat",
    )
    # TODO: considerar bordes redondeados usando temas ttkbootstrap en el futuro.

    # Etiquetas con color de texto consistente y ancho razonable para wraps.
    style.configure(
        "TLabel",
        foreground="#222222",
        wraplength=560,
    )

    return style


def enable_high_contrast(style: ttk.Style) -> None:
    """
    TODO: aplicar paleta alto contraste (fondos oscuros, texto claro, etc.).
    """
    # TODO: implementar cuando se defina la estrategia de accesibilidad.
    pass


def increase_font_size(style: ttk.Style) -> None:
    """
    TODO: incrementar fuentes globales y actualizar estilos dependientes.
    """
    # TODO: implementar cuando se diseñe la lógica de escalado dinámico.
    pass
