# -*- coding: utf-8 -*-
"""
GUI de la Calculadora Financiera (Tkinter + ttkbootstrap si est� disponible)
- Inicio / Calculadora / Plan de inversi�n
- Accesibilidad: A-, A+, Modo daltonismo (alto contraste)
- Idiomas: Espa�ol / English / Portugu�s
- Scroll vertical en Plan de inversi�n
- Fricci�n e impuestos (b�sico): comisi�n dep�sito, compra/venta %, adm. anual %, IVA comisiones %, ISR ganancia %
- Resumen + Evoluci�n anual (incluye columnas Comisiones e Impuestos)
"""

from __future__ import annotations
import math
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import font as tkfont
import locale
import sys
from dataclasses import dataclass, field
from functools import partial

# ===== Theme bootstrap (opcional) =====
BOOT = None
try:
    import ttkbootstrap as tb
    BOOT = tb
except Exception:
    BOOT = None


# ===== i18n =====
LANGUAGES = {
    "es": {
        "app_title": "Calculadora Financiera para j�venes",
        "tab_home": "Inicio",
        "tab_calc": "Calculadora",
        "tab_plan": "Plan de inversi�n",
        "access": "Accesibilidad:",
        "font_minus": "A-",
        "font_plus": "A+",
        "daltonic": "Modo daltonismo",
        "language": "Idioma:",
        "home_title": "Bienvenido a aprender a invertir",
        "home_sub": "Simula metas, entiende comisiones e impuestos y practica con la calculadora cient�fica.",
        "home_start": "Comenzar plan de inversi�n",
        "home_calc": "Explorar calculadora",
        "hint": "Sugerencia: cambia el idioma y el tama�o de fuente desde la barra superior.",
        "params": "Par�metros de inversi�n",
        "initial_amount": "Monto inicial (MX$)",
        "monthly_contrib": "Aporte mensual (MX$)",
        "horizon_years": "Horizonte (a�os)",
        "annual_return": "Rendimiento anual (%)",
        "inflation": "Inflaci�n anual (%)",
        "friction": "Fricci�n e impuestos (MX)",
        "deposit_fee": "Comisi�n por dep�sito (%)",
        "buy_sell": "Compra/Venta (%)",
        "mgmt": "Adm. anual (%)",
        "vat_comm": "IVA sobre comisiones (%)",
        "isr_gain": "ISR sobre ganancia (%)",
        "contrib_growth": "Crecimiento anual de aportes (%)",
        "custody_fixed": "Cuota fija de custodia (MXN/mes)",
        "market_spread": "Market spread de salida (%)",
        "summary": "Resumen",
        "nominal_value": "Valor final (nominal)",
        "total_contrib": "Aportes totales",
        "gain": "Ganancia generada",
        "real_value": "Valor ajustado por inflaci�n",
        "need_monthly": "Se necesita un aporte mensual positivo para proyectar la inversi�n.",
        "copy": "Copiar resumen",
        "evolution": "Evoluci�n anual",
        "years": "A�os a invertir",
        "final_balance": "Saldo total final",
        "cum_contrib": "Aporte acumulado",
        "gain_col": "Ganancia",
        "real_col": "Valor real",
        "fees_col": "Comisiones",
        "taxes_col": "Impuestos",
    },
    "en": {
        "app_title": "Finance Calculator for youth",
        "tab_home": "Home",
        "tab_calc": "Calculator",
        "tab_plan": "Investment plan",
        "access": "Accessibility:",
        "font_minus": "A-",
        "font_plus": "A+",
        "daltonic": "Color-blind mode",
        "language": "Language:",
        "home_title": "Welcome to learn investing",
        "home_sub": "Simulate goals, understand fees and taxes, and practice with the scientific calculator.",
        "home_start": "Start investment plan",
        "home_calc": "Open calculator",
        "hint": "Tip: change language and font size from the top bar.",
        "params": "Investment parameters",
        "initial_amount": "Initial amount",
        "monthly_contrib": "Monthly contribution",
        "horizon_years": "Horizon (years)",
        "annual_return": "Annual return (%)",
        "inflation": "Inflation (%)",
        "friction": "Friction & taxes",
        "deposit_fee": "Deposit fee (%)",
        "buy_sell": "Buy/Sell (%)",
        "mgmt": "Mgmt. fee (%)",
        "vat_comm": "VAT on fees (%)",
        "isr_gain": "Income tax on gain (%)",
        "contrib_growth": "Contribution growth (%)",
        "custody_fixed": "Custody flat fee (MXN/mo)",
        "market_spread": "Exit market spread (%)",
        "summary": "Summary",
        "nominal_value": "Final value (nominal)",
        "total_contrib": "Total contributions",
        "gain": "Generated gain",
        "real_value": "Real value (inflation-adjusted)",
        "need_monthly": "A positive monthly contribution is required.",
        "copy": "Copy summary",
        "evolution": "Yearly evolution",
        "years": "Years",
        "final_balance": "Final balance",
        "cum_contrib": "Cum. contribution",
        "gain_col": "Gain",
        "real_col": "Real value",
        "fees_col": "Fees",
        "taxes_col": "Taxes",
    },
    "pt": {
        "app_title": "Calculadora Financeira para jovens",
        "tab_home": "In�cio",
        "tab_calc": "Calculadora",
        "tab_plan": "Plano de investimento",
        "access": "Acessibilidade:",
        "font_minus": "A-",
        "font_plus": "A+",
        "daltonic": "Modo dalt�nico",
        "language": "Idioma:",
        "home_title": "Bem-vindo para aprender a investir",
        "home_sub": "Simule metas, entenda taxas e impostos e pratique com a calculadora cient�fica.",
        "home_start": "Come�ar plano de investimento",
        "home_calc": "Abrir calculadora",
        "hint": "Dica: altere idioma e fonte na barra superior.",
        "params": "Par�metros de investimento",
        "initial_amount": "Montante inicial",
        "monthly_contrib": "Aporte mensal",
        "horizon_years": "Horizonte (anos)",
        "annual_return": "Retorno anual (%)",
        "inflation": "Infla��o anual (%)",
        "friction": "Atrito e impostos",
        "deposit_fee": "Taxa de dep�sito (%)",
        "buy_sell": "Compra/Venda (%)",
        "mgmt": "Adm. anual (%)",
        "vat_comm": "IVA sobre taxas (%)",
        "isr_gain": "IR sobre ganho (%)",
        "contrib_growth": "Crescimento do aporte (%)",
        "custody_fixed": "Custodia fixa (MXN/mes)",
        "market_spread": "Spread de saida (%)",
        "summary": "Resumo",
        "nominal_value": "Valor final (nominal)",
        "total_contrib": "Aportes totais",
        "gain": "Ganho gerado",
        "real_value": "Valor real (ajustado)",
        "need_monthly": "� necess�rio aporte mensal positivo.",
        "copy": "Copiar resumo",
        "evolution": "Evolu��o anual",
        "years": "Anos",
        "final_balance": "Saldo final",
        "cum_contrib": "Aporte acumulado",
        "gain_col": "Ganho",
        "real_col": "Valor real",
        "fees_col": "Comiss�es",
        "taxes_col": "Impostos",
    },
}

