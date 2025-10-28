import tkinter as tk
from tkinter import ttk, messagebox
import ast
import math

from frontend.i18n import get_strings


class CalcScreen(ttk.Frame):
    def __init__(self, parent, base_font_size: int):
        super().__init__(parent, padding=12)
        self.base_font_size = base_font_size
        self.strings = get_strings()
        self._build_ui()

    def _build_ui(self) -> None:
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)

        self._disp = ttk.Entry(
            self,
            font=("TkDefaultFont", self.base_font_size + 2),
            justify="right",
        )
        self._disp.grid(row=0, column=0, sticky="ew", pady=(0, 8))

        rows = [
            ["7", "8", "9", "/"],
            ["4", "5", "6", "*"],
            ["1", "2", "3", "-"],
            ["0", ".", "=", "+"],
            ["(", ")", "^", "\u221a", "C", "CE"],
        ]

        grid = ttk.Frame(self)
        grid.grid(row=1, column=0)

        max_cols = max(len(row) for row in rows)
        for col in range(max_cols):
            grid.columnconfigure(col, weight=1, uniform="calc")

        for r, row in enumerate(rows):
            for c, label in enumerate(row):
                ttk.Button(
                    grid,
                    text=label,
                    width=5,
                    command=lambda t=label: self._put(t),
                ).grid(row=r, column=c, padx=4, pady=4, sticky="nsew")

        self._disp.bind("<Return>", lambda _e: self._on_eval())

    def _put(self, txt: str) -> None:
        if txt == "C":
            self._disp.delete(0, "end")
            return
        if txt == "CE":
            current = self._disp.get()
            if current.endswith("sqrt("):
                self._disp.delete(len(current) - 5, "end")
            elif current:
                self._disp.delete(len(current) - 1, "end")
            return
        if txt == "=":
            self._on_eval()
            return
        if txt == "\u221a":
            self._disp.insert("end", "sqrt(")
            return
        self._disp.insert("end", txt)

    def _on_eval(self) -> None:
        self._safe_eval()

    def _safe_eval(self) -> None:
        expr = self._disp.get().strip().replace("^", "**")
        if not expr:
            return
        allowed = {
            "sqrt": math.sqrt,
            "sin": math.sin,
            "cos": math.cos,
            "tan": math.tan,
            "log": math.log10,
            "log10": math.log10,
            "ln": math.log,
            "pow": math.pow,
            "pi": math.pi,
            "e": math.e,
        }
        try:
            node = ast.parse(expr, mode="eval")
            for n in ast.walk(node):
                if isinstance(n, ast.Call):
                    if not isinstance(n.func, ast.Name) or n.func.id not in allowed:
                        raise ValueError("Expresion no permitida")
                elif isinstance(n, ast.Name):
                    if n.id not in allowed:
                        raise ValueError("Nombre no permitido")
                elif isinstance(
                    n,
                    (
                        ast.Expression,
                        ast.BinOp,
                        ast.UnaryOp,
                        ast.Load,
                        ast.Add,
                        ast.Sub,
                        ast.Mult,
                        ast.Div,
                        ast.Pow,
                        ast.Mod,
                        ast.USub,
                        ast.UAdd,
                        ast.Constant,
                        ast.Num,
                        ast.Tuple,
                    ),
                ):
                    continue
                else:
                    raise ValueError("Expresion no permitida")
            value = eval(compile(node, "<calc>", "eval"), {"__builtins__": None}, allowed)
            self._disp.delete(0, "end")
            self._disp.insert(0, str(value))
        except Exception as exc:
            messagebox.showerror("Error", f"Expresion invalida:\n{exc}")
