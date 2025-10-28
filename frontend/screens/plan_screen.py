import tkinter as tk
from tkinter import ttk

from frontend.i18n import get_strings
from frontend.layout.section_frame import SectionFrame
from frontend.theme.base_theme import get_theme


class PlanScreen(tk.Frame):
    """Pantalla principal del plan de inversion (modo estatico en espanol)."""

    def __init__(self, parent) -> None:
        self.theme = get_theme(high_contrast=False)
        super().__init__(parent, bg=self.theme["bg_main"])
        self.strings = get_strings()

        self.section = SectionFrame(
            self,
            title=self.strings["plan_title"],
            subtitle="Simula tus aportes, rendimiento y valor real (ajustado por inflacion)",
            high_contrast=False,
        )
        self.section.pack(fill="both", expand=True)

        self._init_vars()
        self._build_inputs_area()
        self._build_summary_area()
        self._recalcular()

    def _init_vars(self) -> None:
        self.var_monto_inicial = tk.StringVar(value="0")
        self.var_aporte_mensual = tk.StringVar(value="200")
        self.var_horizonte = tk.StringVar(value="5")
        self.var_rendimiento = tk.StringVar(value="10.0")
        self.var_inflacion = tk.StringVar(value="4.0")
        self.var_comision = tk.StringVar(value="0.0")
        self.var_iva = tk.StringVar(value="16.0")
        self.var_isr = tk.StringVar(value="10.0")

        self.var_valor_final_nominal = tk.StringVar(value="MXS 0.00")
        self.var_aportes_totales = tk.StringVar(value="MXS 0.00")
        self.var_ganancia_generada = tk.StringVar(value="MXS 0.00")
        self.var_valor_real = tk.StringVar(value="MXS 0.00")

    def _build_inputs_area(self) -> None:
        inputs_container = tk.Frame(self.section.left_col, bg=self.theme["bg_panel"])
        inputs_container.pack(fill="both", expand=True)

        label_font = (self.theme["font_family"], 10, "bold")
        field_definitions = [
            (self.strings["initial_amount"], self.var_monto_inicial),
            (self.strings["monthly_contrib"], self.var_aporte_mensual),
            (self.strings["horizon_years"], self.var_horizonte),
            (self.strings["annual_return"], self.var_rendimiento),
            (self.strings["inflation"], self.var_inflacion),
            (self.strings["deposit_fee"], self.var_comision),
            (self.strings["vat_comm"], self.var_iva),
            (self.strings["isr_gain"], self.var_isr),
        ]

        inputs_container.grid_columnconfigure(0, weight=1)
        inputs_container.grid_columnconfigure(1, weight=1)

        for row, (label_text, variable) in enumerate(field_definitions):
            label = tk.Label(
                inputs_container,
                text=label_text,
                font=label_font,
                fg=self.theme["text_primary"],
                bg=self.theme["bg_panel"],
                anchor="w",
            )
            label.grid(row=row, column=0, sticky="w", padx=(0, self.theme["padding"]), pady=(0, 4))

            entry = ttk.Entry(inputs_container, textvariable=variable, width=18)
            entry.grid(row=row, column=1, sticky="ew", pady=(0, 4))

        ttk.Button(inputs_container, text="Calcular", command=self._recalcular).grid(
            row=len(field_definitions),
            column=0,
            columnspan=2,
            sticky="ew",
            pady=(self.theme["padding"], 0),
        )

    def _build_summary_area(self) -> None:
        summary_card = tk.Frame(
            self.section.right_col,
            bg=self.theme["bg_panel"],
            highlightthickness=1,
            highlightbackground=self.theme["border"],
            padx=self.theme["padding"],
            pady=self.theme["padding"],
        )
        summary_card.pack(fill="both", expand=True)

        header = tk.Label(
            summary_card,
            text=self.strings["summary"],
            font=(self.theme["font_family"], 16, "bold"),
            fg=self.theme["text_primary"],
            bg=self.theme["bg_panel"],
            anchor="w",
        )
        header.pack(fill="x", pady=(0, self.theme["padding"]))

        summary_items = [
            (self.strings["nominal_value"], self.var_valor_final_nominal),
            (self.strings["total_contrib"], self.var_aportes_totales),
            (self.strings["gain"], self.var_ganancia_generada),
            (self.strings["real_value"], self.var_valor_real),
        ]

        for label_text, variable in summary_items:
            row_frame = tk.Frame(summary_card, bg=self.theme["bg_panel"])
            row_frame.pack(fill="x", pady=(0, 4))

            tk.Label(
                row_frame,
                text=f"{label_text}:",
                font=(self.theme["font_family"], 11, "bold"),
                fg=self.theme["text_secondary"],
                bg=self.theme["bg_panel"],
            ).pack(side="left")

            tk.Label(
                row_frame,
                textvariable=variable,
                font=(self.theme["font_family"], 11),
                fg=self.theme["text_primary"],
                bg=self.theme["bg_panel"],
                anchor="e",
            ).pack(side="right")

        table_frame = tk.Frame(summary_card, bg=self.theme["bg_panel"])
        table_frame.pack(fill="both", expand=True, pady=(self.theme["padding"], 0))

        columns = ("year", "balance", "contrib", "gain", "real", "fees", "taxes")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=8)
        self.tree.pack(side="left", fill="both", expand=True)

        headings = {
            "year": self.strings["years"],
            "balance": self.strings["final_balance"],
            "contrib": self.strings["cum_contrib"],
            "gain": self.strings["gain_col"],
            "real": self.strings["real_col"],
            "fees": self.strings["fees_col"],
            "taxes": self.strings["taxes_col"],
        }

        for col in columns:
            anchor = "center" if col == "year" else "e"
            self.tree.heading(col, text=headings[col])
            self.tree.column(col, anchor=anchor, stretch=True, width=140)

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)

    def _recalcular(self) -> None:
        monto_inicial = self._to_float(self.var_monto_inicial.get())
        aporte_mensual = self._to_float(self.var_aporte_mensual.get())
        horizonte = max(1, int(self._to_float(self.var_horizonte.get(), default=1)))
        rendimiento = self._to_float(self.var_rendimiento.get()) / 100
        inflacion = self._to_float(self.var_inflacion.get()) / 100
        comision = self._to_float(self.var_comision.get()) / 100
        iva = self._to_float(self.var_iva.get()) / 100
        isr = self._to_float(self.var_isr.get()) / 100

        balance = monto_inicial
        aportes_acumulados = monto_inicial
        comisiones_acumuladas = 0.0
        impuestos_acumulados = 0.0

        self.tree.delete(*self.tree.get_children())

        for year in range(1, horizonte + 1):
            aportes_anuales = aporte_mensual * 12
            comisiones_anuales = aportes_anuales * comision
            iva_anual = comisiones_anuales * iva
            comisiones_totales = comisiones_anuales + iva_anual

            balance = (balance + aportes_anuales - comisiones_totales) * (1 + rendimiento)
            aportes_acumulados += aportes_anuales
            comisiones_acumuladas += comisiones_totales

            ganancia_bruta = max(0.0, balance - aportes_acumulados)
            impuesto_anual = ganancia_bruta * isr
            impuestos_acumulados += impuesto_anual
            balance_neto = balance - impuesto_anual

            valor_real = balance_neto / ((1 + inflacion) ** year)

            self.tree.insert(
                "",
                "end",
                values=(
                    year,
                    self._format_currency(balance_neto),
                    self._format_currency(aportes_acumulados),
                    self._format_currency(ganancia_bruta),
                    self._format_currency(valor_real),
                    self._format_currency(comisiones_acumuladas),
                    self._format_currency(impuestos_acumulados),
                ),
            )

        valor_final_nominal = balance - impuestos_acumulados
        valor_real_final = valor_final_nominal / ((1 + inflacion) ** horizonte)

        self.var_valor_final_nominal.set(self._format_currency(valor_final_nominal))
        self.var_aportes_totales.set(self._format_currency(aportes_acumulados))
        self.var_ganancia_generada.set(self._format_currency(valor_final_nominal - aportes_acumulados))
        self.var_valor_real.set(self._format_currency(valor_real_final))

    @staticmethod
    def _to_float(value: str, default: float = 0.0) -> float:
        try:
            return float(value.replace(",", ""))
        except (ValueError, AttributeError):
            return default

    @staticmethod
    def _format_currency(amount: float) -> str:
        return f"MXS {amount:,.2f}"