HELP_TEXTS = {
    "es": {
        "initial_amount": (
            "Capital inicial",
            "• Monto con el que comienzas.\n"
            "• Se invierte desde el mes 1.\n"
            "Ej.: Si pones 5,000 MXN y aportas 1,000/mes, el primer mes parte de 6,000 (menos comisiones de deposito)."
        ),
        "monthly_contrib": (
            "Aporte mensual",
            "• Dinero que agregas cada mes antes de comisiones.\n"
            "• Si activas 'Crecimiento anual de aportes', este monto sube mes a mes."
        ),
        "horizon_years": (
            "Horizonte (años)",
            "• Tiempo total de la inversion.\n"
            "• Al final se simula una venta unica (compra/venta + spread)."
        ),
        "annual_return": (
            "Rendimiento anual nominal (%)",
            "• Tasa esperada antes de inflacion.\n"
            "• Se capitaliza mensual: r_m = (1+r)^(1/12)-1."
        ),
        "inflation": (
            "Inflacion anual (%)",
            "• Sirve para calcular 'Valor real'.\n"
            "• No modifica depositos ni impuestos."
        ),
        "deposit_fee": (
            "Comision por deposito (%)",
            "• Porcentaje descontado a cada aporte mensual.\n"
            "• El IVA se muestra en 'Comisiones', pero no aumenta el saldo."
        ),
        "buy_sell": (
            "Comision de compra/venta (%)",
            "• Se aplica una sola vez al final del horizonte al liquidar.\n"
            "• El IVA se muestra en 'Comisiones'."
        ),
        "mgmt": (
            "Administracion anual (%)",
            "• Cobro del administrador, prorrateado mensual.\n"
            "• El fee reduce el saldo; el IVA solo se reporta en 'Comisiones'."
        ),
        "vat_comm": (
            "IVA sobre comisiones (%)",
            "• Impuesto a las comisiones cobradas (deposito, administracion, custodia).\n"
            "• No aumenta el saldo; solo se refleja como costo."
        ),
        "isr_gain": (
            "ISR sobre ganancia (%)",
            "• Impuesto anual sobre la ganancia positiva del año.\n"
            "• Si el año cierra en perdida, no se cobra ISR ese año."
        ),
        "contrib_growth": (
            "Crecimiento anual de aportes (%)",
            "• Aumenta el aporte cada mes segun una tasa anual.\n"
            "• Ej.: 6% anual ≈ 0.486% mensual."
        ),
        "custody_fixed": (
            "Cuota fija de custodia (MXN/mes)",
            "• Cargo mensual fijo; reduce el saldo.\n"
            "• El IVA de esta cuota se reporta como 'Comisiones'."
        ),
        "market_spread": (
            "Market spread de salida (%)",
            "• Perdida por diferencia bid/ask y deslizamiento al vender.\n"
            "• Se aplica una sola vez al final (ademas de compra/venta)."
        ),
    },
    "en": {
        "initial_amount": (
            "Initial capital",
            "• Money you start with (invested from month 1).\n"
            "• Example: 5,000 + 1,000/month → first month bases on 6,000 minus deposit fees."
        ),
        "monthly_contrib": (
            "Monthly contribution",
            "• Amount added each month before fees.\n"
            "• If 'Contribution growth' is set, this increases monthly."
        ),
        "horizon_years": (
            "Horizon (years)",
            "• Total investment time.\n"
            "• A single exit (fees + spread) is simulated at the end."
        ),
        "annual_return": (
            "Nominal annual return (%)",
            "• Expected return before inflation.\n"
            "• Compounded monthly: r_m = (1+r)^(1/12)-1."
        ),
        "inflation": (
            "Annual inflation (%)",
            "• Used to compute 'Real value'.\n"
            "• Does not change deposits or taxes."
        ),
        "deposit_fee": (
            "Deposit fee (%)",
            "• Percentage charged on each monthly deposit.\n"
            "• VAT is shown under 'Fees'."
        ),
        "buy_sell": (
            "Buy/Sell fee (%)",
            "• Applied once at the end upon liquidation.\n"
            "• VAT shown under 'Fees'."
        ),
        "mgmt": (
            "Management fee (%)",
            "• Charged monthly from the balance.\n"
            "• VAT reported as fee."
        ),
        "vat_comm": (
            "VAT on fees (%)",
            "• Tax on fees (deposit, management, custody).\n"
            "• Does not increase balance; shown as cost."
        ),
        "isr_gain": (
            "Tax on gains (%)",
            "• Annual tax on positive yearly gains only."
        ),
        "contrib_growth": (
            "Contribution growth (%)",
            "• Increases monthly deposit according to annual rate.\n"
            "• Example: 6%/yr ≈ 0.486%/mo."
        ),
        "custody_fixed": (
            "Custody flat fee (MXN/mo)",
            "• Fixed monthly fee; reduces balance.\n"
            "• VAT reported as fee."
        ),
        "market_spread": (
            "Exit market spread (%)",
            "• Loss from bid/ask and slippage when selling at the end."
        ),
    },
    "pt": {
        "initial_amount": (
            "Capital inicial",
            "• Dinheiro com que voce comeca (investido desde o 1° mes).\n"
            "• Ex.: 5.000 + 1.000/mês → base de 6.000 menos taxas de deposito."
        ),
        "monthly_contrib": (
            "Aporte mensal",
            "• Valor adicionado todo mes antes de taxas.\n"
            "• Com 'Crescimento do aporte', aumenta mensalmente."
        ),
        "horizon_years": (
            "Horizonte (anos)",
            "• Tempo total da aplicacao.\n"
            "• Saida unica no final (taxas + spread)."
        ),
        "annual_return": (
            "Retorno anual nominal (%)",
            "• Antes da inflacao; capitalizado mensalmente."
        ),
        "inflation": (
            "Inflacao anual (%)",
            "• Usada para 'Valor real'."
        ),
        "deposit_fee": (
            "Taxa de deposito (%)",
            "• Percentual cobrado em cada aporte mensal."
        ),
        "buy_sell": (
            "Taxa de compra/venda (%)",
            "• Aplicada uma vez no final."
        ),
        "mgmt": (
            "Administracao anual (%)",
            "• Cobrança mensal sobre o saldo; IVA reportado em 'Taxas'."
        ),
        "vat_comm": (
            "IVA sobre taxas (%)",
            "• Imposto sobre taxas (deposito, administracao, custodia)."
        ),
        "isr_gain": (
            "Imposto sobre ganho (%)",
            "• Cobrado somente se o ano fechar com ganho positivo."
        ),
        "contrib_growth": (
            "Crescimento do aporte (%)",
            "• Aumenta o aporte mensal conforme taxa anual."
        ),
        "custody_fixed": (
            "Custodia fixa (MXN/mês)",
            "• Tarifa mensal fixa; reduz o saldo."
        ),
        "market_spread": (
            "Spread de saida (%)",
            "• Perda por bid/ask e slippage na venda final."
        ),
    },
}

