# -*- coding: utf-8 -*-

"""

AplicaciÃ³n educativa de cÃ¡lculo e inversiÃ³n con enfoque inclusivo.

Incluye calculadora cientÃ­fica con fondo personalizable y simulador de inversiÃ³n

con controles de accesibilidad (tamaÃ±o de fuente, modo daltonismo e idiomas).

Requisitos:

    pip install pillow

"""

from __future__ import annotations

import math
import os
from dataclasses import dataclass
from typing import Callable, Dict, Optional, Tuple
import tkinter as tk
import tkinter.font as tkfont
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk

LANGUAGE_ORDER = ("es", "en", "pt")
LANGUAGES: Dict[str, Dict[str, str]] = {

    "es": {

        "language_name": "EspaÃ±ol",

        "app_title": "Calculadora Financiera Inclusiva",

        "tab_calculator": "Calculadora",

        "tab_investment": "Plan de inversiÃ³n",

        "accessibility": "Accesibilidad:",

        "font_down": "A-",

        "font_up": "A+",

        "color_mode": "Modo daltonismo",

        "language_label": "Idioma:",

        "calc_hint_idle": "Tip: Usa los botones cientÃ­ficos (sin, log, sqrt) o escribe tu propia expresiÃ³n.",

        "calc_hint_active": "ExpresiÃ³n actual: {expression}",

        "calc_hint_result": "Resultado: {result}. Usa Ans para reutilizarlo o prueba nuevas funciones.",

        "calc_error": "ExpresiÃ³n invÃ¡lida",

        "calc_error_message": "Revisa la expresiÃ³n; cierra parÃ©ntesis y usa operadores vÃ¡lidos.",

        "investment_parameters": "ParÃ¡metros de inversiÃ³n",

        "investment_summary": "Resumen",

        "investment_evolution": "EvoluciÃ³n anual",

        "investment_initial": "Monto inicial (MX$)",

        "investment_monthly": "Aporte mensual (MX$)",

        "investment_years": "Horizonte (aÃ±os)",

        "investment_return": "Rendimiento anual (%)",

        "investment_inflation": "InflaciÃ³n anual (%)",

        "investment_copy_summary": "Copiar resumen",

        "summary_final_value": "Valor final (nominal)",

        "summary_contributions": "Aportes totales",

        "summary_gain": "Ganancia generada",

        "summary_real": "Valor ajustado por inflaciÃ³n",

        "table_year": "AÃ±os a invertir",

        "table_balance": "Saldo total final",

        "table_contrib": "Aporte acumulado",

        "table_gain": "Ganancia",

        "table_real": "Valor real",

        "investment_lesson": "DespuÃ©s de {years} aÃ±os, tu ahorro podrÃ­a valer {final}. Invertir con constancia genera {gain} sobre los aportes realizados. Con la inflaciÃ³n estimada, el poder de compra equivaldrÃ­a a {real}. Usa la tabla para mostrar a la familia cÃ³mo crece el dinero con paciencia.",

        "investment_need_monthly": "Ingresa un aporte mensual mayor a 0 y hasta 50,000 MXN.",

        "investment_need_monthly_plain": "Se necesita un aporte mensual positivo para proyectar la inversiÃ³n.",

        "investment_warning_title": "Dato requerido",

        "investment_limit_note": "Nota: El aporte mensual se limitÃ³ a MX$ 50,000.",

        "copy_summary_title": "Resumen copiado",

        "copy_summary_message": "Datos copiados al portapapeles.",

        "investment_summary_template": "Monto inicial: {initial} MX$\nAporte mensual: {monthly} MX$\nAÃ±os: {years}\nRendimiento anual: {rate:.1f} %\nInflaciÃ³n anual: {inflation:.1f} %\n\nValor final: {final}\nAportes totales: {contrib}\nGanancia generada: {gain}\nValor ajustado por inflaciÃ³n: {real}",

        "help_initial_technical": "Capital aportado al inicio de la inversiÃ³n.",

        "help_initial_plain": "Dinero que colocas solo una vez al comenzar.",

        "help_monthly_technical": "DepÃ³sitos periÃ³dicos que alimentan la inversiÃ³n.",

        "help_monthly_plain": "Lo que ahorrarÃ¡s cada mes.",

        "help_years_technical": "Cantidad de aÃ±os que permanecerÃ¡ invertido el capital.",

        "help_years_plain": "Tiempo que dejarÃ¡s crecer tu dinero.",

        "help_return_technical": "Rentabilidad anual esperada en porcentaje.",

        "help_return_plain": "Rendimiento promedio que esperas cada aÃ±o.",

        "help_inflation_technical": "VariaciÃ³n anual de precios que reduce el poder de compra.",

        "help_inflation_plain": "CuÃ¡nto suben los precios cada aÃ±o.",

        "help_final_technical": "Saldo con interÃ©s compuesto.",

        "help_final_plain": "Dinero que podrÃ­as tener al final.",

        "help_contrib_technical": "Suma de todos los depÃ³sitos realizados.",

        "help_contrib_plain": "Todo lo que habrÃ¡s aportado.",

        "help_gain_technical": "Ganancia tras restar aportes al saldo final.",

        "help_gain_plain": "Lo que el dinero ganÃ³ gracias al interÃ©s.",

        "help_real_technical": "Saldo final ajustado por inflaciÃ³n.",

        "help_real_plain": "Poder de compra equivalente en el futuro.",

    },

    "en": {

        "language_name": "English",

        "app_title": "Inclusive Financial Calculator",

        "tab_calculator": "Calculator",

        "tab_investment": "Investment plan",

        "accessibility": "Accessibility:",

        "font_down": "A-",

        "font_up": "A+",

        "color_mode": "Color-blind mode",

        "language_label": "Language:",

        "calc_hint_idle": "Tip: Use scientific buttons (sin, log, sqrt) or type your own expression.",

        "calc_hint_active": "Current expression: {expression}",

        "calc_hint_result": "Result: {result}. Use Ans to reuse it or explore new functions.",

        "calc_error": "Invalid expression",

        "calc_error_message": "Check the expression; close parentheses and use valid operators.",

        "investment_parameters": "Investment parameters",

        "investment_summary": "Summary",

        "investment_evolution": "Year-by-year evolution",

        "investment_initial": "Initial amount (MX$)",

        "investment_monthly": "Monthly deposit (MX$)",

        "investment_years": "Investment horizon (years)",

        "investment_return": "Annual return (%)",

        "investment_inflation": "Annual inflation (%)",

        "investment_copy_summary": "Copy summary",

        "summary_final_value": "Final value (nominal)",

        "summary_contributions": "Total contributions",

        "summary_gain": "Generated gain",

        "summary_real": "Value adjusted for inflation",

        "table_year": "Years to invest",

        "table_balance": "Final total balance",

        "table_contrib": "Accumulated deposit",

        "table_gain": "Gain",

        "table_real": "Real value",

        "investment_lesson": "After {years} years your savings could reach {final}. Consistent investing generates {gain} over the contributed money. With estimated inflation, the purchasing power would be {real}. Use the table to explain how patience grows money for the family.",

        "investment_need_monthly": "Enter a monthly deposit greater than 0 and up to 50,000 MXN.",

        "investment_need_monthly_plain": "A positive monthly deposit is required to project the investment.",

        "investment_warning_title": "Missing data",

        "investment_limit_note": "Note: Monthly deposit was limited to MX$ 50,000.",

        "copy_summary_title": "Summary copied",

        "copy_summary_message": "Data copied to the clipboard.",

        "investment_summary_template": "Initial amount: {initial} MX$\nMonthly deposit: {monthly} MX$\nYears: {years}\nAnnual return: {rate:.1f} %\nAnnual inflation: {inflation:.1f} %\n\nFinal value: {final}\nTotal contributions: {contrib}\nGenerated gain: {gain}\nInflation-adjusted value: {real}",

        "help_initial_technical": "Capital contributed at the start of the investment.",

        "help_initial_plain": "Money you put in only once at the beginning.",

        "help_monthly_technical": "Recurring deposits feeding the investment.",

        "help_monthly_plain": "What you plan to save each month.",

        "help_years_technical": "Number of years the capital remains invested.",

        "help_years_plain": "Total time you let the money grow.",

        "help_return_technical": "Expected yearly profitability (percentage).",

        "help_return_plain": "Average return you expect each year.",

        "help_inflation_technical": "Yearly price variation eroding purchasing power.",

        "help_inflation_plain": "How much prices rise per year.",

        "help_final_technical": "Balance including compound interest.",

        "help_final_plain": "Money you might have at the end.",

        "help_contrib_technical": "Sum of all contributions made.",

        "help_contrib_plain": "Everything you deposit along the way.",

        "help_gain_technical": "Gain after subtracting contributions from the final balance.",

        "help_gain_plain": "What your money earned thanks to the return.",

        "help_real_technical": "Final balance adjusted for inflation.",

        "help_real_plain": "What that money would buy in the future.",

    },

    "pt": {

        "language_name": "PortuguÃªs",

        "app_title": "Calculadora Financeira Inclusiva",

        "tab_calculator": "Calculadora",

        "tab_investment": "Plano de investimento",

        "accessibility": "Acessibilidade:",

        "font_down": "A-",

        "font_up": "A+",

        "color_mode": "Modo daltÃ´nico",

        "language_label": "Idioma:",

        "calc_hint_idle": "Dica: Use os botÃµes cientÃ­ficos (sin, log, sqrt) ou digite sua prÃ³pria expressÃ£o.",

        "calc_hint_active": "ExpressÃ£o atual: {expression}",

        "calc_hint_result": "Resultado: {result}. Use Ans para reutilizÃ¡-lo ou testar novas funÃ§Ãµes.",

        "calc_error": "ExpressÃ£o invÃ¡lida",

        "calc_error_message": "Verifique a expressÃ£o; feche parÃªnteses e use operadores vÃ¡lidos.",

        "investment_parameters": "ParÃ¢metros do investimento",

        "investment_summary": "Resumo",

        "investment_evolution": "EvoluÃ§Ã£o anual",

        "investment_initial": "Montante inicial (MX$)",

        "investment_monthly": "Aporte mensal (MX$)",

        "investment_years": "Horizonte (anos)",

        "investment_return": "Retorno anual (%)",

        "investment_inflation": "InflaÃ§Ã£o anual (%)",

        "investment_copy_summary": "Copiar resumo",

        "summary_final_value": "Valor final (nominal)",

        "summary_contributions": "Aportes totais",

        "summary_gain": "Ganho gerado",

        "summary_real": "Valor ajustado pela inflaÃ§Ã£o",

        "table_year": "Anos para investir",

        "table_balance": "Saldo total final",

        "table_contrib": "Aporte acumulado",

        "table_gain": "Ganho",

        "table_real": "Valor real",

        "investment_lesson": "ApÃ³s {years} anos, sua poupanÃ§a pode chegar a {final}. Investir com constÃ¢ncia gera {gain} sobre os aportes. Com a inflaÃ§Ã£o estimada, o poder de compra seria {real}. Use a tabela para mostrar Ã  famÃ­lia como a paciÃªncia faz o dinheiro crescer.",

        "investment_need_monthly": "Informe um aporte mensal maior que 0 e atÃ© 50.000 MXN.",

        "investment_need_monthly_plain": "Ã necessÃ¡rio um aporte mensal positivo para projetar o investimento.",

        "investment_warning_title": "Dado necessÃ¡rio",

        "investment_limit_note": "Nota: O aporte mensal foi limitado a MX$ 50.000.",

        "copy_summary_title": "Resumo copiado",

        "copy_summary_message": "Dados copiados para a Ã¡rea de transferÃªncia.",

        "investment_summary_template": "Montante inicial: {initial} MX$\nAporte mensal: {monthly} MX$\nAnos: {years}\nRetorno anual: {rate:.1f} %\nInflaÃ§Ã£o anual: {inflation:.1f} %\n\nValor final: {final}\nAportes totais: {contrib}\nGanho gerado: {gain}\nValor ajustado pela inflaÃ§Ã£o: {real}",

        "help_initial_technical": "Capital aplicado no inÃ­cio.",

        "help_initial_plain": "Dinheiro que vocÃª investe apenas ao comeÃ§ar.",

        "help_monthly_technical": "DepÃ³sitos recorrentes do investimento.",

        "help_monthly_plain": "Quanto vocÃª guarda por mÃªs.",

        "help_years_technical": "Quantidade de anos aplicados.",

        "help_years_plain": "Tempo total deixando o dinheiro render.",

        "help_return_technical": "Rentabilidade anual esperada em porcentagem.",

        "help_return_plain": "Retorno mÃ©dio esperado a cada ano.",

        "help_inflation_technical": "VariaÃ§Ã£o anual dos preÃ§os.",

        "help_inflation_plain": "Quanto os preÃ§os sobem por ano.",

        "help_final_technical": "Saldo final com juros compostos.",

        "help_final_plain": "Dinheiro que vocÃª terÃ¡ ao final.",

        "help_contrib_technical": "Soma de todos os aportes.",

        "help_contrib_plain": "Tudo o que depositou.",

        "help_gain_technical": "Ganho apÃ³s subtrair aportes.",

        "help_gain_plain": "Quanto o dinheiro rendeu.",

        "help_real_technical": "Saldo ajustado pela inflaÃ§Ã£o.",

        "help_real_plain": "Poder de compra equivalente no futuro.",

    },

}

