# -*- coding: utf-8 -*-
"""
GUI de la Calculadora Financiera (Tkinter + ttkbootstrap si está disponible)
- Inicio / Calculadora / Plan de inversión
- Accesibilidad: A-, A+, Modo daltonismo (alto contraste)
- Idiomas: Español / English / Português
- Scroll vertical en Plan de inversión
- Fricción e impuestos (básico): comisión depósito, compra/venta %, adm. anual %, IVA comisiones %, ISR ganancia %
- Resumen + Evolución anual (incluye columnas Comisiones e Impuestos)
"""

from __future__ import annotations
import math
import tkinter as tk
from tkinter import ttk, messagebox
import locale
import sys
from dataclasses import dataclass, field

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
        "app_title": "Calculadora Financiera para jóvenes",
        "tab_home": "Inicio",
        "tab_calc": "Calculadora",
        "tab_plan": "Plan de inversión",
        "access": "Accesibilidad:",
        "font_minus": "A-",
        "font_plus": "A+",
        "daltonic": "Modo daltonismo",
        "language": "Idioma:",
        "home_title": "Bienvenido a aprender a invertir",
        "home_sub": "Simula metas, entiende comisiones e impuestos y practica con la calculadora científica.",
        "home_start": "Comenzar plan de inversión",
        "home_calc": "Explorar calculadora",
        "hint": "Sugerencia: cambia el idioma y el tamaño de fuente desde la barra superior.",
        "params": "Parámetros de inversión",
        "initial_amount": "Monto inicial (MX$)",
        "monthly_contrib": "Aporte mensual (MX$)",
        "horizon_years": "Horizonte (años)",
        "annual_return": "Rendimiento anual (%)",
        "inflation": "Inflación anual (%)",
        "friction": "Fricción e impuestos (MX)",
        "deposit_fee": "Comisión por depósito (%)",
        "buy_sell": "Compra/Venta (%)",
        "mgmt": "Adm. anual (%)",
        "vat_comm": "IVA sobre comisiones (%)",
        "isr_gain": "ISR sobre ganancia (%)",
        "summary": "Resumen",
        "nominal_value": "Valor final (nominal)",
        "total_contrib": "Aportes totales",
        "gain": "Ganancia generada",
        "real_value": "Valor ajustado por inflación",
        "need_monthly": "Se necesita un aporte mensual positivo para proyectar la inversión.",
        "copy": "Copiar resumen",
        "evolution": "Evolución anual",
        "years": "Años a invertir",
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
        "tab_home": "Início",
        "tab_calc": "Calculadora",
        "tab_plan": "Plano de investimento",
        "access": "Acessibilidade:",
        "font_minus": "A-",
        "font_plus": "A+",
        "daltonic": "Modo daltônico",
        "language": "Idioma:",
        "home_title": "Bem-vindo para aprender a investir",
        "home_sub": "Simule metas, entenda taxas e impostos e pratique com a calculadora científica.",
        "home_start": "Começar plano de investimento",
        "home_calc": "Abrir calculadora",
        "hint": "Dica: altere idioma e fonte na barra superior.",
        "params": "Parâmetros de investimento",
        "initial_amount": "Montante inicial",
        "monthly_contrib": "Aporte mensal",
        "horizon_years": "Horizonte (anos)",
        "annual_return": "Retorno anual (%)",
        "inflation": "Inflação anual (%)",
        "friction": "Atrito e impostos",
        "deposit_fee": "Taxa de depósito (%)",
        "buy_sell": "Compra/Venda (%)",
        "mgmt": "Adm. anual (%)",
        "vat_comm": "IVA sobre taxas (%)",
        "isr_gain": "IR sobre ganho (%)",
        "summary": "Resumo",
        "nominal_value": "Valor final (nominal)",
        "total_contrib": "Aportes totais",
        "gain": "Ganho gerado",
        "real_value": "Valor real (ajustado)",
        "need_monthly": "É necessário aporte mensal positivo.",
        "copy": "Copiar resumo",
        "evolution": "Evolução anual",
        "years": "Anos",
        "final_balance": "Saldo final",
        "cum_contrib": "Aporte acumulado",
        "gain_col": "Ganho",
        "real_col": "Valor real",
        "fees_col": "Comissões",
        "taxes_col": "Impostos",
    },
}