class Tooltip:
    """Lightweight tooltip that adapts to ttkbootstrap when available."""

    def __init__(self, widget, text, delay=350):
        self.widget = widget
        self.text = text
        self.delay = delay
        self._id = None
        self._tip = None
        widget.bind("<Enter>", self._schedule, add="+")
        widget.bind("<Leave>", self._hide, add="+")
        widget.bind("<ButtonPress>", self._hide, add="+")

    def _schedule(self, _event=None):
        if self._id:
            self.widget.after_cancel(self._id)
        self._id = self.widget.after(self.delay, self._show)

    def _show(self):
        if self._tip or not self.text:
            return
        bbox = None
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

    def _hide(self, _event=None):
        if self._id:
            self.widget.after_cancel(self._id)
            self._id = None
        if self._tip:
            self._tip.destroy()
            self._tip = None





def fmt_currency(value: float, symbol: str = "MX$") -> str:
    try:
        # Intento con configuraci�n local del usuario
        return f"{symbol} {value:,.2f}"
    except Exception:
        return f"{symbol} {value:.2f}"


@dataclass
class Inputs:
    initial: float = 0.0
    monthly: float = 0.0
    years: int = 1
    annual_return: float = 10.0     # %
    inflation: float = 4.0          # %
    # Fricci�n e impuestos
    fee_deposit: float = 0.0        # %
    buy_sell: float = 0.0           # %
    mgmt: float = 0.0               # %
    vat_on_fees: float = 16.0       # %
    tax_gain: float = 10.0          # %
    contrib_growth: float = 0.0     # % anual
    custody_fixed: float = 0.0      # MXN/mes
    market_spread: float = 0.0      # % aplicado al final


