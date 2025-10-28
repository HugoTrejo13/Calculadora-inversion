"""Reusable tooltip widget extracted from the legacy interface."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk

try:
    import ttkbootstrap as tb  # type: ignore

    BOOT = tb
except Exception:  # pragma: no cover
    BOOT = None


class Tooltip:
    """Lightweight tooltip that adapts to ttkbootstrap when available."""

    def __init__(self, widget: tk.Misc, text: str, delay: int = 350) -> None:
        self.widget = widget
        self.text = text
        self.delay = delay
        self._id: str | None = None
        self._tip: tk.Toplevel | None = None

        widget.bind("<Enter>", self._schedule, add="+")
        widget.bind("<Leave>", self._hide, add="+")
        widget.bind("<ButtonPress>", self._hide, add="+")

    def _schedule(self, _event: tk.Event | None = None) -> None:
        if self._id:
            self.widget.after_cancel(self._id)
        self._id = self.widget.after(self.delay, self._show)

    def _show(self) -> None:
        if self._tip or not self.text:
            return

        try:
            bbox = self.widget.bbox("insert")
        except Exception:
            bbox = None

        x_offset = bbox[0] if bbox else 0
        y_offset = bbox[1] if bbox else 0
        x = self.widget.winfo_rootx() + x_offset + 20
        y = self.widget.winfo_rooty() + y_offset + 24

        self._tip = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")

        frame_cls = BOOT.Frame if BOOT else ttk.Frame
        label_cls = BOOT.Label if BOOT else ttk.Label

        frame_kwargs = {"padding": 6, "relief": "solid", "borderwidth": 1}
        label_kwargs = {"text": self.text, "justify": "left", "wraplength": 380}

        if BOOT:
            frame_kwargs["bootstyle"] = "secondary"
            label_kwargs["bootstyle"] = "secondary"

        frm = frame_cls(tw, **frame_kwargs)
        frm.pack()
        label_cls(frm, **label_kwargs).pack()

    def _hide(self, _event: tk.Event | None = None) -> None:
        if self._id:
            self.widget.after_cancel(self._id)
            self._id = None
        if self._tip:
            self._tip.destroy()
            self._tip = None


__all__ = ["Tooltip"]