SAFE_GLOBALS: Dict[str, object] = {"__builtins__": {}}

SAFE_LOCALS: Dict[str, object] = {name: getattr(math, name) for name in dir(math) if not name.startswith("_")}

SAFE_LOCALS.update({"abs": abs, "round": round, "pi": math.pi, "e": math.e})

def translate(lang: str, key: str, **kwargs: object) -> str:

    fallback = LANGUAGES["es"]

    template = LANGUAGES.get(lang, fallback).get(key, fallback.get(key, key))

    try:

        return template.format(**kwargs)

    except Exception:

        return template

def format_currency(value: float) -> str:

    return f"MX$ {value:,.2f}"

def setup_styles(root: tk.Tk, base_size: int = 11, colorblind: bool = False) -> None:

    style = ttk.Style(root)

    try:

        style.theme_use("clam")

    except tk.TclError:

        pass

    palette = {

        "base_bg": "#f1f5f9" if colorblind else "#ffffff",

        "base_fg": "#0f172a" if colorblind else "#1f2937",

        "primary_bg": "#006d77" if colorblind else "#2563eb",

        "primary_fg": "white",

        "accent_bg": "#ff6b6b" if colorblind else "#7c3aed",

        "grey_bg": "#1f2937" if colorblind else "#334155",

    }

    root._app_palette = palette  # type: ignore[attr-defined]

    btn_font = ("Segoe UI", base_size, "bold")

    accent_font = ("Segoe UI", base_size + 1, "bold")

    style.configure("Calc.TButton", padding=12, font=btn_font, relief="flat", background=palette["primary_bg"], foreground=palette["primary_fg"], borderwidth=0)

    style.map("Calc.TButton", background=[("active", palette["accent_bg"]), ("disabled", "#cbd5f5")])

    style.configure("Accent.TButton", padding=14, font=accent_font, relief="flat", background=palette["accent_bg"], foreground="white", borderwidth=0)

    style.map("Accent.TButton", background=[("active", palette["primary_bg"])])

    style.configure("Grey.TButton", padding=10, font=btn_font, relief="flat", background=palette["grey_bg"], foreground="white", borderwidth=0)

    style.map("Grey.TButton", background=[("active", palette["accent_bg"])])

    style.configure("Info.TLabel", background=palette["base_bg"], foreground=palette["base_fg"])

    style.configure("Card.TFrame", background=palette["base_bg"])

    style.configure("HelpIcon.TLabel", background=palette["base_bg"], foreground=palette["accent_bg"], font=("Segoe UI", base_size, "bold"))

    style.configure("Invest.TLabel", background=palette["base_bg"], foreground=palette["base_fg"], font=("Segoe UI Semibold", base_size))

    style.configure("InvestValue.TLabel", background=palette["base_bg"], foreground=palette["accent_bg"], font=("Segoe UI", base_size, "bold"))

    style.configure("Invest.TFrame", background=palette["base_bg"])

    style.configure("Invest.TEntry", fieldbackground=palette["base_bg"], foreground=palette["base_fg"])

    style.configure("TNotebook", background=palette["base_bg"])

    style.configure("TNotebook.Tab", font=("Segoe UI", base_size, "bold"))

    style.map("TNotebook.Tab", background=[("selected", palette["primary_bg"]), ("!selected", palette["base_bg"])], foreground=[("selected", palette["primary_fg"]), ("!selected", palette["base_fg"])])

    style.configure("Card.Treeview", font=("Consolas", max(10, base_size - 1)), background=palette["base_bg"], fieldbackground=palette["base_bg"], foreground=palette["base_fg"])

    style.configure("Card.Treeview.Heading", font=("Segoe UI", base_size, "bold"))

    root.configure(background=palette["base_bg"])

    root.option_add("*Font", f"{{Segoe UI}} {base_size}")

    root.option_add("*Label.background", palette["base_bg"])

    root.option_add("*Label.foreground", palette["base_fg"])

    root.option_add("*Frame.background", palette["base_bg"])