@dataclass
class YearRow:
    year: int
    final_balance: float
    cum_contrib: float
    gain: float
    real_value: float
    fees: float
    taxes: float


class App(tk.Tk):
    def __init__(self):
        # ===== Root & style =====
        if BOOT:
            super().__init__()
            self.style = BOOT.Style("flatly")
        else:
            super().__init__()
            self.style = ttk.Style(self)

        self.lang = "es"
        self.strings = LANGUAGES[self.lang]

        self.title(self.strings["app_title"])
        self.geometry("1200x720")
        self.minsize(980, 600)

        # ===== Accesibilidad (estado) =====
        self.base_font_size = tkfont.nametofont("TkDefaultFont").cget("size")
        self.cb_var = tk.BooleanVar(value=False)

        # ===== Top bar =====
        self._build_topbar()

        # ===== Notebook con tabs =====
        self.nb = ttk.Notebook(self)
        self.nb.pack(fill="both", expand=True)

        self.home_tab = ttk.Frame(self.nb)
        self.calc_tab = ttk.Frame(self.nb)
        self.plan_tab = ttk.Frame(self.nb)

        self.nb.add(self.home_tab, text=self.strings["tab_home"])
        self.nb.add(self.calc_tab, text=self.strings["tab_calc"])
        self.nb.add(self.plan_tab, text=self.strings["tab_plan"])

        # ===== Contenidos =====
        self._build_home()
        self._build_calc_placeholder()
        self._build_plan()

        self._apply_font_size()

    # ---------- UI Building ----------

    def _build_topbar(self):
        top = ttk.Frame(self)
        top.pack(fill="x", padx=8, pady=6)

        # Accesibilidad
        ttk.Label(top, text=self.strings["access"]).pack(side="left", padx=(0, 6))
        ttk.Button(top, text=self.strings["font_minus"], command=self._font_minus, width=4).pack(side="left")
        ttk.Button(top, text=self.strings["font_plus"], command=self._font_plus, width=4).pack(side="left", padx=(6, 12))
        ttk.Label(top, text="|").pack(side="left", padx=(8, 8))

        chk = ttk.Checkbutton(
            top, text=self.strings["daltonic"],
            variable=self.cb_var, command=self._toggle_contrast
        )
        chk.pack(side="left")

        # Idioma
        ttk.Label(top, text=self.strings["language"]).pack(side="left", padx=(18, 6))
        self.lang_cmb = ttk.Combobox(top, values=["Espa�ol", "English", "Portugu�s"], width=16, state="readonly")
        self.lang_cmb.current(0)
        self.lang_cmb.bind("<<ComboboxSelected>>", self._on_change_lang)
        self.lang_cmb.pack(side="left")

    def _build_home(self):
        c = ttk.Frame(self.home_tab)
        c.pack(expand=True)

        ttk.Label(c, text=self.strings["home_title"], font=("TkDefaultFont", self.base_font_size + 6, "bold")).pack(pady=(60, 10))
        ttk.Label(c, text=self.strings["home_sub"]).pack(pady=(0, 20))

        btns = ttk.Frame(c)
        btns.pack(pady=10)
        ttk.Button(btns, text=self.strings["home_start"], command=lambda: self.nb.select(self.plan_tab)).grid(row=0, column=0, padx=8)
        ttk.Button(btns, text=self.strings["home_calc"], command=lambda: self.nb.select(self.calc_tab)).grid(row=0, column=1, padx=8)

        ttk.Label(c, text=self.strings["hint"]).pack(pady=(30, 0))

    def _build_calc_placeholder(self):
        w = ttk.Frame(self.calc_tab, padding=12)
        w.pack(fill="both", expand=True)
        ttk.Label(w, text="(Pr�ximamente: calculadora cient�fica)").pack(anchor="w")

    def _help_text(self, key: str) -> tuple[str, str]:
        lang = getattr(self, "lang", "es")
        d = HELP_TEXTS.get(lang, HELP_TEXTS["es"])
        return d.get(key, ("", ""))



    def _help_icon(self, parent: tk.Misc, key: str):
        title, body = self._help_text(key)
        if not title and not body:
            return ttk.Label(parent, text="")
        txt = f"{title}\n\n{body}" if body else title
        lbl = ttk.Label(parent, text=" ?", cursor="question_arrow")
        Tooltip(lbl, txt)
        return lbl




    def _build_plan(self):
        # Scrollable canvas
        outer = ttk.Frame(self.plan_tab)
        outer.pack(fill="both", expand=True)

        canvas = tk.Canvas(outer, highlightthickness=0)
        vbar = ttk.Scrollbar(outer, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=vbar.set)
        vbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        inner = ttk.Frame(canvas)
        inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=inner, anchor="nw")

        # Mouse-wheel scrolling
        def _wheel(event):
            delta = event.delta if hasattr(event, "delta") else 0
            if delta == 0 and getattr(event, "num", None) in (4, 5):  # X11
                delta = 120 if event.num == 4 else -120
            if delta:
                canvas.yview_scroll(int(-1 * (delta / 120)), "units")

        inner.bind_all("<MouseWheel>", _wheel)
        inner.bind_all("<Button-4>", _wheel)
        inner.bind_all("<Button-5>", _wheel)

        # --- Par�metros ---
        box = ttk.LabelFrame(inner, text=self.strings["params"], padding=12)
        box.pack(fill="x", padx=10, pady=(12, 8))
        ttk.Separator(inner, orient="horizontal").pack(fill="x", padx=10, pady=(0, 6))

        self.var_initial = tk.StringVar(value="0")
        self.var_monthly = tk.StringVar(value="200")
        self.var_years = tk.IntVar(value=5)
        self.var_return = tk.DoubleVar(value=10.0)
        self.var_infl = tk.DoubleVar(value=4.0)
        self.var_growth = tk.DoubleVar(value=0.0)
        self.var_custody = tk.StringVar(value="0.0")
        self.var_spread = tk.StringVar(value="0.0")

        self._labeled_entry(box, self.strings["initial_amount"], self.var_initial, 0, 0)
        self._labeled_entry(box, self.strings["monthly_contrib"], self.var_monthly, 1, 0)
        self._labeled_scale(
            box, self.strings['horizon_years'], self.var_years, 2, 0,
            from_=1, to_=50, step=1,
            fmt=lambda v: f"{int(float(v))} anios",
            help_key='horizon_years'
        )
        self._labeled_scale(
            box, self.strings['annual_return'], self.var_return, 0, 1,
            from_=0.0, to_=25.0, step=0.1,
            fmt=lambda v: f"{float(v):.1f} %",
            help_key='annual_return'
        )
        self._labeled_scale(
            box, self.strings['inflation'], self.var_infl, 1, 1,
            from_=0.0, to_=15.0, step=0.1,
            fmt=lambda v: f"{float(v):.1f} %",
            help_key='inflation'
        )
        self._labeled_scale(
            box, self.strings['contrib_growth'], self.var_growth, 2, 1,
            from_=0.0, to_=15.0, step=0.1,
            fmt=lambda v: f"{float(v):.1f} %",
            help_key='contrib_growth'
        )

        # --- Fricci�n e impuestos ---
        fr = ttk.LabelFrame(inner, text=self.strings["friction"], padding=12)
        fr.pack(fill="x", padx=10, pady=8)
        ttk.Separator(inner, orient="horizontal").pack(fill="x", padx=10, pady=(0, 6))

        self.var_fee_dep = tk.StringVar(value="0.0")
        self.var_buy_sell = tk.StringVar(value="0.0")
        self.var_mgmt = tk.StringVar(value="0.0")
        self.var_vat = tk.StringVar(value="16.0")
        self.var_tax = tk.StringVar(value="10.0")

        self._labeled_entry(fr, self.strings["deposit_fee"], self.var_fee_dep, 0, 0, help_key="deposit_fee")
        self._labeled_entry(fr, self.strings["buy_sell"], self.var_buy_sell, 1, 0, help_key="buy_sell")
        self._labeled_entry(fr, self.strings["mgmt"], self.var_mgmt, 2, 0, help_key="mgmt")
        self._labeled_entry(fr, self.strings["vat_comm"], self.var_vat, 0, 1, help_key="vat_comm")
        self._labeled_entry(fr, self.strings["isr_gain"], self.var_tax, 1, 1, help_key="isr_gain")
        self._labeled_entry(fr, self.strings["market_spread"], self.var_spread, 2, 1, help_key="market_spread")
        self._labeled_entry(fr, self.strings["custody_fixed"], self.var_custody, 3, 1, help_key="custody_fixed")

        # --- Resumen ---
        sm = ttk.LabelFrame(inner, text=self.strings["summary"], padding=12)
        sm.pack(fill="x", padx=10, pady=8)
        ttk.Separator(inner, orient="horizontal").pack(fill="x", padx=10, pady=(0, 6))

        self.lbl_nominal = ttk.Label(sm, text="{}: ".format(self.strings["nominal_value"]))
        self.lbl_total   = ttk.Label(sm, text="{}: ".format(self.strings["total_contrib"]))
        self.lbl_gain    = ttk.Label(sm, text="{}: ".format(self.strings["gain"]))
        self.lbl_real    = ttk.Label(sm, text="{}: ".format(self.strings["real_value"]))

        self.lbl_nominal.grid(row=0, column=0, sticky="w", padx=4, pady=2)
        self.lbl_total.grid(row=1, column=0, sticky="w", padx=4, pady=2)
        self.lbl_gain.grid(row=2, column=0, sticky="w", padx=4, pady=2)
        self.lbl_real.grid(row=3, column=0, sticky="w", padx=4, pady=2)

        self.btn_copy = ttk.Button(sm, text=self.strings["copy"], command=self._copy_summary)
        self.btn_copy.grid(row=0, column=2, rowspan=4, sticky="e", padx=6, pady=4)
        sm.grid_columnconfigure(1, weight=1)

        ttk.Label(inner, text=self.strings["need_monthly"]).pack(anchor="w", padx=14, pady=(2, 8))

        # --- Evolucion anual ---
        cols = ("year", "final", "contrib", "gain", "real", "fees", "taxes")
        tree_frame = ttk.Frame(inner)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=(0, 12))
        self.tree = ttk.Treeview(tree_frame, columns=cols, show="headings", height=12)
        self.tree.pack(side="left", fill="both", expand=True)
        sb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        sb.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=sb.set)


        self.tree.heading("year", text=self.strings.get("years_to_invest", self.strings.get("years", "Year")))
        self.tree.heading("final", text=self.strings["final_balance"])
        self.tree.heading("contrib", text=self.strings["cum_contrib"])
        self.tree.heading("gain", text=self.strings["gain_col"] + " (neto acumulada)")
        self.tree.heading("real", text=self.strings.get("real_value", self.strings.get("real_col", "Real")))
        self.tree.heading("fees", text=self.strings.get("fees", self.strings.get("fees_col", "Fees")))
        self.tree.heading("taxes", text=self.strings.get("taxes", self.strings.get("taxes_col", "Taxes")))

        self.tree.column("year", width=100, anchor="center")
        self.tree.column("final", width=160, anchor="e")
        self.tree.column("contrib", width=160, anchor="e")
        self.tree.column("gain", width=180, anchor="e")
        self.tree.column("real", width=160, anchor="e")
        self.tree.column("fees", width=120, anchor="e")
        self.tree.column("taxes", width=120, anchor="e")

        # disparadores de rec�lculo
        for v in (self.var_initial, self.var_monthly, self.var_years, self.var_return, self.var_infl,
                  self.var_growth, self.var_custody, self.var_spread,
                  self.var_fee_dep, self.var_buy_sell, self.var_mgmt, self.var_vat, self.var_tax):
            v.trace_add("write", lambda *_: self._recalc())

        self._recalc()  # mantener

    def _labeled_scale(self, parent, label, var, row, col, from_, to_, step, fmt, help_key=None):
        frame_cls = BOOT.Frame if BOOT else ttk.Frame
        label_cls = BOOT.Label if BOOT else ttk.Label
        scale_cls = getattr(BOOT, "Scale", ttk.Scale) if BOOT else ttk.Scale

        frm = frame_cls(parent)
        frm.grid(row=row, column=col, padx=8, pady=6, sticky="ew")
        parent.grid_columnconfigure(col, weight=1)

        head = frame_cls(frm)
        head.pack(anchor="w", fill="x")

        label_cls(head, text=label).pack(side="left")
        if help_key:
            self._help_icon(head, help_key).pack(side="left", padx=(4, 0))

        val_lbl = label_cls(head, text=fmt(var.get()))
        val_lbl.pack(side="right")

        def on_move(_value=None):
            try:
                current = float(var.get())
            except Exception:
                current = from_
            snapped = round(current / step) * step
            snapped = max(min(snapped, to_), from_)
            if abs(snapped - current) > 1e-9:
                var.set(snapped)
            val_lbl.config(text=fmt(snapped))

        scale_cls(
            frm,
            orient="horizontal",
            from_=from_,
            to=to_,
            variable=var,
            command=lambda _v: on_move(),
        ).pack(fill="x")
        on_move()

        var.trace_add("write", lambda *_: self._recalc())


    def _labeled_entry(self, parent, label, var, row, col, help_key=None, width=16):
        frame_cls = BOOT.Frame if BOOT else ttk.Frame
        label_cls = BOOT.Label if BOOT else ttk.Label
        entry_cls = BOOT.Entry if BOOT else ttk.Entry

        frm = frame_cls(parent)
        frm.grid(row=row, column=col, padx=8, pady=6, sticky="ew")
        parent.grid_columnconfigure(col, weight=1)

        head = frame_cls(frm)
        head.pack(anchor="w", fill="x")

        label_cls(head, text=label).pack(side="left")
        if help_key:
            self._help_icon(head, help_key).pack(side="left", padx=(4, 0))

        entry_cls(frm, textvariable=var, width=width).pack(anchor="w")

    # ---------- Logic ----------

    def _collect_inputs(self) -> Inputs:
        def f(s, d=0.0):
            try:
                return float(str(s).replace(",", "."))
            except Exception:
                return d

        def i(s, d=1):
            try:
                return max(0, int(float(str(s))))
            except Exception:
                return d

        years = max(1, int(self.var_years.get() or 1))

        return Inputs(
            initial=f(self.var_initial.get(), 0.0),
            monthly=f(self.var_monthly.get(), 0.0),
            years=years,
            annual_return=float(self.var_return.get() or 0.0),
            inflation=float(self.var_infl.get() or 0.0),
            fee_deposit=f(self.var_fee_dep.get(), 0.0),
            buy_sell=f(self.var_buy_sell.get(), 0.0),
            mgmt=f(self.var_mgmt.get(), 0.0),
            vat_on_fees=f(self.var_vat.get(), 16.0),
            tax_gain=f(self.var_tax.get(), 10.0),
            contrib_growth=float(self.var_growth.get() or 0.0),
            custody_fixed=f(self.var_custody.get(), 0.0),
            market_spread=f(self.var_spread.get(), 0.0),
        )

    def _simulate(self, p: Inputs) -> tuple[list[YearRow], float, float, float, float]:
        """Simulacion mensual con:

Depositos mensuales (comision de deposito + IVA solo reportado en costos).
Administracion mensual prorrateada (el fee reduce saldo; el IVA solo se reporta).
Impuesto anual sobre ganancia positiva.
Comision de compra/venta aplicada una sola vez al final del horizonte.
        """
        # Tasas mensuales compuestas
        r_m = (1.0 + p.annual_return / 100.0) ** (1.0 / 12.0) - 1.0
        mgmt_m = (p.mgmt / 100.0) / 12.0
        infl_y = p.inflation / 100.0
        g_m = (1.0 + p.contrib_growth / 100.0) ** (1.0 / 12.0) - 1.0

        balance = p.initial
        cum_contrib = p.initial

        rows: list[YearRow] = []

        if p.years <= 0:
            nominal = balance
            total_contrib = cum_contrib
            total_gain = max(0.0, nominal - total_contrib)
            return [], nominal, total_contrib, total_gain, nominal

        dep_current = p.monthly

        for year in range(1, p.years + 1):
            start_balance = balance
            fees_year = 0.0
            taxes_year = 0.0
            gross_contrib_year = 0.0  # aportes brutos del a"o
            net_in_year = 0.0         # lo que realmente entra tras comisi"n dep"sito
            for _m in range(12):
                dep = dep_current
                if dep > 0:
                    fee_dep = dep * (p.fee_deposit / 100.0)
                    iva_dep = fee_dep * (p.vat_on_fees / 100.0)
                    net_dep = dep - fee_dep

                    balance += net_dep
                    cum_contrib += dep
                    gross_contrib_year += dep
                    net_in_year += net_dep
                    fees_year += (fee_dep + iva_dep)  # IVA se reporta como costo pero no reduce balance

                # comisi"n de administraci"n mensual
                if mgmt_m > 0:
                    fee_mgmt = balance * mgmt_m
                    iva_mgmt = fee_mgmt * (p.vat_on_fees / 100.0)
                    balance -= fee_mgmt
                    fees_year += (fee_mgmt + iva_mgmt)

                if p.custody_fixed > 0.0:
                    fee_fix = p.custody_fixed
                    iva_fix = fee_fix * (p.vat_on_fees / 100.0)
                    balance -= fee_fix
                    fees_year += (fee_fix + iva_fix)

                # inter"s mensual compuesto
                balance += balance * r_m

                # crecimiento del aporte mensual
                dep_current *= (1.0 + g_m)

            # Ganancia efectiva del a"o (antes de impuestos)
            gain_before_tax = balance - start_balance - net_in_year
            tax = (gain_before_tax * (p.tax_gain / 100.0)) if gain_before_tax > 0 else 0.0
            taxes_year += tax
            balance -= tax

            # Valor real a fin de a"o
            real_val = balance / ((1.0 + infl_y) ** year)

            gain_cum = balance - cum_contrib
            if abs(gain_cum) < 1e-9:
                gain_cum = 0.0

            rows.append(YearRow(
                year=year,
                final_balance=balance,
                cum_contrib=cum_contrib,
                gain=gain_cum,
                real_value=real_val,
                fees=fees_year,
                taxes=taxes_year,
            ))


        # Comisi"n de compra/venta SOLO al final del horizonte (si aplica)
        if p.buy_sell > 0:
            fee_bs = balance * (p.buy_sell / 100.0)
            iva_bs = fee_bs * (p.vat_on_fees / 100.0)
            balance -= fee_bs
            rows[-1] = YearRow(
                year=rows[-1].year,
                final_balance=balance,
                cum_contrib=rows[-1].cum_contrib,
                gain=rows[-1].gain - fee_bs,  # impacto neto en ultimo ano
                real_value=balance / ((1.0 + infl_y) ** p.years),
                fees=rows[-1].fees + fee_bs + iva_bs,
                taxes=rows[-1].taxes
            )

        if p.market_spread > 0:
            spread_loss = balance * (p.market_spread / 100.0)
            balance -= spread_loss
            last = rows[-1]
            rows[-1] = YearRow(
                year=last.year,
                final_balance=balance,
                cum_contrib=last.cum_contrib,
                gain=balance - last.cum_contrib,
                real_value=balance / ((1.0 + infl_y) ** p.years),
                fees=last.fees + spread_loss,
                taxes=last.taxes,
            )

        # Sanity check: final balance should match contributions plus net gain
        for rr in rows:
            if abs((rr.cum_contrib + rr.gain) - rr.final_balance) > 0.01:
                print(f"[WARN] Ano {rr.year}: final != contrib + ganancia {rr.final_balance:.2f} vs {(rr.cum_contrib + rr.gain):.2f}")

        nominal = balance
        total_contrib = cum_contrib
        total_gain = max(0.0, nominal - total_contrib)
        real_total = nominal / ((1.0 + infl_y) ** p.years)
        return rows, nominal, total_contrib, total_gain, real_total


    def _recalc(self):
        p = self._collect_inputs()
        if p.monthly <= 0 and p.initial <= 0:
            self._clear_summary()
            return
        rows, nominal, contrib, gain, real = self._simulate(p)

        # resumen
        self.lbl_nominal.config(text=f"{self.strings['nominal_value']}  {fmt_currency(nominal)}")
        self.lbl_total.config(text=f"{self.strings['total_contrib']}  {fmt_currency(contrib)}")
        self.lbl_gain.config(text=f"{self.strings['gain']}  {fmt_currency(gain)}")
        self.lbl_real.config(text=f"{self.strings['real_value']}  {fmt_currency(real)}")

        # tabla
        for i in self.tree.get_children():
            self.tree.delete(i)
        for r in rows:
            self.tree.insert("", "end", values=(
                r.year,
                fmt_currency(r.final_balance),
                fmt_currency(r.cum_contrib),
                fmt_currency(r.gain),
                fmt_currency(r.real_value),
                fmt_currency(r.fees),
                fmt_currency(r.taxes),
            ))

    def _clear_summary(self):
        self.lbl_nominal.config(text='{}: '.format(self.strings['nominal_value']))
        self.lbl_total.config(text='{}: '.format(self.strings['total_contrib']))
        self.lbl_gain.config(text='{}: '.format(self.strings['gain']))
        self.lbl_real.config(text='{}: '.format(self.strings['real_value']))
        for i in self.tree.get_children():
            self.tree.delete(i)

    # ---------- Actions ----------

    def _copy_summary(self):
        try:
            text = "\n".join([
                self.lbl_nominal.cget("text"),
                self.lbl_total.cget("text"),
                self.lbl_gain.cget("text") + " (neto acumulada)",
                self.lbl_real.cget("text"),
            ])
            self.clipboard_clear()
            self.clipboard_append(text)
            self.update()
            messagebox.showinfo("OK", "Resumen copiado al portapapeles.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _font_minus(self):
        self._apply_font_scale(-1)

    def _font_plus(self):
        self._apply_font_scale(1)

    def _apply_font_scale(self, delta: int):
        self.base_font_size = max(8, min(18, self.base_font_size + delta))
        for name in ("TkDefaultFont", "TkTextFont", "TkHeadingFont", "TkMenuFont", "TkFixedFont", "TkTooltipFont"):
            try:
                f = tkfont.nametofont(name)
                f.configure(size=self.base_font_size)
            except tk.TclError:
                pass
        self.update_idletasks()


    def _apply_font_size(self):
        f = ("TkDefaultFont", self.base_font_size)
        try:
            self.option_clear()
        except Exception:
            pass
        self.option_add("*Font", f)

    def _toggle_contrast(self):
        try:
            import ttkbootstrap as tb  # noqa: F401
            self.style.theme_use("darkly" if self.cb_var.get() else "flatly")
        except Exception:
            s = ttk.Style()
            if self.cb_var.get():
                s.theme_use("clam")
                s.configure("TLabel", foreground="#000000")
                s.configure("TButton", foreground="#000000")
                s.configure("TScale", troughcolor="#d9d9d9")
            else:
                try:
                    s.theme_use("default")
                except tk.TclError:
                    pass

    def _on_change_lang(self, _evt=None):
        idx = self.lang_cmb.current()
        self.lang = ("es", "en", "pt")[idx]
        self.strings = LANGUAGES[self.lang]
        self.title(self.strings["app_title"])

        # Renombrar tabs
        self.nb.tab(self.home_tab, text=self.strings["tab_home"])
        self.nb.tab(self.calc_tab, text=self.strings["tab_calc"])
        self.nb.tab(self.plan_tab, text=self.strings["tab_plan"])

        # Reconstruir contenidos sensibles a idioma
        for w in self.home_tab.winfo_children():
            w.destroy()
        for w in self.plan_tab.winfo_children():
            w.destroy()
        self._build_home()
        self._build_plan()

# ---- Launch (cuando se ejecuta directo este archivo) ----
if __name__ == "__main__":
    App().mainloop()
