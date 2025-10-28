from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional, Set, Tuple

import tkinter as tk
from tkinter import messagebox, ttk

from frontend.i18n import get_strings

STRINGS = get_strings()


def fmt_currency(value: float, symbol: str = "MX$") -> str:
    try:
        return f"{symbol} {value:,.2f}"
    except Exception:
        return f"{symbol} {value:.2f}"


@dataclass
class DebtInputs:
    title: str
    cost: float
    down_payment: float
    cat_annual: float
    open_pct: float
    insurance_monthly: float
    term_months: int
    extra_months: Set[int]
    extra_amount: float
    skip_months: Set[int]
    inflation_annual: float


def _parse_month_list(text: str) -> Set[int]:
    months: Set[int] = set()
    if not text:
        return months
    for chunk in text.replace(" ", "").split(","):
        if not chunk:
            continue
        try:
            month = int(float(chunk))
        except Exception:
            continue
        if 1 <= month <= 12:
            months.add(month)
    return months


def simulate_debt(data: DebtInputs) -> Tuple[List[Tuple[int, float, float, float, float, float, float, float]], Dict[str, float]]:
    strings = STRINGS
    principal = data.cost - data.down_payment
    if principal <= 0:
        raise ValueError(strings.get("debt_invalid_amount", "Necesitas que el monto financiado sea positivo."))

    rate = (1.0 + data.cat_annual / 100.0) ** (1.0 / 12.0) - 1.0 if data.cat_annual else 0.0
    term = max(data.term_months, 1)

    if rate > 0:
        payment = rate * principal / (1.0 - (1.0 + rate) ** (-term))
    else:
        payment = principal / term
    payment = max(payment, 0.0)

    balance = principal
    rows: List[Tuple[int, float, float, float, float, float, float, float]] = []
    total_interest = 0.0
    total_paid = 0.0
    total_fees = 0.0
    interest_acc = 0.0
    month = 0
    open_fee = max(0.0, data.open_pct / 100.0 * data.cost)
    inflation_rate = data.inflation_annual / 100.0
    base_inflation = 1.0 + inflation_rate
    max_months = term + 600

    while balance > 1e-6 and month < max_months:
        month += 1
        interest = balance * rate if rate else 0.0
        interest = max(interest, 0.0)
        scheduled_payment = payment
        principal_payment = 0.0

        if month in data.skip_months:
            scheduled_payment = interest
            principal_payment = 0.0
        else:
            principal_payment = max(scheduled_payment - interest, 0.0)
            if principal_payment > balance:
                principal_payment = balance
                scheduled_payment = interest + principal_payment

        balance -= principal_payment

        extra = 0.0
        if month in data.extra_months and month not in data.skip_months and data.extra_amount > 0 and balance > 0:
            extra = min(data.extra_amount, balance)
            balance -= extra
            principal_payment += extra

        payment_total = scheduled_payment + extra
        fees = data.insurance_monthly
        if month == 1:
            fees += open_fee

        total_interest += interest
        total_fees += fees
        total_paid += payment_total
        interest_acc += interest

        if base_inflation > 0:
            real_balance = balance / (base_inflation ** (month / 12.0))
        else:
            real_balance = balance

        rows.append(
            (
                month,
                payment_total,
                interest,
                principal_payment,
                fees,
                balance,
                interest_acc,
                real_balance,
            )
        )

    if balance > 1e-4:
        raise ValueError(strings.get("debt_not_liquidated", "El crédito no se liquida con los parámetros actuales."))

    months = month
    total_paid_with_fees = total_paid + total_fees
    if base_inflation > 0:
        real_cost = total_paid_with_fees / (base_inflation ** (months / 12.0))
    else:
        real_cost = total_paid_with_fees

    summary = {
        "months": months,
        "total_paid": total_paid_with_fees,
        "total_interest": total_interest,
        "total_fees": total_fees,
        "real_cost": real_cost,
    }

    return rows, summary