class Tooltip:
    def __init__(self, widget: tk.Widget, text: str, wrap: int = 260) -> None:
        self.widget = widget
        self.text = text
        self.wrap = wrap
        self.tip: Optional[tk.Toplevel] = None
        widget.bind("<Enter>", self._on_enter)
        widget.bind("<Leave>", self._on_leave)
        widget.bind("<FocusOut>", self._on_leave)

    def update(self, text: str) -> None:
        self.text = text

    def _on_enter(self, _event: tk.Event) -> None:
        if self.tip or not self.text:
            return
        x = self.widget.winfo_rootx() + 16
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 8
        self.tip = tk.Toplevel(self.widget)
        self.tip.wm_overrideredirect(True)
        self.tip.wm_geometry(f"+{x}+{y}")
        tk.Label(
            self.tip,
            text=self.text,
            wraplength=self.wrap,
            justify="left",
            background="#111827",
            foreground="#f8fafc",
            relief="solid",
            borderwidth=1,
            padx=8,
            pady=6,
        ).pack()

    def _on_leave(self, _event: tk.Event) -> None:
        if self.tip is not None:
            self.tip.destroy()
            self.tip = None

class CalculatorFrame(ttk.Frame):

    def __init__(self, master: tk.Widget, language_var: tk.StringVar, bg_path: Optional[str] = None, fallback_bg: str = "#f3f4f6") -> None:

        super().__init__(master, padding=12, style="Card.TFrame")

        self.language_var = language_var

        self.expression = tk.StringVar(value="")

        self.bg_path = bg_path

        self.fallback_bg = fallback_bg

        self.bg_image: Optional[Image.Image] = None

        self.bg_label: Optional[tk.Label] = None

        self.hint = tk.StringVar(value="")

        self.last_result = "0"

        self._build_ui()

        self.expression.trace_add("write", lambda *_: self._update_hint())

        self.update_language()

    def _build_ui(self) -> None:

        self.grid_columnconfigure(0, weight=1)

        self.grid_rowconfigure(1, weight=1)

        canvas = tk.Frame(self)

        canvas.grid(row=0, column=0, sticky="nsew")

        canvas.grid_columnconfigure(0, weight=1)

        self.bg_label = tk.Label(canvas, bd=0)

        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        if self.bg_path and os.path.exists(self.bg_path):

            try:

                self.bg_image = Image.open(self.bg_path).convert("RGBA")

            except Exception as exc:

                messagebox.showwarning("Fondo", f"No se pudo abrir la imagen.\n{exc}")

        canvas.bind("<Configure>", lambda _event: self.refresh_palette())

        entry = tk.Entry(

            canvas,

            textvariable=self.expression,

            font=tkfont.Font(family="Segoe UI", size=20),

            justify="right",

            bd=1,

            relief="solid",

        )

        entry.grid(row=0, column=0, sticky="nsew", ipady=12, pady=(0, 12))

        buttons = ttk.Frame(self, style="Card.TFrame")

        buttons.grid(row=1, column=0, sticky="nsew")

        for col in range(4):

            buttons.grid_columnconfigure(col, weight=1)

        layout = [

            ("(", 0, 0), (")", 0, 1), ("DEL", 0, 2), ("C", 0, 3),

            ("7", 1, 0), ("8", 1, 1), ("9", 1, 2), ("/", 1, 3),

            ("4", 2, 0), ("5", 2, 1), ("6", 2, 2), ("*", 2, 3),

            ("1", 3, 0), ("2", 3, 1), ("3", 3, 2), ("-", 3, 3),

            ("0", 4, 0), (".", 4, 1), ("^", 4, 2), ("+", 4, 3),

            ("sqrt", 5, 0), ("x^2", 5, 1), ("sin", 5, 2), ("cos", 5, 3),

            ("tan", 6, 0), ("log", 6, 1), ("ln", 6, 2), ("pi", 6, 3),

        ]

        for text, row, col in layout:

            style = "Grey.TButton" if text in {"DEL", "C"} else "Calc.TButton"

            ttk.Button(buttons, text=text, style=style, command=lambda value=text: self._on_press(value)).grid(row=row, column=col, padx=4, pady=4, sticky="nsew")

        ttk.Button(buttons, text="Ans", style="Calc.TButton", command=lambda: self._on_press("Ans")).grid(row=7, column=0, padx=4, pady=4, sticky="nsew")

        ttk.Button(buttons, text="=", style="Accent.TButton", command=lambda: self._on_press("=")).grid(row=7, column=1, columnspan=3, padx=4, pady=4, sticky="nsew")

        ttk.Label(self, textvariable=self.hint, style="Info.TLabel", wraplength=560).grid(row=2, column=0, sticky="we", pady=(8, 0))

    def refresh_palette(self) -> None:

        if not self.bg_label:

            return

        if not self.bg_image:

            palette = getattr(self.master.winfo_toplevel(), "_app_palette", {})

            self.bg_label.configure(bg=palette.get("base_bg", self.fallback_bg), image="")

            return

        width = max(1, self.bg_label.winfo_width())

        height = max(1, self.bg_label.winfo_height())

        scaled = self.bg_image.resize((width, height), Image.LANCZOS)

        photo = ImageTk.PhotoImage(scaled)

        self.bg_label.configure(image=photo)

        self.bg_label.image = photo

    def _on_press(self, value: str) -> None:

        if value == "C":

            self.expression.set("")

            return

        if value == "DEL":

            self.expression.set(self.expression.get()[:-1])

            return

        if value == "Ans":

            self.expression.set(self.expression.get() + self.last_result)

            return

        if value == "=":

            expression = self.expression.get().replace("^", "**")

            if not expression.strip():

                return

            try:

                result = eval(expression, SAFE_GLOBALS, SAFE_LOCALS)

            except Exception:

                lang = self.language_var.get()

                messagebox.showerror(translate(lang, "calc_error"), translate(lang, "calc_error_message"))

                return

            self.last_result = str(result)

            self.expression.set(self.last_result)

            self.hint.set(translate(self.language_var.get(), "calc_hint_result", result=result))

            return

        mapping = {"sqrt": "sqrt(", "x^2": "**2", "sin": "sin(", "cos": "cos(", "tan": "tan(", "log": "log10(", "ln": "log(", "pi": "pi", "^": "**"}

        self.expression.set(self.expression.get() + mapping.get(value, value))

    def _update_hint(self) -> None:

        text = self.expression.get()

        if text:

            self.hint.set(translate(self.language_var.get(), "calc_hint_active", expression=text))

        else:

            self.hint.set(translate(self.language_var.get(), "calc_hint_idle"))

    def update_language(self) -> None:

        self._update_hint()