def fmt_currency(value: float, symbol: str = "MX$") -> str:
    try:
        # Intento con configuración local del usuario
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
    # Fricción e impuestos
    fee_deposit: float = 0.0        # %
    buy_sell: float = 0.0           # %
    mgmt: float = 0.0               # %
    vat_on_fees: float = 16.0       # %
    tax_gain: float = 10.0          # %


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
        self.base_font_size = 11
        self.high_contrast = tk.BooleanVar(value=False)

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

        chk = ttk.Checkbutton(
            top, text=self.strings["daltonic"],
            variable=self.high_contrast, command=self._toggle_contrast
        )
        chk.pack(side="left")

        # Idioma
        ttk.Label(top, text=self.strings["language"]).pack(side="left", padx=(18, 6))
        self.lang_cmb = ttk.Combobox(top, values=["Español", "English", "Português"], width=16, state="readonly")
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
        ttk.Label(w, text="(Próximamente: calculadora científica)").pack(anchor="w")

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
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        inner.bind_all("<MouseWheel>", _wheel)

        # --- Parámetros ---
        box = ttk.LabelFrame(inner, text=self.strings["params"], padding=12)
        box.pack(fill="x", padx=10, pady=(12, 8))

        self.var_initial = tk.StringVar(value="0")
        self.var_monthly = tk.StringVar(value="200")
        self.var_years = tk.StringVar(value="5")
        self.var_return = tk.StringVar(value="10.0")
        self.var_infl = tk.StringVar(value="4.0")

        self._labeled_entry(box, self.strings["initial_amount"], self.var_initial, 0, 0)
        self._labeled_entry(box, self.strings["monthly_contrib"], self.var_monthly, 1, 0)
        self._labeled_entry(box, self.strings["horizon_years"], self.var_years, 2, 0)
        self._labeled_entry(box, self.strings["annual_return"], self.var_return, 0, 1)
        self._labeled_entry(box, self.strings["inflation"], self.var_infl, 1, 1)

        # --- Fricción e impuestos ---
        fr = ttk.LabelFrame(inner, text=self.strings["friction"], padding=12)
        fr.pack(fill="x", padx=10, pady=8)

        self.var_fee_dep = tk.StringVar(value="0.0")
        self.var_buy_sell = tk.StringVar(value="0.0")
        self.var_mgmt = tk.StringVar(value="0.0")
        self.var_vat = tk.StringVar(value="16.0")
        self.var_tax = tk.StringVar(value="10.0")

        self._labeled_entry(fr, self.strings["deposit_fee"], self.var_fee_dep, 0, 0)
        self._labeled_entry(fr, self.strings["buy_sell"], self.var_buy_sell, 1, 0)
        self._labeled_entry(fr, self.strings["mgmt"], self.var_mgmt, 2, 0)
        self._labeled_entry(fr, self.strings["vat_comm"], self.var_vat, 0, 1)
        self._labeled_entry(fr, self.strings["isr_gain"], self.var_tax, 1, 1)

        # --- Resumen ---
        sm = ttk.LabelFrame(inner, text=self.strings["summary"], padding=12)
        sm.pack(fill="x", padx=10, pady=8)

        self.lbl_nominal = ttk.Label(sm, text=f"{self.strings['nominal_value']}:  ?")
        self.lbl_total = ttk.Label(sm, text=f"{self.strings['total_contrib']}:  ?")
        self.lbl_gain = ttk.Label(sm, text=f"{self.strings['gain']}:  ?")
        self.lbl_real = ttk.Label(sm, text=f"{self.strings['real_value']}:  ?")

        self.lbl_nominal.grid(row=0, column=0, sticky="w", padx=4, pady=2)
        self.lbl_total.grid(row=1, column=0, sticky="w", padx=4, pady=2)
        self.lbl_gain.grid(row=2, column=0, sticky="w", padx=4, pady=2)
        self.lbl_real.grid(row=3, column=0, sticky="w", padx=4, pady=2)

        self.btn_copy = ttk.Button(sm, text=self.strings["copy"], command=self._copy_summary)
        self.btn_copy.grid(row=0, column=1, rowspan=4, sticky="e", padx=6, pady=4)

        ttk.Label(inner, text=self.strings["need_monthly"]).pack(anchor="w", padx=14, pady=(2, 8))

        # --- Evolución anual ---
        ev = ttk.LabelFrame(inner, text=self.strings["evolution"], padding=8)
        ev.pack(fill="both", expand=True, padx=10, pady=(0, 12))

        cols = ("year", "final", "contrib", "gain", "real", "fees", "taxes")
        self.tree = ttk.Treeview(ev, columns=cols, show="headings", height=8)
        self.tree.pack(side="left", fill="both", expand=True)
        sb = ttk.Scrollbar(ev, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")

        self.tree.heading("year", text=self.strings["years"])
        self.tree.heading("final", text=self.strings["final_balance"])
        self.tree.heading("contrib", text=self.strings["cum_contrib"])
        self.tree.heading("gain", text=self.strings["gain_col"])
        self.tree.heading("real", text=self.strings["real_col"])
        self.tree.heading("fees", text=self.strings["fees_col"])
        self.tree.heading("taxes", text=self.strings["taxes_col"])

        self.tree.column("year", width=110, anchor="center")
        self.tree.column("final", width=150, anchor="e")
        self.tree.column("contrib", width=150, anchor="e")
        self.tree.column("gain", width=120, anchor="e")
        self.tree.column("real", width=150, anchor="e")
        self.tree.column("fees", width=120, anchor="e")
        self.tree.column("taxes", width=120, anchor="e")

        # disparadores de recálculo
        for v in (self.var_initial, self.var_monthly, self.var_years, self.var_return, self.var_infl,
                  self.var_fee_dep, self.var_buy_sell, self.var_mgmt, self.var_vat, self.var_tax):
            v.trace_add("write", lambda *_: self._recalc())

        self._recalc()

    def _labeled_entry(self, parent, label, var, row, col):
        frm = ttk.Frame(parent)
        frm.grid(row=row, column=col, padx=8, pady=6, sticky="ew")
        parent.grid_columnconfigure(col, weight=1)
        ttk.Label(frm, text=label).pack(anchor="w")
        e = ttk.Entry(frm, textvariable=var, width=16)
        e.pack(anchor="w")

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

        return Inputs(
            initial=f(self.var_initial.get(), 0.0),
            monthly=f(self.var_monthly.get(), 0.0),
            years=i(self.var_years.get(), 1),
            annual_return=f(self.var_return.get(), 10.0),
            inflation=f(self.var_infl.get(), 4.0),
            fee_deposit=f(self.var_fee_dep.get(), 0.0),
            buy_sell=f(self.var_buy_sell.get(), 0.0),
            mgmt=f(self.var_mgmt.get(), 0.0),
            vat_on_fees=f(self.var_vat.get(), 16.0),
            tax_gain=f(self.var_tax.get(), 10.0),
        )

    def _simulate(self, p: Inputs) -> tuple[list[YearRow], float, float, float, float]:
        """
        Simulación anual con:
        - Depósitos mensuales.
        - Comisión por depósito (aplicada a cada aporte nuevo).
        - Buy/Sell % aplicado una vez al final sobre el saldo total (modelo simple).
        - Administración anual % sobre saldo promedio del año.
        - IVA sobre comisiones (depósitos + admin + buy/sell).
        - ISR sobre ganancia anual (después de comisiones, antes de IVA? -> IVA no afecta base del ISR).
        - Inflación anual para valor real.
        """
        months = p.years * 12
        r_m = (p.annual_return / 100.0) / 12.0
        infl_y = p.inflation / 100.0

        balance = p.initial
        cum_contrib = p.initial
        rows: list[YearRow] = []
        sum_fees = 0.0
        sum_taxes = 0.0
        last_year_balance = balance

        for year in range(1, p.years + 1):
            fees_year = 0.0
            taxes_year = 0.0
            contrib_year = 0.0
            start_balance = balance

            # 12 meses
            for m in range(12):
                # Depósito del mes
                dep = p.monthly
                if dep > 0:
                    fee_dep = dep * (p.fee_deposit / 100.0)
                    iva_dep = fee_dep * (p.vat_on_fees / 100.0)
                    net_dep = dep - fee_dep
                    fees_year += (fee_dep + iva_dep)
                    contrib_year += dep
                    cum_contrib += dep
                    balance += net_dep

                # Interés mensual
                interest = balance * r_m
                balance += interest

            # Comisión de administración anual sobre saldo promedio (aprox mitad)
            # Modelo simple: mgmt% del promedio de saldo del año (start+end)/2
            avg_balance = (start_balance + balance) / 2.0
            fee_mgmt = avg_balance * (p.mgmt / 100.0)
            iva_mgmt = fee_mgmt * (p.vat_on_fees / 100.0)
            fees_year += (fee_mgmt + iva_mgmt)
            balance -= fee_mgmt  # IVA no reduce saldo, es costo externo (pero lo mostramos en fees)

            # Buy/Sell al cierre del año (si se liquidara ese año)
            fee_bs = balance * (p.buy_sell / 100.0)
            iva_bs = fee_bs * (p.vat_on_fees / 100.0)
            fees_year += (fee_bs + iva_bs)
            balance -= fee_bs

            # Ganancia del año (aprox): (saldo fin - saldo inicio - aportes netos del año)
            # Aportes netos: lo que efectivamente entró, dep - fee_dep (IVA es costo, no entra al saldo)
            # Para simplicidad: usamos contrib_year*(1 - fee_dep%) como aproximación
            net_in = contrib_year * (1 - (p.fee_deposit / 100.0))
            gain_year = max(0.0, balance - start_balance - net_in)

            # ISR sobre ganancia
            tax = gain_year * (p.tax_gain / 100.0)
            taxes_year += tax
            balance -= tax

            sum_fees += fees_year
            sum_taxes += taxes_year

            # Valor real
            real_val = balance / ((1.0 + infl_y) ** year)

            rows.append(YearRow(
                year=year,
                final_balance=balance,
                cum_contrib=cum_contrib,
                gain=max(0.0, balance - last_year_balance - contrib_year),
                real_value=real_val,
                fees=fees_year,
                taxes=taxes_year,
            ))
            last_year_balance = balance

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
        self.lbl_nominal.config(text=f"{self.strings['nominal_value']}:  ?")
        self.lbl_total.config(text=f"{self.strings['total_contrib']}:  ?")
        self.lbl_gain.config(text=f"{self.strings['gain']}:  ?")
        self.lbl_real.config(text=f"{self.strings['real_value']}:  ?")
        for i in self.tree.get_children():
            self.tree.delete(i)

    # ---------- Actions ----------

    def _copy_summary(self):
        try:
            text = "\n".join([
                self.lbl_nominal.cget("text"),
                self.lbl_total.cget("text"),
                self.lbl_gain.cget("text"),
                self.lbl_real.cget("text"),
            ])
            self.clipboard_clear()
            self.clipboard_append(text)
            self.update()
            messagebox.showinfo("OK", "Resumen copiado al portapapeles.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _font_minus(self):
        self.base_font_size = max(9, self.base_font_size - 1)
        self._apply_font_size()

    def _font_plus(self):
        self.base_font_size = min(18, self.base_font_size + 1)
        self._apply_font_size()

    def _apply_font_size(self):
        f = ("TkDefaultFont", self.base_font_size)
        try:
            self.option_clear()
        except Exception:
            pass
        self.option_add("*Font", f)

    def _toggle_contrast(self):
        if BOOT:
            self.style.theme_use("darkly" if self.high_contrast.get() else "flatly")
        else:
            # fallback simple: cambiar fondo y relief
            bg = "#222" if self.high_contrast.get() else None
            fg = "#fff" if self.high_contrast.get() else None
            if bg:
                self.configure(bg=bg)

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