class DebtScreen(ttk.Frame):
    def __init__(self, parent: tk.Misc, base_font_size: int) -> None:
        super().__init__(parent)
        self.strings = STRINGS
        self.base_font_size = base_font_size

        self._init_variables()
        self._build_layout()

    def _init_variables(self) -> None:
        self.var_title = tk.StringVar(value=self.strings.get("debt_default_title", "Credito"))
        self.var_cost = tk.StringVar(value="0")
        self.var_down = tk.StringVar(value="0")
        self.var_cat = tk.StringVar(value="20.0")
        self.var_open_pct = tk.StringVar(value="0.0")
        self.var_insurance = tk.StringVar(value="0.0")
        self.var_term = tk.StringVar(value="12")
        self.var_extra_months = tk.StringVar(value="")
        self.var_extra_amount = tk.StringVar(value="0")
        self.var_skip_months = tk.StringVar(value="")
        self.var_inflation = tk.StringVar(value="4.0")

    def _build_layout(self) -> None:
        self.columnconfigure(0, weight=1)

        container = ttk.Frame(self, padding=12)
        container.grid(row=0, column=0, sticky="nsew")
        container.columnconfigure(0, weight=1)

        params = ttk.LabelFrame(container, text=self.strings["debt_params"], padding=12)
        params.grid(row=0, column=0, sticky="ew")
        for col in range(3):
            params.columnconfigure(col, weight=1)

        self._labeled_entry(params, self.strings["debt_field_title"], self.var_title, 0, 0, width=24)
        self._labeled_entry(params, self.strings["debt_field_cost"], self.var_cost, 0, 1, width=14)
        self._labeled_entry(params, self.strings["debt_field_down"], self.var_down, 0, 2, width=14)
        self._labeled_entry(params, self.strings["debt_field_cat"], self.var_cat, 1, 0, width=14)
        self._labeled_entry(params, self.strings["debt_field_open_pct"], self.var_open_pct, 1, 1, width=14)
        self._labeled_entry(params, self.strings["debt_field_insurance"], self.var_insurance, 1, 2, width=14)
        self._labeled_entry(params, self.strings["debt_field_term"], self.var_term, 2, 0, width=14)
        self._labeled_entry(params, self.strings["debt_field_extra_months"], self.var_extra_months, 2, 1, width=18)
        self._labeled_entry(params, self.strings["debt_field_extra_amount"], self.var_extra_amount, 2, 2, width=14)
        self._labeled_entry(params, self.strings["debt_field_skip_months"], self.var_skip_months, 3, 0, width=18)
        self._labeled_entry(params, self.strings["debt_field_inflation"], self.var_inflation, 3, 1, width=14)

        calc_button = ttk.Button(params, text=self.strings["debt_calc"], command=self._on_calc_click)
        calc_button.grid(row=4, column=0, columnspan=3, pady=(10, 0), sticky="ew")

        table_frame = ttk.LabelFrame(container, text=self.strings["debt_table"], padding=12)
        table_frame.grid(row=1, column=0, sticky="nsew", pady=(12, 0))
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)

        columns = (
            "month",
            "payment",
            "interest",
            "principal",
            "fees",
            "balance",
            "interest_acc",
            "real",
        )

        self.debt_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=12)
        self.debt_tree.grid(row=0, column=0, sticky="nsew")

        self.debt_tree.heading("month", text=self.strings["debt_col_month"])
        self.debt_tree.column("month", width=70, anchor="center")

        for col in columns[1:]:
            heading_key = {
                "payment": "debt_col_payment",
                "interest": "debt_col_interest",
                "principal": "debt_col_principal",
                "fees": "debt_col_fees",
                "balance": "debt_col_balance",
                "interest_acc": "debt_col_interest_acc",
                "real": "debt_col_real",
            }[col]
            self.debt_tree.heading(col, text=self.strings[heading_key])
            self.debt_tree.column(col, anchor="e", width=120)

        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.debt_tree.yview)
        hsb = ttk.Scrollbar(table_frame, orient="horizontal", command=self.debt_tree.xview)
        self.debt_tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

        summary = ttk.LabelFrame(container, text=self.strings["debt_summary"], padding=12)
        summary.grid(row=2, column=0, sticky="ew", pady=(12, 0))

        self.debt_lbl_total = ttk.Label(
            summary,
            text=f"{self.strings['debt_summary_total']}: {fmt_currency(0.0)}",
        )
        self.debt_lbl_total.grid(row=0, column=0, sticky="w")

        self.debt_lbl_interest = ttk.Label(
            summary,
            text=f"{self.strings['debt_summary_interest']}: {fmt_currency(0.0)}",
        )
        self.debt_lbl_interest.grid(row=0, column=1, sticky="w", padx=(16, 0))

        self.debt_lbl_real = ttk.Label(
            summary,
            text=f"{self.strings['debt_summary_real']}: {fmt_currency(0.0)}",
        )
        self.debt_lbl_real.grid(row=1, column=0, sticky="w", pady=(6, 0))

        self.debt_lbl_time = ttk.Label(
            summary,
            text=f"{self.strings['debt_summary_time']}: 0 / 0.0",
        )
        self.debt_lbl_time.grid(row=1, column=1, sticky="w", padx=(16, 0), pady=(6, 0))

    def _labeled_entry(self, parent: ttk.LabelFrame, label: str, variable: tk.Variable, row: int, column: int, width: int = 16) -> None:
        wrapper = ttk.Frame(parent)
        wrapper.grid(row=row, column=column, padx=8, pady=6, sticky="ew")
        parent.grid_columnconfigure(column, weight=1)

        header = ttk.Frame(wrapper)
        header.pack(anchor="w", fill="x")
        ttk.Label(header, text=label).pack(side="left")
        ttk.Entry(wrapper, textvariable=variable, width=width).pack(anchor="w")

    def _collect_inputs(self) -> Optional[DebtInputs]:
        def as_float(value: str | float, default: float = 0.0) -> float:
            try:
                return float(str(value).replace(",", "."))
            except Exception:
                return default

        cost = as_float(self.var_cost.get(), 0.0)
        down = as_float(self.var_down.get(), 0.0)
        cat = as_float(self.var_cat.get(), 0.0)
        open_pct = as_float(self.var_open_pct.get(), 0.0)
        insurance = as_float(self.var_insurance.get(), 0.0)
        extra_amount = max(0.0, as_float(self.var_extra_amount.get(), 0.0))
        inflation = as_float(self.var_inflation.get(), 0.0)

        try:
            term = int(float(self.var_term.get()))
        except Exception:
            term = 0
        term = max(term, 1)

        financed = cost - down
        if financed <= 0:
            messagebox.showerror(self.strings["tab_debt"], self.strings["debt_invalid_amount"])
            return None

        extra_months = _parse_month_list(self.var_extra_months.get())
        skip_months = _parse_month_list(self.var_skip_months.get())
        title = self.var_title.get().strip() or self.strings.get("debt_default_title", "Credito")

        return DebtInputs(
            title=title,
            cost=cost,
            down_payment=down,
            cat_annual=cat,
            open_pct=open_pct,
            insurance_monthly=insurance,
            term_months=term,
            extra_months=extra_months,
            extra_amount=extra_amount,
            skip_months=skip_months,
            inflation_annual=inflation,
        )

    def _on_calc_click(self) -> None:
        data = self._collect_inputs()
        if not data:
            return
        try:
            rows, summary = simulate_debt(data)
        except ValueError as exc:
            messagebox.showerror(self.strings["tab_debt"], str(exc))
            return
        self._render_results(rows, summary)

    def _render_results(self, rows: List[Tuple[int, float, float, float, float, float, float, float]], summary: Dict[str, float]) -> None:
        for item in self.debt_tree.get_children():
            self.debt_tree.delete(item)

        for row in rows:
            month, payment_total, interest, principal_payment, fees, balance, interest_acc, real_balance = row
            self.debt_tree.insert(
                "",
                "end",
                values=(
                    month,
                    fmt_currency(payment_total),
                    fmt_currency(interest),
                    fmt_currency(principal_payment),
                    fmt_currency(fees),
                    fmt_currency(balance),
                    fmt_currency(interest_acc),
                    fmt_currency(real_balance),
                ),
            )

        months = summary.get("months", 0)
        years = months / 12.0 if months else 0.0
        total_paid = summary.get("total_paid", 0.0)
        total_interest = summary.get("total_interest", 0.0)
        real_cost = summary.get("real_cost", 0.0)

        self.debt_lbl_total.config(
            text=f"{self.strings['debt_summary_total']}: {fmt_currency(total_paid)}"
        )
        self.debt_lbl_interest.config(
            text=f"{self.strings['debt_summary_interest']}: {fmt_currency(total_interest)}"
        )
        self.debt_lbl_real.config(
            text=f"{self.strings['debt_summary_real']}: {fmt_currency(real_cost)}"
        )
        self.debt_lbl_time.config(
            text=f"{self.strings['debt_summary_time']}: {months} / {years:.1f}"
        )