@dataclass

class HelpConfig:

    label: ttk.Label

    tooltip: Tooltip

class InvestmentFrame(ttk.Frame):

    def __init__(self, master: tk.Widget, language_var: tk.StringVar) -> None:

        super().__init__(master, padding=18, style="Card.TFrame")

        self.language_var = language_var

        self.initial = tk.StringVar(value="1000")

        self.monthly = tk.StringVar(value="200")

        self.years = tk.StringVar(value="5")

        self.rate = tk.DoubleVar(value=10.0)

        self.inflation = tk.DoubleVar(value=4.0)

        self.frequency = tk.StringVar(value="Mensuall")

        self.capitalization = tk.StringVar(value="Mensuall")

        self.deposit_fee_value = tk.StringVar(value="0")

        self.deposit_fee_mode = tk.StringVar(value="%")

        self.admin_fee = tk.StringVar(value="0.0")

        self.sell_fee = tk.StringVar(value="0.0")

        self.withholding = tk.StringVar(value="0.50")

        self.uma_value = tk.StringVar(value="")

        self.uma_multiplier = tk.StringVar(value="5")

        self.isr_sale = tk.StringVar(value="10.0")

        self.isr_dividend = tk.StringVar(value="10.0")

        self.dividend_rate = tk.StringVar(value="0.0")

        self.instrument_type = tk.StringVar(value="Ahorro/Bonos")

        self.goal_amount = tk.StringVar(value="")

        self.final_value = tk.StringVar(value="MX$ 0.00")

        self.contribution = tk.StringVar(value="MX$ 0.00")

        self.gain = tk.StringVar(value="MX$ 0.00")

        self.real_value = tk.StringVar(value="MX$ 0.00")

        self.lesson = tk.StringVar(value="")

        self._warning_shown = False

        self.help_items: Dict[str, HelpConfig] = {}

        self._value_labels: Dict[str, Tuple[ttk.Label, tk.Variable, str]] = {}

        self._build_ui()

        self._bind_updates()

        self.update_language()

        self.update_projection()

    def _build_header(self, parent: tk.Widget, key: str) -> ttk.Frame:

        container = ttk.Frame(parent)

        container.pack(fill="x", pady=(0, 8))

        label = ttk.Label(container, text="", style="Info.TLabel", font=("Segoe UI", 12, "bold"))

        label.pack(side="left")

        self.help_items[f"section_{key}"] = HelpConfig(label, Tooltip(label, ""))

        return container

    def _add_entry_row(

        self,

        parent: ttk.Frame,

        row: int,

        text_key: str,

        variable: tk.Variable,

        help_key: Optional[str] = None,

        factory: Optional[Callable[[tk.Widget], tk.Widget]] = None,

    ) -> None:

        row_frame = ttk.Frame(parent, style="Invest.TFrame", padding=(0, 4))

        row_frame.grid(row=row, column=0, sticky="ew", pady=6)

        row_frame.columnconfigure(2, weight=1)

        label = ttk.Label(row_frame, text="", style="Invest.TLabel")

        label.grid(row=0, column=0, sticky="w", padx=(0, 8))

        icon = ttk.Label(row_frame, text="?", style="HelpIcon.TLabel")

        icon.grid(row=0, column=1, sticky="w", padx=(0, 12))

        if factory:

            widget = factory(row_frame)

        else:

            widget = ttk.Entry(row_frame, textvariable=variable, width=16, justify="right", style="Invest.TEntry")

            widget.configure(validate="key", validatecommand=(self.register(self._validate_amount), "%P"))

        widget.grid(row=0, column=2, sticky="ew")

        tooltip = Tooltip(icon, "")

        self.help_items[text_key] = HelpConfig(label, tooltip)

        if help_key:

            self.help_items[help_key] = HelpConfig(icon, tooltip)

        setattr(self, f"{text_key}_widget", widget)

    def _add_scale_row(

        self,

        parent: ttk.Frame,

        row: int,

        text_key: str,

        variable: tk.DoubleVar,

        from_: float,

        to: float,

        step: float,

        help_key: Optional[str] = None,

    ) -> None:

        row_frame = ttk.Frame(parent, style="Invest.TFrame", padding=(0, 4))

        row_frame.grid(row=row, column=0, sticky="ew", pady=6)

        row_frame.columnconfigure(3, weight=1)

        label = ttk.Label(row_frame, text="", style="Invest.TLabel")

        label.grid(row=0, column=0, sticky="w", padx=(0, 8))

        icon = ttk.Label(row_frame, text="?", style="HelpIcon.TLabel")

        icon.grid(row=0, column=1, sticky="w", padx=(0, 12))

        scale = ttk.Scale(

            row_frame,

            from_=from_,

            to=to,

            orient="horizontal",

            variable=variable,

            command=lambda value, key=text_key, var=variable, st=step: self._on_scale_change(key, var, st, value),

        )

        scale.grid(row=0, column=2, sticky="ew")

        value_label = ttk.Label(row_frame, text="", style="InvestValue.TLabel")

        value_label.grid(row=0, column=3, sticky="e", padx=(12, 0))

        tooltip = Tooltip(icon, "")

        self.help_items[text_key] = HelpConfig(label, tooltip)

        if help_key:

            self.help_items[help_key] = HelpConfig(icon, tooltip)

        self._value_labels[text_key] = (value_label, variable, "{value:.1f} %")

        setattr(self, f"{text_key}_widget", scale)

        self._update_value_label(text_key)

    def _on_scale_change(self, key: str, variable: tk.DoubleVar, step: float, value: str) -> None:

        rounded = round(float(value) / step) * step

        variable.set(rounded)

        self._update_value_label(key)

    def _update_value_label(self, key: str) -> None:

        info = self._value_labels.get(key)

        if not info:

            return

        label, variable, fmt = info

        label.config(text=fmt.format(value=float(variable.get())))

    def _build_ui(self) -> None:

        params = ttk.Frame(self, style="Invest.TFrame")

        params.pack(fill="x", pady=(0, 18))

        self._build_header(params, "investment_parameters")

        form = ttk.Frame(params, style="Invest.TFrame")

        form.pack(fill="x")

        self._add_entry_row(form, 0, "investment_initial", self.initial, help_key="help_initial")

        self._add_entry_row(form, 1, "investment_monthly", self.monthly, help_key="help_monthly")

        def create_year_spin(parent: tk.Widget) -> tk.Spinbox:

            spin = tk.Spinbox(

                parent,

                textvariable=self.years,

                from_=1,

                to=40,

                increment=1,

                width=6,

                justify="right",

                relief="solid",

                highlightthickness=1,

                command=self.update_projection,

            )

            spin.bind("<KeyRelease>", lambda _event: self.update_projection())

            return spin

        self._add_entry_row(form, 2, "investment_years", self.years, help_key="help_years", factory=create_year_spin)

        self._add_scale_row(form, 3, "investment_return", self.rate, from_=0.0, to=25.0, step=0.1, help_key="help_return")

        self._add_scale_row(form, 4, "investment_inflation", self.inflation, from_=0.0, to=15.0, step=0.1, help_key="help_inflation")

        friction = ttk.LabelFrame(self, text="Fricción e impuestos (MX)")
        friction.pack(fill="x", pady=(0, 18))
        for col in range(6):
            friction.columnconfigure(col, weight=1 if col % 2 == 1 else 0)

        ttk.Label(friction, text="Frecuencia de aporte").grid(row=0, column=0, sticky="w", padx=(8, 4), pady=4)
        self.cb_freq_aporte = ttk.Combobox(friction, values=["Mensual", "Quincenal", "Anual"], textvariable=self.frequency, state="readonly")
        self.cb_freq_aporte.grid(row=0, column=1, sticky="ew", padx=(0, 12), pady=4)
        Tooltip(self.cb_freq_aporte, "Mensual=1/mes, Quincenal=2/mes, Anual=1/año")
        ttk.Label(friction, text="Capitalización").grid(row=0, column=2, sticky="w", padx=(8, 4), pady=4)
        self.cb_capitalizacion = ttk.Combobox(friction, values=["Mensual", "Anual"], textvariable=self.capitalization, state="readonly")
        self.cb_capitalizacion.grid(row=0, column=3, sticky="ew", padx=(0, 12), pady=4)
        Tooltip(self.cb_capitalizacion, "Determina cómo se acumulan los intereses")

        ttk.Label(friction, text="Comisión por depósito").grid(row=1, column=0, sticky="w", padx=(8, 4), pady=4)
        self.e_com_dep_val = ttk.Entry(friction, textvariable=self.deposit_fee_value, width=12)
        self.e_com_dep_val.grid(row=1, column=1, sticky="w", padx=(0, 4), pady=4)
        Tooltip(self.e_com_dep_val, "% del aporte o MXN por cada depósito")
        ttk.Radiobutton(friction, text="%", variable=self.deposit_fee_mode, value="%").grid(row=1, column=2, sticky="w", padx=(0, 4), pady=4)
        ttk.Radiobutton(friction, text="MXN", variable=self.deposit_fee_mode, value="MXN").grid(row=1, column=3, sticky="w", padx=(0, 12), pady=4)
        ttk.Label(friction, text="Adm. anual (%)").grid(row=1, column=4, sticky="w", padx=(8, 4), pady=4)
        self.e_com_adm_anual = ttk.Entry(friction, textvariable=self.admin_fee, width=12)
        self.e_com_adm_anual.grid(row=1, column=5, sticky="w", padx=(0, 12), pady=4)
        Tooltip(self.e_com_adm_anual, "% sobre el saldo, prorrateado mensual")

        ttk.Label(friction, text="Compra/Venta (%)").grid(row=2, column=0, sticky="w", padx=(8, 4), pady=4)
        self.e_com_compra_venta = ttk.Entry(friction, textvariable=self.sell_fee, width=12)
        self.e_com_compra_venta.grid(row=2, column=1, sticky="w", padx=(0, 12), pady=4)
        Tooltip(self.e_com_compra_venta, "% sobre el monto operado al inicio/fin")
        ttk.Label(friction, text="Retención intereses (%)").grid(row=2, column=2, sticky="w", padx=(8, 4), pady=4)
        self.e_ret_intereses = ttk.Entry(friction, textvariable=self.withholding, width=12)
        self.e_ret_intereses.grid(row=2, column=3, sticky="w", padx=(0, 12), pady=4)
        Tooltip(self.e_ret_intereses, "Retención provisional anual en México (editable)")

        ttk.Label(friction, text="UMA anual (MXN)").grid(row=3, column=0, sticky="w", padx=(8, 4), pady=4)
        self.e_uma_anual = ttk.Entry(friction, textvariable=self.uma_value, width=12)
        self.e_uma_anual.grid(row=3, column=1, sticky="w", padx=(0, 12), pady=4)
        Tooltip(self.e_uma_anual, "Cálculo pedagógico de exento por intereses")
        ttk.Label(friction, text="Exento (x UMA)").grid(row=3, column=2, sticky="w", padx=(8, 4), pady=4)
        self.e_exento_x_uma = ttk.Entry(friction, textvariable=self.uma_multiplier, width=12)
        self.e_exento_x_uma.grid(row=3, column=3, sticky="w", padx=(0, 12), pady=4)
        Tooltip(self.e_exento_x_uma, "Cálculo pedagógico de exento por intereses")

        ttk.Label(friction, text="ISR venta acc/ETF (%)").grid(row=4, column=0, sticky="w", padx=(8, 4), pady=4)
        self.e_isr_venta = ttk.Entry(friction, textvariable=self.isr_sale, width=12)
        self.e_isr_venta.grid(row=4, column=1, sticky="w", padx=(0, 12), pady=4)
        Tooltip(self.e_isr_venta, "Tasa sobre ganancia al vender (editable)")
        ttk.Label(friction, text="ISR dividendos (%)").grid(row=4, column=2, sticky="w", padx=(8, 4), pady=4)
        self.e_isr_dividendos = ttk.Entry(friction, textvariable=self.isr_dividend, width=12)
        self.e_isr_dividendos.grid(row=4, column=3, sticky="w", padx=(0, 12), pady=4)
        Tooltip(self.e_isr_dividendos, "Tasas educativas, editables")
        ttk.Label(friction, text="% dividendo anual (opcional)").grid(row=4, column=4, sticky="w", padx=(8, 4), pady=4)
        self.e_porcentaje_dividendo = ttk.Entry(friction, textvariable=self.dividend_rate, width=12)
        self.e_porcentaje_dividendo.grid(row=4, column=5, sticky="w", padx=(0, 12), pady=4)
        Tooltip(self.e_porcentaje_dividendo, "Tasas educativas, editables")

        ttk.Label(friction, text="Tipo de instrumento").grid(row=5, column=0, sticky="w", padx=(8, 4), pady=4)
        self.cb_tipo_instrumento = ttk.Combobox(friction, values=["Ahorro/Bonos", "Fondo", "Acción/ETF", "Otro"], textvariable=self.instrument_type, state="readonly")
        self.cb_tipo_instrumento.grid(row=5, column=1, columnspan=2, sticky="ew", padx=(0, 12), pady=4)
        Tooltip(self.cb_tipo_instrumento, "Activa GAT/GAT Real en Ahorro/Bonos")
        ttk.Label(friction, text="Meta (MXN)").grid(row=5, column=3, sticky="w", padx=(8, 4), pady=4)
        self.e_meta_mxn = ttk.Entry(friction, textvariable=self.goal_amount, width=16)
        self.e_meta_mxn.grid(row=5, column=4, sticky="w", padx=(0, 8), pady=4)
        Tooltip(self.e_meta_mxn, "Objetivo de monto al final del horizonte")
        self.btn_meta_inversa = ttk.Button(friction, text="Meta inversa…")
        self.btn_meta_inversa.grid(row=5, column=5, sticky="ew", padx=(0, 12), pady=4)

        summary = ttk.Frame(self, style="Invest.TFrame")
        summary = ttk.Frame(self, style="Invest.TFrame")

        summary.pack(fill="x", pady=(0, 18))

        self._build_header(summary, "investment_summary")

        summary_body = ttk.Frame(summary, style="Invest.TFrame")

        summary_body.pack(fill="x")

        for col in range(3):

            summary_body.grid_columnconfigure(col, weight=1 if col == 2 else 0)

        self._create_summary_row(summary_body, 0, "summary_final_value", self.final_value, "help_final")

        self._create_summary_row(summary_body, 1, "summary_contributions", self.contribution, "help_contrib")

        self._create_summary_row(summary_body, 2, "summary_gain", self.gain, "help_gain")

        self._create_summary_row(summary_body, 3, "summary_real", self.real_value, "help_real")

        self.copy_button = ttk.Button(summary_body, text="", style="Calc.TButton", command=self.copy_summary)

        self.copy_button.grid(row=0, column=3, rowspan=4, padx=(18, 0), sticky="nswe")

        explanation = ttk.Label(self, textvariable=self.lesson, style="Info.TLabel", wraplength=640, justify="left")

        explanation.pack(fill="x", pady=(0, 18))

        table_container = ttk.Frame(self, style="Invest.TFrame")

        table_container.pack(fill="both", expand=True)

        self._build_header(table_container, "investment_evolution")

        columns = ("year", "balance", "contrib", "gain", "real")

        self.tree = ttk.Treeview(table_container, columns=columns, show="headings", style="Card.Treeview", height=8)

        for col in columns:

            self.tree.heading(col, text="")

            self.tree.column(col, anchor="center", stretch=True, width=140)

        self.tree.pack(fill="both", expand=True)

    def _create_summary_row(self, parent: ttk.Frame, row: int, text_key: str, variable: tk.StringVar, help_key: str) -> None:

        label = ttk.Label(parent, text="")

        label.grid(row=row, column=0, sticky="w")

        icon = ttk.Label(parent, text="?", style="HelpIcon.TLabel")

        icon.grid(row=row, column=1, sticky="w", padx=(6, 10))

        ttk.Label(parent, textvariable=variable, style="Info.TLabel").grid(row=row, column=2, sticky="w")

        tooltip = Tooltip(icon, "")

        self.help_items[text_key] = HelpConfig(label, tooltip)

        self.help_items[help_key] = HelpConfig(icon, tooltip)

    def _bind_updates(self) -> None:

        for var in (self.initial, self.monthly, self.years):

            var.trace_add("write", lambda *_: self.update_projection())

        def make_handler(key: str):

            def handler(*_):

                self._update_value_label(key)

                self.update_projection()

            return handler

        self.rate.trace_add("write", make_handler("investment_return"))

        self.inflation.trace_add("write", make_handler("investment_inflation"))

    def refresh_palette(self, palette: Dict[str, str]) -> None:

        widgets = [

            getattr(self, "investment_initial_widget", None),

            getattr(self, "investment_monthly_widget", None),

            getattr(self, "investment_years_widget", None),

            getattr(self, "investment_return_widget", None),

            getattr(self, "investment_inflation_widget", None),

        ]

        for widget in widgets:

            if not isinstance(widget, tk.Widget):

                continue

            try:

                keys = set(widget.keys()) if hasattr(widget, "keys") else set()

                if "background" in keys:

                    widget.configure(background=palette.get("base_bg", "#ffffff"))

                if "foreground" in keys:

                    widget.configure(foreground=palette.get("base_fg", "#000000"))

                if "insertbackground" in keys:

                    widget.configure(insertbackground=palette.get("base_fg", "#000000"))

                if "highlightbackground" in keys:

                    widget.configure(highlightbackground=palette.get("primary_bg", "#2563eb"))

                if "highlightcolor" in keys:

                    widget.configure(highlightcolor=palette.get("primary_bg", "#2563eb"))

            except tk.TclError:

                continue

    def _validate_amount(self, proposed: str) -> bool:

        if not proposed:

            return True

        candidate = proposed.strip().replace(",", "")

        if candidate == ".":

            return True

        try:

            return float(candidate) >= 0

        except ValueError:

            return False

    def _parse_float(self, var: tk.Variable, default: float = 0.0) -> float:

        try:

            raw = var.get()

        except tk.TclError:

            return default

        if isinstance(raw, (int, float)):

            return float(raw)

        text = str(raw).strip().replace(",", "")

        if not text:

            return default

        try:

            return float(text)

        except ValueError:

            return default

    def update_projection(self) -> None:

        lang = self.language_var.get()

        initial = max(0.0, self._parse_float(self.initial, 0.0))

        monthly_value = self._parse_float(self.monthly, 0.0)

        limit_hit = False

        if monthly_value > 50000:

            monthly_value = 50000.0

            self.monthly.set("50000")

            limit_hit = True

        if monthly_value <= 0:

            self._show_monthly_warning(bool(str(self.monthly.get()).strip()), lang)

            return

        years = max(1, int(self._parse_float(self.years, 1)))

        rate = max(0.0, float(self.rate.get())) / 100.0

        inflation = max(0.0, float(self.inflation.get())) / 100.0

        balance = initial

        contributions = initial

        monthly_rate = rate / 12.0

        rows = []

        for month in range(1, years * 12 + 1):

            balance = balance * (1 + monthly_rate) + monthly_value

            contributions += monthly_value

            if month % 12 == 0:

                year = month // 12

                gain = balance - contributions

                real = balance / ((1 + inflation) ** year) if inflation > 0 else balance

                rows.append((year, balance, contributions, gain, real))

        if rows:

            _, final_balance, contrib, gain_value, real_value = rows[-1]

        else:

            final_balance = balance

            contrib = contributions

            gain_value = balance - contributions

            real_value = balance

        self.final_value.set(format_currency(final_balance))

        self.contribution.set(format_currency(contrib))

        self.gain.set(format_currency(gain_value))

        self.real_value.set(format_currency(real_value))

        for item in self.tree.get_children():

            self.tree.delete(item)

        for year, saldo, aporte, ganancia, real in rows:

            self.tree.insert("", "end", values=(year, format_currency(saldo), format_currency(aporte), format_currency(ganancia), format_currency(real)))

        message = translate(lang, "investment_lesson", years=years, final=format_currency(final_balance), gain=format_currency(gain_value), real=format_currency(real_value))

        if limit_hit:

            message += " " + translate(lang, "investment_limit_note")

        self.lesson.set(message)

    def _show_monthly_warning(self, show_popup: bool, lang: str) -> None:

        for item in self.tree.get_children():

            self.tree.delete(item)

        self.final_value.set("MX$ 0.00")

        self.contribution.set("MX$ 0.00")

        self.gain.set("MX$ 0.00")

        self.real_value.set("MX$ 0.00")

        self.lesson.set(translate(lang, "investment_need_monthly_plain"))

        if show_popup and not self._warning_shown:

            messagebox.showwarning(translate(lang, "investment_warning_title"), translate(lang, "investment_need_monthly"))

            self._warning_shown = True

        widget = getattr(self, "investment_monthly_widget", None)

        if isinstance(widget, tk.Widget):

            widget.focus_set()

    def copy_summary(self) -> None:

        lang = self.language_var.get()

        summary = translate(

            lang,

            "investment_summary_template",

            initial=self.initial.get(),

            monthly=self.monthly.get(),

            years=self.years.get(),

            rate=self.rate.get(),

            inflation=self.inflation.get(),

            final=self.final_value.get(),

            contrib=self.contribution.get(),

            gain=self.gain.get(),

            real=self.real_value.get(),

        )

        self.clipboard_clear()

        self.clipboard_append(summary)

        messagebox.showinfo(translate(lang, "copy_summary_title"), translate(lang, "copy_summary_message"))

    def update_language(self) -> None:

        lang = self.language_var.get()

        section_keys = {

            "section_investment_parameters": "investment_parameters",

            "section_investment_summary": "investment_summary",

            "section_investment_evolution": "investment_evolution",

        }

        for section, key in section_keys.items():

            config = self.help_items.get(section)

            if config:

                text = translate(lang, key)

                config.label.config(text=text)

                config.tooltip.update(text)

        help_pairs = {

            "investment_initial": ("help_initial_technical", "help_initial_plain"),

            "investment_monthly": ("help_monthly_technical", "help_monthly_plain"),

            "investment_years": ("help_years_technical", "help_years_plain"),

            "investment_return": ("help_return_technical", "help_return_plain"),

            "investment_inflation": ("help_inflation_technical", "help_inflation_plain"),

            "summary_final_value": ("help_final_technical", "help_final_plain"),

            "summary_contributions": ("help_contrib_technical", "help_contrib_plain"),

            "summary_gain": ("help_gain_technical", "help_gain_plain"),

            "summary_real": ("help_real_technical", "help_real_plain"),

        }

        for key, (technical, plain) in help_pairs.items():

            config = self.help_items.get(key)

            if config:

                config.label.config(text=translate(lang, key))

                config.tooltip.update(f"{translate(lang, technical)}\n\n{translate(lang, plain)}")

        for col, key in {"year": "table_year", "balance": "table_balance", "contrib": "table_contrib", "gain": "table_gain", "real": "table_real"}.items():

            self.tree.heading(col, text=translate(lang, key))

        self.copy_button.config(text=translate(lang, "investment_copy_summary"))

        self.lesson.set(translate(lang, "investment_need_monthly_plain"))

class AccessibilityBar(ttk.Frame):

    def __init__(self, master: "App") -> None:

        super().__init__(master, padding=10, style="Card.TFrame")

        self.app = master

        self.language_display = tk.StringVar()

        self.caption = ttk.Label(self, text="")

        self.caption.pack(side="left", padx=(0, 8))

        self.decrease_btn = ttk.Button(self, text="A-", style="Grey.TButton", command=lambda: master.adjust_font(-1))

        self.decrease_btn.pack(side="left")

        self.increase_btn = ttk.Button(self, text="A+", style="Grey.TButton", command=lambda: master.adjust_font(1))

        self.increase_btn.pack(side="left", padx=(6, 12))

        self.mode_check = ttk.Checkbutton(self, text="", command=master.toggle_colorblind, variable=master.colorblind_mode)

        self.mode_check.pack(side="left")

        self.language_label = ttk.Label(self, text="")

        self.language_label.pack(side="left", padx=(16, 4))

        self.language_combo = ttk.Combobox(self, textvariable=self.language_display, state="readonly", width=14)

        self.language_combo.pack(side="left")

        self.language_combo.bind("<<ComboboxSelected>>", self._on_language_selected)

        self.update_language()

    def _on_language_selected(self, _event: tk.Event) -> None:

        display = self.language_display.get()

        for code in LANGUAGE_ORDER:

            if LANGUAGES[code]["language_name"] == display:

                if code != self.app.language_var.get():

                    self.app.change_language(code)

                break

    def update_language(self) -> None:

        lang = self.app.language_var.get()

        self.caption.config(text=translate(lang, "accessibility"))

        self.decrease_btn.config(text=translate(lang, "font_down"))

        self.increase_btn.config(text=translate(lang, "font_up"))

        self.mode_check.config(text=translate(lang, "color_mode"))

        self.language_label.config(text=translate(lang, "language_label"))

        values = [LANGUAGES[code]["language_name"] for code in LANGUAGE_ORDER]

        self.language_combo["values"] = values

        self.language_display.set(LANGUAGES[lang]["language_name"])

class App(tk.Tk):

    def __init__(self) -> None:

        super().__init__()

        self.base_font_size = 11

        self.colorblind_mode = tk.BooleanVar(value=False)

        self.language_var = tk.StringVar(value="es")

        setup_styles(self, base_size=self.base_font_size, colorblind=self.colorblind_mode.get())

        self.title(translate(self.language_var.get(), "app_title"))

        self.geometry("900x760")

        self.accessibility_bar = AccessibilityBar(self)

        self.accessibility_bar.pack(fill="x")

        self.notebook = ttk.Notebook(self)

        self.notebook.pack(fill="both", expand=True)

        bg_path = filedialog.askopenfilename(

            title="Selecciona una imagen de fondo",

            filetypes=[("ImÃ¡genes", "*.png;*.jpg;*.jpeg;*.bmp;*.gif"), ("Todos", "*.*")],

        )

        palette = getattr(self, "_app_palette", {"base_bg": "#ffffff", "primary_bg": "#2563eb"})

        self.calculator_frame = CalculatorFrame(

            self.notebook,

            language_var=self.language_var,

            bg_path=bg_path if bg_path else None,

            fallback_bg=palette.get("base_bg", "#f3f4f6"),

        )

        self.investment_frame = InvestmentFrame(self.notebook, language_var=self.language_var)

        self.notebook.add(self.calculator_frame, text=translate(self.language_var.get(), "tab_calculator"))

        self.notebook.add(self.investment_frame, text=translate(self.language_var.get(), "tab_investment"))

        self.language_var.trace_add("write", lambda *_: self.apply_language())

    def apply_language(self) -> None:

        lang = self.language_var.get()

        setup_styles(self, base_size=self.base_font_size, colorblind=self.colorblind_mode.get())

        palette = getattr(self, "_app_palette", {"base_bg": "#ffffff", "primary_bg": "#2563eb"})

        self.title(translate(lang, "app_title"))

        self.notebook.tab(self.calculator_frame, text=translate(lang, "tab_calculator"))

        self.notebook.tab(self.investment_frame, text=translate(lang, "tab_investment"))

        self.accessibility_bar.update_language()

        self.calculator_frame.update_language()

        self.investment_frame.update_language()

        self.calculator_frame.refresh_palette()

        self.investment_frame.refresh_palette(palette)

    def adjust_font(self, delta: int) -> None:

        self.base_font_size = max(9, min(20, self.base_font_size + delta))

        self.apply_language()

    def toggle_colorblind(self) -> None:

        self.apply_language()

    def change_language(self, code: str) -> None:

        self.language_var.set(code)

if __name__ == "__main__":

    App().mainloop()

